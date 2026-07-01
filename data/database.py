import sqlite3


# =========================
# DATABASE CONFIG
# =========================
# Pfad zur SQLite-Datenbankdatei.
# Wenn die Datei nicht existiert, wird sie automatisch erstellt.

DB_PATH = "data/weather_app.db"


# =========================
# INITIALISIERUNG DER DATENBANK
# =========================
# Erstellt die Tabelle für Favoriten-Städte, falls sie noch nicht existiert.

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
# FAVORIT SPEICHERN
# =========================
# Speichert eine Stadt in der Datenbank als Favorit.
# Wird verwendet, wenn der User auf "⭐ Save Favorite" klickt.

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
# FAVORITEN LADEN
# =========================
# Gibt alle gespeicherten Lieblingsstädte zurück.
# Rückgabe: Liste von Tupeln (id, city_name, country, lat, lon)

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
# FAVORIT LÖSCHEN
# =========================
# Entfernt eine Stadt aus den Favoriten anhand von Name + Land.
# (Hinweis: könnte auch über ID robuster gemacht werden)

def delete_favorite(city, country):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM favorite_cities
        WHERE city_name = ? AND country = ?
    """, (city, country))

    conn.commit()
    conn.close()