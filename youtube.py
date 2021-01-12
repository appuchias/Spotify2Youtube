# pylint: disable=no-member
import os
from time import sleep

import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors

scopes = ["https://www.googleapis.com/auth/youtube"]


def login(credentials_file: str = "client_secret.json"):
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


def youtube(songs_q: list = [], pname: str = "Playlist by API"):
    youtube = login("client_secret.json")

    # Actual valuable traffic
    playlist_id = (
        youtube.playlists()
        .insert(
            part="snippet,status",
            body={
                "snippet": {
                    "title": pname,
                    "description": "Playlist from Spotify",
                    "tags": ["By Appu", "Spotify"],
                    "defaultLanguage": "es",
                },
                "status": {"privacyStatus": "private"},
            },
        )
        .execute()
    )["id"]

    for song in songs_q:
        try:
            video = (
                youtube.search()
                .list(
                    part="snippet", maxResults=1, q=f"{song[0]}, {', '.join(song[1])}"
                )
                .execute()["items"]
            )[0]

            youtube.playlistItems().insert(
                part="snippet",
                body={
                    "snippet": {
                        "playlistId": playlist_id,
                        "position": 0,
                        "resourceId": {
                            "kind": "youtube#video",
                            "videoId": video["id"]["videoId"],
                        },
                    }
                },
            ).execute()

            print(f" - Added \"{video['snippet']['title']}\" to the playlist\n")

            sleep(0.5)
        except googleapiclient.errors.HttpError:
            youtube = login("client_secret2.json")

            video = (
                youtube.search()
                .list(
                    part="snippet", maxResults=1, q=f"{song[0]}, {', '.join(song[1])}"
                )
                .execute()["items"]
            )[0]

            youtube.playlistItems().insert(
                part="snippet",
                body={
                    "snippet": {
                        "playlistId": playlist_id,
                        "position": 0,
                        "resourceId": {
                            "kind": "youtube#video",
                            "videoId": video["id"]["videoId"],
                        },
                    }
                },
            ).execute()

    print("\nDone adding songs")


if __name__ == "__main__":
    youtube(
        [
            ("I'll come back to you", ["Rxseboy", "Powfu"]),
            ("Throw it all away", ["Powfu", "Jomie"]),
        ]
    )
