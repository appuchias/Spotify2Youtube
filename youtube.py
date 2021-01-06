# pylint: disable=no-member
import os

from pprint import pprint

import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors

scopes = ["https://www.googleapis.com/auth/youtube"]


def main(videos_q: list = None):
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"
    client_secrets_file = "client_secret.json"

    # Get credentials and create an API client
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        client_secrets_file, scopes
    )
    credentials = flow.run_console()
    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, credentials=credentials
    )

    playlist_create = youtube.playlists().insert(
        part="snippet,status",
        body={
            "snippet": {
                "title": "Sample playlist created via API",
                "description": "This is a sample playlist description.",
                "tags": ["sample playlist", "API call"],
                "defaultLanguage": "en",
            },
            "status": {"privacyStatus": "private"},
        },
    )

    playlist = playlist_create.execute()
    playlist_id = playlist["id"]

    videos_dict = (
        youtube.search().list(part="snippet", maxResults=5, q="surfing").execute()
    )

    videos = videos_dict["items"]

    pprint(videos)
    pprint(playlist_id)


if __name__ == "__main__":
    main()
