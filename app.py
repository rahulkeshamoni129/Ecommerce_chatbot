from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import numpy as np
import pickle, json, os, re
from datetime import datetime
import logging

app = Flask(__name__)
CORS(app)

# --- Simple Conversation Context ---
# In a real app, this would be session-based (e.g., using Flask sessions)
conversation_context = {}

# --- Mock Order Data (instead of MongoDB) ---
mock_orders = {
    "ORD100": {"status": "In transit", "eta": "2 days", "tracking": "TRK1234567890", "carrier": "FedEx"},
    "ORD101": {"status": "Delivered", "eta": "Delivered", "tracking": "TRK0987654321", "carrier": "UPS"},
    "ORD102": {"status": "Processing", "eta": "3-5 days", "tracking": "TRK1122334455", "carrier": "USPS"},
    "ORD103": {"status": "Shipped", "eta": "1 day", "tracking": "TRK5566778899", "carrier": "DHL"},
    "ORD104": {"status": "In transit", "eta": "4 days", "tracking": "TRK9988776655", "carrier": "FedEx"},
}

# --- Load Model + Tokenizer + Label Encoder (safe) ---
MODEL_PATH = os.path.join("model", "chatbot_model.h5")
TOKENIZER_PATH = os.path.join("model", "tokenizer.pickle")
LABEL_ENCODER_PATH = os.path.join("model", "label_encoder.pickle")
INTENTS_PATH = os.path.join("model", "intents.json")

model = None
tokenizer = None
lbl_encoder = None
intents = {"intents": []}
sklearn_pipeline = None

# Try loading sklearn fallback pipeline if present
SKLEARN_PIPELINE_PATH = os.path.join("model", "sklearn_pipeline.pkl")
if os.path.exists(SKLEARN_PIPELINE_PATH):
    try:
        sklearn_pipeline = pickle.load(open(SKLEARN_PIPELINE_PATH, "rb"))
        print("✓ Loaded sklearn pipeline model")
    except Exception:
        sklearn_pipeline = None

# Only load TensorFlow if sklearn is not available
if sklearn_pipeline is None:
    try:
        # Try to load TensorFlow model artifacts lazily; importing tensorflow can fail on some systems
        if os.path.exists(MODEL_PATH):
            try:
                from tensorflow.keras.models import load_model as tf_load_model
                from tensorflow.keras.preprocessing.sequence import pad_sequences as tf_pad_sequences
                model = tf_load_model(MODEL_PATH)
                # expose pad_sequences function for later use
                pad_sequences = tf_pad_sequences
                print("✓ Loaded TensorFlow model")
            except Exception:
                logging.exception("TensorFlow present but failed to import or load model. Will try sklearn fallback.")
        if os.path.exists(TOKENIZER_PATH):
            try:
                tokenizer = pickle.load(open(TOKENIZER_PATH, "rb"))
            except Exception:
                logging.exception("Failed to load tokenizer.pkl")
        if os.path.exists(LABEL_ENCODER_PATH):
            try:
                lbl_encoder = pickle.load(open(LABEL_ENCODER_PATH, "rb"))
            except Exception:
                logging.exception("Failed to load label_encoder.pkl")
    except Exception as e:
        logging.exception("Failed to load model artifacts: %s", e)
else:
    print("✓ Using sklearn model (faster startup)")

# Load intents
if os.path.exists(INTENTS_PATH):
    intents = json.load(open(INTENTS_PATH, encoding="utf-8"))

# Load product data
with open("model/products.json", "r", encoding="utf-8") as f:
    products_data = json.load(f)["products"]

# Organize products by category for easier lookup
products_by_category = {}
for product in products_data:
    category = product.get("category", "Uncategorized")
    if category not in products_by_category:
        products_by_category[category] = []
    products_by_category[category].append(product)

def preprocess_text(text: str) -> str:
    # Minimal preprocessing: lower, strip, remove excessive whitespace and simple punctuation
    text = text.lower().strip()
    text = re.sub(r"[\r\n]+", " ", text)
    text = re.sub(r"[^a-z0-9\s'?-]", "", text)
    text = re.sub(r"\s+", " ", text)
    return text

def get_product_details(product_name):
    """Searches for a product by name and returns its details."""
    for product in products_data:
        if product_name.lower() in product["name"].lower():
            return product
    return None

def predict_intent_tag(text: str) -> tuple:
    """Predicts the intent tag for a given text using available models.
    Returns (tag, confidence_score)"""
    # 1. TensorFlow Model
    if model is not None and tokenizer is not None and lbl_encoder is not None:
        try:
            seq = tokenizer.texts_to_sequences([text])
            padded = pad_sequences(seq, truncating='post', maxlen=30)  # Updated to match training
            result = model.predict(padded, verbose=0)
            confidence = float(np.max(result))
            pred_index = int(np.argmax(result, axis=1)[0])
            tag = lbl_encoder.inverse_transform([pred_index])[0]
            return (tag, confidence)
        except Exception:
            logging.exception("TensorFlow prediction failed.")

    # 2. Scikit-learn Fallback
    if sklearn_pipeline is not None:
        try:
            tag = sklearn_pipeline.predict([text])[0]
            return (tag, 0.7)  # Assume moderate confidence for sklearn
        except Exception:
            logging.exception("Sklearn pipeline prediction failed.")

    # 3. Keyword Matching Fallback
    for intent in intents.get("intents", []):
        for pattern in intent.get("patterns", []):
            if pattern.lower() in text:
                return (intent.get("tag"), 0.6)
    
    return ("fallback", 0.0) # Default fallback if no match

