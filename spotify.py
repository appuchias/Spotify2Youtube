# pylint: disable=wildcard-import, missing-module-docstring, no-member
import tekore as tk


def main():
    client_id, client_secret, _redirect_uri = tk.config_from_file(".env")

    token = tk.request_client_token(client_id, client_secret)
    # token = tk.prompt_for_user_token(client_id, client_secret, _redirect_uri)

    sp = tk.Spotify(token)

    user_id = input("User ID:\n> ")
    playlists = sp.playlists(user_id).items

    p_id = playlists[0].id

    full_playlist = [
        track.track for track in sp.playlist(playlist_id=p_id).tracks.items
    ]  # [track1(obj), track2(obj)]

    tracks = [
        (track.name, [artist.name for artist in track.artists])
        for track in full_playlist
    ]  # [(song1, [artist1, artist2]), (song2, [artist3, artist4])]

    return tracks


if __name__ == "__main__":
    print(main())
