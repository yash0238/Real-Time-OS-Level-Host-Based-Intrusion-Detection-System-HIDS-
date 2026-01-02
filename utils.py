import os
import csv
from datetime import datetime
import json

IPCACHE_FILE = "logs/ip_cache.json"

def ensure_logs_dir():
    if not os.path.exists("logs"):
        os.makedirs("logs")

def timestamp():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def append_rows_to_csv(path, fieldnames, rows):
    """append a list of dict rows to CSV (create header if missing)."""
    ensure_logs_dir()
    file_exists = os.path.isfile(path)
    with open(path, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()
        for r in rows:
            writer.writerow(r)

def write_csv(path, df):
    ensure_logs_dir()
    df.to_csv(path, index=False)

# IP cache to avoid repeated lookups and to allow offline runs.
def load_ip_cache():
    if not os.path.exists(IPCACHE_FILE):
        return {}
    try:
        with open(IPCACHE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}

def save_ip_cache(cache):
    ensure_logs_dir()
    with open(IPCACHE_FILE, "w", encoding="utf-8") as f:
        json.dump(cache, f, indent=2)
