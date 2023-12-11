from django.test import TestCase, RequestFactory
from django.core.cache import cache
from rest_framework import status
from unittest.mock import patch, MagicMock
from services.ghibli_client import GhibliClient, ResourceNotFound
from movies.views import ListMovies

class ListMoviesTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    @patch('services.ghibli_client.GhibliClient.get_movie_by_id')
    @patch('services.ghibli_client.GhibliClient.get_people_by_link')
    def test_get_all_movies_success(self, mock_get_people, mock_get_movies):
        mock_get_movies.return_value = [
            {"id": "1", "title": "Movie 1", "people": ["https://people_url_1"]},
            {"id": "2", "title": "Movie 2", "people": ["https://people_url_1"]}
        ]
        mock_get_people.return_value = {"id": "1", "name": "Actor 1", "species": "species_link_1", "url": "https://people_url_1"}

        request = self.factory.get('/movies/')
        response = ListMovies.as_view()(request)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(cache.get("all_movies"), mock_get_movies.return_value)

    @patch('services.ghibli_client.GhibliClient.get_movie_by_id')
    @patch('services.ghibli_client.GhibliClient.get_people_by_link')
    def test_get_movie_by_id_success(self, mock_get_people, mock_get_movies):
        movie_id = "1"
        mock_get_movies.return_value = [
            {"id": "1", "title": "Movie 1", "people": ["https://people_url_1"]}
        ]
        mock_get_people.return_value = {"id": "1", "name": "Actor 1", "species": "https://species_link_1", "url": "https://people_url_1"}

        request = self.factory.get('/movies/', {'movie_id': movie_id})
        response = ListMovies.as_view()(request)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(cache.get(movie_id), mock_get_movies.return_value)

    @patch('services.ghibli_client.GhibliClient.get_movie_by_id')
    def test_get_movie_by_id_not_found(self, mock_get_movies):
        movie_id = "nonexistent_id"
        mock_get_movies.side_effect = ResourceNotFound("Movie not found")

        request = self.factory.get('/movies/', {'movie_id': movie_id})
        response = ListMovies.as_view()(request)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    @patch('services.ghibli_client.GhibliClient.get_movie_by_id')
    def test_get_movie_by_id_api_failure(self, mock_get_movies):
        movie_id = "1"
        mock_get_movies.side_effect = Exception("API failure")

        request = self.factory.get('/movies/', {'movie_id': movie_id})
        response = ListMovies.as_view()(request)

        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
