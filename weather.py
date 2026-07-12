import streamlit as st
import requests
from datetime import datetime

# Page Setup (Wide layout)
st.set_page_config(page_title="zenibyte by Karan", page_icon="🌤️", layout="wide")

# Custom UI Styling
st.markdown("""
    <style>
    .stApp {
        background-image: url("https://images.unsplash.com/photo-1506744038136-46273834b3fb?q=80&w=2070&auto=format&fit=crop");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }
    .block-container {
        background-color: rgba(255, 255, 255, 0.88);
        padding: 30px !important;
        border-radius: 20px;
        margin-top: 20px;
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.2);
    }
    [data-testid="stSidebar"] {
        background-color: rgba(15, 23, 42, 0.9) !important;
    }
    [data-testid="stSidebar"] * {
        color: white !important;
    }
    .main-card { background-color: #f1f5f9; padding: 20px; border-radius: 12px; border: 1px solid #cbd5e1; color: #0f172a; }
    .metric-box { background-color: #ffffff; padding: 15px; border-radius: 8px; text-align: center; border: 1px solid #e2e8f0; box-shadow: 0 2px 4px rgba(0,0,0,0.02); color: #0f172a; }
    .dev-badge {
        background-color: #0284c7;
        color: white;
        padding: 6px 12px;
        font-size: 14px;
        font-weight: bold;
        border-radius: 20px;
        display: inline-block;
        margin-bottom: 10px;
    }
    .footer {
        width: 100%;
        background-color: #0f172a;
        color: white;
        text-align: center;
        padding: 15px;
        font-size: 15px;
        border-radius: 10px;
        margin-top: 40px;
    }
    </style>
""", unsafe_allow_html=True)

# Sidebar
st.sidebar.markdown("## 🔍 zenibyte Control Panel")
menu_opt = st.sidebar.radio("Go To Page:", ["🏠 Home Page", "ℹ️ About App", "🌍 Country Overview", "👨‍💻 Developer Corner"])
country_select = st.sidebar.selectbox("Select Country:", ["India 🇮🇳", "United States 🇺🇸", "United Kingdom 🇬🇧", "Australia 🇦🇺", "Canada 🇨🇦"])

# Logic
if menu_opt == "🏠 Home Page":
    st.markdown("<div class='dev-badge'>🚀 zenibyte by Karan</div>", unsafe_allow_html=True)
    st.title("🗺️ zenibyte Live Weather & Road Dashboard")
    city = st.text_input("Apne City ka naam likhein:", "Ludhiana")
    
    if st.button("Mausam Ka Haal Dekhein"):
        # (Yahan wahi API logic rahega jo pehle tha)
        st.success(f"📍 Location Data for {city} | Powered by zenibyte")
        # ... baaki weather code yahan waisa hi rahega ...

elif menu_opt == "ℹ️ About App":
    st.title("ℹ️ About zenibyte")
    st.write("This application is a premium weather telemetry tool built by Karan.")

elif menu_opt == "👨‍💻 Developer Corner":
    st.title("👨‍💻 Developer Profile")
    st.success("Primary Architect: **Karan**")
    st.markdown("Brand: **zenibyte** | Founder: **Karan**")

# Footer
st.markdown("""
    <div class='footer'>
        © 2026 zenibyte | Owner: Karan | All Rights Reserved.
    </div>
""", unsafe_allow_html=True)
