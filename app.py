import os
import io
from datetime import datetime

import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

st.set_page_config(page_title="BA Project Dashboard", layout="wide")

IMAGES_DIR = os.path.join(os.path.dirname(__file__), "images")


@st.cache_data
def load_csv(name):
    path = os.path.join(IMAGES_DIR, name)
    if not os.path.exists(path):
        return None
    try:
        return pd.read_csv(path)
    except Exception:
        try:
            return pd.read_excel(path)
        except Exception:
            return None


def list_available_files():
    if not os.path.exists(IMAGES_DIR):
        return []
    return sorted([f for f in os.listdir(IMAGES_DIR) if f.lower().endswith(('.csv','.xlsx'))])


def show_overview():
    st.title("Business Analytics — Project Dashboard")
    st.markdown("Use the left menu to explore RFM clusters, CLV, forecasts, and model results.")

    files = list_available_files()
    st.subheader("Available output files")
    st.write(files)

    desc = load_csv('descriptive_statistics.csv')
    miss = load_csv('missing_summary.csv')
    if desc is not None:
        st.subheader('Descriptive Statistics')
        st.dataframe(desc)
    if miss is not None:
        st.subheader('Missing Values Summary')
        st.dataframe(miss)


def make_rfm_boxplots(df, cols):
    fig = make_subplots(rows=1, cols=len(cols), subplot_titles=cols)
    for i, c in enumerate(cols, start=1):
        fig.add_trace(go.Box(y=df[c].dropna(), name=c, boxpoints='outliers'), row=1, col=i)
    fig.update_layout(height=400, showlegend=False)
    return fig


def show_rfm_clusters():
    st.header('RFM & Customer Clustering')

    rfm = load_csv('rfm_with_cluster.csv')
    if rfm is None:
        rfm = load_csv('rfm_final.csv')

    cluster_profile = load_csv('cluster_profile.csv')
    if cluster_profile is None:
        cluster_profile = load_csv('cluster_summary.csv')

    if rfm is None:
        st.warning('RFM dataset not found in images/. Please run the notebook to produce `rfm_with_cluster.csv` or `rfm_final.csv`.')
        return

    st.subheader('Sample of RFM with cluster labels')
    st.dataframe(rfm.head(100))

    if 'cluster' in rfm.columns:
        counts = rfm['cluster'].value_counts().sort_index()
        fig = px.bar(x=counts.index.astype(str), y=counts.values, labels={'x':'Cluster','y':'Customers'}, title='Customers per Cluster')
        st.plotly_chart(fig, width='stretch')

    if cluster_profile is not None:
        st.subheader('Cluster Profile')
        st.dataframe(cluster_profile)

    if set(['Recency','Frequency','Monetary']).issubset(rfm.columns):
        cols = ['Recency','Frequency','Monetary']
        fig = make_rfm_boxplots(rfm, cols)
        st.plotly_chart(fig, width='stretch')


def show_clv():
    st.header('Customer Lifetime Value (CLV)')
    clv = load_csv('customer_clv_results.csv')
    if clv is None:
        st.warning('CLV results not found (customer_clv_results.csv).')
        return

    st.subheader('Top customers by estimated CLV')
    n = st.slider('Top N customers', min_value=5, max_value=50, value=10)
    if 'CLV' not in clv.columns:
        st.warning('CLV column not found in the file.')
        st.dataframe(clv.head(n))
        return

    top = clv.sort_values(by='CLV', ascending=False).head(n)
    st.dataframe(top)

    fig = px.bar(top, x=top.columns[0], y='CLV', title=f'Top {n} Customers by CLV')
    st.plotly_chart(fig, width='stretch')

    st.subheader('Average CLV by cluster (if available)')
    if 'cluster' in clv.columns:
        agg = clv.groupby('cluster', as_index=False)['CLV'].mean().sort_values('CLV', ascending=False)
        st.dataframe(agg)
        fig2 = px.bar(agg, x='cluster', y='CLV', title='Average CLV by Cluster')
        st.plotly_chart(fig2, width='stretch')


def show_forecast():
    st.header('Sales Forecast')
    sf = load_csv('sales_forecast.csv')
    if sf is None:
        st.warning('Sales forecast file not found (`sales_forecast.csv`).')
        return

    st.subheader('Forecast data sample')
    st.dataframe(sf.head())

    date_col = None
    val_col = None
    for c in sf.columns:
        if 'date' in c.lower():
            date_col = c
        if 'forecast' in c.lower() or 'sales' in c.lower() or 'value' in c.lower():
            val_col = c

    if date_col is None:
        date_col = sf.columns[0]
    if val_col is None:
        val_col = sf.columns[1] if len(sf.columns) > 1 else sf.columns[0]

    try:
        sf[date_col] = pd.to_datetime(sf[date_col])
        fig = px.line(sf, x=date_col, y=val_col, title='Sales Forecast')
        st.plotly_chart(fig, width='stretch')
    except Exception:
        st.write('Unable to parse forecast dates — showing raw table instead.')


def show_model_metrics():
    st.header('Model Evaluation & Feature Importances')
    metrics = load_csv('model_evaluation_results.csv')
    fi = load_csv('feature_importances.csv')

    if metrics is not None:
        st.subheader('Model Metrics')
        st.dataframe(metrics)
        if 'ROC_AUC' in metrics.columns:
            fig = px.bar(metrics, x='Model', y='ROC_AUC', title='Model ROC AUC')
            st.plotly_chart(fig, width='stretch')
    else:
        st.warning('Model evaluation results not found.')

    if fi is not None:
        st.subheader('Feature Importances (Random Forest)')
        if fi.shape[1] == 1:
            s = fi.iloc[:,0]
            s = s.sort_values(ascending=False)
            fig = px.bar(x=s.values, y=s.index, orientation='h')
            st.plotly_chart(fig, width='stretch')
        else:
            cols = fi.columns.tolist()
            feat = cols[0]
            val = cols[1]
            fig = px.bar(fi.sort_values(val, ascending=False), x=feat, y=val, title='Feature Importances')
            st.plotly_chart(fig, width='stretch')
    else:
        st.info('Feature importances file not found.')


def show_data_explorer():
    st.header('Data Explorer')
    files = list_available_files()
    choice = st.selectbox('Choose a file to view', options=['-- choose --'] + files)
    if choice and choice != '-- choose --':
        df = load_csv(choice)
        if df is None:
            st.error('Unable to load file: ' + choice)
            return
        st.subheader(f'Preview — {choice}')
        st.dataframe(df)

        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button('Download CSV', csv, file_name=choice, mime='text/csv')


def main():
    pages = {
        'Overview': show_overview,
        'RFM & Clusters': show_rfm_clusters,
        'CLV': show_clv,
        'Forecast': show_forecast,
        'Model Metrics': show_model_metrics,
        'Data Explorer': show_data_explorer,
    }

    st.sidebar.title('Navigation')
    page = st.sidebar.radio('Go to', list(pages.keys()))

    with st.sidebar.expander('Helpful notes'):
        st.write('- This app reads CSV/XLSX files from the `images/` folder created by the notebook.')
        st.write('- If a dataset is missing, run `BA_NEW_vs.ipynb` to regenerate outputs.')

    pages[page]()


if __name__ == '__main__':
    main()
