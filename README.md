# 🩺 Chronic Kidney Disease (CKD) Prediction – Flask Web App

This is a Flask-based web application for predicting Chronic Kidney Disease (CKD) using machine learning models such as Random Forest, XGBoost, and CatBoost. It provides a web interface where users can input medical data and receive real-time predictions.

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Flask](https://img.shields.io/badge/Flask-2.x-lightgrey)
![License](https://img.shields.io/badge/License-MIT-green)

---

## 🚀 Features

- 🔍 Predict CKD using trained machine learning models
- 👩‍⚕️ Role-based login for patients, doctors, and admins
- 📊 Interactive result display and recommendations
- 🧼 Built-in data preprocessing and model loading
- 🌐 User-friendly web interface using Flask templates

---

## 🧑‍💻 How to Run the App

### 1. Clone the Repository

```bash
git clone https://github.com/anushkagarg-30/CKD-Flask-App.git
cd CKD-Flask-App
````

### 2. Set Up a Virtual Environment (Optional but Recommended)

```bash
python -m venv env
# On Windows
env\Scripts\activate
# On macOS/Linux
source env/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Start the Flask Application

```bash
python app.py
```

Now open your browser and go to:
[http://127.0.0.1:5000](http://127.0.0.1:5000)

---

## 📁 Project Structure

```
CKD-Flask-App/
├── app.py                  # Main Flask app
├── models.py               # ML model loading and prediction logic
├── templates/              # HTML templates for views
├── static/                 # Static files (images, CSS)
├── utilities/              # Data preprocessing utilities
├── catboost_info/          # Logs from CatBoost training
├── requirements.txt        # Python dependencies
├── .gitignore              # Ignored files/folders
└── README.md               # Project documentation
```

---

## 📊 Dataset

This application uses the **Chronic Kidney Disease dataset** from the [UCI Machine Learning Repository](https://archive.ics.uci.edu/ml/datasets/chronic_kidney_disease). The dataset includes patient-level attributes such as:

* Blood Pressure
* Albumin
* Sugar
* Red Blood Cells
* Hemoglobin
* Serum Creatinine
* and more...

---

## 📦 Requirements

* Python 3.8+
* Flask
* scikit-learn
* pandas
* numpy
* xgboost
* catboost

Install them via `requirements.txt` or manually.

---

## 📄 License

This project is licensed under the MIT License. See the `LICENSE` file for more details.

---

## 👩‍💻 Author

**Anushka Garg**
GitHub: [@anushkagarg-30](https://github.com/anushkagarg-30)

```
