import threading
import time
import psutil
from datetime import datetime
from utils import append_rows_to_csv, timestamp

PROCESS_CSV = "logs/process_log.csv"
PROCESS_FIELDS = ['timestamp', 'pid', 'name', 'username', 'cpu_percent', 'memory_percent', 'num_threads']

class ProcessMonitor(threading.Thread):
    def __init__(self, interval=1.0):
        super().__init__(daemon=True)
        self.interval = interval
        self._stop = threading.Event()

    def stop(self):
        self._stop.set()



    def run(self):
        psutil.cpu_percent(interval=None)
        while not self._stop.is_set():
            now = timestamp()
            rows = []
            for p in psutil.process_iter(['pid', 'name', 'username']):
                try:
                    info = p.info
                    cpu = p.cpu_percent(interval=None)                #returns last computed value; we rely on periodic sampling
                    mem = p.memory_percent()
                    threads = p.num_threads()
                    rows.append({
                        'timestamp': now,
                        'pid': info.get('pid'),
                        'name': info.get('name') or '',
                        'username': info.get('username') or '',
                        'cpu_percent': round(cpu, 2),
                        'memory_percent': round(mem, 2),
                        'num_threads': threads
                    })
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
            if rows:
                append_rows_to_csv(PROCESS_CSV, PROCESS_FIELDS, rows)
            time.sleep(self.interval)
