import streamlit as st
import google.generativeai as genai
import requests

st.set_page_config(page_title="Phase 4: LLM Chatbot", page_icon="💬", layout="wide")
st.title("Phase 4: Weather Chatbot")
st.write("Ask me questions about the weather and your plans!")

try:
    GEMINI_API_KEY = st.secrets["key"]
    genai.configure(api_key=GEMINI_API_KEY)
except Exception:
    st.error("Error: Could not configure Google Gemini API.")
    st.stop()

def get_coords(city_name):
    url = "https://geocoding-api.open-meteo.com/v1/search"
    params = {
        "name": city_name,
        "count": 1,
        "language": "en",
        "format": "json"
    }
    try:
        response = requests.get(url, params=params)
        data = response.json()
        
        if "results" in data:
            lat = data["results"][0]["latitude"]
            lon = data["results"][0]["longitude"]
            return lat, lon
        else:
            return None, None
    except Exception as e:
        st.error(f"Geocoding Error: {e}")
        return None, None


def getweather():
    lat, lon = get_coords(city_name)
    
    URL = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": lat,
        "longitude": lon,
        "current": "temperature_2m,relative_humidity_2m,is_day,precipitation,wind_speed_10m",
        "forecast_days": 1
    }
    try:
        response = requests.get(URL, params=params)
        response.raise_for_status()
        return f"Current weather data: {response.json().get('current', {})}"
    except Exception as e:
        return f"Error retrieving weather: {e}"


if "chat_session" not in st.session_state:
    weather = getweather()
    
    system_prompt = f"""
    You are a helpful and friendly weather chatbot.
    Use the following real-time data to answer the user's questions.
    
    REAL-TIME DATA:
    {weather_context}
    """
    
    model = genai.GenerativeModel('gemini-2.5-pro')
    st.session_state.chat_session = model.start_chat(
        history=[
            {"role": "user", "parts": [system_prompt]},
            {"role": "model", "parts": ["I'm ready to answer questions about the current weather! What's up?"]}
        ]
    )

for message in st.session_state.chat_session.history:
    if message.role != "user" or "REAL-TIME DATA" not in message.parts[0]:
        with st.chat_message(message.role):
            st.markdown(message.parts[0])

if user_prompt := st.chat_input("Ask about the weather..."):
    with st.chat_message("user"):
        st.markdown(user_prompt)

    try:
        response = st.session_state.chat_session.send_message(user_prompt)
        
        with st.chat_message("model"):
            st.markdown(response.text)
            
    except Exception as e:
        st.error(f"An error occurred: {e}")
