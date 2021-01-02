from django.urls import path
from . import views

urlpatterns = [
    path("", views.home),
    path("home", views.home),
    path("home/code=<str:statuscode>/", views.home),
    path("spotify/", views.spotify),
    path("404/", views._404),
]
