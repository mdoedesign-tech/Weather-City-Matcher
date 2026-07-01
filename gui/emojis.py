
# =========================
# SUN / WEATHER VIBE
# =========================
def get_sun_emoji(vibe):
        if vibe == 1:
            return "⛈️ Storm mode"
        elif vibe == 2:
            return "🌧️ Heavy clouds"
        elif vibe == 3:
            return "🌦️ Mixed vibes"
        elif vibe == 4:
            return "☁️ Cloudy calm"
        elif vibe == 5:
            return "🌤️ Almost sunny"
        else:
            return "☀️ Full sunshine"
        

# =========================
# TEMPERATURE EMOJI MAPPING
# =========================
def get_temp_emoji(temp):
        if temp < -10:
            return "🧊 Freezing chaos"
        elif temp < 5:
            return "🥶 Very cold"
        elif temp < 15:
            return "🧥 Jacket weather"
        elif temp < 25:
            return "🙂 Perfect balance"
        elif temp < 35:
            return "😎 Hot & nice"
        else:
            return "🔥 Extreme heat"
        

# =========================
# HUMIDITY / HAIR LOGIC
# =========================      
def get_hair_emoji(h):
        if h < 20:
            return "💨 dry / frizzy-safe " 
        elif h < 40:
            return "✨ nice hair day" 
        elif h < 60:
            return "💁‍♀️ normal / manageable" 
        elif h < 80:
            return "🌫️ slightly chaotic" 
        else:
            return "🌧️💇‍♀️ full humidity disaster"  
        

# =========================
# WEATHER DESCRIPTION MAPPING
# =========================
def get_weather_desc_emoji(desc):
            # Normalisieren, damit Groß-/Kleinschreibung egal ist
            desc = desc.lower() 


            # Klassifikation nach Schlüsselwörtern
            if "thunder" in desc:
                return "⛈️ Storm"
            elif "rain" in desc or "drizzle" in desc:
                return "🌧️ Rain"
            elif "snow" in desc:
                return "❄️ Snow"
            elif "cloud" in desc:
                return "☁️ Clouds"
            elif "clear" in desc:
                return "☀️ Clear sky"
            elif "mist" in desc or "fog" in desc or "haze" in desc:
                return "🌫️ Foggy"
            else:
                return "🌍 Unknown"