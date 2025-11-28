import streamlit as st

# Title of App
st.title("Web Development Lab03")

# Assignment Data 
# TODO: Fill out your team number, section, and team members

st.header("CS 1301")
st.subheader("Team 53, Web Development - Section C")
st.subheader("Rishi Muni, Kathryn Stribling")


# Introduction
# TODO: Write a quick description for all of your pages in this lab below, in the form:
#       1. **Page Name**: Description
#       2. **Page Name**: Description
#       3. **Page Name**: Description
#       4. **Page Name**: Description

st.write("""
Welcome to our Streamlit Web Development Lab03 app! You can navigate between the pages using the sidebar to the left. The following pages are:

1. Home Page
2. API Interaction
3. Data Processing via LLM 
4. AI ChatBot

""")


st.divider()

# --- Page Descriptions ---
st.header("Page Descriptions")
st.write(""" 
1.  **Home Page**: Select a page from the following to explore and visualize data
    collected from a Star Wars API!

2.  **Phase 2 API:** This page fetches data from an external weather API. You can input
    any latitude and longitude to get the real-time temperature forecast,
    which is then displayed on an interactive chart.

3.  **Phase 3 LLM Generator:**
    This page uses the weather API data and feeds it into the Google Gemini
    LLM. Based on user inputs (like location and a desired activity), it
    generates a specialized text, like a "go/no-go" recommendation.

4.  **Phase 4 LLM Chatbot:**
    This page features a fully interactive chatbot. It uses the same
    real-time weather data to answer your questions, like "Is it a good
    day to go for a run?" or "What should I wear today?".
    
""")

st.sidebar.success("Select a page above to get started.")
