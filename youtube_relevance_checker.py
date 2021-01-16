import json


class Dict2Obj:
    def __init__(self, dictionary):
        self.__dict__.update(dictionary)


def dict2obj(dictionary: dict):
    return json.loads(json.dumps(dictionary), object_hook=Dict2Obj)


def fmt(text):  # Remove "(),-" from the title
    return text.replace("(", "").replace(")", "").replace(",", "").replace("- ", "")


tracks_score = 0


def get_top_video(videos: list[dict], song: list[tuple]):
    for video_dict in videos:
        score = 0
        video = dict2obj(video_dict)  # Get the video into a dict

        # Make the formatted splitted title a variable
        full_title = fmt(f"{song[0]} - {', '.join(song[1])}").split(" ")

        # Split the video title into words
        title_words = fmt(video.snippet.title).split(" ")

        # Give a score to each video according to title matches
        for word in full_title:
            if word in title_words:
                score += 1
        if "Official" in title_words and "Audio" in title_words:
            score += 5

        if score >= tracks_score:  # Save best video (only last one)
            top_video = video_dict

    return top_video
