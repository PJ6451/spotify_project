cols = [
    "date_added",
    "uri",
    "track_href",
    "name",
    "artist",
    "country",
    "type",
    "tempo",
    "duration_ms",
    "time_signature",
    "key",
    "mode",
    "danceability",
    "energy",
    "loudness",
    "liveness",
    "valence",
    "speechiness",
    "acousticness",
    "instrumentalness",
]


def transform(data):
    return [set_values_in_correct_order(row) for row in data]


def set_values_in_correct_order(row: dict) -> dict:
    filtered_row = {}
    for col in cols:
        if col == "uri":
            filtered_row[col] = row["id"]
        else:
            filtered_row[col] = row[col]
    return filtered_row
