# AI-Powered Email Spam Classification Web Application

A full-stack, end-to-end Machine Learning web application that instantly classifies email or SMS messages as **Spam** or **Not Spam**. The project utilizes an optimized Machine Learning NLP pipeline in the backend and provides an interactive, modern, responsive web user interface for real-time predictions.

---

## ✨ Features

- **🎯 High Performance ML Model**
  - Multinomial Naive Bayes classifier with **97.7% accuracy**
  - Optimized TF-IDF feature extraction and vectorization
  - Fast inference (~1-2ms per prediction)

- **🧹 Robust Text Preprocessing**
  - Lowercasing and punctuation removal
  - Advanced tokenization with stopword filtering
  - Porter Stemming for morphological analysis
  - Customizable preprocessing pipeline

- **🎨 Modern Responsive UI**
  - Clean, minimal interface with Inter typography
  - FontAwesome icon library integration
  - Mobile-first responsive design
  - Dark/Light theme support

- **⚡ Real-time Processing**
  - Dynamic character counter (0-500 characters)
  - Instantaneous asynchronous API responses
  - Smooth loading animations
  - Context-aware feedback messages

- **🔔 Smart Feedback System**
  - Color-coded spam/safe alerts
  - Confidence score display
  - Classification certainty indicators
  - Detailed result analytics

---

## 📁 Project Structure

```
spam_detector/
│
├── data/
│   ├── spam_dataset.tsv          # Primary labeled training dataset (5,572 messages)
│   └── emails.csv                # Supplemental email corpus
│
├── model/
│   ├── spam_classifier.pkl       # Serialized Multinomial Naive Bayes model
│   └── tfidf_vectorizer.pkl      # Fitted TF-IDF vectorizer (100K features)
│
├── static/
│   ├── css/
│   │   └── style.css             # Custom styling (Flexbox, animations, themes)
│   └── js/
│       └── script.js             # DOM manipulation & async API handlers
│
├── templates/
│   └── index.html                # Semantic HTML5 frontend template
│
├── preprocessing.py              # Text pipeline module
├── train_model.py                # Model training & evaluation script
├── predict.py                    # Prediction utility & CLI interface
├── app.py                        # Flask application server
├── requirements.txt              # Python dependencies
└── README.md                     # Project documentation
```

---

### Running the Web Application

```bash
python app.py
```

The application will start on `http://localhost:5000`
