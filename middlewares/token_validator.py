from rest_framework import status
from django.http import JsonResponse

class TokenValidation:

    GHIBLI_KEY = 'THIS_IS_GHIBLI_TOKEN'

    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        
        headers = request.headers
        token = headers.get('ghiblikey', None)
        
        if token != self.GHIBLI_KEY:
            return JsonResponse({
                "error": "Token is expired or not valid."
            }, safe=False, status=status.HTTP_403_FORBIDDEN)
        
        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response
