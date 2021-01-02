from django.shortcuts import render
from django.http import QueryDict

# Create your views here.
def home(request):
    query = QueryDict(request.META["QUERY_STRING"])
    statuscode = query.get("code")
    state = query.get("state")
    return render(request, "main/home.html", {"statuscode": statuscode, "state": state})


def spotify(request):
    return render(request, "main/spotify.html")


def _404(request):
    return render(request, "main/404.html")
