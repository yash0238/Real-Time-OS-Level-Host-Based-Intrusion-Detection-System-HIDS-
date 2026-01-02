import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="OS HIDS Dashboard", layout="wide")

st.title("OS-Level HIDS Dashboard")

if os.path.exists("logs/process_log.csv"):
    dfp = pd.read_csv("logs/process_log.csv")
    st.subheader("Latest Process Log (tail)")
    st.dataframe(dfp.tail(50))

if os.path.exists("logs/network_log.csv"):
    dfn = pd.read_csv("logs/network_log.csv")
    st.subheader("Latest Network Connections (tail)")
    st.dataframe(dfn.tail(50))

if os.path.exists("logs/alerts.csv"):
    dfa = pd.read_csv("logs/alerts.csv")
    st.subheader("Detected Alerts")
    st.dataframe(dfa)
else:
    st.info("No alerts.csv found yet.")
