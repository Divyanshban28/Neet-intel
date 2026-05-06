import json
import requests
import streamlit as st
import pandas as pd
from collections import Counter

# --- CLOUD DATABASE CONNECTORS ---
GIST_ID = st.secrets.get("GIST_ID")
TOKEN = st.secrets.get("GITHUB_TOKEN")
URL = f"https://api.github.com/gists/{GIST_ID}"
HEADERS = {"Authorization": f"token {TOKEN}"}

def load_data():
    """Fetch history from Gist"""
    try:
        res = requests.get(URL, headers=HEADERS)
        if res.status_code == 200:
            return json.loads(res.json()["files"]["tests.json"]["content"])
        return []
    except:
        return []

def save_data(new_test):
    """Sync data to Gist"""
    history = load_data()
    history.append(new_test)
    payload = {"files": {"tests.json": {"content": json.dumps(history, indent=2)}}}
    res = requests.patch(URL, headers=HEADERS, json=payload)
    return res.status_code == 200

def get_metrics(meta, subjects, logs):
    """Calculates the intelligence metrics"""
    reasons = Counter([l['reason'] for l in logs])
    # Leak Score calculation: (Silly + Time + Guess) / Total Errors
    avoidable = sum(v for k, v in reasons.items() if k != "Conceptual")
    leak_score = round(avoidable / max(len(logs), 1), 2)
    
    return {
        "leak_score": leak_score,
        "reasons": dict(reasons),
        "hotspots": Counter([l['chapter'] for l in logs]).most_common(3)
    }
