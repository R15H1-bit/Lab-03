import streamlit as st
import requests
import pandas as pd

st.set_page_config(page_title="Phase 2: Weather API", page_icon="✍️", layout="wide")
st.title("Phase 2: Real-Time Weather API")
st.write("This page fetches and displays weather data from the Open-Meteo API.")

st.header("Step 1: Choose Your Location")
st.write("Enter coordinates to fetch the weather forecast.")

lat_input = st.number_input(
    "Enter Latitude (e.g., 33.7756)", 
    value=33.7756,  # Defaults to Georgia Tech
    format="%.4f"
)

lon_input = st.number_input(
    "Enter Longitude (e.g., -84.3963)", 
    value=-84.3963, # Defaults to Georgia Tech
    format="%.4f"
)

def fetch_weather(lat, lon):
    URL = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": lat,
        "longitude": lon,
        "hourly": "temperature_2m" 
    }
    try:
        response = requests.get(URL, params=params)
        response.raise_for_status() 
        return response.json()
    
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching data: {e}")
        return None

st.header("Step 2: Get Forecast")
if st.button("Fetch Weather Forecast"):
    data = fetch_weather(lat_input, lon_input)

    if data:
        st.subheader("Raw API Data")
        st.json(data) 

        st.subheader("Dynamic Visual: 7-Day Temperature Forecast")        
        hourly_data = data.get("hourly", {})
        if "time" in hourly_data and "temperature_2m" in hourly_data:
            
            df = pd.DataFrame({
                "Time": pd.to_datetime(hourly_data["time"]),
                "Temperature (°C)": hourly_data["temperature_2m"]
            })
            
            df = df.set_index("Time")
            st.dataframe(df.head())
            st.line_chart(df)
        
        else:
            st.warning("Could not find 'hourly' data in the API response.")
    else:
        st.error("Failed to retrieve data.")
