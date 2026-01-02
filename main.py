import time
from process_monitor import ProcessMonitor
from network_monitor import NetworkMonitor
from anomaly_detector import run_detection
from visualizer import plot_top_process_cpu, plot_alerts, plot_time_series_for_pid
from utils import ensure_logs_dir
import argparse
import psutil
try:
    from plyer import notification
    PLYER_AVAILABLE = True
except Exception:
    PLYER_AVAILABLE = False

def notify(title, message):
    if PLYER_AVAILABLE:
        notification.notify(title=title, message=message, timeout=5)
    else:
        print(f"[NOTIFY] {title} - {message}")



def main(run_seconds=60, proc_interval=1.0, net_interval=2.0):
    ensure_logs_dir()
    pm = ProcessMonitor(interval=proc_interval)
    nm = NetworkMonitor(interval=net_interval)
    print("Starting monitors")
    pm.start()
    nm.start()
    print(f"Monitors running for {run_seconds} seconds. You can continue with your normal activities")
    try:
        for i in range(int(run_seconds)):
            time.sleep(1)
    except KeyboardInterrupt:
        print("Keyboard Interrupt")
    print("Stopping monitors")
    pm.stop()
    nm.stop()
    time.sleep(1)
    
    anomalies = run_detection()     #detection
    if anomalies is not None and not anomalies.empty:
        notify("HIDS Alert", f"{len(anomalies)} anomalies detected")

        top = anomalies.sort_values('cpu_percent', ascending=False).head(1)     #plot top CPU process timeseries
        if not top.empty:
            pid = int(top.iloc[0]['pid'])
            name = top.iloc[0]['name']
            plot_time_series_for_pid(pid, name)
    else:
        print("No anomalies found.")
    plot_top_process_cpu()
    plot_alerts()
    print("All done. Check logs/ for outputs.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--time", type=int, default=60, help="Monitoring duration in seconds")
    args = parser.parse_args()
    main(run_seconds=args.time)
