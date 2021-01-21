# pylint: disable=no-member
from youtube_relevance_checker import get_top_video

import os
from time import sleep
from itertools import cycle

import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors

scopes = ["https://www.googleapis.com/auth/youtube"]

client_secrets = cycle(
    ["client_secret.json", "client_secret2.json", "client_secret3.json"]
)


def _login():
    global client_secrets

    credentials_file = next(client_secrets)
    print("[" + credentials_file + "]\n")

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
        print(
            " [!] Credentials quota fulfilled.\n  -  Logging in with other credentials.\n"
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


def tracks2youtube(songs_q: list, pname: str):
    youtube = _login()

    # Actual valuable traffic
    try:
        playlist_id, playlist_link = _create_playlist(youtube, pname)
    except googleapiclient.errors.HttpError:
        print(
            " [!] Credentials quota fulfilled.\n  -  Logging in with other credentials.\n"
        )
        youtube = _login()
        playlist_id = _create_playlist(youtube, pname)

    for song in songs_q:
        try:
            videos = (
                youtube.search()
                .list(
                    part="snippet", maxResults=5, q=f"{song[0]} - {', '.join(song[1])}"
                )
                .execute()["items"]
            )

        except googleapiclient.errors.HttpError:  # Quota from credentials 1 fulfilled
            print(
                " [!] Credentials quota fulfilled.\n  -  Logging in with other credentials.\n"
            )
            youtube = _login()

            videos = (
                youtube.search()
                .list(
                    part="snippet", maxResults=5, q=f"{song[0]}, {', '.join(song[1])}"
                )
                .execute()["items"]
            )

        finally:
            assert len(videos) == 5, "Not enough videos"
            video = get_top_video(videos, song)
            # print(video)

            # Avoid KeyError from getting videoId from a playlist
            if not video["id"]["kind"] == "youtube#playlist":
                video_id = video["id"]["videoId"]
                video_title = video["snippet"]["title"]
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

                print(f'\n [✓] Added "{video_title}" to the playlist. ({video_url})')

                sleep(0.5)
            else:
                print(
                    f" [!] Playlist marked as top video. Oops!\n - ({video_title} - {video_url})"
                )

    print("\n" * 20)
    print(f"\nDone adding songs. Playlist: {playlist_link}")


if __name__ == "__main__":
    tracks2youtube(
        [
            ("I'll come back to you", ["Rxseboy", "Powfu"]),
            ("Throw it all away", ["Powfu", "Jomie"]),
        ],
        "",
    )
