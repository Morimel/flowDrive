from .models import User

def create_user(data):
    """
    Создает нового пользователя.
    """
    user = User.objects.create(**data)
    return user

def update_user(user_id, data):
    """
    Обновляет существующего пользователя.
    """
    try:
        user = User.objects.get(id=user_id)
        for field, value in data.items():
            setattr(user, field, value)
        user.save()
        return user
    except User.DoesNotExist:
        return None
