from django.urls import path
from . import views

urlpatterns = [
    path("", views.home),
    path("spotify/", views.spotify),
    path("404/", views._404),
]
