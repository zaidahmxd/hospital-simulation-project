import streamlit as st
import pandas as pd
import random

# 1. SETUP & THEME
st.set_page_config(page_title="Hospital Flow", layout="centered")

# Custom Dark Mode & Premium UI
st.markdown("""
    <style>
    .stApp { background-color: #0b0e14; color: #e0e0e0; }
    .token-box {
        background: #161b22;
        padding: 40px;
        border-radius: 25px;
        border: 2px solid #238636;
        text-align: center;
        margin: 20px 0px;
        box-shadow: 0px 10px 30px rgba(0,0,0,0.5);
    }
    .doctor-card {
        background: #1c2128;
        padding: 12px;
        border-radius: 8px;
        border-left: 4px solid #58a6ff;
        margin-bottom: 8px;
    }
    </style>
    """, unsafe_all_ow_html=True)

# 2. THE DATA "BRAIN" (Initialized to prevent TypeErrors)
if 'queue_list' not in st.session_state:
    st.session_state['queue_list'] = []
if 'staff_list' not in st.session_state:
    st.session_state['staff_list'] = ["Dr. Zaid (Chief)", "Dr. Anya (ER)"]
if 'user_token' not in st.session_state:
    st.session_state['user_token'] = ""

# 3. SIDEBAR NAVIGATION
st.sidebar.title("🏥 Main Menu")
choice = st.sidebar.selectbox("Access Level:", ["Patient Portal", "Admin Settings"])

# --- ADMIN VIEW ---
if choice == "Admin Settings":
    st.title("🛡️ Staff Administration")
    
    # Section: Manage Doctors
    st.subheader("Manage On-Call Doctors")
    new_doc_name = st.text_input("Enter Doctor's Name")
    
    col_add, col_clear = st.columns(2)
    if col_add.button("Add to Duty"):
        if new_doc_name:
            st.session_state['staff_list'].append(new_doc_name)
            st.rerun()
            
    if col_clear.button("Clear Entire Queue"):
        st.session_state['queue_list'] = []
        st.session_state['user_token'] = ""
        st.rerun()

    st.write("---")
    st.write("Current Staff Members:")
    for idx, name in enumerate(st.session_state['staff_list']):
        c1, c2 = st.columns([5, 1])
        c1.write(f"🔹 {name}")
        if c2.button("❌", key=f"del_{idx}"):
            st.session_state['staff_list'].pop(idx)
            st.rerun()

# --- PATIENT VIEW ---
else:
    st.title("🏥 Hospital Check-In")

    # FEATURE: SHOW USER'S TOKEN (BIG & CLEAR)
    if st.session_state['user_token']:
        st.markdown(f"""
            <div class="token-box">
                <p style='color: #8b949e; letter-spacing: 2px;'>YOUR CURRENT TOKEN</p>
                <h1 style='font-size: 90px; color: #3fb950; margin: 10px 0;'>{st.session_state['user_token']}</h1>
                <p>Status: <span style='color: #ffa657;'>Waiting for Service</span></p>
            </div>
            """, unsafe_all_ow_html=True)

    # FEATURE: TOKEN GENERATOR
    with st.expander("Generate New Token", expanded=not st.session_state['user_token']):
        name_input = st.text_input("Patient Full Name")
        triage_input = st.selectbox("Urgency", ["Routine", "Urgent", "Emergency"])
        
        if st.button("Get My Token"):
            if name_input:
                t_id = f"H-{random.randint(100, 999)}"
                new_entry = {"ID": t_id, "Triage": triage_input}
                
                # Logic: Emergency jumps to the top
                if triage_input == "Emergency":
                    st.session_state['queue_list'].insert(0, new_entry)
                else:
                    st.session_state['queue_list'].append(new_entry)
                
                st.session_state['user_token'] = t_id
                st.rerun()

    # FEATURE: PUBLIC LIST (CLEAN)
    st.write("---")
    st.subheader("📋 Public Waitlist")
    if len(st.session_state['queue_list']) > 0:
        # We wrap this in a DataFrame to keep it clean
        df_display = pd.DataFrame(st.session_state['queue_list'])
        st.dataframe(df_display, use_container_width=True, hide_index=True)
    else:
        st.info("The lobby is currently empty.")

    # FEATURE: DOCTORS ON DUTY
    st.write("---")
    st.subheader("👨‍⚕️ Available Doctors")
    for doc in st.session_state['staff_list']:
        st.markdown(f'<div class="doctor-card">{doc}</div>', unsafe_all_ow_html=True)
