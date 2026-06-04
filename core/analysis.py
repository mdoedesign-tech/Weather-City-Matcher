
# open weather description to 6 scale 
def weather_to_vibe(desc: str) -> int:
    desc = desc.lower()

    if "thunder" in desc:
        return 1
    elif "rain" in desc or "drizzle" in desc:
        return 2
    elif "snow" in desc:
        return 2
    elif "mist" in desc or "fog" in desc or "haze" in desc:
        return 3
    elif "cloud" in desc:
        return 4
    elif "clear" in desc:
        return 6
    else:
        return 3
    
# itt lesz score rendszer a megadott és API-ból húzott értékekből
def score_city(
    sun_pref: int,
    temp_pref: float,
    humidity_pref: int,
    temp_actual: float,
    humidity_actual: int,
    weather_desc: str
):
    
# itt számoljuk ki a három különböző preferencia egyéni score-ját

# weather-vibe score
    actual_vibe = weather_to_vibe(weather_desc)

    vibe_diff = abs(sun_pref - actual_vibe)
    vibe_score = max(0, 100 - vibe_diff * 20)

# tempreture score
    temp_diff = abs(temp_pref - temp_actual)
    temp_score = max(0, 100 - temp_diff * 3)

#humidity score
    humidity_diff = abs(humidity_pref - humidity_actual)
    humidity_score = max(0, 100 - humidity_diff)



# itt számoljuk ki az egyesített score-t a városra nézve a személyes preferenciákhoz képest
    total_score = (vibe_score + temp_score + humidity_score) / 3

    return round(total_score)





