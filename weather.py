import streamlit as st
import requests
from datetime import datetime

# Page Design
st.set_page_config(page_title="Weather Dashboard", page_icon="🌤️", layout="wide")

# Custom CSS styling text ko sundar dikhane ke liye
st.markdown("""
    <style>
    .main-card { background-color: #f0f4f9; padding: 20px; border-radius: 15px; margin-bottom: 20px; }
    .forecast-card { background-color: #ffffff; padding: 15px; border-radius: 10px; text-align: center; border: 1px solid #e1e8ed; }
    </style>
""", unsafe_allow_html=True)

st.title("🌦️ Weather Dashboard")

# City Input
city = st.text_input("Apne City ka naam likhein:", "Ludhiana")

# API Keys/URLs
geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1&language=en&format=json"

weather_codes = {
    0: "☀️ Clear sky", 1: "🌤️ Mainly clear", 2: "⛅ Partly sunny", 3: "☁️ Overcast",
    45: "🌫️ Fog", 48: "🌫️ Fog", 51: "🌧️ Drizzle", 61: "🌧️ Rain", 71: "❄️ Snow", 95: "⛈️ Thunderstorm"
}

if st.button("Mausam Dekhein"):
    try:
        geo_response = requests.get(geo_url).json()
        
        if "results" in geo_response:
            lat = geo_response["results"][0]["latitude"]
            lon = geo_response["results"][0]["longitude"]
            location_name = geo_response["results"][0]["name"]
            state = geo_response["results"][0].get("admin1", "")
            
            # Current, Hourly aur Daily saara data ek sath lana
            weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=temperature_2m,relative_humidity_2m,apparent_temperature,weather_code,wind_speed_10m,surface_pressure&hourly=temperature_2m,weather_code&daily=weather_code,temperature_2m_max,temperature_2m_min&timezone=auto"
            data = requests.get(weather_url).json()
            
            # 1. CURRENT WEATHER SECTION
            current = data["current"]
            status = weather_codes.get(current["weather_code"], "🌈 Clear")
            
            st.success(f"📍 {location_name}, {state}")
            
            # Layout splitting for current details
            col1, col2 = st.columns([2, 3])
            
            with col1:
                st.markdown(f"### Current weather")
                st.markdown(f"<h1>{current['temperature_2m']}°C</h1>", unsafe_allow_html=True)
                st.markdown(f"**{status}**")
                st.write(f"Feels like {current['apparent_temperature']}°C")
                
            with col2:
                st.markdown("<br>", unsafe_allow_html=True)
                c_a, c_b, c_c = st.columns(3)
                c_a.metric("Wind", f"{current['wind_speed_10m']} km/h")
                c_b.metric("Humidity", f"{current['relative_humidity_2m']}%")
                c_c.metric("Pressure", f"{int(current['surface_pressure'])} mb")

            st.markdown("---")
            
            # 2. HOURLY FORECAST (Next few hours)
            st.subheader("⏰ Hourly Overview")
            hourly_cols = st.columns(6)
            current_hour = datetime.now().hour
            
            for i, col in enumerate(hourly_cols):
                idx = current_hour + (i * 2) # Har 2 ghante ka gap dikhane ke liye
                if idx < len(data["hourly"]["temperature_2m"]):
                    time_str = data["hourly"]["time"][idx].split("T")[1]
                    temp_h = data["hourly"]["temperature_2m"][idx]
                    code_h = data["hourly"]["weather_code"][idx]
                    status_h = weather_codes.get(code_h, "🌤️").split(" ")[0] # sirf emoji ke liye
                    
                    with col:
                        st.markdown(f"""
                        <div class='forecast-card'>
                            <p style='color:gray;'>{time_str}</p>
                            <h2>{status_h}</h2>
                            <p><b>{temp_h}°C</b></p>
                        </div>
                        """, unsafe_allow_html=True)

            st.markdown("---")

            # 3. DAILY FORECAST (Next 5 Days)
            st.subheader("📅 5-Day Forecast")
            daily_cols = st.columns(5)
            
            for i, col in enumerate(daily_cols):
                date_str = data["daily"]["time"][i]
                date_obj = datetime.strptime(date_str, "%Y-%m-%d")
                day_name = date_obj.strftime("%a\n%d") # E.g., Mon 13
                
                max_t = data["daily"]["temperature_2m_max"][i]
                min_t = data["daily"]["temperature_2m_min"][i]
                code_d = data["daily"]["weather_code"][i]
                status_d = weather_codes.get(code_d, "🌤️").split(" ")[0]
                
                with col:
                    st.markdown(f"""
                    <div class='forecast-card'>
                        <h4>{day_name}</h4>
                        <h1>{status_d}</h1>
                        <p style='color:#ff4b4b; margin:0;'>High: {max_t}°C</p>
                        <p style='color:#0066cc; margin:0;'>Low: {min_t}°C</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
        else:
            st.error("Sheher ka naam sahi nahi hai. Kripya check karein.")
    except Exception as e:
        st.error("Data load nahi ho pa raha hai.")
