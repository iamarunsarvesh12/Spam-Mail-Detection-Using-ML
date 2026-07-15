import re
import string
import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize


def download_nltk_resources():
    """
    Download the NLTK resources required for cleaning, if they are not
    already present. This only needs to run once per machine.
    """
    resources = {
        "tokenizers/punkt": "punkt",
        "tokenizers/punkt_tab": "punkt_tab",
        "corpora/stopwords": "stopwords",
    }
    for path, name in resources.items():
        try:
            nltk.data.find(path)
        except LookupError:
            nltk.download(name, quiet=True)


download_nltk_resources()

STOPWORDS = set(stopwords.words("english"))
STEMMER = PorterStemmer()


def clean_text(message: str) -> str:
    """
    Clean a single raw email/SMS message and return a normalized,
    space-separated string of stemmed keywords ready for vectorization.

    Steps:
        - Lowercase everything so "Free" and "free" are treated the same
        - Strip URLs and email addresses (common spam signals become
          noise for a bag-of-words model, so we drop the raw text but
          keep a placeholder token instead)
        - Remove punctuation and digits
        - Tokenize into words
        - Remove stopwords and very short tokens
        - Stem each remaining word to its root form
    """
    message = message.lower()
    message = re.sub(r"http\S+|www\S+", " urllink ", message)
    message = re.sub(r"\S+@\S+", " emailaddr ", message)
    message = message.translate(str.maketrans("", "", string.punctuation))
    message = re.sub(r"\d+", " ", message)
    tokens = word_tokenize(message)

    cleaned_tokens = [
        STEMMER.stem(word)
        for word in tokens
        if word not in STOPWORDS and len(word) > 1
    ]

    return " ".join(cleaned_tokens)


def clean_series(messages):
    """
    Apply clean_text() to a pandas Series (or any iterable) of messages.
    Used when cleaning the entire dataset in bulk during training.
    """
    return [clean_text(msg) for msg in messages]


if __name__ == "__main__":
    # Quick manual test
    sample = "Congratulations!! You WON a FREE prize. Click http://bit.ly/claim now!!!"
    print("Original:", sample)
    print("Cleaned :", clean_text(sample))
