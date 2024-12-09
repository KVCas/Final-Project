import streamlit as st
import folium
from streamlit_folium import st_folium
import requests

api_key = 'c0ba78f77f34b65fb4488ff743644cb3'
base_url = "https://api.openweathermap.org/data/2.5/"

def weather_data(city):
    url = f"{base_url}weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(url)
    data = response.json()
    if response.status_code == 200:
        return {
            'city': data['name'],
            'lat': data['coord']['lat'],
            'lon': data['coord']['lon'],
            'current_temp': round(data['main']['temp']),
            'feels_like': round(data['main']['feels_like']),
            'humidity': round(data['main']['humidity']),
            'description': data['weather'][0]['description'],
            'country': data['sys']['country']
        }
    else:
        st.error("City not found or API error. Please check the city name.")
        return None

def Create_Map(weather):
    weather_map = folium.Map(location=[weather['lat'], weather['lon']], zoom_start=10)
    
    popup_info = (
        f"<b>City:</b> {weather['city']}<br>"
        f"<b>Temperature:</b> {weather['current_temp']}°C (Feels like {weather['feels_like']}°C)<br>"
        f"<b>Humidity:</b> {weather['humidity']}%<br>"
        f"<b>Description:</b> {weather['description']}"
    )
    
    folium.Marker(
        [weather['lat'], weather['lon']],
        popup=popup_info,
        icon=folium.Icon(color='blue', icon='info-sign')
    ).add_to(weather_map)
    
    return weather_map

def app():
    st.title("Weather Map Viewer")
    city = st.text_input("Enter a city name:", placeholder="e.g., Toronto, New York")
    
    if city:
        weather = weather_data(city)
        if weather:
            st.subheader(f"Weather Map for {weather['city']}, {weather['country']}")
            weather_map = Create_Map(weather)
            st_folium(weather_map, width=700, height=500)
        else:
            st.error("Unable to fetch weather data. Please try again.")

if __name__ == "__main__":
    app()
