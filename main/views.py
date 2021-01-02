from django.shortcuts import render

# Create your views here.
def home(response, statuscode: str = None):
    if statuscode:
        return render(response, "main/home.html", {"statuscode": statuscode})
    return render(response, "main/home.html")


def spotify(response):
    return render(response, "main/spotify.html")


def _404(response):
    return render(response, "main/404.html")
