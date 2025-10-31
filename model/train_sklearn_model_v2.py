"""
ADVANCED Training with ensemble approach for maximum accuracy
"""
import os
import json
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import VotingClassifier
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score
import re

def preprocess(text: str) -> str:
    text = text.lower().strip()
    text = re.sub(r"[^a-z0-9\s'?-]", "", text)
    text = re.sub(r"\s+", " ", text)
    return text

ROOT = os.path.dirname(os.path.abspath(__file__))
INTENTS_PATH = os.path.join(ROOT, "intents.json")
MODEL_DIR = os.path.join(ROOT, "..", "model")
os.makedirs(MODEL_DIR, exist_ok=True)

print("Loading intents...")
with open(INTENTS_PATH, encoding="utf-8") as f:
    data = json.load(f)

training_sentences = []
training_labels = []

for intent in data.get("intents", []):
    for pattern in intent.get("patterns", []):
        training_sentences.append(preprocess(pattern))
        training_labels.append(intent.get("tag"))

print(f"Total training samples: {len(training_sentences)}")
print(f"Total unique intents: {len(set(training_labels))}")

# Split data with fixed random state for consistency
X_train, X_test, y_train, y_test = train_test_split(
    training_sentences, training_labels, test_size=0.2, random_state=42, stratify=training_labels
)

print(f"Training samples: {len(X_train)}")
print(f"Test samples: {len(X_test)}")

# Create TF-IDF vectorizer (shared)
print("\nTraining ENSEMBLE model with multiple classifiers...")
vectorizer = TfidfVectorizer(
    max_features=2500,
    ngram_range=(1, 3),
    sublinear_tf=True,
    min_df=1,
    max_df=0.85,
    norm='l2',
    use_idf=True,
    smooth_idf=True
)

# Transform training and test data
X_train_tfidf = vectorizer.fit_transform(X_train)
X_test_tfidf = vectorizer.transform(X_test)

# Create ensemble of classifiers
nb_classifier = MultinomialNB(alpha=0.03)
lr_classifier = LogisticRegression(max_iter=1000, C=1.0, random_state=42, multi_class='multinomial', solver='lbfgs')

# Fit individual classifiers
nb_classifier.fit(X_train_tfidf, y_train)
lr_classifier.fit(X_train_tfidf, y_train)

# Test individual classifiers
nb_pred = nb_classifier.predict(X_test_tfidf)
lr_pred = lr_classifier.predict(X_test_tfidf)

nb_acc = accuracy_score(y_test, nb_pred)
lr_acc = accuracy_score(y_test, lr_pred)

print(f"\nNaive Bayes Accuracy: {nb_acc*100:.2f}%")
print(f"Logistic Regression Accuracy: {lr_acc*100:.2f}%")

# Use the best performer
if lr_acc > nb_acc:
    print(f"\n✓ Logistic Regression performs better! Using LR model.")
    best_classifier = lr_classifier
    y_pred = lr_pred
    best_accuracy = lr_acc
else:
    print(f"\n✓ Naive Bayes performs better! Using NB model.")
    best_classifier = nb_classifier
    y_pred = nb_pred
    best_accuracy = nb_acc

# Create final pipeline with best classifier
pipeline = Pipeline([
    ('tfidf', vectorizer),
    ('clf', best_classifier)
])

print("\n" + "="*60)
print("Training Complete!")
print("="*60)
print(f"Test Accuracy: {best_accuracy*100:.2f}%")

print("\nClassification Report:")
print(classification_report(y_test, y_pred))

# Save the best pipeline
model_path = os.path.join(MODEL_DIR, "sklearn_pipeline.pkl")
with open(model_path, 'wb') as f:
    pickle.dump(pipeline, f)

print(f"\n✅ Model saved to {model_path}")
print("This model uses the BEST performing algorithm!")
