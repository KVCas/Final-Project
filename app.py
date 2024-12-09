import streamlit as st
from Home import app as home_app
from Weather_Forecast import app as Weather_Forecast_app
from Weather_map import app as Weather_map_app

st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Home", "Interactive Interface", "Map Viewer"])

if page == "Home":
    home_app()
elif page == "Interactive Interface":
    Weather_Forecast_app()
elif page == "Map Viewer":
    Weather_map_app()
