import json


class _Dict2Obj:
    def __init__(self, dictionary):
        self.__dict__.update(dictionary)


def _dict2obj(dictionary: dict):
    return json.loads(json.dumps(dictionary), object_hook=_Dict2Obj)


def _fmt(text):  # Remove "(),-" from the title
    return text.replace("(", "").replace(")", "").replace(",", "").replace("- ", "")


def get_top_video(videos: list[dict], song: tuple):
    assert type(videos) == list, "Videos type is not list"
    assert type(song) == tuple, "Song type is not tuple"

    tracks_score = 0

    for video_dict in videos:
        score = 0
        video = _dict2obj(video_dict)  # Get the video into a dict

        # Make the formatted splitted title a variable
        full_title = _fmt(f"{song[0]} - {', '.join(song[1])}").split(" ")

        # Split the video title into words
        title_words = _fmt(video.snippet.title).split(" ")
        l_title_w = [word.lower() for word in title_words]

        # Give a score to each video according to title matches
        for word in full_title:
            if word in title_words:
                score += 1
        extras = 0
        for s in [
            "official" in l_title_w,
            "oficial" in l_title_w,
            "audio" in l_title_w,
            "video" in l_title_w,
            "videoclip" in l_title_w,
        ]:
            if s:
                extras += 1

        score += extras * 5

        if score >= tracks_score:  # Save best video (only last one)
            tracks_score = score
            top_video = video_dict

    return top_video
