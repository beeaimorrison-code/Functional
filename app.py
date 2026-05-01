import streamlit as st
import pandas as pd
import pydeck as pdk
from datetime import datetime
import urllib.parse

# --- 1. SYSTEM CONFIGURATION & DYNAMIC THEME ---
st.set_page_config(page_title="Abuja Hybrid Satellite Security", layout="wide")

# background logic based on login status
if 'personnel_auth' not in st.session_state or not st.session_state.personnel_auth:
    page_bg = "#800000"  # Institutional Maroon
    content_color = "#FFFFFF"
else:
    page_bg = "#111111"  # Dark mode for dashboard contrast
    content_color = "#FFFFFF"

st.markdown(f"""
    <style>
    .stApp {{
        background-color: {page_bg};
    }}
    h1, h2, h3, p, span, .stMarkdown {{
        color: {content_color} !important;
    }}
    /* USSD Mobile UI Simulation */
    .ussd-container {{
        background-color: #000000;
        color: #00FF00;
        padding: 30px;
        border-radius: 35px;
        border: 8px solid #333333;
        max-width: 380px;
        margin: auto;
        font-family: 'Courier New', Courier, monospace;
        box-shadow: 0px 20px 40px rgba(0,0,0,0.6);
    }}
    /* Custom Button Styling */
    .stButton>button {{
        background-color: #5a0000;
        color: white;
        border: 1px solid #ffffff;
        width: 100%;
    }}
    </style>
    """, unsafe_allow_html=True)

# --- 2. BACKEND DATA & ABUJA LANDMARK GEOGRAPHY ---
if 'db' not in st.session_state:
    st.session_state.db = pd.DataFrame(columns=["Incident", "Landmark", "Manual_Address", "Weight", "Time", "lat", "lon"])
if 'audit_trail' not in st.session_state:
    st.session_state.audit_trail = pd.DataFrame(columns=["Timestamp", "Personnel", "Action"])
if 'personnel_auth' not in st.session_state:
    st.session_state.personnel_auth = False

# Coordinate mapping for Abuja Landmarks (FCT Sector)
LANDMARKS = {
    "Wuse II Central": [9.0778, 7.4767],
    "Garki District": [9.0333, 7.4833],
    "Maitama Sector": [9.0883, 7.5022],
    "Asokoro Extension": [9.0483, 7.5147],
    "Gwarinpa Estate": [9.1097, 7.4042],
    "Kubwa Hub": [9.1558, 7.3271],
    "Nyanya Sector": [9.0167, 7.5667]
}

# --- 3. SIDEBAR: PERSONNEL ACCESS ---
st.sidebar.title("👮 Personnel Command")
if not st.session_state.personnel_auth:
    with st.sidebar.form("personnel_login"):
        p_id = st.text_input("Personnel ID", placeholder="Enter Name or ID")
        p_key = st.text_input("Access Key", type="password")
        if st.form_submit_button("Enter Abuja Dashboard"):
            if p_key.lower() == "thesis2026":
                st.session_state.personnel_auth = True
                st.session_state.current_user = p_id
                log = pd.DataFrame([{"Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 
                                     "Personnel": p_id, "Action": "Accessed Hybrid Tactical Hub"}])
                st.session_state.audit_trail = pd.concat([st.session_state.audit_trail, log], ignore_index=True)
                st.rerun()
            else:
                st.sidebar.error("Invalid Personnel Key")
else:
    st.sidebar.success(f"Active Session: {st.session_state.current_user}")
    if st.sidebar.button("Log Out"):
        st.session_state.personnel_auth = False
        st.rerun()

# --- 4. PORTAL ROUTING ---

# SCENARIO A: Public Access (Common Citizens - No Password)
if not st.session_state.personnel_auth:
    st.title("🛡️ Hybrid USSD Security Mapping Framework")
    st.subheader("Simulating Zero-Data Offline Incident Reporting (Abuja Sector)")
    st.divider()

    col_sim, col_doc = st.columns([1, 1.2])

    with col_sim:
        st.markdown('<div class="ussd-container">', unsafe_allow_html=True)
        st.markdown("### GSM TERMINAL")
        st.markdown("**Session: *123#**")
        st.markdown("---")
        
        with st.form("ussd_report", clear_on_submit=True):
            user_input = st.text_input("Option (1.Robbery 2.Kidnap 3.Suspicious)")
            user_land = st.selectbox("Current Landmark", list(LANDMARKS.keys()))
            user_manual = st.text_input("Specific Location/Address", placeholder="e.g. House 4, Close B")
            
            if st.form_submit_button("SEND SIGNAL"):
                mapping = {"1": "Robbery", "2": "Kidnapping", "3": "Suspicious Activity"}
                weights = {"1": 15, "2": 25, "3": 10}
                
                if user_input in mapping:
                    report = pd.DataFrame([{
                        "Incident": mapping[user_input],
                        "Landmark": user_land,
                        "Manual_Address": user_manual if user_manual else "Not Specified",
                        "Weight": weights[user_input],
                        "Time": datetime.now().strftime("%H:%M:%S"),
                        "lat": LANDMARKS[user_land][0],
                        "lon": LANDMARKS[user_land][1]
                    }])
                    st.session_state.db = pd.concat([st.session_state.db, report], ignore_index=True)
                    st.success(f"✔ Signal from {user_land} sent.")
                else:
                    st.error("Invalid Input")
        st.markdown('</div>', unsafe_allow_html=True)

    with col_doc:
        st.markdown("### Dissertation Simulation Logic")
        st.write("""
        - **Barrier-Free Reporting:** Abuja citizens access this terminal instantly without passwords.
        - **Hybrid Verification:** System uses geofenced landmarks AND manual text overrides for street-level accuracy.
        - **Navigation Ready:** Telemetry is forwarded to responders for precise external navigation.
        """)
        st.info("The Responder Dashboard is restricted. Please use the sidebar to log in as security personnel.")

# SCENARIO B: Personnel Access (Security Dashboard & Data Hub)
else:
    st.title(f"👮 Abuja Tactical Command: {st.session_state.current_user}")
    
    st.subheader("Live Abuja Incident Database & Navigation Hub")
    if not st.session_state.db.empty:
        for index, row in st.session_state.db.iloc[::-1].iterrows():
            with st.expander(f"🚨 {row['Incident']} - {row['Landmark']} ({row['Time']})"):
                st.write(f"**Reported Specifics:** {row['Manual_Address']}")
                
                c1, c2 = st.columns(2)
                with c1:
                    # Link based on internal coordinates
                    g_coord_url = f"https://www.google.com/maps/search/?api=1&query={row['lat']},{row['lon']}"
                    st.link_button("Map to Landmark (GPS)", g_coord_url)
                with c2:
                    # Link based on manual search query
                    if row['Manual_Address'] != "Not Specified":
                        search_q = urllib.parse.quote(f"{row['Manual_Address']}, {row['Landmark']}, Abuja")
                        g_search_url = f"https://www.google.com/maps/search/?api=1&query={search_q}"
                        st.link_button("Map to Specific Address", g_search_url)
                    else:
                        st.write("No specific address provided.")
    else:
        st.info("System Online. Standing by for telemetry from FCT districts...")
        
    st.divider()
    st.subheader("Personnel Activity Logs")
    st.table(st.session_state.audit_trail.iloc[::-1])
