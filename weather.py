import streamlit as st
import requests
from datetime import datetime

# Page Setup (Wide layout)
st.set_page_config(page_title="Ultimate Weather Dashboard", page_icon="🌤️", layout="wide")

# Custom UI Styling (Nature Background, Cards aur Developer Footer ke liye)
st.markdown("""
    <style>
    /* Full Page Background with Nature Image */
    .stApp {
        background-image: url("https://images.unsplash.com/photo-1506744038136-46273834b3fb?q=80&w=2070&auto=format&fit=crop");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }
    
    /* Content over background readability kelie white overlay wrapper */
    .block-container {
        background-color: rgba(255, 255, 255, 0.85);
        padding: 30px !important;
        border-radius: 20px;
        margin-top: 20px;
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.2);
    }
    
    .main-card { background-color: #f1f5f9; padding: 20px; border-radius: 12px; border: 1px solid #cbd5e1; }
    .metric-box { background-color: #ffffff; padding: 15px; border-radius: 8px; text-align: center; border: 1px solid #e2e8f0; box-shadow: 0 2px 4px rgba(0,0,0,0.02); }
    .aqi-good { color: #15803d; font-weight: bold; }
    .aqi-mod { color: #b45309; font-weight: bold; }
    .aqi-poor { color: #b91c1c; font-weight: bold; }
    
    /* Developer Footer Styling */
    .footer {
        position: relative;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: #0f172a;
        color: white;
        text-align: center;
        padding: 15px;
        font-size: 16px;
        font-weight: bold;
        border-radius: 10px;
        margin-top: 40px;
        box-shadow: 0px -4px 10px rgba(0, 0, 0, 0.1);
    }
    </style>
""", unsafe_allow_html=True)

st.title("🗺️ Ultimate Live Weather & Road Dashboard")

# City Input
city = st.text_input("Apne City ka naam likhein:", "Ludhiana")

# Geocoding API
geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1&language=en&format=json"

# Detailed Weather Codes Map
weather_codes = {
    0: "☀️ Clear sky (Ekdum Saaf)", 1: "🌤️ Mainly clear", 2: "⛅ Partly sunny", 3: "☁️ Overcast (Badal chaye hain)",
    45: "🌫️ Fog (Dhund)", 48: "🌫️ Rime fog", 51: "🌧️ Drizzle (Boonda-baandi)", 61: "🌧️ Light Rain (Baarish)", 
    63: "🌧️ Moderate Rain", 65: "🌧️ Heavy Rain (Tez Baarish)", 80: "🌧️ Rain Showers", 95: "⛈️ Thunderstorm (Garaj ke sath baarish)"
}

def get_aqi_status(us_aqi):
    if us_aqi <= 50: return "🟢 Good (Hawa Saaf Hai)", "aqi-good"
    elif us_aqi <= 100: return "🟡 Moderate (Theek-thak)", "aqi-mod"
    else: return "🔴 Poor (Kharab Hawa)", "aqi-poor"

