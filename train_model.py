import pickle

import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

from preprocessing import clean_series

DATA_PATH = "data/spam_dataset.tsv"
MODEL_PATH = "model/spam_classifier.pkl"
VECTORIZER_PATH = "model/tfidf_vectorizer.pkl"


def load_data(path: str) -> pd.DataFrame:
    """
    Load the dataset. Expected format: tab-separated file with two columns
    -> label ("ham"/"spam") and the raw message text (no header row).
    """
    df = pd.read_csv(path, sep="\t", header=None, names=["label", "message"])
    return df

def prepare_features(df: pd.DataFrame):
    # Clean every message in the dataset
    df["cleaned_message"] = clean_series(df["message"])
    # Convert labels to numeric: spam = 1, ham (not spam) = 0
    df["label_num"] = df["label"].map({"ham": 0, "spam": 1})
    vectorizer = TfidfVectorizer(max_features=3000, ngram_range=(1, 2))
    X = vectorizer.fit_transform(df["cleaned_message"])
    y = df["label_num"].values
    return X, y, vectorizer

def train_and_evaluate(X, y):
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    model = MultinomialNB()
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print(f"\nModel Accuracy: {accuracy * 100:.2f}%\n")
    print("Classification Report:")
    print(classification_report(y_test, y_pred, target_names=["Not Spam", "Spam"]))
    print("Confusion Matrix:")
    print(confusion_matrix(y_test, y_pred))
    return model


def save_artifacts(model, vectorizer):
    """Persist the trained model and vectorizer so predict.py can reuse them."""
    with open(MODEL_PATH, "wb") as f:
        pickle.dump(model, f)
    with open(VECTORIZER_PATH, "wb") as f:
        pickle.dump(vectorizer, f)
    print(f"\nSaved model to '{MODEL_PATH}'")
    print(f"Saved vectorizer to '{VECTORIZER_PATH}'")


def main():
    print("Loading dataset...")
    df = load_data(DATA_PATH)
    print(f"Loaded {len(df)} messages ({(df['label']=='spam').sum()} spam, "
          f"{(df['label']=='ham').sum()} not spam)")
    print("\nCleaning text and extracting TF-IDF features...")
    X, y, vectorizer = prepare_features(df)
    print("Training Naive Bayes classifier...")
    model = train_and_evaluate(X, y)
    save_artifacts(model, vectorizer)


if __name__ == "__main__":
    main()
