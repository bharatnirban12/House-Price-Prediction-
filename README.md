# 🏠 House Price Prediction System

An end-to-end Machine Learning project that predicts house prices using structured data. This project is built with a **production-ready pipeline**, includes **MLflow experiment tracking**, and is deployed with **FastAPI (backend)** and **Streamlit (frontend)** on Render.

---

## 🚀 Features

* 🔹 Advanced Regression Models (Linear, Ridge, Lasso, ElasticNet)
* 🔹 Tree-based Models (Random Forest, XGBoost)
* 🔹 Feature Engineering & Outlier Handling
* 🔹 Cross-validation & Hyperparameter tuning
* 🔹 MLflow Experiment Tracking
* 🔹 FastAPI for model serving
* 🔹 Streamlit for interactive frontend
* 🔹 Cloud deployment on Render

---

## 🧠 Problem Statement

Predict the **SalePrice** of houses based on various features such as area, quality, neighborhood, and more using regression techniques.

---

## 📊 Dataset

* Dataset: *House Prices: Advanced Regression Techniques*
* Contains 80+ features related to residential homes.

---

## 🏗️ Project Structure

```
house_price_prediction/
│
├── data/
│   ├── raw/
│   ├── processed/
│
├── notebooks/
│   ├── 01_eda.ipynb
│   ├── 04_prediction_test.ipynb
│
├── src/
│   ├── components/
│   ├── pipeline/
│
├── models/
│   ├── model.pkl
│
├── app/
│   ├── main.py
│   ├── frontend.py
│   ├── schema.py
│
├──.streamlit
├── mlruns/
├── requirements.txt
├── README.md
```

---

## 🔄 ML Pipeline

1. Data Ingestion
2. Data Preprocessing
3. Feature Engineering
4. Train/Test Split
5. Model Training (Ridge, Lasso, ElasticNet, etc.)
6. Evaluation (RMSE, R²)
7. MLflow Tracking
8. Model Saving
9. API Deployment

> ⚠️ Note: Feature engineering is performed during the EDA stage and implemented in the preprocessing pipeline for production.

---

## 📈 Model Performance

* Best Model: **Ridge Regression**
* RMSE (log scale): ~0.12
* Approx prediction error: **~3–10%**

---

## ⚙️ Tech Stack

* Python
* Scikit-learn
* XGBoost
* MLflow
* FastAPI
* Streamlit

---

## 🧪 Run Locally

### 1. Clone repository

```
git clone https://github.com/your-username/house_price_prediction.git
cd house_price_prediction
```

### 2. Install dependencies

```
pip install -r requirements.txt
```

### 3. Run FastAPI

```
uvicorn app.main:app --reload
```

### 4. Run Streamlit

```
streamlit run app/frontend.py
```

---

## 🧠 Key Learnings

* Building production-ready ML pipelines
* Handling real-world data issues (missing values, outliers)
* Bias-variance tradeoff and regularization
* Experiment tracking with MLflow
* Deploying ML models as APIs
* Full-stack ML application (Backend + Frontend)

---

## 🏆 Conclusion

This project demonstrates how to move from **EDA → Modeling → Deployment**, building a complete ML system ready for real-world usage.

---

## 👨‍💻 Author
Bharat Budhram Nirban

