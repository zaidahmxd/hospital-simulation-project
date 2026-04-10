import streamlit as st
import pandas as pd
import time

# --- CONFIGURATION & UI STYLE ---
st.set_page_config(page_title="Hospital Command Center", layout="wide")
st.title("🏥 Healthcare Flow & Resource Simulator")
st.markdown("---")

# --- SIDEBAR: THE SIMULATION ENGINE (The "What-If" Sliders) ---
st.sidebar.header("⚙️ Simulation Parameters")
num_doctors = st.sidebar.slider("Number of Doctors (Resources)", 1, 10, 3)
avg_service_time = st.sidebar.slider("Avg. Consultation Time (mins)", 5, 60, 15)
arrival_rate = st.sidebar.slider("Patient Arrival Rate (per hour)", 1, 30, 10)

# --- MATH LOGIC (Queuing Theory) ---
# Service Rate (mu) = patients per hour per doctor
mu = 60 / avg_service_time
total_mu = mu * num_doctors
utilization = arrival_rate / total_mu

# --- MAIN DASHBOARD: LIVE ANALYTICS ---
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("System Utilization", f"{round(utilization * 100, 1)}%")
    if utilization > 0.9:
        st.error("⚠️ BOTTLENECK DETECTED")
    else:
        st.success("✅ System Stable")

with col2:
    # Formula for expected wait time in an M/M/c queue (simplified)
    expected_wait = max(0, (utilization / (total_mu - arrival_rate)) * 60)
    st.metric("Avg. Wait Time", f"{round(expected_wait, 1)} mins")

with col3:
    st.metric("Resources Active", f"{num_doctors} Doctors")

st.markdown("---")

# --- THE TOKEN SYSTEM (Interactive Part) ---
st.subheader("🎟️ Patient Token Kiosk")
t_col1, t_col2 = st.columns([1, 2])

with t_col1:
    patient_name = st.text_input("Patient Name")
    triage = st.selectbox("Triage Level", ["1 - Emergency", "2 - Urgent", "3 - Routine"])
    if st.button("Generate Token"):
        st.balloons()
        st.success(f"Token Generated for {patient_name}!")
        # In a real app, this would write to your Google Sheet

with t_col2:
    st.write("**Live Priority Queue Board**")
    # Dummy data for visualization
    queue_data = pd.DataFrame({
        "Token": ["H-101", "H-102", "H-103"],
        "Severity": ["Emergency", "Urgent", "Routine"],
        "Status": ["In Progress", "Waiting", "Waiting"]
    })
    st.table(queue_data)

# --- RESOURCE HEATMAP ---
st.markdown("---")
st.subheader("📍 Department Heatmap")
# Visualizing bottlenecks
dept_data = pd.DataFrame({
    'Department': ['Emergency', 'Laboratory', 'Pharmacy', 'Radiology'],
    'Occupancy': [95, 40, 70, 20]
})
st.bar_chart(data=dept_data, x='Department', y='Occupancy')
