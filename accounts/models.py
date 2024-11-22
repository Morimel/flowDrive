from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

class UserManager(BaseUserManager):
    def create_user(self, phone, email, name, password=None):
        if not phone or not email:
            raise ValueError("Phone and email are required")
        user = self.model(phone=phone, email=self.normalize_email(email), name=name)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone, email, name, password):
        user = self.create_user(phone, email, name, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser, PermissionsMixin):
    phone = models.CharField(max_length=15, unique=True)
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=50)
    bonus = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = ['email', 'name']

    def __str__(self):
        return self.phone

class News(models.Model):
    title = models.CharField(max_length=255)  # Заголовок новости
    content = models.TextField()             # Содержание новости
    image = models.ImageField(upload_to='news_images/', null=True, blank=True)  # Изображение
    created_at = models.DateTimeField(auto_now_add=True)  # Дата создания
    updated_at = models.DateTimeField(auto_now=True)      # Дата последнего обновления

    def __str__(self):
        return self.title