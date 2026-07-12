import streamlit as st
import requests
from datetime import datetime

# Page Setup
st.set_page_config(page_title="zenibyte by Karan", page_icon="🌤️", layout="wide")

# CSS Styling (Sidebar + Cards)
st.markdown("""
    <style>
    .stApp { background-image: url("https://images.unsplash.com/photo-1506744038136-46273834b3fb?q=80&w=2070&auto=format&fit=crop"); background-size: cover; }
    .block-container { background-color: rgba(255, 255, 255, 0.88); padding: 30px; border-radius: 20px; }
    [data-testid="stSidebar"] { background-color: rgba(15, 23, 42, 0.9) !important; color: white !important; }
    .main-card { background-color: #f1f5f9; padding: 20px; border-radius: 12px; border: 1px solid #cbd5e1; color: #0f172a; }
    .metric-box { background-color: #ffffff; padding: 15px; border-radius: 8px; text-align: center; border: 1px solid #e2e8f0; }
    .dev-badge { background-color: #0284c7; color: white; padding: 6px 12px; border-radius: 20px; display: inline-block; }
    .footer { background-color: #0f172a; color: white; text-align: center; padding: 15px; border-radius: 10px; margin-top: 40px; }
    </style>
""", unsafe_allow_html=True)

# Sidebar
st.sidebar.markdown("## 🔍 zenibyte Control Panel")
menu_opt = st.sidebar.radio("Go To Page:", ["🏠 Home Page", "ℹ️ About App", "🌍 Country Overview", "👨‍💻 Developer Corner"])
country_select = st.sidebar.selectbox("Select Country:", ["India 🇮🇳", "United States 🇺🇸", "United Kingdom 🇬🇧"])

# Logic
if menu_opt == "🏠 Home Page":
    st.markdown("<div class='dev-badge'>🚀 zenibyte by Karan</div>", unsafe_allow_html=True)
    st.title("🗺️ zenibyte Live Weather & Road Dashboard")
    city = st.text_input("Apne City ka naam likhein:", "Ludhiana")
    
    if st.button("Mausam Ka Haal Dekhein"):
        try:
            # Fix: Geocoding
            geo = requests.get(f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1").json()
            if "results" in geo:
                lat, lon = geo["results"][0]["latitude"], geo["results"][0]["longitude"]
                # Fix: Weather Data
                weather = requests.get(f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=temperature_2m,relative_humidity_2m,wind_speed_10m&daily=temperature_2m_max,temperature_2m_min,weather_code&timezone=auto").json()
                curr = weather["current"]
                
                st.success(f"📍 Location Data for {city} | Powered by zenibyte")
                c1, c2, c3 = st.columns(3)
                c1.markdown(f"<div class='metric-box'>🌡️ Temp<br><b>{curr['temperature_2m']}°C</b></div>", unsafe_allow_html=True)
                c2.markdown(f"<div class='metric-box'>💧 Humidity<br><b>{curr['relative_humidity_2m']}%</b></div>", unsafe_allow_html=True)
                c3.markdown(f"<div class='metric-box'>💨 Wind<br><b>{curr['wind_speed_10m']} km/h</b></div>", unsafe_allow_html=True)
                
                st.subheader("📅 5-Day Forecast")
                for i in range(5):
                    st.write(f"Day {i+1}: Max {weather['daily']['temperature_2m_max'][i]}°C | Min {weather['daily']['temperature_2m_min'][i]}°C")
            else:
                st.error("City nahi mili! Sahi naam daalo.")
        except Exception as e:
            st.error("Server se connect nahi ho paa raha, check internet!")

# Footer
st.markdown("<div class='footer'>© 2026 zenibyte | Owner: Karan | All Rights Reserved.</div>", unsafe_allow_html=True)
