from django.contrib.auth.backends import ModelBackend
from .models import User

class CustomModelBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            User.set_password(password)
        else:
            if self.user_can_authenticate(user):
                return user