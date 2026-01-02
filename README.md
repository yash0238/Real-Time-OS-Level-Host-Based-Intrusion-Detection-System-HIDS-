# Real-Time-OS-Level-Host-Based-Intrusion-Detection-System-HIDS
A real-time, OS-level Host-Based Intrusion Detection System (HIDS) that monitors actual Windows system processes and network connections, detects abnormal behavior using machine learning and statistical methods, and visualizes anomalies for security and performance insights.

<div align="center">

![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Platform](https://img.shields.io/badge/Platform-Linux%20%7C%20Windows%20%7C%20macOS-lightgrey.svg)

**A real-time, ML-powered intrusion detection system for monitoring and securing your operating system**

[Features](#-features) • [Installation](#-installation) • [Usage](#-usage) • [Architecture](#-architecture) • [Screenshots](#-screenshots)

</div>

---

## 🎯 Overview

This Host-based Intrusion Detection System (HIDS) provides comprehensive real-time monitoring of system processes and network connections, using machine learning to automatically detect anomalous behavior that could indicate security threats, malware, or system compromise.

### Key Capabilities

- **Real-time Process Monitoring**: Tracks CPU usage, memory consumption, and thread counts for all running processes
- **Network Activity Surveillance**: Monitors TCP/UDP connections with IP geolocation and organization lookup
- **ML-Based Anomaly Detection**: Uses Isolation Forest algorithm to identify suspicious processes
- **Statistical Analysis**: Z-score based fallback detection for robust threat identification
- **Interactive Dashboard**: Web-based Streamlit interface for live monitoring
- **Automated Alerts**: Desktop notifications for immediate threat awareness
- **Detailed Visualizations**: Matplotlib charts for forensic analysis

---

## 🚀 Features

### Monitoring Engine
- ⚡ **Concurrent Threading**: Independent process and network monitors running simultaneously
- 📊 **Configurable Intervals**: Customize sampling rates (default: 1s for processes, 2s for network)
- 💾 **CSV Logging**: Timestamped data persistence for historical analysis
- 🌐 **IP Intelligence**: Automatic geolocation and ISP identification for remote connections
- 🔄 **Smart Caching**: Offline capability with IP lookup caching

### Detection System
- 🤖 **Isolation Forest ML Model**: Unsupervised learning for anomaly detection (3% contamination threshold)
- 📈 **Z-Score Analysis**: Statistical outlier detection with configurable threshold (default: 3.0σ)
- 🎯 **PID Aggregation**: Process-level analysis for accurate threat identification
- 🚨 **Alert Generation**: Automatic CSV reports with detection metadata

### Visualization & Reporting
- 📉 **Top Consumers Chart**: Bar graphs of highest CPU-consuming processes
- 📈 **Time-Series Plots**: Resource usage trends for flagged processes
- 📊 **Alert Dashboard**: Ranked visualization of detected anomalies
- 🖥️ **Streamlit Web UI**: Interactive dashboard for real-time monitoring

---

## 📦 Installation

### Prerequisites
- Python 3.7 or higher
- pip package manager

### Quick Start

```bash
# Clone the repository
git clone https://github.com/yourusername/os-hids.git
cd os-hids

# Install dependencies
pip install -r requirements.txt
