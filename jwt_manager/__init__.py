from typing import Tuple, Optional
import jwt
from django.http import HttpRequest
from django.conf import settings
from django.db.models import Model
from rest_framework import status, exceptions


class AuthException(exceptions.APIException):
    def __init__(self, status_code=500, detail=None):
        self.status_code = status_code
        super().__init__(detail)


class JWTAuthentication:

    def authenticate(self, request: HttpRequest) -> Optional[Tuple[Model, None]]:
        jwt_access_token = request.META.get('HTTP_AUTHORIZATION', None)

        if jwt_access_token and jwt_access_token.startswith('Bearer '):
            jwt_access_token = jwt_access_token.split('Bearer ')[1]

        if not jwt_access_token:
            raise AuthException(status_code=status.HTTP_401_UNAUTHORIZED, detail={"Error": "JWT missing"})

        try:
            token_payload = jwt.decode(jwt_access_token, settings.JWT_KEY, algorithms=['HS256'])
        except jwt.exceptions.PyJWTError as error:
            raise AuthException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f'{error}')

        username = token_payload.get("username")
        password = token_payload.get("password")

        if not username:
            raise AuthException(status_code=status.HTTP_401_UNAUTHORIZED, detail={"Missing username"})
        from .models import JWTUser
        return JWTUser(username, password), None