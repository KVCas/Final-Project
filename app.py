import streamlit as st
from Home import app as home_app
from Weather_Forecast import app as interactive_app


st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Home", "Interactive Interface"])

if page == "Home":
    home_app()
elif page == "Interactive Interface":
    interactive_app()
