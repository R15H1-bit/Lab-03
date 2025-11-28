import streamlit as st
import google.generativeai as genai
import requests

st.set_page_config(page_title="Phase 4: LLM Chatbot", page_icon="💬", layout="wide")
st.title("Phase 4: Weather Chatbot")
st.write("Ask me questions about the weather and your plans!")

try:
    GEMINI_API_KEY = st.secrets["AIzaSyDzsv6WhpyXl5muGXvpyy0lFm-ccQQ-d4A]
    genai.configure(api_key=GEMINI_API_KEY)
except Exception:
    st.error("Error: Could not configure Google Gemini API. Make sure your `secrets.toml` file is correct.")
    st.stop()

def get_weather_context():
    """Fetches weather data to be used as context for the chatbot."""
    lat, lon = 33.7756, -84.3963 # Georgia Tech
    
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
        return f"Error fetching weather: {e}"


if "chat_session" not in st.session_state:
    weather_context = get_weather_context()
    
    system_prompt = f"""
    You are a helpful and friendly weather chatbot.
    Use the following real-time data to answer the user's questions.
    Do not mention you have this data unless it's needed to answer.
    
    REAL-TIME DATA:
    {weather_context}
    """
    
    model = genai.GenerativeModel('gemini-1.5-flash')
    st.session_state.chat_session = model.start_chat(
        history=[
            {"role": "user", "parts": [system_prompt]},
            {"role": "model", "parts": ["Got it. I'm ready to answer questions about the current weather! What's up?"]}
        ]
    )

for message in st.session_state.chat_session.history:
    # Don't show the initial system prompt
    if message.role != "user" or "REAL-TIME DATA" not in message.parts[0]:
        with st.chat_message(message.role):
            st.markdown(message.parts[0])

if user_prompt := st.chat_input("Ask about the weather..."):
    # Add user message to chat
    with st.chat_message("user"):
        st.markdown(user_prompt)

    try:
        # Send message to Gemini
        response = st.session_state.chat_session.send_message(user_prompt)
        
        # Display Gemini's response
        with st.chat_message("model"):
            st.markdown(response.text)
            
    except Exception as e:
        st.error(f"An error occurred: {e}")
        st.info("This can happen due to rate limits or content safety filters.")
