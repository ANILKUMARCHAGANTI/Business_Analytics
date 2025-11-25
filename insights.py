import os
import pandas as pd
import numpy as np

IMAGES_DIR = os.path.join(os.path.dirname(__file__), "images")

def load_any(paths):
    for p in paths:
        fp = os.path.join(IMAGES_DIR, p)
        if os.path.exists(fp):
            try:
                return pd.read_csv(fp)
            except Exception:
                try:
                    return pd.read_excel(fp)
                except Exception:
                    continue
    return None


def safe_read(name):
    fp = os.path.join(IMAGES_DIR, name)
    if os.path.exists(fp):
        try:
            return pd.read_csv(fp)
        except Exception:
            try:
                return pd.read_excel(fp)
            except Exception:
                return None
    return None


def main():
    os.makedirs(IMAGES_DIR, exist_ok=True)

    # Load RFM (per-customer) and CLV results
    rfm = load_any(['rfm_with_cluster.csv', 'rfm_final.csv', 'images/rfm_with_cluster.csv'])
    clv = load_any(['customer_clv_results.csv', 'images/customer_clv_results.csv'])
    rfm_for_model = load_any(['rfm_for_model.csv', 'images/rfm_for_model.csv'])
    sales_fc = safe_read('sales_forecast.csv')

    kpis = []

    if rfm is not None:
        total_customers = int(rfm.shape[0])
        total_monetary = float(rfm['Monetary'].sum()) if 'Monetary' in rfm.columns else float(rfm.select_dtypes(include=[np.number]).sum().sum())
        total_freq = int(rfm['Frequency'].sum()) if 'Frequency' in rfm.columns else None
        avg_order_value = None
        if total_freq and total_freq > 0:
            avg_order_value = total_monetary / total_freq

        kpis.append(('total_customers', total_customers))
        kpis.append(('total_revenue', round(total_monetary,2)))
        if avg_order_value is not None:
            kpis.append(('avg_order_value', round(avg_order_value,2)))
    else:
        kpis.append(('total_customers', 'N/A'))
        kpis.append(('total_revenue', 'N/A'))

    if clv is not None and 'CLV' in clv.columns:
        avg_clv = float(clv['CLV'].mean())
        top5_clv = clv.sort_values('CLV', ascending=False).head(5)
        kpis.append(('average_clv', round(avg_clv,2)))
        kpis.append(('top_5_clv_customers', ';'.join(map(str, top5_clv.iloc[:,0].astype(str).tolist()))))

    if rfm_for_model is not None and 'ChurnFlag' in rfm_for_model.columns:
        churn_rate = float(rfm_for_model['ChurnFlag'].mean())
        kpis.append(('churn_rate', round(churn_rate,4)))

    if sales_fc is not None:
        # sum forecast if numeric
        numeric_cols = sales_fc.select_dtypes(include=[np.number]).columns.tolist()
        if numeric_cols:
            kpis.append(('forecast_sum_preview', round(float(sales_fc[numeric_cols[0]].sum()),2)))

    # Save KPI summary
    kpi_df = pd.DataFrame(kpis, columns=['metric','value'])
    kpi_csv = os.path.join(IMAGES_DIR, 'kpi_summary.csv')
    kpi_df.to_csv(kpi_csv, index=False)
    print('Saved KPI summary to', kpi_csv)

    # Write a short insights text file
    insights = []
    insights.append('KPI Summary generated from notebook outputs in images/')
    for m,v in kpis:
        insights.append(f'- {m}: {v}')

    if rfm is not None:
        # Top revenue customers (by Monetary)
        if 'Monetary' in rfm.columns:
            top = rfm.sort_values('Monetary', ascending=False).head(5)
            insights.append('\nTop 5 customers by Monetary value:')
            for idx,row in top.iterrows():
                # use iloc to avoid FutureWarning when accessing by position
                try:
                    cid = row.iloc[0]
                except Exception:
                    cid = row.index[0] if len(row.index) > 0 else idx
                val = row.get('Monetary', None)
                insights.append(f'  - {cid}: {val}')
        # Cluster insights
        if 'cluster' in rfm.columns:
            cluster_profile = rfm.groupby('cluster').agg({'Monetary':'sum','Frequency':'sum'}).reset_index()
            best = cluster_profile.sort_values('Monetary', ascending=False).head(1)
            if not best.empty:
                c = int(best.iloc[0]['cluster'])
                insights.append(f'\nCluster {c} contributes the highest monetary value — consider prioritizing retention or personalized offers for this segment.')

    out_txt = os.path.join(IMAGES_DIR, 'insights.txt')
    with open(out_txt, 'w', encoding='utf-8') as f:
        f.write('\n'.join(insights))

    print('Saved narrative insights to', out_txt)


if __name__ == '__main__':
    main()
