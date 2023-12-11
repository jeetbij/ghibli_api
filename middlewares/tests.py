from django.test import TestCase
from django.http import JsonResponse
from django.test.client import RequestFactory
from rest_framework import status
from middlewares.token_validator import TokenValidation

class TokenValidationMiddlewareTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_valid_token(self):
        middleware = TokenValidation(get_response=lambda x: JsonResponse({}))
        request = self.factory.get('/movies/', HTTP_GHIBLIKEY='THIS_IS_GHIBLI_TOKEN')

        response = middleware(request)

        self.assertEqual(response.status_code, 200)

    def test_invalid_token(self):
        middleware = TokenValidation(get_response=lambda x: JsonResponse({}))
        request = self.factory.get('/movies/', HTTP_GHIBLIKEY='INVALID_TOKEN')

        response = middleware(request)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_missing_token(self):
        middleware = TokenValidation(get_response=lambda x: JsonResponse({}))
        request = self.factory.get('/movies/')

        response = middleware(request)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
