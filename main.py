from spotify import spotify
from youtube import tracks2youtube
from time import sleep
from rich.console import Console
from rich.table import Table
import re, os

url_regex = re.compile(r"http(?:s)?://open.spotify.com/playlist/(.*)\?si=.*")

playlist_id = url_regex.search(
    input("Type the Spotify playlist URL to migrate:\n> ")
).group(1)

os.system("cls")

tracks, playlist_name = spotify(playlist_id)
print(" [✓] Spotify playlist tracks retrieval successful\n")

console = Console()
t = Table(show_header=True, header_style="bold cyan")

t.add_column("Playlist title")
t.add_column("Track number")
t.add_row(playlist_name, str(len(tracks)))

console.print(t)
print("\n\n - Starting youtube addition in 3 seconds...")

sleep(3)

os.system("cls")

tracks2youtube(list(reversed(tracks)), playlist_name)  # Reversed to keep the order
