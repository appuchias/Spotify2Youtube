# pylint: disable=wildcard-import, missing-module-docstring
import tekore as tk

client_id, client_secret, redirect_uri = tk.config_from_file(".env")

token = tk.request_client_token(client_id, client_secret)
# token = tk.prompt_for_user_token(client_id, client_secret, redirect_uri)

sp = tk.Spotify(token)

user_id = input("User ID:\n> ")
playlists = sp.playlists(user_id).items  # pylint: disable=E1101

p_id = playlists[0].id

full_playlist = [
    track.track for track in sp.playlist(playlist_id=p_id).tracks.items  # pylint: disable=E1101
]

tracks = [
    (track.name, [artist.name for artist in track.artists]) for track in full_playlist
]
