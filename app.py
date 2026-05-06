import streamlit as st
import datetime
from analysis import load_data, save_data, get_metrics

st.set_page_config(page_title="NEET Intel Engine", layout="wide")

# Sidebar
st.sidebar.title("🩺 NEET Intelligence")
nav = st.sidebar.radio("Go to", ["Dashboard", "New Test Entry", "History"])

history = load_data()

if nav == "Dashboard":
    st.title("Performance Analytics")
    if not history:
        st.info("No data yet. Log your first test to see trends.")
    else:
        last = history[-1]
        col1, col2 = st.columns(2)
        col1.metric("Latest Score", last['meta']['score'])
        col2.metric("Tests Taken", len(history))
        # Future: Add Plotly graphs here

elif nav == "New Test Entry":
    st.title("📝 Log Test Details")
    with st.form("test_form"):
        # Section 1: Meta
        c1, c2, c3 = st.columns(3)
        name = c1.text_input("Test Name")
        date = c2.date_input("Date")
        score = c3.number_input("Total Score", 0, 720)
        
        # Section 2: Subjects
        subjects = {}
        for sub in ["Physics", "Chemistry", "Botany", "Zoology"]:
            sc1, sc2 = st.columns(2)
            m = sc1.number_input(f"{sub} Marks", 0, 180)
            w = sc2.number_input(f"{sub} Mistakes", 0, 45)
            subjects[sub] = {"marks": m, "wrong": w}
        
        # Section 3: Mistake Logging
        total_w = sum(s['wrong'] for s in subjects.values())
        st.write(f"### Log {total_w} Mistakes")
        logs = []
        for i in range(total_w):
            with st.expander(f"Error #{i+1}"):
                l1, l2, l3 = st.columns(3)
                ch = l1.text_input("Chapter", key=f"ch{i}")
                tp = l2.text_input("Topic", key=f"tp{i}")
                rs = l3.selectbox("Reason", ["Conceptual", "Silly", "Time", "NCERT", "Guess"], key=f"rs{i}")
                logs.append({"chapter": ch, "topic": tp, "reason": rs})
        
        if st.form_submit_button("Sync & Generate"):
            meta = {"name": name, "date": str(date), "score": score}
            metrics = get_metrics(meta, subjects, logs)
            if save_data({"meta": meta, "subjects": subjects, "logs": logs}):
                st.success("Synced to Cloud!")
                st.json(metrics)

elif nav == "History":
    st.title("📜 Previous Tests")
    for test in reversed(history):
        with st.expander(f"{test['meta']['date']} - {test['meta']['name']}"):
            st.write(f"**Score:** {test['meta']['score']}")
            st.write(test['subjects'])
