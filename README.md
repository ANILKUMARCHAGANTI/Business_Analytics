# A Comprehensive Business Analytics Framework for E-Commerce  
**Customer Segmentation • Churn Prediction • CLV Estimation • Sales Forecasting • BI Dashboards**

[![Status](https://img.shields.io/badge/status-complete-brightgreen.svg)]()
[![Python](https://img.shields.io/badge/python-3.8%2B-blue.svg)]()
[![Streamlit](https://img.shields.io/badge/streamlit-app-orange.svg)]()

---

## 🔎 Project Summary
Team Details:
- Ch.Dinesh          BL.EN.U4CSE22213
- G.Krishna Koushik  BL.EN.U4CSE22023
- P.Jaya Chetan      BL.EN.U4CSE22044
- Ch.Anil Kumar      BL.EN.U4CSE22213
- Project Mentor: Dr. Sajitha Krishnan Assistant Professor, Department of Computer Science and Engineeirng, School of Computing, Bangalore

This repository presents a complete **end-to-end business analytics framework** for e-commerce retail data. The project integrates data preprocessing, exploratory analysis, customer segmentation, churn prediction, Customer Lifetime Value (CLV) estimation, time-series sales forecasting, and interactive dashboards through **Streamlit** and **Power BI**.

The pipeline supports data-driven decisions for improving retention, maximizing customer value, and forecasting future sales trends.

---

## 📌 Important Files in This Repository

- `BA_NEW_vs.ipynb` — Main analysis notebook (EDA, RFM, clustering, ML, forecasting, CLV)
- `BA_NEW (2).ipynb` — Additional notebook backup
- `app.py` — Streamlit dashboard for interactive insights
- `images/` — Charts generated during analysis
- `bi_exports/` — CSV exports for BI dashboards (RFM, forecast, churn outputs)
- `report/` — PPT/PDF project report
- `requirements.txt` — Python package dependencies

Dataset link:  
https://huggingface.co/datasets/electricsheepafrica/nigerian_retail_and_ecommerce_purchase_history_records



---
## 🗂 Repository Details

```plaintext
Business_Analytics/
├── BA_NEW_vs.ipynb
├── app.py
├── images/
│   ├── cluster_pca_projection.png
│   ├── sales_forecast_clean.png
│   ├── payment_method_revenue.png
│   └── ...
├── bi_exports/
│   ├── rfm_full_data.csv
│   ├── sales_forecast.csv
│   ├── model_results.csv
│   └── ...
│   ├── Business_Analytics_Project_Report.pdf
│   ├── presentation.pptx
│   └── ...
├── requirements.txt
└── README.md\
---
## 🗂 **Clone the Repository**
git clone https://github.com/ANILKUMARCHAGANTI/Business_Analytics.git
cd Business_Analytics
**Create & Activate Virtual Environment**
python -m venv .venv
**Windows:**
.venv\Scripts\activate
**macOS/Linux:**
source .venv/bin/activate
**Install Dependencies**
pip install -r requirements.txt

---
## 📊 **Model Performance Summary**
| Model               | Accuracy | Precision | Recall | F1-Score | ROC-AUC |
|---------------------|----------|-----------|--------|----------|---------|
| Logistic Regression | 0.9309   | 0.9972    | 0.9227 | 0.9585   | 0.9613  |
| Random Forest       | 0.8974   | 1.0000    | 0.8814 | 0.9370   | 0.9639  |
| Decision Tree       | 0.7322   | 0.9867    | 0.6998 | 0.8188   | 0.8942  |
| XGBoost             | 0.9355   | 1.0000    | 0.9254 | 0.9612   | 0.9640  |
---
**Key Observations:**
- **XGBoost** delivered the best overall performance (highest F1 and AUC).  
- **Logistic Regression** also performed extremely well and offers high interpretability.  
- **Random Forest** showed excellent precision but slightly lower recall.  
- **Decision Tree** had the weakest performance due to overfitting.

---
**Dashboard features include**:
Customer segments (RFM + Clusters)
Churn probability insights
Customer Lifetime Value (CLV)
Sales Forecast (ARIMA)
Visual Data Explorer
Downloadable CSV insights
