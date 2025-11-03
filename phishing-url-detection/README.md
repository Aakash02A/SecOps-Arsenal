# 🧩 PHISHING URL DETECTION PROJECT

## 🎯 Objective  
Detect and classify **phishing URLs** by analyzing their structure and textual patterns using **machine learning**.  
The project extracts various lexical and statistical features from URLs and trains a **Random Forest Classifier** to identify malicious or safe websites.

---

## 📊 Dataset  
- **Source:** [Malicious and Benign URL Dataset – Kaggle](https://www.kaggle.com/datasets/sid321axn/malicious-urls-dataset)  
- **File Used:** `malicious_phish.csv`  
- **Columns:**  
  - `url` → The website address  
  - `type` → Category label (phishing, benign, defacement, malware)  

---

## ⚙️ Workflow  

1. **Data Loading & Exploration**  
   - Load the dataset (`malicious_phish.csv`) using pandas  
   - Display info, unique labels, and missing values  

2. **Label Encoding**  
   - Convert textual target labels (`type`) into numeric form using `LabelEncoder`  

3. **Feature Engineering**  
   Extract lexical and structural features from URLs, such as:  
   - URL length  
   - Hostname length  
   - Path length  
   - Number of special characters (`-`, `.`, `@`, `?`, `=`)  
   - Number of digits  
   - Count of HTTPS / HTTP occurrences  
   - Number of suspicious words (`login`, `secure`, `update`, etc.)  

4. **Model Training**  
   - Split data into **train (80%)** and **test (20%)**  
   - Train a **Random Forest Classifier** with 200 estimators  

5. **Evaluation**  
   - Evaluate model performance using:  
     - Accuracy score  
     - Classification report (precision, recall, F1-score)  
     - Confusion matrix  
   - Visualize feature importance using matplotlib  

6. **Model Saving**  
   - Save the trained model and label encoder using `joblib`  
     - `phishing_url_detector.pkl`  
     - `label_encoder.pkl`  

7. **Prediction on New URLs**  
   - Test the model with sample URLs, e.g.:  
     ```
     http://freebonus-login-secure-account.com
     ```
   - Output → Predicted label (e.g., phishing, benign, malware, etc.)

---

## 🧠 Key Learnings  

- How to extract **lexical and statistical features** from URLs  
- How to encode categorical target variables for machine learning  
- Application of **Random Forest** for classification tasks  
- Evaluating classification models using standard metrics  
- End-to-end ML pipeline: **data → model → evaluation → deployment**

---

## 📈 Results  

| Metric | Description |
|:--------|:-------------|
| **Model** | RandomForestClassifier (200 trees) |
| **Accuracy** | ~96–98% (varies by dataset) |
| **Top Features** | `url_length`, `count_digits`, `suspicious_words`, `count.` |

## 🧩 Features Extracted  

| Feature | Description |
|:----------|:-------------|
| `url_length` | Total length of the URL |
| `hostname_length` | Length of the domain (hostname) |
| `path_length` | Length of the URL path |
| `count-`, `count@`, `count?`, `count=`, `count.` | Counts of respective symbols |
| `count_digits` | Number of digits in the URL |
| `count_https`, `count_http` | Whether the URL contains `https` or `http` |
| `suspicious_words` | Count of suspicious keywords (`login`, `secure`, `account`, etc.) |

