import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import config.config as sc

sc.set_spotify_creds()

country_uri_map = {
    "Japan": "37i9dQZEVXbKXQ4mDTEBXq",
    "USA": "37i9dQZEVXbLRQDuF5jeBp",
    "El Salvador": "37i9dQZEVXbLxoIml4MYkT",
}


def query_data(date: str):
    sp = get_spotipy_client()
    data_by_country = []
    for country, uri in country_uri_map.items():
        playlist = sp.playlist(f"spotify:playlist:{uri}")
        uris, names, artists = parse_data(playlist)
        check_uri_and_artists(uris, artists)
        songs = combine_data(date, sp, country, uris, names, artists)
        data_by_country.extend(songs)
    return data_by_country


def get_spotipy_client() -> spotipy.client.Spotify:
    auth_manager = SpotifyClientCredentials()
    try:
        sp = spotipy.Spotify(auth_manager=auth_manager)
    except spotipy.SpotifyOauthError as Error:
        raise Error
    return sp


def parse_data(playlist: dict):
    uris = [track["track"]["uri"] for track in playlist["tracks"]["items"]]
    names = [track["track"]["name"] for track in playlist["tracks"]["items"]]
    artists = [
        track["track"]["artists"][0]["name"] for track in playlist["tracks"]["items"]
    ]

    return uris, names, artists


def combine_data(
    date: str,
    sp: spotipy.client.Spotify,
    country: str,
    uris: list,
    names: list,
    artists: list,
) -> dict:
    song_features = sp.audio_features(uris)
    songs = song_features.copy()
    for ind, song in enumerate(songs):
        song["name"] = names[ind]
        song["artist"] = artists[ind]
        song["country"] = country
        song["date_added"] = date
    return songs


def check_uri_and_artists(uris: list, artists: list):
    checks = [check_data_not_null(data) for data in [uris, artists]]
    if all(checks):
        print("Artist and URI's are not null")
    else:
        raise ValueError("Artist or URI value is null, please check data")


def check_data_not_null(data: list) -> bool:
    if None in data:
        return False
    elif "" in data:
        return False
    else:
        return True