def get_random_response_for_tag(tag: str) -> str:
    """Finds a random response for a given intent tag."""
    for intent in intents.get("intents", []):
        if intent.get("tag") == tag:
            return np.random.choice(intent.get("responses", ["Sorry, I didn't get that."]))
    return "My apologies, I'm not sure how to respond to that."

def get_response(user_input: str) -> str:
    original = user_input
    processed_text = preprocess_text(user_input)
    
    # Priority 1: Handle contextual follow-up
    last_question = conversation_context.get('last_question')
    if last_question == 'offer_tracking_details':
        tag, confidence = predict_intent_tag(processed_text)
        if tag == 'affirmative' or confidence > 0.5:
            order_id = conversation_context.get('subject')
            conversation_context.clear()  # Clear context after use
            if order_id and order_id in mock_orders:
                order_info = mock_orders[order_id]
                if order_info.get("tracking"):
                    return f"The tracking number for order {order_id} is {order_info['tracking']}. You can track it on the {order_info.get('carrier', 'carrier')} website."
                else:
                    return f"I couldn't find specific tracking details for order {order_id}, but it is on its way!"
            else:
                return "I seem to have lost the order ID. Could you provide it again?"
    
    # Clear context if the user asks something new
    conversation_context.clear()

    # Priority 2: Check for order ID in a new message
    order_id_match = re.search(r'ORD\d+', original.upper())
    if not order_id_match:
        # Match patterns like "order id is 12345", "orderid 12345", "order #12345"
        order_id_match = re.search(r"order\s*(?:id|#|number)?\s*(?:is|:)?\s*([A-Za-z0-9-]{4,16})", original, flags=re.IGNORECASE)

    if order_id_match:
        order_id = order_id_match.group(0) if 'ORD' in order_id_match.group(0).upper() else order_id_match.group(1)
        # Normalize order ID to uppercase
        order_id = order_id.upper()
        
        if order_id in mock_orders:
            order_info = mock_orders[order_id]
            status = order_info.get("status", "In transit")
            eta = order_info.get("eta", "2 days")
            # Set context for a potential follow-up
            conversation_context['last_question'] = 'offer_tracking_details'
            conversation_context['subject'] = order_id
            return f"I found order {order_id}. Its current status is: {status} — expected delivery in {eta}. Would you like tracking details?"
        else:
            return "I couldn't find an order with that ID. Please double-check the order number."

    # Priority 3: Predict intent with confidence
    tag, confidence = predict_intent_tag(processed_text)
    
    # If confidence is too low, use fallback
    if confidence < 0.3:  # Lowered threshold
        return "I'm not quite sure what you're asking. Could you please rephrase that? I can help with orders, products, payments, shipping, and more."

    # Handle product listing
    if tag == "list_products":
        mentioned_category = None
        for cat in products_by_category.keys():
            if cat.lower() in original.lower():
                mentioned_category = cat
                break
        
        if mentioned_category:
            products_in_category = products_by_category.get(mentioned_category, [])
            if products_in_category:
                # List the first 5 products to keep the response clean
                product_names = [p['name'] for p in products_in_category[:5]]
                response = f"Here are some products in the {mentioned_category} category: {', '.join(product_names)}. Which one would you like to know more about?"
                return response
            else:
                return f"Sorry, I couldn't find any products in the {mentioned_category} category."
        else:
            # If no category is mentioned, ask for one using the intent's predefined responses
            return get_random_response_for_tag(tag)

    if tag == "product_inquiry":
        found_product = None
        # Simple keyword matching for product names in the original input
        for product in products_data:
            if product["name"].lower() in original.lower():
                found_product = product
                break
        
        if found_product:
            stock_status = "In stock" if found_product["in_stock"] else "Out of stock"
            return f"Here are the details for {found_product['name']}: {found_product['description']} The price is ${found_product['price']}. Currently, it is {stock_status}."
    
    # Priority 4: Get a standard response for any other intent
    return get_random_response_for_tag(tag)

# Load the single, bundled HTML file content
with open("templates/index_bundle.html", "r", encoding="utf-8") as f:
    INDEX_HTML = f.read()

@app.route("/")
def home():
    return INDEX_HTML

@app.route("/health")
def health():
    return jsonify({"status": "ok", "intents": len(intents.get("intents", []))})


@app.route("/chat", methods=["POST"])
def chat():
    payload = request.get_json(force=True, silent=True) or {}
    user_message = payload.get("message", "").strip()
    if not user_message:
        return jsonify({"reply": "Please send a message."}), 400

    bot_reply = get_response(user_message)

    # Chat history logging removed (no MongoDB needed)
    # In production, you could log to a file or other storage

    return jsonify({"reply": bot_reply})


if __name__ == "__main__":
    # Use 0.0.0.0 when deploying in containers, default to local dev
    debug_flag = os.environ.get("FLASK_DEBUG", "False").lower() in ("1", "true", "yes")
    app.run(host=os.environ.get("FLASK_RUN_HOST", "127.0.0.1"), port=int(os.environ.get("PORT", 5000)), debug=debug_flag)
