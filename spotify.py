# pylint: disable=wildcard-import, missing-module-docstring
import tekore as tk
from pprint import pprint

client_id, client_secret, redirect_uri = tk.config_from_file(".env")

token = tk.request_client_token(client_id, client_secret)
# token = tk.prompt_for_user_token(client_id, client_secret, redirect_uri)

sp = tk.Spotify(token)

user_id = input("User ID:\n> ")
playlists = sp.playlists(user_id).items  # pylint: disable=E1101

simple_playlist = playlists[0]

full_playlist = [track.track for track in sp.playlist(playlist_id=simple_playlist.id).tracks.items]

tracks = [(track.name, [artist.name for artist in track.artists]) for track in full_playlist]
