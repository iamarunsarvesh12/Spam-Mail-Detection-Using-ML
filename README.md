# Spam Email Detection Using Machine Learning

A simple, modular ML pipeline that classifies an email/SMS message as
**Spam** or **Not Spam**, built with `pandas`, `numpy`, `scikit-learn`,
and `nltk`.

## Project Structure

```
spam_detector/
├── data/
│   └── spam_dataset.tsv       # Labeled training data (ham/spam messages)
├── model/
│   ├── spam_classifier.pkl    # Saved trained model (created after training)
│   └── tfidf_vectorizer.pkl   # Saved TF-IDF vectorizer (created after training)
├── preprocessing.py           # Text cleaning (lowercasing, stopword removal, stemming)
├── train_model.py             # Trains and evaluates the model, saves it to disk
├── predict.py                 # Loads the model and classifies new messages
└── requirements.txt
```

## Setup (VS Code)

1. Open this folder in VS Code.
2. Create/activate a virtual environment (recommended):
   ```
   python -m venv venv
   venv\Scripts\activate      # Windows
   source venv/bin/activate   # macOS/Linux
   ```
3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

## How to Run

**Step 1 — Train the model** (run once, or whenever you update the dataset):
```
python train_model.py
```
This cleans the data, converts it to TF-IDF features, trains a Naive Bayes
classifier, prints accuracy/metrics, and saves the model to `model/`.

**Step 2 — Classify emails interactively:**
```
python predict.py
```
You'll be prompted to type a message, and the program will print whether
it's **Spam** or **Not Spam**, along with a confidence score. Type `exit`
to quit.

### Example
```
Enter email message: Congratulations! You won a free prize.
--------------------------------------------------
Result           : Spam
Spam Probability : 88.38%
--------------------------------------------------
```

## Using it in your own code

```python
from predict import predict_message

result = predict_message("Hi, can we reschedule our meeting to 3pm tomorrow?")
print(result)  # {'label': 'Not Spam', 'spam_probability': 0.02}
```

## How It Works (Pipeline Overview)

1. **Input** — `predict.py` accepts a raw email/SMS message as a string.
2. **Cleaning** (`preprocessing.py`) — lowercases text, removes URLs/emails/
   punctuation/numbers, tokenizes, removes stopwords, and stems each word.
3. **Vectorization** (`train_model.py`) — converts cleaned text into
   numerical features using **TF-IDF** (unigrams + bigrams, top 3000
   features) so the model can process it mathematically.
4. **Model Training** — a **Multinomial Naive Bayes** classifier is trained
   on the TF-IDF features (fast and well-suited to text classification).
5. **Prediction** — new messages are cleaned and vectorized the same way,
   then passed through the trained model to get a Spam/Not Spam label and
   a confidence score.
6. **Output** — the result is printed clearly to the user.

## Model Performance

On a held-out 20% test split of the dataset (5,572 labeled messages):
- **Accuracy: ~97.7%**
- High precision on spam (very few false positives — legitimate emails
  are rarely misflagged), satisfying the project's accuracy and speed
  requirements.

## Notes

- The dataset used (`data/spam_dataset.tsv`) is the widely-used SMS Spam
  Collection dataset (ham/spam labeled messages), a good general-purpose
  stand-in for email spam classification. You can swap in your own labeled
  dataset as long as it follows the same tab-separated `label<TAB>message`
  format.
- To retrain after changing the dataset, just rerun `train_model.py`.
