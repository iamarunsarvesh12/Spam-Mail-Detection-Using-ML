import pickle

from preprocessing import clean_text

MODEL_PATH = "model/spam_classifier.pkl"
VECTORIZER_PATH = "model/tfidf_vectorizer.pkl"

_model = None
_vectorizer = None


def load_artifacts():
    """Load the trained model and TF-IDF vectorizer from disk (once)."""
    global _model, _vectorizer
    if _model is None or _vectorizer is None:
        try:
            with open(MODEL_PATH, "rb") as f:
                _model = pickle.load(f)
            with open(VECTORIZER_PATH, "rb") as f:
                _vectorizer = pickle.load(f)
        except FileNotFoundError:
            raise RuntimeError(
                "Model files not found. Please run 'python train_model.py' "
                "first to train and save the model."
            )
    return _model, _vectorizer


def predict_message(message: str) -> dict:
    """
    Classify a single email/SMS message.

    Returns a dictionary with:
        - label: "Spam" or "Not Spam"
        - spam_probability: model's confidence that the message is spam (0-1)
    """
    model, vectorizer = load_artifacts()

    # Apply the SAME cleaning steps used during training
    cleaned = clean_text(message)

    # Convert cleaned text into the same TF-IDF feature space as training
    features = vectorizer.transform([cleaned])

    # Predict class (0 = Not Spam, 1 = Spam) and probability
    prediction = model.predict(features)[0]
    probability = model.predict_proba(features)[0][1]  # probability of class "spam"

    label = "Spam" if prediction == 1 else "Not Spam"

    return {"label": label, "spam_probability": round(float(probability), 4)}


def run_cli():
    """Simple command-line interface for classifying emails interactively."""
    print("=" * 50)
    print(" Spam Email Detection System")
    print("=" * 50)
    print("Type an email message below and press Enter to classify it.")
    print("Type 'exit' to quit.\n")

    while True:
        message = input("Enter email message: ").strip()

        if message.lower() == "exit":
            print("Goodbye!")
            break

        if not message:
            print("Please enter a non-empty message.\n")
            continue

        result = predict_message(message)

        # Output: Display the final result clearly to the user
        print("-" * 50)
        print(f"Result           : {result['label']}")
        print(f"Spam Probability : {result['spam_probability'] * 100:.2f}%")
        print("-" * 50 + "\n")


if __name__ == "__main__":
    run_cli()
