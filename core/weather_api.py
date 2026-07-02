from dotenv import load_dotenv
load_dotenv()

import os
import requests

# =========================
# API KEY
# =========================
# Der API-Key wird aus der .env Datei geladen.
# Dadurch bleibt der Key sicher und steht nicht direkt im Code.

API_KEY = os.getenv("OPENWEATHER_API_KEY")


# =========================
# CITY SEARCH (GEOCODING API)
# =========================
# Wandelt einen Stadtnamen in geografische Koordinaten um.
# Beispiel: "Berlin" → [lat, lon, Land, genaue Treffer]

def search_city(city):
    url = "https://api.openweathermap.org/geo/1.0/direct"

    params = {
        "q": city,          # Suchbegriff (Stadtname)
        "limit": 5,         # maximale Anzahl an Ergebnissen
        "appid": API_KEY
    }

    response = requests.get(url, params=params)


    # API liefert direkt JSON (Liste von möglichen Städten)
    return response.json()

 # Debug (később törölhető)
    print("Status:", response.status_code)
    print("Response:", response.text)

    if response.status_code != 200:
        return []

    data = response.json()

    if not isinstance(data, list):
        return []

    return data

# =========================
# WEATHER FETCH
# =========================
# Holt aktuelle Wetterdaten für eine bestimmte Position (lat/lon)
# von der OpenWeather API.

def get_weather(lat, lon):
    url = "https://api.openweathermap.org/data/2.5/weather"

    params = {
        "lat": lat,             # geografische Breite 
        "lon": lon,             # geografische Länge
        "appid": API_KEY,       # API Key
        "units": "metric"       # Temperatur in Celsius
    }

    response = requests.get(url, params=params)
    data = response.json()


    # =========================
    # ERROR HANDLING
    # =========================
    # Falls die API keinen erfolgreichen Status zurückgibt,
    # wird ein einheitliches Fehlerobjekt zurückgegeben.

    if response.status_code != 200:
        return {"error": "No such city baby!"}
    

    # =========================
    # DATA TRANSFORMATION
    # =========================
    # Rohdaten der API werden in ein einfaches,
    # internes Format umgewandelt.
    
    return {
        "city": data["name"],
        "country": data["sys"]["country"],
        "temp": data["main"]["temp"],
        "description": data["weather"][0]["description"],
        "humidity": data["main"]["humidity"]
    }