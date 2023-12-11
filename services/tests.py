import unittest
from unittest.mock import patch, MagicMock
from services.ghibli_client import GhibliClient, ResourceNotFound, APIRequestFailed

class TestGhibliClient(unittest.TestCase):
    @patch('requests.get')
    def test_get_movie_by_id_success(self, mock_get):
        movie_id = 'some_movie_id'
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = '{"title": "Movie Title"}'
        mock_get.return_value = mock_response

        ghibli_client = GhibliClient()
        result = ghibli_client.get_movie_by_id(movie_id)

        self.assertEqual(result, {"title": "Movie Title"})

    @patch('requests.get')
    def test_get_movie_by_id_not_found(self, mock_get):
        movie_id = 'nonexistent_movie_id'
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response

        ghibli_client = GhibliClient()

        with self.assertRaises(ResourceNotFound):
            ghibli_client.get_movie_by_id(movie_id)

    @patch('requests.get')
    def test_get_movie_by_id_api_failure(self, mock_get):
        movie_id = 'some_movie_id'
        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_get.return_value = mock_response

        ghibli_client = GhibliClient()

        with self.assertRaises(APIRequestFailed):
            ghibli_client.get_movie_by_id(movie_id)

    @patch('requests.get')
    def test_get_people_by_link_success(self, mock_get):
        link = 'some_people_link'
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = '[{"name": "Person Name"}]'
        mock_get.return_value = mock_response

        ghibli_client = GhibliClient()
        result = ghibli_client.get_people_by_link(link)

        self.assertEqual(result, {"name": "Person Name"})

    @patch('requests.get')
    def test_get_people_by_link_not_found(self, mock_get):
        link = 'nonexistent_people_link'
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response

        ghibli_client = GhibliClient()

        with self.assertRaises(ResourceNotFound):
            ghibli_client.get_people_by_link(link)

    @patch('requests.get')
    def test_get_people_by_link_api_failure(self, mock_get):
        link = 'some_people_link'
        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_get.return_value = mock_response

        ghibli_client = GhibliClient()

        with self.assertRaises(APIRequestFailed):
            ghibli_client.get_people_by_link(link)

if __name__ == '__main__':
    unittest.main()
