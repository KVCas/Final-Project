import streamlit as st
import requests
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from datetime import timedelta

api_key = 'c0ba78f77f34b65fb4488ff743644cb3'
base_url = "https://api.openweathermap.org/data/2.5/"

def weather_data(city):
    url = f"{base_url}weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(url)
    data = response.json()
    if response.status_code == 200:
        return {
            'city': data['name'],
            'current_temp': round(data['main']['temp']),
            'feels_like': round(data['main']['feels_like']),
            'temp_min': round(data['main']['temp_min']),
            'temp_max': round(data['main']['temp_max']),
            'humidity': round(data['main']['humidity']),
            'description': data['weather'][0]['description'],
            'country': data['sys']['country']
        }
    else:
        st.error("Error fetching data. Please check the city name.")
        return None

def train_models(df):
    focus_data = [
        'LOCAL_YEAR', 'LOCAL_DAY', 'MIN_TEMPERATURE', 'MAX_TEMPERATURE',
        'TOTAL_PRECIPITATION', 'MIN_REL_HUMIDITY', 'MAX_REL_HUMIDITY'
    ]
    cleaned_df = df[focus_data].copy()
    cleaned_df['MIN_TEMPERATURE'] = cleaned_df['MIN_TEMPERATURE'].interpolate()
    cleaned_df['MAX_TEMPERATURE'] = cleaned_df['MAX_TEMPERATURE'].interpolate()
    cleaned_df['TOTAL_PRECIPITATION'] = cleaned_df['TOTAL_PRECIPITATION'].fillna(cleaned_df['TOTAL_PRECIPITATION'].mean())
    cleaned_df['MIN_REL_HUMIDITY'] = cleaned_df['MIN_REL_HUMIDITY'].fillna(cleaned_df['MIN_REL_HUMIDITY'].mean())
    cleaned_df['MAX_REL_HUMIDITY'] = cleaned_df['MAX_REL_HUMIDITY'].fillna(cleaned_df['MAX_REL_HUMIDITY'].mean())
    cleaned_df['Rain_Tomorrow'] = (cleaned_df['TOTAL_PRECIPITATION'] > 1.0).astype(int)

    cleaned_df = cleaned_df.dropna()
    
    features = ['MIN_TEMPERATURE', 'MAX_TEMPERATURE', 'MIN_REL_HUMIDITY', 'MAX_REL_HUMIDITY']
    X = cleaned_df[features]
    y = cleaned_df['Rain_Tomorrow']
    rain_model = RandomForestClassifier(n_estimators=100, random_state=42)
    rain_model.fit(X, y)

    temp_X = cleaned_df['MAX_TEMPERATURE'][:-1].values.reshape(-1, 1)
    temp_y = cleaned_df['MAX_TEMPERATURE'][1:].values
    temp_model = RandomForestRegressor(n_estimators=100, random_state=42)
    temp_model.fit(temp_X, temp_y)

    humidity_X = cleaned_df['MAX_REL_HUMIDITY'][:-1].values.reshape(-1, 1)
    humidity_y = cleaned_df['MAX_REL_HUMIDITY'][1:].values
    humidity_model = RandomForestRegressor(n_estimators=100, random_state=42)
    humidity_model.fit(humidity_X, humidity_y)

    return rain_model, temp_model, humidity_model

def predict_future_trends(model, current_value, steps=5):
    predictions = [current_value]
    for _ in range(steps):
        next_value = model.predict(np.array([[predictions[-1]]]))[0]
        predictions.append(next_value)
    return predictions[1:]

def app():
    st.title("Interactive Weather Forecast with Predictions")

    city = st.text_input("Enter a city name:", placeholder="e.g., Toronto, New York")
    df = pd.read_csv("climate-daily.csv") 
    if city:
        current_weather = weather_data(city)
        if current_weather:
            st.subheader(f"Current Weather in {current_weather['city']}, {current_weather['country']}")
            st.write(f"Temperature: {current_weather['current_temp']}°C (Feels like {current_weather['feels_like']}°C)")
            st.write(f"Description: {current_weather['description']}")
            st.write(f"Humidity: {current_weather['humidity']}%")
            st.write(f"Min Temperature: {current_weather['temp_min']}°C")
            st.write(f"Max Temperature: {current_weather['temp_max']}°C")

            rain_model, temp_model, humidity_model = train_models(df)

            user_input = pd.DataFrame({
                'MIN_TEMPERATURE': [current_weather['temp_min']],
                'MAX_TEMPERATURE': [current_weather['temp_max']],
                'MIN_REL_HUMIDITY': [current_weather['humidity']],
                'MAX_REL_HUMIDITY': [current_weather['humidity']],
            })
            rain_prediction = rain_model.predict(user_input)[0]
            st.write(f"Rain Prediction: {'Yes' if rain_prediction else 'No'}")

            future_temps = predict_future_trends(temp_model, current_weather['temp_max'])
            future_humidity = predict_future_trends(humidity_model, current_weather['humidity'])

            st.subheader("Future Predictions")
            st.write("**Temperature (Next 5 Hours):**")
            for i, temp in enumerate(future_temps, start=1):
                st.write(f"Hour {i}: {round(temp, 1)}°C")

            st.write("**Humidity (Next 5 Hours):**")
            for i, hum in enumerate(future_humidity, start=1):
                st.write(f"Hour {i}: {round(hum, 1)}%")
        else:
            st.write("Please enter a valid city name.")

if __name__ == "__main__":
    app()