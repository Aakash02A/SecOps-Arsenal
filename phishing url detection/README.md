# Phishing URL Detection

This project is a machine learning pipeline to detect phishing, defacement, malware, and benign URLs. It uses handcrafted URL features and TF-IDF vectorization combined with a LightGBM or RandomForest classifier.

## Features

- URL lexical features (length, digits, dots, hyphens, underscores)
- Hostname features (subdomains, IP address in hostname)
- URL entropy
- HTTPS presence
- Tokenized URL features (1-3 grams) with TF-IDF

## Dataset

- The dataset is from Kaggle and contains over 650,000 URLs labeled as:
  - `benign`
  - `phishing`
  - `defacement`
  - `malware`

Make sure your CSV has at least the following columns:

- `url` — the URL string  
- `type` — class label (`benign`, `phishing`, `defacement`, `malware`)  

The script will try to detect similar column names automatically.
