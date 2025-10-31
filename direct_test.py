"""
Simple direct test of sklearn model
"""
import pickle
import json

print("="*80)
print("SKLEARN MODEL DIRECT TEST")
print("="*80 + "\n")

# Load sklearn model
with open('model/sklearn_pipeline.pkl', 'rb') as f:
    sklearn_pipeline = pickle.load(f)
print("✓ Loaded sklearn model\n")

# Load intents
with open('model/intents.json', 'r') as f:
    intents_data = json.load(f)
print(f"✓ Loaded {len(intents_data['intents'])} intents\n")

def test_query(text):
    """Test a single query"""
    predicted_tag = sklearn_pipeline.predict([text])[0]
    
    # Try to get confidence if available (not available for LinearSVC)
    try:
        probabilities = sklearn_pipeline.predict_proba([text])[0]
        confidence = max(probabilities)
    except AttributeError:
        # LinearSVC doesn't have predict_proba, use decision_function instead
        decision = sklearn_pipeline.decision_function([text])[0]
        # Normalize decision scores to 0-1 range
        max_score = max(decision)
        confidence = 1.0 / (1.0 + abs(max_score))  # Simplified confidence
    
    # Get response
    response = "No response found"
    for intent in intents_data['intents']:
        if intent['tag'] == predicted_tag:
            response = intent['responses'][0]
            break
    
    return predicted_tag, confidence, response

# Test cases - focus on previously weak intents
test_cases = [
    "how long does shipping take",
    "do you ship internationally",
    "what are the shipping costs",
    "express shipping available",
    "i need technical support",
    "any promotions today",
    "how can i return an item",
    "tell me about your company",
    "yes that's correct",
    "hello",
    "can i pay using credit card",
    "show me electronics",
]

print("="*80)
print("TESTING USER'S QUERIES")
print("="*80 + "\n")

for query in test_cases:
    tag, conf, response = test_query(query)
    
    print(f"Query: '{query}'")
    print(f"  → Predicted Intent: {tag}")
    print(f"  → Confidence: {conf:.1%}")
    print(f"  → Bot Response: {response}")
    print()

print("="*80)
print("✅ ANALYSIS COMPLETE - Check if responses match expected intents:")
print("  - 'hi' should be 'greeting'")
print("  - 'check order status' should be 'order_status'")
print("  - 'pay using credit card' should be 'payments'")
print("  - 'order id is 12345' should be 'order_status'")
print("  - 'tell me a joke' should be 'jokes' (if intent exists)")
print("  - 'show me electronics' should be 'list_products'")
print("="*80)
