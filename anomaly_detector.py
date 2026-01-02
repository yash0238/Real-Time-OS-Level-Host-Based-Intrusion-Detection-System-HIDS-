import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
from utils import write_csv, timestamp
import os
PROCESS_CSV = "logs/process_log.csv"
ALERTS_CSV = "logs/alerts.csv"
SUMMARY_CSV = "logs/summary_report.csv"

def load_process_data():
    if not os.path.isfile(PROCESS_CSV):
        return pd.DataFrame()
    df = pd.read_csv(PROCESS_CSV)
    df['cpu_percent'] = pd.to_numeric(df['cpu_percent'], errors='coerce').fillna(0)
    df['memory_percent'] = pd.to_numeric(df['memory_percent'], errors='coerce').fillna(0)
    return df



def aggregate_by_pid(df):
    agg = df.groupby(['pid', 'name']).agg({
        'cpu_percent': 'mean',
        'memory_percent': 'mean',
        'num_threads': 'mean'
    }).reset_index()
    return agg

def detect_isolationforest(agg_df, contamination=0.03):
    if agg_df.shape[0] < 5:
        return pd.DataFrame()  # not enough samples
    features = agg_df[['cpu_percent', 'memory_percent', 'num_threads']].fillna(0)
    model = IsolationForest(contamination=contamination, random_state=42)
    labels = model.fit_predict(features)
    agg_df['anomaly_iforest'] = labels  # -1 anomaly, 1 normal
    anomalies = agg_df[agg_df['anomaly_iforest'] == -1].copy()
    anomalies['detected_by'] = 'isolation_forest'
    return anomalies


def detect_zscore(agg_df, z_thresh=3.0):
    df = agg_df.copy()
    df['cpu_z'] = (df['cpu_percent'] - df['cpu_percent'].mean()) / (df['cpu_percent'].std(ddof=0) + 1e-9)
    df['mem_z'] = (df['memory_percent'] - df['memory_percent'].mean()) / (df['memory_percent'].std(ddof=0) + 1e-9)
    anomalies = df[(df['cpu_z'].abs() > z_thresh) | (df['mem_z'].abs() > z_thresh)].copy()
    anomalies['detected_by'] = 'zscore'
    return anomalies

def run_detection():
    df = load_process_data()
    if df.empty:
        print("No process data yet.")
        return pd.DataFrame()
    agg = aggregate_by_pid(df)
    anomalies = detect_isolationforest(agg)         #ML-based detection
    if anomalies.empty:
        anomalies = detect_zscore(agg)
    if not anomalies.empty:
        anomalies['detected_at'] = timestamp()
        write_csv(ALERTS_CSV, anomalies)
        # produce simple summary
        summary = {
            'detected_at': timestamp(),
            'num_processes_scanned': int(agg.shape[0]),
            'num_anomalies': int(anomalies.shape[0]),
            'top_cpu': float(agg['cpu_percent'].max())
        }
        write_csv(SUMMARY_CSV, pd.DataFrame([summary]))
        print(f"Detected {anomalies.shape[0]} anomalies. Alerts written to {ALERTS_CSV}")
    else:
        print("No anomalies detected in this run.")
    return anomalies
