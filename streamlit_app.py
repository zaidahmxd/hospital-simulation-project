import streamlit as st
import pandas as pd
import random

# 1. PAGE CONFIG & DARK THEME AESTHETICS
st.set_page_config(page_title="Hospital Pro", layout="centered")

st.markdown("""
    <style>
    .main { background-color: #0e1117; color: white; }
    .stButton>button { width: 100%; border-radius: 10px; height: 3em; background-color: #2e7d32; color: white; }
    .token-card { 
        background: rgba(255, 255, 255, 0.05); 
        padding: 25px; 
        border-radius: 15px; 
        border: 1px solid rgba(255, 255, 255, 0.1);
        text-align: center;
        margin-bottom: 20px;
    }
    .admin-box {
        background: rgba(255, 75, 75, 0.05);
        padding: 20px;
        border-radius: 15px;
        border: 1px dashed #ff4b4b;
    }
    </style>
    """, unsafe_all_ow_html=True)

# 2. INITIALIZE DATA (This keeps the app from resetting)
if 'queue' not in st.session_state:
    st.session_state.queue = []
if 'doctors' not in st.session_state:
    st.session_state.doctors = ["Dr. Smith (General)", "Dr. Khanna (Cardio)"]
if 'my_token' not in st.session_state:
    st.session_state.my_token = None

# 3. SIDEBAR NAVIGATION (Admin vs Patient)
st.sidebar.title("🏥 Navigation")
mode = st.sidebar.radio("Go to:", ["Patient Portal", "Admin Dashboard"])

# --- ADMIN DASHBOARD ---
if mode == "Admin Dashboard":
    st.title("🛡️ Admin Settings")
    st.markdown("Only authorized staff should access this area.")
    
    with st.container():
        st.write("### Manage Doctors")
        new_doc = st.text_input("Add New Doctor Name")
        if st.button("Add Doctor"):
            if new_doc:
                st.session_state.doctors.append(new_doc)
                st.rerun()
        
        st.write("---")
        st.write("### Current Active Doctors")
        for i, doc in enumerate(st.session_state.doctors):
            cols = st.columns([3, 1])
            cols[0].write(doc)
            if cols[1].button("Remove", key=f"del_{i}"):
                st.session_state.doctors.pop(i)
                st.rerun()

# --- PATIENT PORTAL ---
else:
    st.title("🏥 Patient Check-In")
    
    # Feature 1: Personal Token Display (Separate from Board)
    if st.session_state.my_token:
        st.markdown(f"""
            <div class="token-card">
                <h2 style='color: #4CAF50;'>YOUR TOKEN</h2>
                <h1 style='font-size: 70px;'>{st.session_state.my_token['id']}</h1>
                <p>Status: <b>{st.session_state.my_token['status']}</b></p>
                <p>Estimated Wait: 15 mins</p>
            </div>
            """, unsafe_all_ow_html=True)

    # Feature 2: Registration Form
    with st.expander("Register for a New Token", expanded=not st.session_state.my_token):
        name = st.text_input("Enter Full Name")
        triage = st.selectbox("Urgency", ["Routine", "Urgent", "Emergency"])
        
        if st.button("Generate My Token"):
            if name:
                new_id = f"H-{random.randint(1000, 9999)}"
                new_entry = {"id": new_id, "name": name, "triage": triage, "status": "Waiting"}
                
                # Priority Logic: Emergencies go to the front
                if triage == "Emergency":
                    st.session_state.queue.insert(0, new_entry)
                else:
                    st.session_state.queue.append(new_entry)
                
                st.session_state.my_token = new_entry
                st.rerun()

    # Feature 3: Live Priority Board (Simple List)
    st.write("---")
    st.subheader("📋 Public Waitlist")
    if st.session_state.queue:
        df = pd.DataFrame(st.session_state.queue)[['id', 'triage', 'status']]
        st.table(df)
    else:
        st.info("No one is currently in the queue.")

    # Feature 4: Display Doctors (View Only for Patients)
    st.write("---")
    st.subheader("👨‍⚕️ Doctors on Duty")
    cols = st.columns(len(st.session_state.doctors) if st.session_state.doctors else 1)
    for i, doc in enumerate(st.session_state.doctors):
        with cols[i % len(cols)]:
            st.info(doc)
