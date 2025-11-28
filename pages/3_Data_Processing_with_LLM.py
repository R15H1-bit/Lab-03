import streamlit as st
import google.generativeai as genai
import requests

st.set_page_config(page_title="Phase 3: LLM Generator", page_icon="🤖", layout="wide")
st.title("Phase 3: LLM-Powered Activity Planner")


key = st.secrets["key"]
genai.configure(api_key=key)
model = genai.GenerativeModel('gemini-pro')


def weather(lat, lon):
    """Fetches a summary of the weather."""
    URL = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": lat,
        "longitude": lon,
        "daily": "temperature_2m_max,temperature_2m_min,precipitation_sum",
        "forecast_days": 1
    }
    try:
        response = requests.get(URL, params=params)
        response.raise_for_status()
        data = response.json()
        
        daily_data = data.get("daily", {})
        summary = f"""
        Today's Forecast:
        - Max Temp: {daily_data.get('temperature_2m_max', ['N/A'])[0]} °C
        - Min Temp: {daily_data.get('temperature_2m_min', ['N/A'])[0]} °C
        - Total Precipitation: {daily_data.get('precipitation_sum', ['N/A'])[0]} mm
        """
        return summary
    except Exception as e:
        st.error(f"Error fetching weather data: {e}")
        return None

st.header("Step 1: Plan Your Activity")

location_name = st.text_input("Enter a location name (e.g., 'Atlanta')", value="Atlanta")

if location_name.lower() == "atlanta":
    lat, lon = 33.7756, -84.3963
else:
    lat, lon = 40.7128, -74.0060 # Default to NYC

activity = st.text_input("What activity are you planning?", "a 5K run")

if st.button("Generate Activity Recommendation"):
    weather_data = weather(lat, lon)
    
    if weather_data:
        st.subheader(f"Today's Weather for {location_name}:")
        st.text(weather_data)
        
        prompt = f"""
        You are a helpful planning assistant. Based on the following weather data,
        generate a short recommendation for my planned activity.
        
        My planned activity: {activity}
        Weather Data:
        {weather_data}
        
        Start your response with a clear "Recommendation" and provide 2-3 setences about why.
        """
        
        st.subheader("LLM Recommendation:")
        
        try:
            with st.spinner("Gemini is thinking..."):
                response = model.generate_content(prompt)
                print(response.txt)
                st.markdown(response.text)
        except Exception as e:
            st.error(f"An error occurred with the LLM: {e}")
