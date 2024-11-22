from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.mail import send_mail
from .models import User, News
from .serializers import NewsSerializer, RegisterSerializer, LoginSerializer, UserSerializer
from django.contrib.auth import login
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from .serializers import UserSerializer
import random

random_number = random.randint(1000, 9999)


class NewsListCreateView(APIView):
    """
    Вьюха для получения списка новостей и создания новой новости с изображением.
    """
    def get(self, request):
        news = News.objects.all()
        serializer = NewsSerializer(news, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = NewsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class NewsDetailView(APIView):
    """
    Вьюха для получения, обновления и удаления отдельной новости с изображением.
    """
    def get(self, request, news_id):
        try:
            news = News.objects.get(id=news_id)
        except News.DoesNotExist:
            return Response({"error": "News not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = NewsSerializer(news)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, news_id):
        try:
            news = News.objects.get(id=news_id)
        except News.DoesNotExist:
            return Response({"error": "News not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = NewsSerializer(news, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, news_id):
        try:
            news = News.objects.get(id=news_id)
            news.delete()
            return Response({"message": "News deleted"}, status=status.HTTP_204_NO_CONTENT)
        except News.DoesNotExist:
            return Response({"error": "News not found"}, status=status.HTTP_404_NOT_FOUND)

class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            try:
                user = serializer.save()
                # Отправка письма через SMTP
                send_mail(
                    'Ваш код подтверждения!',
                    f"{str(random_number)}",
                    'sattarzhanovdev@gmail.com',
                    [user.email],
                )
                return Response({'message': 'User registered successfully'}, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def get_tokens_for_user(user):
    """
    Генерация JWT токенов для пользователя.
    """
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            tokens = get_tokens_for_user(user)
            return Response({"tokens": tokens})
        return Response(serializer.errors)
    
class UserListView(APIView):
    """
    Вьюха для работы с пользователями:
    - GET: Получение списка пользователей
    - POST: Создание нового пользователя
    - PUT: Обновление данных пользователя
    """

    def get(self, request):
        """
        Возвращает список всех пользователей.
        """
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, user_id=None):
        """
        Обновляет данные существующего пользователя.
        """
        if not user_id:
            return Response({"error": "User ID is required for PUT requests"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        # Обновляем данные пользователя
        serializer = UserSerializer(user, data=request.data, partial=True)  # partial=True позволяет обновлять только переданные поля
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
class UserDetailView(APIView):
    """
    Эндпоинт для получения информации о текущем пользователе.
    """
    permission_classes = [IsAuthenticated]  # Требуется аутентификация

    def get(self, request):
        user = request.user  # Текущий пользователь определяется из токена
        serializer = UserSerializer(user)
        return Response(serializer.data, status=200)