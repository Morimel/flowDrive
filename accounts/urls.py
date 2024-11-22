from django.urls import path
from .views import RegisterView, LoginView, UserListView, NewsListCreateView, NewsDetailView, UserDetailView

urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('login/', LoginView.as_view()),
    path('users/', UserListView.as_view()),  # Новый маршрут для получения всех пользователей
    path('users/<int:user_id>/', UserListView.as_view()),  # PUT: Обновление пользователя по ID
    path('news/', NewsListCreateView.as_view(), name='news-list-create'),  # GET и POST
    path('news/<int:news_id>/', NewsDetailView.as_view(), name='news-detail'),  # GET, PUT, DELETE
    path('api/user/', UserDetailView.as_view(), name='user-detail'),

]
