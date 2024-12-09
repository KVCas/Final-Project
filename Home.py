import streamlit as st

def app():
    st.title("🌦️ Weather Insights and Predictions")
    st.subheader("Welcome to the Data-Driven Weather Hub")

    st.write("""
    This app combines live weather data and predictive modeling to provide comprehensive weather insights.  
    From real-time conditions and weather prediction, this is your weather analysis platform.
    """)

    st.write("""
    ### What can you do here?
    - **Explore Current Weather**: Get live updates for any city around the globe.
    - **Rain Prediction**: Curious about tomorrow’s precipitation? Let our machine learning model guide you.
    - **Future Insights**: Analyze temperature and humidity trends with advanced regression techniques.
    - **Interactive Map**: Visualize weather details in a interactive map.
    """)

    st.sidebar.subheader("Navigation")
    st.sidebar.write("Use this sidebar to navigate to the interactive page.")

if __name__ == "__main__":
    app()