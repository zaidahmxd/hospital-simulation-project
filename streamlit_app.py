import streamlit as st
import pandas as pd
import random

# 1. THEME & AESTHETICS
st.set_page_config(page_title="Hospital Command Center", layout="centered")

# Custom CSS for that "Premium" look
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; }
    div[data-testid="stMetricValue"] { color: #4CAF50; }
    .token-card { 
        background: rgba(255, 255, 255, 0.05); 
        padding: 30px; 
        border-radius: 20px; 
        border: 2px solid #4CAF50;
        text-align: center;
        margin-bottom: 25px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
    }
    .doctor-tag {
        background: #1e2130;
        padding: 10px;
        border-radius: 10px;
        border-left: 5px solid #2196F3;
        margin: 5px 0;
    }
    </style>
    """, unsafe_all_ow_html=True)

# 2. DATA INITIALIZATION (The "Brain")
if 'queue' not in st.session_state:
    st.session_state.queue = []
if 'doctors' not in st.session_state:
    st.session_state.doctors = ["Dr. Arhaan (General)", "Dr. Sara (Emergency)"]
if 'my_token_id' not in st.session_state:
    st.session_state.my_token_id = None

# 3. NAVIGATION
st.sidebar.title("🏥 Hospital Menu")
mode = st.sidebar.radio("Switch View:", ["Patient Portal", "Admin Settings"])

# --- ADMIN SETTINGS (Hidden from Patients) ---
if mode == "Admin Settings":
    st.title("🛡️ Admin Control Panel")
    
    # Manage Doctors
    st.subheader("👨‍⚕️ Manage Hospital Staff")
    new_doc = st.text_input("Enter Doctor Name & Speciality")
    if st.button("Add Doctor to Duty"):
        if new_doc:
            st.session_state.doctors.append(new_doc)
            st.success(f"Added {new_doc}")
    
    st.write("---")
    st.write("**Current Staff (Click to remove):**")
    for i, doc in enumerate(st.session_state.doctors):
        col_a, col_b = st.columns([4, 1])
        col_a.write(f"📍 {doc}")
        if col_b.button("🗑️", key=f"del_{i}"):
            st.session_state.doctors.pop(i)
            # This line forces a refresh safely
            st.empty() 

# --- PATIENT PORTAL ---
else:
    st.title("🏥 Patient Check-In")

    # FEATURE: YOUR PRIVATE TOKEN CARD
    if st.session_state.my_token_id:
        st.markdown(f"""
            <div class="token-card">
                <p style='color: #888; margin-bottom: 0;'>YOUR PERSONAL TOKEN</p>
                <h1 style='font-size: 80px; margin: 0; color: #4CAF50;'>{st.session_state.my_token_id}</h1>
                <p style='font-size: 18px;'>Please wait in the lobby. We will call you soon.</p>
            </div>
            """, unsafe_all_ow_html=True)

    # FEATURE: REGISTRATION FORM
    with st.expander("Register for a Token", expanded=not st.session_state.my_token_id):
        p_name = st.text_input("Full Name")
        p_triage = st.selectbox("Urgency Level", ["Routine Checkup", "Urgent Care", "EMERGENCY"])
        
        if st.button("Generate Token"):
            if p_name:
                token = f"TK-{random.randint(100, 999)}"
                new_patient = {"id": token, "name": p_name, "triage": p_triage}
                
                # Priority logic: EMERGENCY goes to top
                if p_triage == "EMERGENCY":
                    st.session_state.queue.insert(0, new_patient)
                else:
                    st.session_state.queue.append(new_patient)
                
                st.session_state.my_token_id = token
                st.write("Token Generated! Look above.")

    # FEATURE: PUBLIC LIVE BOARD (ID ONLY)
    st.write("---")
    st.subheader("📋 Live Waitlist Status")
    if st.session_state.queue:
        # We only show IDs on the public board for privacy
        display_df = pd.DataFrame(st.session_state.queue)[['id', 'triage']]
        st.table(display_df)
    else:
        st.info("The queue is currently empty.")

    # FEATURE: DOCTORS ON DUTY
    st.write("---")
    st.subheader("👨‍⚕️ Available Doctors")
    if st.session_state.doctors:
        for d in st.session_state.doctors:
            st.markdown(f'<div class="doctor-tag">{d}</div>', unsafe_all_ow_html=True)
    else:
        st.warning("No doctors currently assigned.")
