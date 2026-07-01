
# =========================
# WEATHER TO VIBE MAPPING
# =========================
# Wandelt eine Wetterbeschreibung (API String)
# in eine einfache 1–6 Skala um.
#
# Ziel: komplexe Wetterdaten in eine "Gefühls-Skala" übersetzen.

def weather_to_vibe(desc: str) -> int:
    desc = desc.lower()

    if "thunder" in desc:
        return 1                # sehr schlechtes Wetter
    elif "rain" in desc or "drizzle" in desc:
        return 2
    elif "snow" in desc:
        return 2
    elif "mist" in desc or "fog" in desc or "haze" in desc:
        return 3
    elif "cloud" in desc:
        return 4
    elif "clear" in desc:
        return 6                # perfektes Wetter
    else:
        return 3                # neutraler Default
    


    
# =========================
# CITY SCORING SYSTEM
# =========================
# Berechnet, wie gut eine Stadt zu den persönlichen
# User-Präferenzen passt.
#
# Output: Score zwischen 0 und 100

def score_city(
    sun_pref: int,          # gewünschte Wetter-Stimmung (1–6)
    temp_pref: float,       # bevorzugte Temperatur
    humidity_pref: int,     # gewünschte Luftfeuchtigkeit
    temp_actual: float,     # aktuelle Temperatur
    humidity_actual: int,   # aktuelle Luftfeuchtigkeit
    weather_desc: str       # Wetterbeschreibung (API)
):
    
    # =========================
    # 1. WEATHER VIBE SCORE
    # =========================
    # Vergleich zwischen gewünschtem Wettergefühl und realem Wetter

    actual_vibe = weather_to_vibe(weather_desc)

    vibe_diff = abs(sun_pref - actual_vibe)
    vibe_score = max(0, 100 - vibe_diff * 20)


    # =========================
    # 2. TEMPERATURE SCORE
    # =========================
    # Je größer der Unterschied, desto schlechter der Score

    temp_diff = abs(temp_pref - temp_actual)
    temp_score = max(0, 100 - temp_diff * 3)


    # =========================
    # 3. HUMIDITY SCORE
    # =========================

    humidity_diff = abs(humidity_pref - humidity_actual)
    humidity_score = max(0, 100 - humidity_diff)



    # =========================
    # FINAL SCORE
    # =========================
    # Durchschnitt aus allen drei Teil-Scores
    total_score = (vibe_score + temp_score + humidity_score) / 3

    return round(total_score)





