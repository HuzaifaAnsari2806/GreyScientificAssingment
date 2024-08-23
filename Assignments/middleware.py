import requests
from django.conf import settings
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework_jwt.utils import jwt_decode_handler

class Auth0JSONWebTokenAuthentication(JSONWebTokenAuthentication):
    def authenticate(self, request):
        auth = request.headers.get('Authorization', None)
        if not auth:
            return None

        parts = auth.split()
        if parts[0].lower() != 'bearer':
            return None
        elif len(parts) == 1:
            raise ValueError('Authorization header must be in the format: Bearer <token>')
        elif len(parts) > 2:
            raise ValueError('Authorization header must be in the format: Bearer <token>')

        token = parts[1]
        return self.authenticate_credentials(token)

    def authenticate_credentials(self, token):
        try:
            decoded_token = jwt_decode_handler(token)
            user_info = self.get_user_info(decoded_token)
            return (user_info, token)
        except Exception as e:
            raise ValueError('Invalid token.')

    def get_user_info(self, decoded_token):
        user_info_url = f'https://{settings.AUTH0_DOMAIN}/userinfo'
        headers = {
            'Authorization': f'Bearer {decoded_token["access_token"]}',
        }
        response = requests.get(user_info_url, headers=headers)
        response.raise_for_status()
        return response.json()
