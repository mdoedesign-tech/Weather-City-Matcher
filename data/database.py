import sqlite3

DB_PATH = "data/weather_app.db"


# =========================
# INIT DB
# =========================
def init_db():
    conn = sqlite3.connect(DB_PATH)
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


# =========================
# SAVE FAVORITE
# =========================
def save_favorite(city, country, lat, lon):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO favorite_cities (city_name, country, lat, lon)
        VALUES (?, ?, ?, ?)
    """, (city, country, lat, lon))

    conn.commit()
    conn.close()


# =========================
# GET FAVORITES
# =========================
def get_favorites():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM favorite_cities
    """)

    rows = cursor.fetchall()

    conn.close()
    return rows


# =========================
# DELETE FAVORITE
# =========================
def delete_favorite(city, country):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM favorite_cities
        WHERE city_name = ? AND country = ?
    """, (city, country))

    conn.commit()
    conn.close()