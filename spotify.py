import spotipy as sp
from spotipy.oauth2 import SpotifyOAuth
from rich.traceback import install
from dotenv import load_dotenv

load_dotenv()
install()


def get_spotify_tracks(pid: str = None) -> tuple[list[tuple[str, list[str]]], str]:
    spotify = sp.Spotify(auth_manager=SpotifyOAuth(scope="playlist-modify-private"))

    playlist = spotify.playlist(playlist_id=pid)  # Get the playlist object to get the name
    tracks_objects = spotify.playlist_items(pid, offset=0)["items"]  # Get tracks items
    tracks_items = [
        track["track"] for track in tracks_objects  # Omit worthless information for this use case
    ]

    tracks = [  # Create the tuple list made of [(song1 name, [artists]), (song2 name, [artists])]
        (track["name"], [artist["name"] for artist in track["artists"]]) for track in tracks_items
    ]

    return (tracks, playlist["name"])  # Return all the info in a tuple


if __name__ == "__main__":
    print(get_spotify_tracks("2ThrUxO3KmVj0wQ7hDPD39"))  # Test in a custom private playlist
