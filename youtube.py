# pylint: disable=no-member
import os
from itertools import cycle
from rich.console import Console

import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors

scopes = ["https://www.googleapis.com/auth/youtube"]

client_secrets = cycle(["client_secret.json", "client_secret2.json", "client_secret3.json"])
c = Console()


def _login():
    global client_secrets

    credentials_file = next(client_secrets)
    c.print("[dim yellow][" + credentials_file + "]\n")

    # General values
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"  # 0 if public

    api_service_name, api_version = "youtube", "v3"
    client_secrets_file = credentials_file

    # Get credentials and create an API client
    credentials = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        client_secrets_file, scopes
    ).run_console()
    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, credentials=credentials
    )

    return youtube


def _create_playlist(youtube, pname: str = "Playlist by API"):
    try:
        playlist_id = (
            youtube.playlists()
            .insert(
                part="snippet,status",
                body={
                    "snippet": {
                        "title": pname,
                        "description": "Playlist from Spotify",
                        "defaultLanguage": "es",
                    },
                    "status": {"privacyStatus": "unlisted"},
                },
            )
            .execute()
        )["id"]
    except googleapiclient.errors.HttpError:
        c.print(
            "[bold red] [!] Credentials quota fulfilled.\n  -  Logging in with other credentials.\n"
        )
        youtube = _login()

        playlist_id = (
            youtube.playlists()
            .insert(
                part="snippet,status",
                body={
                    "snippet": {
                        "title": pname,
                        "description": "Playlist from Spotify",
                        "defaultLanguage": "es",
                    },
                    "status": {"privacyStatus": "unlisted"},
                },
            )
            .execute()
        )["id"]

    return playlist_id, f"https://www.youtube.com/playlist?list={playlist_id}"


def _search(youtube, q: str):
    video = (
        youtube.search()
        .list(
            part="snippet",
            type="youtube#video",
            maxResults=1,
            q=q,
            prettyPrint=True,
        )
        .execute()["items"][0]
    )
    return video


def tracks2youtube(songs_q: list, pname: str):
    youtube = _login()

    # Actual valuable traffic
    try:
        playlist_id, playlist_link = _create_playlist(youtube, pname)

    # Quota from credentials fulfilled
    except googleapiclient.errors.HttpError:
        c.print(
            "[bold red] [!] Credentials quota fulfilled.\n  -  Logging in with other credentials.\n"
        )
        youtube = _login()
        playlist_id, playlist_link = _create_playlist(youtube, pname)

    for song in songs_q:
        try:
            video = _search(youtube, f"{song[0]} - {', '.join(song[1])}")

        # Quota from credentials fulfilled
        except googleapiclient.errors.HttpError:
            c.print(
                "[bold red] [!] Credentials quota fulfilled.\n  -  Logging in with other credentials.\n"
            )
            youtube = _login()

            video = _search(youtube, f"{song[0]} - {', '.join(song[1])}")

        # Whichever the case it is
        finally:
            video_id = video["id"]["videoId"]
            video_url = f"https://youtube.com/watch?v={video_id}"

            youtube.playlistItems().insert(
                part="snippet",
                body={
                    "snippet": {
                        "playlistId": playlist_id,
                        "position": 0,
                        "resourceId": {
                            "kind": "youtube#video",
                            "videoId": video_id,
                        },
                    }
                },
            ).execute()

            c.print(
                f'[bold green]\n [✓] Added "{video["snippet"]["title"]}" to the playlist. ({video_url})'
            )

    c.print("\n" * 5 + f"[bold green]\nDone adding songs. Playlist: {playlist_link}")


if __name__ == "__main__":
    tracks2youtube(
        [
            ("I'll come back to you", ["Rxseboy", "Powfu"]),
            ("Throw it all away", ["Powfu", "Jomie"]),
        ],
        "",
    )
