"""
ULTIMATE ACCURACY BOOST - Advanced ML with cross-validation and SVM
"""
import os
import json
import pickle
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import LinearSVC
from sklearn.pipeline import Pipeline
from sklearn.model_selection import cross_val_score, train_test_split
from sklearn.metrics import classification_report, accuracy_score
import re

def preprocess(text: str) -> str:
    text = text.lower().strip()
    text = re.sub(r"[^a-z0-9\s'?-]", "", text)
    text = re.sub(r"\s+", " ", text)
    return text

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INTENTS_PATH = os.path.join(ROOT, "model", "intents.json")
MODEL_DIR = os.path.join(ROOT, "model")
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

# Split data
X_train, X_test, y_train, y_test = train_test_split(
    training_sentences, training_labels, test_size=0.2, random_state=42, stratify=training_labels
)

print(f"Training samples: {len(X_train)}")
print(f"Test samples: {len(X_test)}")

print("\n" + "="*60)
print("TESTING MULTIPLE ALGORITHMS WITH CROSS-VALIDATION")
print("="*60)

# Test configuration 1: Naive Bayes (original)
pipeline_nb = Pipeline([
    ('tfidf', TfidfVectorizer(max_features=2000, ngram_range=(1, 3), sublinear_tf=True, min_df=1, max_df=0.8)),
    ('clf', MultinomialNB(alpha=0.05))
])

# Test configuration 2: Linear SVM (often better for text)
pipeline_svm = Pipeline([
    ('tfidf', TfidfVectorizer(max_features=2000, ngram_range=(1, 3), sublinear_tf=True, min_df=1, max_df=0.8)),
    ('clf', LinearSVC(C=1.0, max_iter=2000, random_state=42))
])

# Test configuration 3: Optimized Naive Bayes
pipeline_nb_opt = Pipeline([
    ('tfidf', TfidfVectorizer(max_features=2500, ngram_range=(1, 3), sublinear_tf=True, min_df=1, max_df=0.85)),
    ('clf', MultinomialNB(alpha=0.02))
])

# Cross-validation scores (more reliable than single split)
print("\n1. Naive Bayes (Original)")
cv_scores_nb = cross_val_score(pipeline_nb, training_sentences, training_labels, cv=5, scoring='accuracy')
print(f"   Cross-Val Accuracy: {cv_scores_nb.mean()*100:.2f}% (+/- {cv_scores_nb.std()*100:.2f}%)")

print("\n2. Linear SVM")
cv_scores_svm = cross_val_score(pipeline_svm, training_sentences, training_labels, cv=5, scoring='accuracy')
print(f"   Cross-Val Accuracy: {cv_scores_svm.mean()*100:.2f}% (+/- {cv_scores_svm.std()*100:.2f}%)")

print("\n3. Optimized Naive Bayes")
cv_scores_nb_opt = cross_val_score(pipeline_nb_opt, training_sentences, training_labels, cv=5, scoring='accuracy')
print(f"   Cross-Val Accuracy: {cv_scores_nb_opt.mean()*100:.2f}% (+/- {cv_scores_nb_opt.std()*100:.2f}%)")

# Choose best model
scores = {
    'Naive Bayes (Original)': (cv_scores_nb.mean(), pipeline_nb),
    'Linear SVM': (cv_scores_svm.mean(), pipeline_svm),
    'Optimized Naive Bayes': (cv_scores_nb_opt.mean(), pipeline_nb_opt)
}

best_name = max(scores, key=lambda k: scores[k][0])
best_score, best_pipeline = scores[best_name]

print("\n" + "="*60)
print(f"🏆 WINNER: {best_name}")
print(f"   Average CV Accuracy: {best_score*100:.2f}%")
print("="*60)

# Train best model on full training set
print(f"\nTraining {best_name} on full training data...")
best_pipeline.fit(X_train, y_train)

# Evaluate on test set
y_pred = best_pipeline.predict(X_test)
test_accuracy = accuracy_score(y_test, y_pred)

print("\n" + "="*60)
print("FINAL MODEL PERFORMANCE")
print("="*60)
print(f"Test Set Accuracy: {test_accuracy*100:.2f}%")

print("\nClassification Report:")
print(classification_report(y_test, y_pred))

# Save the best model
model_path = os.path.join(MODEL_DIR, "sklearn_pipeline.pkl")
with open(model_path, 'wb') as f:
    pickle.dump(best_pipeline, f)

print(f"\n✅ Best model ({best_name}) saved to {model_path}")
print(f"📊 Final Accuracy: {test_accuracy*100:.2f}%")
