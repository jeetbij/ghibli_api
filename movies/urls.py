from movies.views import ListMovies
from django.urls import path

urlpatterns = [
    path("", ListMovies.as_view(), name="movies"),
]
