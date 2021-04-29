import spotipy as sp
from spotipy.oauth2 import SpotifyOAuth
from rich.traceback import install
from dotenv import load_dotenv

load_dotenv()
install()


def get_spotify_tracks(pid: str = None) -> tuple[list[tuple[str, list[str]]], str]:
    spotify = sp.Spotify(auth_manager=SpotifyOAuth(scope="playlist-modify-private"))

    print(pid)
    playlist = spotify.playlist(playlist_id=pid)
    tracks_objects = spotify.playlist_items(pid, offset=0)["items"]
    tracks_items = [track["track"] for track in tracks_objects]
    print(tracks_items)

    tracks = [
        (track["name"], [artist["name"] for artist in track["artists"]]) for track in tracks_items
    ]

    return (tracks, playlist["name"])


if __name__ == "__main__":
    print(get_spotify_tracks("2ThrUxO3KmVj0wQ7hDPD39"))
