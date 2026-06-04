# 🌤️ City Match – Weather Preference App

An interactive Streamlit app that matches cities based on your personal weather preferences (temperature, humidity, and general weather vibe).

You can search for cities, view real-time weather data, and see how well a city matches your ideal conditions.

---

## 🚀 Features

- 🔎 City search with OpenWeather geocoding API  
- 🌦️ Real-time weather data (temperature, humidity, conditions)  
- 🎯 Personal preference sliders (sun, temperature, hair/humidity comfort)  
- 💯 City match score system (0–100)  
- ⭐ Save favorite cities (SQLite database)  
- 💡 Emoji-based UI for better UX  

---

## 🛠️ Tech Stack

- Python 🐍  
- Streamlit  
- SQLite  
- OpenWeather API  
- python-dotenv (.env config)

---

## 📦 Installation

### 1. Clone the repository

git clone https://github.com/your-username/travle_dashboard.git  
cd travle_dashboard  

---

### 2. Create a virtual environment (recommended)

python -m venv .venv  

Mac/Linux:
source .venv/bin/activate  

Windows:
.venv\Scripts\activate  

---

### 3. Install dependencies

pip install -r requirements.txt  

If you don’t have requirements yet:

pip freeze > requirements.txt  

---

## 🔑 API Key Setup (IMPORTANT)

This project uses the OpenWeather API.

### Step 1 — Get API key
https://openweathermap.org/api

### Step 2 — Create `.env` file in root folder

OPENWEATHER_API_KEY=your_api_key_here  

### Step 3 — Install dotenv

pip install python-dotenv  

---

## ▶️ Run the app

streamlit run gui/app.py  

---

## ⚠️ Important Notes

- ❌ Never commit `.env`
- ❌ Never hardcode API keys
- ✔ `.env` is already ignored in `.gitignore`

---

## 🧠 How it works

The app calculates a match score (0–100):

- Weather condition match  
- Temperature preference match  
- Humidity / hair tolerance match  

---

## 💾 Data storage

SQLite database:

data/weather_app.db  

---

## 🚀 Future ideas

- City ranking system  
- Map-based recommendations  
- Weather travel planner  
- Deploy to Streamlit Cloud  

---

## 👨‍💻 Author

Built as a learning project for APIs + Streamlit + data handling.
