import os
import asyncio
import httpx
import logging

from django.contrib.auth.models import User
from django.db import IntegrityError
from dotenv import load_dotenv
from rest_framework.generics import GenericAPIView, CreateAPIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.response import Response
from rest_framework import status, serializers
from rest_framework.permissions import AllowAny, IsAuthenticated


"""Логирование"""

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


"""Ссылки на endpoints приложения на FastAPI"""

load_dotenv()
fastapi_upload = os.getenv("FASTAPI_UPLOAD_URL")
fastapi_delete = os.getenv("FASTAPI_DELETE_URL")
fastapi_analyse = os.getenv("FASTAPI_ANALYSE_URL")
fastapi_get_text = os.getenv("FASTAPI_GET_TEXT_URL")


"""Формирование токенов access и refresh"""

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        logger.info(f'Token issued for user: {user.username}, Access token: {token}')

        return token

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

class CustomTokenRefreshView(TokenRefreshView):
    pass

# Проверка выдачи токенов
class AuthView(GenericAPIView):
    def get(self, request, **kwargs):

        return Response({'success': "True"})


"""Прокси на FastAPI"""

class UploadDocumentView(GenericAPIView):
    """Прокси на загрузку документа"""
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        file = request.FILES.get("file")
        logger.info(f"Document found: {file}, {file.content_type}, {file.size}")

        files = {"file": (file.name, file, file.content_type)}
        logger.info(files)

        async def upload():
            async with httpx.AsyncClient() as client:
                response = await client.post(fastapi_upload, files=files, timeout=5.0)
                logger.info(f"Response status: {response.status_code}, {response.json()}, {response.headers}")
                return response.json()
        response = asyncio.run(upload())
        return Response(response)


class DeleteDocumentView(GenericAPIView):
    """Прокси на удаление документа"""
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def delete(self, request, doc_id):
        logger.info(doc_id)

        async def delete():
            async with httpx.AsyncClient() as client:
                response = await client.delete(f"{fastapi_delete}/{doc_id}", timeout=5.0)
                logger.info(f"Response status: {response.status_code}, {response.json()}")
                return response.json()
        response = asyncio.run(delete())
        return Response(response)


class AnalyseDocumentView(GenericAPIView):
    """Прокси на выполнение анализа документа"""
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, doc_id):
        logger.info(doc_id)

        async def analyse():
            async with httpx.AsyncClient() as client:
                response = await client.post(f"{fastapi_analyse}/{doc_id}", timeout=5.0)
                logger.info(f"Response status: {response.status_code}, {response.json()}")
                return response.json()
        response = asyncio.run(analyse())
        return Response(response)


class GetTextDocumentView(GenericAPIView):
    """Прокси на получение текста документа"""
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, doc_id):
        logger.info(doc_id)

        async def get_text():
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{fastapi_get_text}/{doc_id}", timeout=5.0)
                logger.info(f"Response status: {response.status_code}, {response.json()}")
                return response.json()
        response = asyncio.run(get_text())
        return Response(response)


"""Сохранение новых пользователей в БД"""

class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "password"]
        extra_kwargs = {
            "password": {"write_only": True}
        }

    def create(self, validated_data):
        try:
            user = User.objects.get(username=validated_data["username"])
            raise serializers.ValidationError("Пользователь с таким именем уже существует")
        except User.DoesNotExist:
            user = User(username=validated_data["username"])
            user.set_password(validated_data["password"])
            user.save()
            return user


class UserRegistrationView(CreateAPIView):
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            try:
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except IntegrityError:
                return Response({"error": "Произошла ошибка при создании пользователя"}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
