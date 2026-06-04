import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

# =========================
# IMPORTS
# =========================
import streamlit as st
from core.weather_api import search_city, get_weather
from gui.emojis import get_sun_emoji, get_hair_emoji, get_temp_emoji, get_weather_desc_emoji
from core.analysis import score_city
from data.database import init_db, save_favorite, get_favorites


# =========================
# INIT DB
# =========================
init_db()


# =========================
# PAGE CONFIG
# =========================
st.set_page_config(page_title="Weather App", layout="wide")
st.title("City Match")

# =========================
# SESSION STATE (IMPORTANT FIX)
# =========================

if "weather" not in st.session_state:
    st.session_state.weather = None   # This is REQUIRED so weather survives button reruns

if "source" not in st.session_state:
    st.session_state.source = None   # "search" or "favorite"


# =========================
# SIDEBAR SETTINGS
# =========================
with st.sidebar:
    st.header("Set your preferences!")
    
    # wie viel licht
    sun_tolerance = st.slider ("Current weather-vibe:", 1, 6, 3)
    
    st.markdown(f"## {get_sun_emoji(sun_tolerance)}")

    st.divider()

    # wie kalt oder heiß
    temp_tolerance = st.slider ("How hot feels okay for you today?", -50, 50, 0)
    
    st.markdown(f"## {get_temp_emoji(temp_tolerance)}")

    st.divider()

    # wie viel fruchtigkeit
    hair_tolerance = st.slider("How much humidity can your hairstyle handle today?", 0, 100, 50) 
    
    st.markdown(f"## {get_hair_emoji(hair_tolerance)}")


# =========================
# CITY SEARCH
# =========================
city = st.text_input("Enter City")

results = []

# Suchen ob es gibt mehrere Stadt mit die gelche Name oder keine Stadt gibt mit deiese Name
if city:
    results = search_city(city)

if city and not results:
    st.warning("No cities found 😢")


# =========================
# CITY SELECT
# =========================
if results:

    options = [
        f"{c['name']} ({c['country']})"
        for c in results
    ]

    selected = st.selectbox ("Select location", options)

    #ausgewählte option
    index = options.index(selected)
    chosen = results[index]

    lat = chosen["lat"]
    lon = chosen["lon"]

    
    # =========================
    # CHECK WEATHER BUTTON
    # =========================
    if st.button("Check it!"):

        
        st.session_state.weather = get_weather(lat, lon) # store weather in session state
        st.session_state.source = "search"

        weather = st.session_state.weather


        if "error" in weather:
            st.error(weather["error"])


# =========================
# GLOBAL WEATHER DISPLAY
# =========================
weather = st.session_state.weather

if weather is not None and "error" not in weather:

    st.success(f"{weather['city']} ({weather['country']})")

    st.write(
        f"Weather: {weather['description']} "
        f"{get_weather_desc_emoji(weather['description'])}"
    )

    st.write(
        f"Temp: {weather['temp']} °C "
        f"{get_temp_emoji(weather['temp'])}"
    )

    st.write(
        f"Humidity: {weather['humidity']}% "
        f"{get_hair_emoji(weather['humidity'])}"
    )



    # =========================
    # SCORE
    # =========================
    score = score_city(
        sun_tolerance,
        temp_tolerance,
        hair_tolerance,
        weather["temp"],
        weather["humidity"],
        weather["description"]
    )

    st.metric("City Match Score", f"{score}/100")


# =========================
# SAVE FAVORITE (ONLY FROM SEARCH)
# =========================

if st.session_state.weather is not None and st.session_state.source == "search":

    if st.button("⭐ Save Favorite"):

        save_favorite(
            st.session_state.weather["city"],
            st.session_state.weather["country"],
            lat,
            lon
        )

        st.success("Saved!")


# =========================
# FAVORITES SIDEBAR
# =========================

favorites = get_favorites()

st.sidebar.header("⭐ Favorites")

for fav in favorites:
    city_name = fav[1]
    country = fav[2]
    lat = fav[3]
    lon = fav[4]

    if st.sidebar.button(
        f"💙 {city_name}, {country}",
        key=f"fav_{city_name}_{country}"
    ):
        
        st.session_state.weather = get_weather(lat, lon)
        st.session_state.source = "favorite"

        st.rerun()
           


        
