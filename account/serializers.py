from rest_framework import serializers

from django.contrib.auth import get_user_model


User = get_user_model()


class UserSignUpSerializer(serializers.ModelSerializer):

    class Meta():
        model = User
        fields = ["username", "email", "first_name", "password"]


class UserLoginSerializer(serializers.ModelSerializer):

    class Meta():
        model = User
        fields = ["id", "username", "email", "password"]