if st.button("Mausam Ka Haal Dekhein"):
    try:
        geo_response = requests.get(geo_url).json()
        
        if "results" in geo_response:
            lat = geo_response["results"][0]["latitude"]
            lon = geo_response["results"][0]["longitude"]
            location_name = geo_response["results"][0]["name"]
            state = geo_response["results"][0].get("admin1", "")
            country = geo_response["results"][0].get("country", "")
            
            # Weather API Call
            weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=temperature_2m,relative_humidity_2m,apparent_temperature,weather_code,wind_speed_10m,surface_pressure&hourly=precipitation_probability,wind_speed_10m,temperature_2m&daily=weather_code,temperature_2m_max,temperature_2m_min,precipitation_sum&timezone=auto"
            data = requests.get(weather_url).json()
            
            # Air Quality API Call
            aqi_url = f"https://air-quality-api.open-meteo.com/v1/air-quality?latitude={lat}&longitude={lon}&current=us_aqi"
            aqi_data = requests.get(aqi_url).json()
            
            # Extract Current Data
            current = data["current"]
            aqi_val = aqi_data["current"]["us_aqi"] if "current" in aqi_data else 45
            aqi_status, aqi_class = get_aqi_status(aqi_val)
            
            status_text = weather_codes.get(current["weather_code"], "🌤️ Normal")
            
            st.success(f"📍 Location Roadmap: {location_name}, {state}, {country}")
            
            # --- ROW 1: CURRENT LIVE WEATHER & AIR QUALITY ---
            col_main1, col_main2 = st.columns([3, 2])
            
            with col_main1:
                st.markdown(f"""
                <div class='main-card'>
                    <h3>⚡ Live Current Weather</h3>
                    <h1 style='font-size: 50px; margin: 0;'>{current['temperature_2m']}°C</h1>
                    <p style='font-size: 20px; font-weight: bold;'>{status_text}</p>
                    <p style='color: #64748b;'>Feels Like: {current['apparent_temperature']}°C</p>
                </div>
                """, unsafe_allow_html=True)
                
            with col_main2:
                st.markdown(f"""
                <div class='main-card' style='background-color: #f8fafc;'>
                    <h3>🍃 Air Quality & Safety Day (AQI)</h3>
                    <h2 style='margin:0;'>Index: {aqi_val}</h2>
                    <p class='{aqi_class}' style='font-size: 18px;'>Status: {aqi_status}</p>
                </div>
                """, unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)

            # --- ROW 2: LIVE METRICS ---
            st.subheader("📊 Live Weather Details & Indicators")
            m1, m2, m3, m4 = st.columns(4)
            
            current_hour_idx = datetime.now().hour
            prob_rain = data["hourly"]["precipitation_probability"][current_hour_idx]
            
            m1.markdown(f"<div class='metric-box'>💧 <b>Humidity (Nami)</b><br><h2>{current['relative_humidity_2m']}%</h2></div>", unsafe_allow_html=True)
            m2.markdown(f"<div class='metric-box'>🌧️ <b>Precipitation (Baarish Prob.)</b><br><h2>{prob_rain}%</h2></div>", unsafe_allow_html=True)
            m3.markdown(f"<div class='metric-box'>💨 <b>Live Wind Speed</b><br><h2>{current['wind_speed_10m']} km/h</h2></div>", unsafe_allow_html=True)
            m4.markdown(f"<div class='metric-box'>🧭 <b>Air Pressure</b><br><h2>{int(current['surface_pressure'])} mb</h2></div>", unsafe_allow_html=True)

            st.markdown("---")

            # --- ROW 3: WIND & HOURLY FORECAST ---
            st.subheader("💨 Wind Forecast & Hourly Overview (Agla 12 Ghante)")
            hourly_slots = st.columns(6)
            for i, col in enumerate(hourly_slots):
                idx = current_hour_idx + (i * 2)
                if idx < len(data["hourly"]["temperature_2m"]):
                    time_raw = data["hourly"]["time"][idx].split("T")[1]
                    temp_h = data["hourly"]["temperature_2m"][idx]
                    wind_h = data["hourly"]["wind_speed_10m"][idx]
                    rain_p = data["hourly"]["precipitation_probability"][idx]
                    
                    col.markdown(f"""
                    <div class='metric-box' style='background-color:#f8fafc;'>
                        <span style='color:gray; font-size:12px;'>⏱️ {time_raw}</span><br>
                        <b>{temp_h}°C</b><br>
                        <span style='font-size:13px; color:#0284c7;'>🌧️ Rain: {rain_p}%</span><br>
                        <span style='font-size:13px; color:#475569;'>💨 Wind: {wind_h}kph</span>
                    </div>
                    """, unsafe_allow_html=True)

            st.markdown("---")

            # --- ROW 4: 5-DAY CALENDAR FORECAST ---
            st.subheader("📅 Weather Calendar (Aage Ke 5 Din Ka Forecast)")
            daily_slots = st.columns(5)
            
            for i, col in enumerate(daily_slots):
                date_str = data["daily"]["time"][i]
                date_obj = datetime.strptime(date_str, "%Y-%m-%d")
                day_display = date_obj.strftime("%A, %d %b")
                
                max_temp = data["daily"]["temperature_2m_max"][i]
                min_temp = data["daily"]["temperature_2m_min"][i]
                rain_sum = data["daily"]["precipitation_sum"][i]
                day_code = data["daily"]["weather_code"][i]
                day_status = weather_codes.get(day_code, "🌤️").split(" ")[0]
                
                col.markdown(f"""
                <div class='metric-box' style='border-top: 4px solid #3b82f6;'>
                    <h5>{day_display}</h5>
                    <h2 style='margin:10px 0;'>{day_status}</h2>
                    <p style='color:#ef4444; margin:2px 0;'>🔺 Max: {max_temp}°C</p>
                    <p style='color:#3b82f6; margin:2px 0;'>🔻 Min: {min_temp}°C</p>
                    <span style='font-size:12px; background-color:#e0f2fe; padding:2px 6px; border-radius:4px; color:#0369a1;'>🌧️ {rain_sum} mm</span>
                </div>
                """, unsafe_allow_html=True)
                
        else:
            st.error("Sheher ka naam sahi nahi hai.")
    except Exception as e:
        st.error("Data connect karne mein dikkat aa rahi hai.")

# --- PERSISTENT DEVELOPER FOOTER ---
st.markdown("""
    <div class='footer'>
        👨‍💻 Developed with ❤️ by Karan
    </div>
""", unsafe_allow_html=True)
