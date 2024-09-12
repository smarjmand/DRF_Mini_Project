from rest_framework.serializers import ModelSerializer
from .models import Todo
from django.contrib.auth import get_user_model

User = get_user_model()


class TodoSerializer(ModelSerializer):

    class Meta:
        model = Todo
        fields = '__all__'


class UserSerializer(ModelSerializer):
    todos = TodoSerializer(read_only=True, many=True)

    class Meta:
        model = User
        fields = '__all__'
