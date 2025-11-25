# A Comprehensive Business Analytics Framework for E-Commerce  
**Customer Segmentation • Churn Prediction • CLV Estimation • Sales Forecasting • BI Dashboards**

[![Status](https://img.shields.io/badge/status-complete-brightgreen.svg)]()
[![Python](https://img.shields.io/badge/python-3.8%2B-blue.svg)]()
[![Streamlit](https://img.shields.io/badge/streamlit-app-orange.svg)]()

---

## 🔎 Project Summary

This repository contains an end-to-end business analytics solution for e-commerce transaction data. The project performs data ingestion and preprocessing, exploratory data analysis (EDA), RFM-based customer segmentation, churn prediction using machine learning, Customer Lifetime Value (CLV) estimation, ARIMA-based sales forecasting, and delivers interactive dashboards via **Streamlit** and analytics-ready visualizations for **Power BI**.

Key deliverables:
- Cleaned and preprocessed dataset
- RFM scoring & K-Means clustering
- Churn prediction models (Logistic Regression, Random Forest, XGBoost, Decision Tree)
- CLV ranking and prioritized retention list
- 6-month sales forecast (ARIMA)
- Streamlit dashboard (`app.py`) and Power BI-ready exports

---

## 🔗 Important files (in this repo)

- `BA_NEW_vs.ipynb` — Primary analysis notebook (Colab/Jupyter).  
- `BA_NEW (2).ipynb` — Additional notebook copy / checkpoints.  
- `app.py` — Streamlit dashboard (interactive exploration & visualizations).  
- `images/` — Saved EDA and model visualizations (plots used in report).  
- `bi_exports/` — CSV exports used for BI dashboards (RFM, forecast, model results).  
- `report/` — PPT / PDF exports for submission.  
- `requirements.txt` — Python dependencies.

> Notebook path examples (in repo):  
> - `https://github.com/ANILKUMARCHAGANTI/Business_Analytics/blob/main/BA_NEW_vs.ipynb`  

---

## 🗂 Repository Structure

Business_Analytics/
├── BA_NEW_vs.ipynb
├── BA_report and ppt
├── app.py
├── images/
├── bi_exports/
├── report/
├── requirements.txt
└── README.md

---

## ⚙️ Setup & Installation

### 1) Clone the repository
```bash
git clone https://github.com/ANILKUMARCHAGANTI/Business_Analytics.git
cd Business_Analytics
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS / Linux
source .venv/bin/activate
pip install -r requirements.txt

### ipynb Notebook
Run the analysis notebook
Google Colab (recommended if you don't have local resources): upload BA_NEW_vs.ipynb to Colab or open from GitHub.
Dataset Link: -`https://huggingface.co/datasets/electricsheepafrica/nigerian_retail_and_ecommerce_purchase_history_records`

### Run streamlit
streamlit run app.py

### Results
![Clusters](images/cluster_pca_projection.png)
![Forecast](images/sales_forecast_clean.png)
![Dashboard sample](images/dashboard_overview.png)
## 📊 Model Performance Summary

| Model               | Accuracy | Precision | Recall | F1-Score | ROC-AUC |
|---------------------|----------|-----------|--------|----------|---------|
| **Logistic Regression** | **0.9309** | **0.9972** | **0.9227** | **0.9585** | **0.9613** |
| **Random Forest**       | 0.8974 | 1.0000 | 0.8814 | 0.9370 | **0.9639** |
| **Decision Tree**       | 0.7322 | 0.9867 | 0.6998 | 0.8188 | 0.8942 |
| **XGBoost**             | **0.9355** | **1.0000** | **0.9254** | **0.9612** | **0.9640** |

**Key Observations:**
- **XGBoost** delivered the best overall performance (highest F1 and AUC).  
- **Logistic Regression** also performed extremely well and offers high interpretability.  
- **Random Forest** showed excellent precision but slightly lower recall.  
- **Decision Tree** had the weakest performance due to overfitting.  

