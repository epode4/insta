from django.contrib.auth.forms import UserCreationForm
from .models import User
from django.contrib.auth import get_user_model

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        # model = User
        model = get_user_model()
        fields = ('username', 'profile_image',)