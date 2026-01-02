import threading
import time
import psutil
from utils import append_rows_to_csv, timestamp, load_ip_cache, save_ip_cache
import socket
import requests
NETWORK_CSV = "logs/network_log.csv"
NETWORK_FIELDS = ['timestamp', 'pid', 'proc_name', 'laddr', 'raddr', 'status', 'rinfo']
USE_IP_API = True  # set True only if you want live lookups and network access

def ip_lookup(ip, cache):
    if ip in cache:
        return cache[ip]
    if not USE_IP_API:
        cache[ip] = "UNKNOWN"
        return "UNKNOWN"
    try:
        url = f"http://ip-api.com/json/{ip}"
        resp = requests.get(url, timeout=3)
        data = resp.json()
        info = f"{data.get('country','?')}|{data.get('org','?')}"
    except Exception:
        info = "UNKNOWN"
    cache[ip] = info
    return info




class NetworkMonitor(threading.Thread):
    def __init__(self, interval=2.0):
        super().__init__(daemon=True)
        self.interval = interval
        self._stop = threading.Event()
        self._ip_cache = load_ip_cache()

    def stop(self):
        self._stop.set()
        save_ip_cache(self._ip_cache)

    def run(self):
        while not self._stop.is_set():
            now = timestamp()
            rows = []
            try:
                conns = psutil.net_connections(kind='inet')  # TCP/UDP IPv4 & IPv6
            except Exception:
                conns = []
            for c in conns:
                try:
                    pid = c.pid
                    laddr = f"{c.laddr.ip}:{c.laddr.port}" if c.laddr else ""
                    raddr = f"{c.raddr.ip}:{c.raddr.port}" if c.raddr else ""
                    status = c.status
                    proc_name = ""
                    if pid:
                        try:
                            proc_name = psutil.Process(pid).name()          # get process name if available
                        except Exception:
                            proc_name = ""
                    rinfo = ""
                    if c.raddr:
                        ip = c.raddr.ip
                        rinfo = ip_lookup(ip, self._ip_cache)
                    rows.append({
                        'timestamp': now,
                        'pid': pid,
                        'proc_name': proc_name,
                        'laddr': laddr,
                        'raddr': raddr,
                        'status': status,
                        'rinfo': rinfo
                    })
                except Exception:
                    continue
            if rows:
                append_rows_to_csv(NETWORK_CSV, NETWORK_FIELDS, rows)
            time.sleep(self.interval)
