from spotify import spotify
from youtube import youtube
import re

url_regex = re.compile(r"http(?:s)?://open.spotify.com/playlist/(.*)\?si=.*")

playlist_id = url_regex.search(
    input("Type the Spotify playlist URL to migrate:\n> ")
).group(1)

tracks, playlist_name = spotify(playlist_id)
print("\n - Spotify playlist tracks retrieval successful\n\n", end="")

youtube(tracks, playlist_name)
