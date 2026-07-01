import pandas as pd


# =========================
# FAVORITEN → DATAFRAME
# =========================
# Wandelt die Rohdaten aus der SQLite-Datenbank (Liste von Tupeln)
# in ein pandas DataFrame um.
#
# Das ist nötig, weil PyDeck / Streamlit besser mit DataFrames arbeiten
# als mit rohen Listen.

def favorites_to_dataframe(favorites):

    return pd.DataFrame(
        favorites,
        columns=[
            "ID",
            "City",
            "Country",
            "Latitude",
            "Longitude"
        ]
    )


# =========================
# MAP CENTER BERECHNUNG
# =========================
# Berechnet den geografischen Mittelpunkt aller gespeicherten Städte.
# Dieser Punkt wird als Startposition für die Karte verwendet.

def get_map_center(df):

    return (
        df["Latitude"].mean(),      # Durchschnitt aller Breitengrade
        df["Longitude"].mean()      # Durchschnitt aller Längengrade
    )