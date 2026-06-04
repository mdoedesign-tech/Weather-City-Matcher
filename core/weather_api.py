import requests

API_KEY = os.getenv("OPENWEATHER_API_KEY")

def search_city(city):
    url = "http://api.openweathermap.org/geo/1.0/direct"

    params = {
        "q": city,
        "limit": 5,
        "appid": API_KEY
    }

    response = requests.get(url, params=params)

    return response.json()

def get_weather(lat, lon):
    url = "https://api.openweathermap.org/data/2.5/weather"

    params = {
        "lat": lat,
        "lon": lon,
        "appid": API_KEY,
        "units": "metric"
    }

    response = requests.get(url, params=params)
    data = response.json()

    if response.status_code != 200:
        return {"error": "No such city baby!"}
    
    return {
        "city": data["name"],
        "country": data["sys"]["country"],
        "temp": data["main"]["temp"],
        "description": data["weather"][0]["description"],
        "humidity": data["main"]["humidity"]
    }