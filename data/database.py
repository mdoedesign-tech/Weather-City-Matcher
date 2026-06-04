import sqlite3

def init_db():
    conn = sqlite3.connect("data/weather_app.db")

    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS favorite_cities (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            city_name TEXT,
            country TEXT,
            lat REAL,
            lon REAL
        )
    """)

    conn.commit()
    conn.close()



def save_favorite(city, country, lat, lon):
    conn = sqlite3.connect("data/weather_app.db")

    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO favorite_cities
        (city_name, country, lat, lon)
        VALUES (?, ?, ?, ?)
    """, (city, country, lat, lon))

    conn.commit()
    conn.close()



def get_favorites():
    conn = sqlite3.connect("data/weather_app.db")

    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM favorite_cities
    """)

    favorites = cursor.fetchall()

    conn.close()

    return favorites


