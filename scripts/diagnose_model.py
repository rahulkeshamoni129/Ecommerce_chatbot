"""
Diagnostic script to test model predictions
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pickle
import numpy as np
import json
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences

# Load artifacts
MODEL_PATH = "model/chatbot_model.h5"
TOKENIZER_PATH = "model/tokenizer.pickle"
LABEL_ENCODER_PATH = "model/label_encoder.pickle"
INTENTS_PATH = "model/intents.json"

print("Loading model artifacts...")
model = load_model(MODEL_PATH)
tokenizer = pickle.load(open(TOKENIZER_PATH, "rb"))
lbl_encoder = pickle.load(open(LABEL_ENCODER_PATH, "rb"))
intents = json.load(open(INTENTS_PATH, encoding="utf-8"))

print(f"Model loaded: {model is not None}")
print(f"Number of classes: {len(lbl_encoder.classes_)}")
print(f"Classes: {lbl_encoder.classes_}")
print(f"Vocabulary size: {len(tokenizer.word_index)}")

# Test predictions
test_inputs = [
    "hello",
    "what payment methods do you accept",
    "how long does shipping take",
    "show me electronics",
    "i want to track my order",
    "can i pay with credit card",
    "contact customer support",
]

print("\n" + "="*60)
print("TESTING MODEL PREDICTIONS")
print("="*60)

for text in test_inputs:
    # Preprocess
    text_lower = text.lower().strip()
    
    # Tokenize and pad
    seq = tokenizer.texts_to_sequences([text_lower])
    padded = pad_sequences(seq, truncating='post', maxlen=25)
    
    # Predict
    result = model.predict(padded, verbose=0)
    confidence = float(np.max(result))
    pred_index = int(np.argmax(result, axis=1)[0])
    tag = lbl_encoder.inverse_transform([pred_index])[0]
    
    # Get top 3 predictions
    top_3_indices = np.argsort(result[0])[-3:][::-1]
    top_3_tags = lbl_encoder.inverse_transform(top_3_indices)
    top_3_confidences = result[0][top_3_indices]
    
    print(f"\nInput: '{text}'")
    print(f"  Predicted: {tag} (confidence: {confidence:.3f})")
    print(f"  Top 3:")
    for i, (t, c) in enumerate(zip(top_3_tags, top_3_confidences), 1):
        print(f"    {i}. {t}: {c:.3f}")
