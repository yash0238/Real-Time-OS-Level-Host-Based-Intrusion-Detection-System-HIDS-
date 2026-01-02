import pandas as pd
import matplotlib.pyplot as plt
import os

PROCESS_CSV = "logs/process_log.csv"
ALERTS_CSV = "logs/alerts.csv"

def plot_top_process_cpu(n=5, out="logs/cpu_top_processes.png"):
    if not os.path.isfile(PROCESS_CSV):
        return
    df = pd.read_csv(PROCESS_CSV)
    grp = df.groupby('name')['cpu_percent'].mean().sort_values(ascending=False).head(n)         # pick top-n process names by mean cpu
    plt.figure(figsize=(8,4))
    grp.plot(kind='bar')
    plt.ylabel("Avg CPU%")
    plt.title(f"Top {n} Processes by Avg CPU%")
    plt.tight_layout()
    plt.savefig(out)
    plt.close()

def plot_time_series_for_pid(pid, name=None, out="logs/usage_timeseries.png"):
    if not os.path.isfile(PROCESS_CSV):
        return
    df = pd.read_csv(PROCESS_CSV)
    df_pid = df[df['pid'] == pid]
    if df_pid.empty:
        return
    df_pid['timestamp'] = pd.to_datetime(df_pid['timestamp'])
    plt.figure(figsize=(10,4))
    plt.plot(df_pid['timestamp'], df_pid['cpu_percent'], label="CPU%")
    plt.plot(df_pid['timestamp'], df_pid['memory_percent'], label="Memory%")
    plt.legend()
    plt.title(f"PID {pid} ({name}) resource usage")
    plt.xlabel("Time")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(out)
    plt.close()

def plot_alerts(out="logs/alerts_summary.png"):
    if not os.path.isfile(ALERTS_CSV):
        return
    df = pd.read_csv(ALERTS_CSV)
    if df.empty:
        return
    # show a bar chart of anomaly scores or cpu_percent if present
    if 'cpu_percent' in df.columns:
        df = df.sort_values('cpu_percent', ascending=False).head(10)
        plt.figure(figsize=(8,4))
        plt.barh(df['name'].astype(str) + " (" + df['pid'].astype(str) + ")", df['cpu_percent'])
        plt.xlabel("CPU%")
        plt.title("Top Alerts by CPU%")
        plt.tight_layout()
        plt.savefig(out)
        plt.close()
