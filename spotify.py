# pylint: disable=wildcard-import, missing-module-docstring, no-member
import tekore as tk


def spotify(pid: str = None):
    assert pid, "No playlist specified"

    client_id, client_secret, _redirect_uri = tk.config_from_file(".env")
    token = tk.request_client_token(client_id, client_secret)
    # token = tk.prompt_for_user_token(client_id, client_secret, _redirect_uri)

    sp = tk.Spotify(token)

    playlist = sp.playlist(playlist_id=pid)

    full_playlist = [
        track.track for track in playlist.tracks.items
    ]

    tracks = [
        (track.name, [artist.name for artist in track.artists])
        for track in full_playlist
    ]

    # [(song1, [artist1, artist2]), (song2, [artist3, artist4])]
    return (tracks, playlist.name)


if __name__ == "__main__":
    print(spotify())
