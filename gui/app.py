import sys
import os


# =========================
# PATH SETUP
# =========================
# Fügt das Hauptverzeichnis des Projekt zum Phython-Pfad hinzu,
# damit Modul aus core/ data/ und gui/ importiert werden können

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

# =========================
# IMPORTS
# =========================
import streamlit as st
import pandas as pd
import pydeck as pdk

# API-Logik (Stadt-Suche und Wetterdaten)
from core.weather_api import search_city, get_weather

# UI-helper für Emojis und visuelle Darstellung
from gui.emojis import get_sun_emoji, get_hair_emoji, get_temp_emoji, get_weather_desc_emoji

# Bewertungslogik (wie gut eine Stadt zu den User-Reference passt)
from core.analysis import score_city

#Datenbankfunktionen (Favoriten speichern / Laden / Löschen)
from data.database import init_db, save_favorite, get_favorites, delete_favorite

# Mapping ß Datenaufbereitung für die Visualisierung
from core.map_utils import favorites_to_dataframe, get_map_center


# =========================
# DATABASE INITIALISIERUNG
# =========================
# Stellt sicher, dass die Datenbank beim Start existiert
init_db()


# =========================
# STREAMLIT PAGE CONFIG
# =========================
st.set_page_config(page_title="Weather App", layout="wide")
st.title("City Match")


# =========================
# SESSION STATE 
# =========================
# Streamlit führt das Skript bei jeder Interaktion neu aus
# session_state speichert Daten zwischen diesen Reloads.

if "weather" not in st.session_state:
    st.session_state.weather = None   # aktuell geladenes wetter

if "source" not in st.session_state:
    st.session_state.source = None   # "search" oder "favorite"

if "selected_favorite" not in st.session_state:
    st.session_state.selected_favorite = None  # aktuell ausgewählter Favorit


# =========================
# SIDEBAR - USER REFERENCES
# =========================
# hier Legt der User fest, welche Wetterbedigungen angenehm sind

with st.sidebar:
    st.header("Set your preferences!")
    
    # Sonnentoleranz (wie "sonning" es sich gut anfühlt)
    sun_tolerance = st.slider ("Current weather-vibe:", 1, 6, 3)
    st.markdown(f"## {get_sun_emoji(sun_tolerance)}")

    st.divider()

    # Temperaturtoleranz (kalt bis heiß)
    temp_tolerance = st.slider ("How hot feels okay for you today?", -50, 50, 0)
    st.markdown(f"## {get_temp_emoji(temp_tolerance)}")

    st.divider()

    # Luftfreuchtigkeit / Haar-Styling-Toleranz
    hair_tolerance = st.slider("How much humidity can your hairstyle handle today?", 0, 100, 50)     
    st.markdown(f"## {get_hair_emoji(hair_tolerance)}")


# =========================
# CITY SEARCH
# =========================
# User gibt eine Stadt ein, danach die API kann merere Treffer zurückgeben

city = st.text_input("Enter City")

results = []

if city:
    results = search_city(city)

# Falls keine Stadt gefunden wurde
if city and not results:
    st.warning("No cities found 😢")


# =========================
# CITY SELECT
# =========================
if results:

    # Dropdown-Optionen für mögliche Städte
    options = [
        f"{c['name']} ({c['country']})"
        for c in results
    ]

    selected = st.selectbox ("Select location", options)

    # ausgewählte Stadt bestimmen
    index = options.index(selected)
    chosen = results[index]

    lat = chosen["lat"]
    lon = chosen["lon"]

    
    # =========================
    # CHECK WEATHER BUTTON
    # =========================
    if st.button("Check it!"):

        # Wetterdaten laden und im Session State speichern
        st.session_state.weather = get_weather(lat, lon) # store weather in session state
        st.session_state.source = "search"

        weather = st.session_state.weather

        # Fehlerbehnadlung der API
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
    # MATCH SCORE
    # =========================
    # Berechnet, wie gut die Stadt zu den Use-Präferenzen passt
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
    # DELETE FAVORITE BUTTON
    # =========================
    fav = st.session_state.get("selected_favorite")

    if st.session_state.source == "favorite" and fav:

        if st.button("🗑️ Delete from favourites"):

            delete_favorite(fav["city"], fav["country"])

            st.success("Deleted 💜")

            st.session_state.selected_favorite = None
            st.session_state.weather = None

            st.rerun()


# =========================
# SAVE FAVORITE
# =========================
# Nur möglich, wenn Daten aus einer Suche stammen

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

df_favorites = favorites_to_dataframe(favorites)

st.sidebar.header("⭐ Favorites")

for fav in favorites:
    city_name = fav[1]
    country = fav[2]
    lat = fav[3]
    lon = fav[4]

    if st.sidebar.button(
        f"💜 {city_name}, {country}",
        key=f"fav_{city_name}_{country}"
    ):
        
        st.session_state.weather = get_weather(lat, lon)
        st.session_state.source = "favorite"

        st.session_state.selected_favorite = {
        "city": city_name,
        "country": country,
        "lat": lat,
        "lon": lon
        }

        st.rerun()
           
# =========================
# TABELLE + KARTE
# =========================

st.divider()
st.subheader("⭐ Favorite Cities")

if not df_favorites.empty:
    st.dataframe(df_favorites.drop(columns=["ID"]))

center_lat, center_lon = get_map_center(df_favorites)

st.subheader("🗺️ Map of Favorites")


# Visualisierung der Favoriten auf einer Karte
st.pydeck_chart(
    pdk.Deck(
        
        initial_view_state=pdk.ViewState(
            latitude=center_lat,
            longitude=center_lon,
            zoom=3
        ),

        layers=[
            pdk.Layer(
                "ScatterplotLayer",
                data=df_favorites,
                get_position='[Longitude, Latitude]',
                get_radius=50000,
                get_fill_color=[180, 0, 255, 220],
                pickable=True
            )
        ],

        tooltip={
            "text": "{City}, {Country}"
        }
    )
)