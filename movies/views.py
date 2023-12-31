from rest_framework.views import APIView
from rest_framework import status
from django.core.cache import cache
from django.http import JsonResponse
from services.ghibli_client import ResourceNotFound
from movies.utils import get_movie_by_id


class ListMovies(APIView):
    # View to list all movies in the system.
    
    def get(self, request, format=None):
        """
        Return a list of all movies or a given movie id.
        """
        params = request.GET
        movie_id = params.get('movie_id', None)
        try:
            cache_key = movie_id if movie_id else "all_movies"
            
            if cache.get(cache_key, None):
                movies = cache.get(cache_key)
            else:
                movies = get_movie_by_id(movie_id)
                cache.add(cache_key, movies, timeout=60)

            return JsonResponse({
                "movies": movies
                }, safe=True, status=status.HTTP_200_OK
            )
        except ResourceNotFound as e:
            return JsonResponse({
                "message": "Movie with given id not found"
            }, safe=True, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return JsonResponse({
                "message": "Something went wrong, try again."
            }, safe=True, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
