import pandas as pd


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

def get_map_center(df):

    return (
        df["Latitude"].mean(),
        df["Longitude"].mean()
    )