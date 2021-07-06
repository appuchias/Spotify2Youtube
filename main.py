from spotify import get_spotify_tracks
from youtube import tracks2youtube
from time import sleep
from rich.console import Console
from rich.table import Table
from rich.traceback import install
import re, os

install()
c = Console()

url_regex = re.compile(r"http(?:s)?://open.spotify.com/playlist/(.*)\?si=.*")

playlist_id = url_regex.search(input("Type the Spotify playlist URL to migrate:\n> ")).group(1)

os.system("cls")

tracks, playlist_name = get_spotify_tracks(playlist_id)
c.print(" [✓] Spotify playlist tracks retrieval successful\n")
c.print("Playlist title - " + playlist_name)
c.print("Tracks number - " + str(len(tracks)))

c.print("\n\n - Starting youtube addition in 3 seconds...")

sleep(3)

os.system("cls")

tracks2youtube(list(reversed(tracks)), playlist_name)  # Reversed to keep the order
