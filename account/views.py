from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from .serializers import UserSignUpSerializer, UserLoginSerializer
from .  import messages
from .import utils

# Create your views here.


User = get_user_model()



class RegisterUserAPIView(APIView):

    def post(self, request, *args, **kwargs):
        """
        Data to be sent:
        ```
        {
            "username": String,
            "email": String,
            "first_name": String,
            "password": String
        }
        ```
        #### Response:
        __Success__
        Status: 201

        ```
        {
            "detail": "User has been successfully registered."
        }
        ```

        """
        data = request.data.copy()
        user_serializer = UserSignUpSerializer(data=data)

        if user_serializer.is_valid():
            data = user_serializer.data
            user = User(username=data['username'],
                        email=data['email'],
                        first_name=data['first_name'])
            user.set_password(data['password'])
            user.save()
            return Response(messages.USER_CREATED, status=status.HTTP_201_CREATED)
        else:
            return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class UserLoginAPIView(APIView):

    def post(self, request, *args, **kwargs):
        """
        Data to be sent:
        ```
        {
            "username": String,
            "password": String
        }
        ```
        #### Response:
        __Success__
        Status: 200

        ```
        {
            "id": Integer,
            "username": String,
            "email": String,
            "token": String
        }
        ```

        __Invalid login:__ status: 401
        ```
        {
            "detail": "Invalid login credentials."
        }
        ```

        __User not active:__ status: 400
        ```
        {
            "detail": "Please verify your email id first."
        }
        ```

        __Other error:__ status:400
        """

        data = request.data.copy()

        try:
            username = data["username"]
            password = data["password"]
        except:
            return Response(messages.NO_USERNAME_PASSWORD, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                token = utils.generate_token(user)
                login_serializer = UserLoginSerializer(user, data=data)
                if login_serializer.is_valid():
                    keys = ["id", "username", "email"]
                    response_dict = {k:v for k,v in list(login_serializer.data.items()) if k in keys}
                    response_dict["token"] = token
                    return Response(response_dict, status=status.HTTP_200_OK)
                else:
                    return Response(login_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response(messages.USER_NOT_ACTIVE, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(messages.INVALID_LOGIN, status=status.HTTP_401_UNAUTHORIZED)



class UserLogoutAPIView(APIView):

    def get(self, request, *args, **kwargs):
        """
        #### Header:
        ```
        {
            "Authorization" : "Token String",
        }
        ```

        #### Response:
        __Success:__ status: 200
        ```
        {
            "detail": "User is successfully logged out."
        }
        ```

        __Error:__ status: 400
        ```
        {
            "detail" : "Some error has occured"
        }
        ```
        """
        try:
            if request.auth.user_id:
                utils.logout_user(request.auth.user_id)
                return Response(messages.LOGOUT_SUCCESSFUL, status=status.HTTP_200_OK)
        except:
            return Response(messages.ERROR, status=status.HTTP_400_BAD_REQUEST)
