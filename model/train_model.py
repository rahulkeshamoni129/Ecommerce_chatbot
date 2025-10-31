import os
import json
import numpy as np
import pickle
import re
from sklearn.model_selection import train_test_split
from tensorflow.keras.optimizers import Adam

# Suppress TensorFlow logging
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

try:
    from tensorflow.keras.models import Sequential
    from tensorflow.keras.layers import Dense, Dropout, Embedding, GlobalAveragePooling1D
    from tensorflow.keras.callbacks import ModelCheckpoint, EarlyStopping
    from tensorflow.keras.utils import to_categorical
    from tensorflow.keras.preprocessing.text import Tokenizer
    from tensorflow.keras.preprocessing.sequence import pad_sequences
except ImportError:
    print("TensorFlow not found. Training will be skipped.")
    exit()

def preprocess(text: str) -> str:
    text = text.lower().strip()
    text = re.sub(r"[^a-z0-9\s'?-]", "", text)
    text = re.sub(r"\s+", " ", text)
    return text


ROOT = os.path.dirname(os.path.abspath(__file__))
INTENTS_PATH = os.path.join(ROOT, "intents.json")
MODEL_DIR = os.path.join(ROOT, "..", "model")
os.makedirs(MODEL_DIR, exist_ok=True)

with open(INTENTS_PATH, encoding="utf-8") as f:
    data = json.load(f)

training_sentences = []
training_labels = []
labels = [] # Use this for classes

for intent in data.get("intents", []):
    if intent.get("tag") not in labels:
        labels.append(intent.get("tag"))
    for pattern in intent.get("patterns", []):
        training_sentences.append(preprocess(pattern))
        training_labels.append(intent.get("tag"))

vocab_size = 10000  # Much larger vocabulary
embedding_dim = 256  # Richer word representations
max_len = 30  # Longer sequences for complex queries
oov_token = "<OOV>"

from sklearn.preprocessing import LabelEncoder
lbl_encoder = LabelEncoder()
lbl_encoder.fit(training_labels)
training_labels_encoded = lbl_encoder.transform(training_labels)

tokenizer = Tokenizer(num_words=vocab_size, oov_token=oov_token)
tokenizer.fit_on_texts(training_sentences)
word_index = tokenizer.word_index
sequences = tokenizer.texts_to_sequences(training_sentences)
padded_sequences = pad_sequences(sequences, truncating='post', maxlen=max_len)

num_classes = len(labels)
y = to_categorical(training_labels_encoded, num_classes=num_classes)

# Split data into training and validation sets (80/20)
X_train, X_val, y_train, y_val = train_test_split(padded_sequences, y, test_size=0.2, random_state=42, stratify=y)

# Define model with improved architecture
model = Sequential()
model.add(Embedding(vocab_size, embedding_dim, input_length=max_len))
model.add(GlobalAveragePooling1D())
model.add(Dense(256, activation='relu'))
model.add(Dropout(0.4))
model.add(Dense(128, activation='relu'))
model.add(Dropout(0.4))
model.add(Dense(64, activation='relu'))
model.add(Dropout(0.3))
model.add(Dense(num_classes, activation='softmax'))

# Compile model with optimized settings
adam = Adam(learning_rate=0.001)  # Standard learning rate
model.compile(loss='categorical_crossentropy', optimizer=adam, metrics=['accuracy'])

# Define ModelCheckpoint to save the best model
checkpoint_path = os.path.join(MODEL_DIR, "chatbot_model.h5") # Corrected path
model_checkpoint = ModelCheckpoint(filepath=checkpoint_path,
                                   save_best_only=True,
                                   monitor='val_accuracy',
                                   mode='max',
                                   verbose=1)

# Train the model with optimized settings
print("Training TensorFlow model (this may take a while)...")

early_stop = EarlyStopping(monitor='val_accuracy', patience=20, restore_best_weights=True, verbose=1)

hist = model.fit(X_train, y_train, 
                 epochs=200,  # More epochs with early stopping
                 batch_size=16,  # Larger batch size
                 validation_data=(X_val, y_val), 
                 callbacks=[model_checkpoint, early_stop], 
                 verbose=1)

print("Model training complete. Best model saved to", checkpoint_path)

# Save tokenizer and label encoder
with open(os.path.join(MODEL_DIR, 'tokenizer.pickle'), 'wb') as handle:
    pickle.dump(tokenizer, handle, protocol=pickle.HIGHEST_PROTOCOL)

with open(os.path.join(MODEL_DIR, 'label_encoder.pickle'), 'wb') as ecn_file:
    pickle.dump(lbl_encoder, ecn_file, protocol=pickle.HIGHEST_PROTOCOL)

print("✅ TensorFlow model trained and saved successfully!")
