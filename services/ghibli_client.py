import requests
import json
from rest_framework.exceptions import APIException

class APIRequestFailed(Exception):
    def __init__(self, message):
        self.message = message          
        super().__init__(message)
    
class ResourceNotFound(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(message)

class GhibliClient:
    def __init__(self):
        self.url = "https://ghibli.rest"

    def movie_url(self):
        return f"{self.url}/films"

    def get_movie_by_id(self, movie_id):
        try:
            params = { "id": movie_id }
            print(f"Making a API call to get movies detail with url - {self.movie_url()} and params - {params}")
            response = requests.get(self.movie_url(), params)
            
            if response.status_code == 200:
                data = json.loads(response.text)
                return data
            elif response.status_code == 404:
                raise ResourceNotFound("Movie with given id not found")
            else:
                raise APIRequestFailed("Somethig went wrong, try again!")
        except Exception as error:
            print(f"API request failed with error --> {error}")
            raise error

    def get_people_by_link(self, link):
        try:
            print(f"Making a API call to get people detail with url - {link}")
            response = requests.get(link, {})
            
            if response.status_code == 200:
                data = json.loads(response.text)
                return data[0]
            elif response.status_code == 404:
                raise ResourceNotFound("People with given id not found")
            else:
                raise APIRequestFailed("Somethig went wrong, try again!")
        except Exception as error:
            print("API request failed with error --> ", error)
            raise error
