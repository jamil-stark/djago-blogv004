import token
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from .models import Profile
from .helper import *
from django.contrib.auth import authenticate, login

from rest_framework import status
from .helper import generate_random_string


class LoginView(APIView):
    def post(self, request):
        try:
            data = request.data
            if data.get("username") is None:
                # status.HTTP_400_BAD_REQUEST = 400 I am using this to show that each status has a value e.g Created = 201, Bad request = 400, Not found = 404, Internal server error = 500, Forbidden = 403, Unauthorized = 401, OK = 200, No content = 204, Conflict = 409, Unprocessable entity = 422, Method not allowed = 405, Gone = 410, Too many requests = 429, Service unavailable = 503, Gateway timeout = 504, Bad gateway = 502, Not implemented = 501, Moved permanently = 301, Moved temporarily = 302, Found = 302, See other = 303, Not modified = 304, Use proxy = 305, Temporary redirect = 307, Permanent redirect = 308
                # You can use the value or the name of the status but I prefer the value since it is more accurate but this is for the sake of understanding and interpretation to the API user in case you are in a team
                return Response(
                    {
                        "status": status.HTTP_400_BAD_REQUEST,
                        "error": "key username not found",
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

            if data.get("password") is None:
                return Response(
                    {
                        "status": status.HTTP_400_BAD_REQUEST,
                        "error": "key password not found",
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

            user = User.objects.filter(username=data.get("username")).first()

            if user is None:
                return Response(
                    {
                        "status": status.HTTP_404_NOT_FOUND,
                        "error": "User not found",
                    },
                    status=status.HTTP_404_NOT_FOUND,
                )

            if not Profile.objects.filter(user=user).first().is_verified:
                return Response(
                    {
                        "status": status.HTTP_403_FORBIDDEN,
                        "error": "Your profile is not verified",
                    },
                    status=status.HTTP_403_FORBIDDEN,
                )

            profile = Profile.objects.filter(user=user).first()
            if profile is None:
                return Response(
                    {
                        "status": status.HTTP_404_NOT_FOUND,
                        "error": "Profile not found",
                    },
                    status=status.HTTP_404_NOT_FOUND,
                )

            if not profile.is_verified:
                return Response(
                    {
                        "status": status.HTTP_403_FORBIDDEN,
                        "error": "Your profile is not verified",
                    },
                    status=status.HTTP_403_FORBIDDEN,
                )
            user_obj = authenticate(
                username=data.get("username"), password=data.get("password")
            )

            if user_obj:
                login(request, user_obj)
                return Response(
                    {
                        "status": status.HTTP_200_OK,
                        "message": "Login successful",
                        "data": {
                            "username": user.username,
                            "email": user.email,
                            "is_active": user.is_active,
                            "is_staff": user.is_staff,
                            "is_superuser": user.is_superuser,
                        },
                        "token": profile.token,
                    },
                    status=status.HTTP_200_OK,
                )
            else:
                return Response(
                    {
                        "status": status.HTTP_401_UNAUTHORIZED,
                        "error": "Invalid credentials",
                    },
                    status=status.HTTP_401_UNAUTHORIZED,
                )
        except Exception as e:
            print(e)
            return Response(
                {
                    "status": status.HTTP_500_INTERNAL_SERVER_ERROR, 
                    "error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


LoginView = LoginView.as_view()


class RegisterView(APIView):
    def post(self, request):
        try:
            data = request.data
            if data.get("username") is None:
                return Response(
                    {
                        "status": status.HTTP_400_BAD_REQUEST,
                        "error": "key username not provided in request",
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

            if data.get("password") is None:
                return Response(
                    {
                        "status": status.HTTP_400_BAD_REQUEST,
                        "error": "key password not provided in request",
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

            if data.get("email") is None:
                return Response(
                    {
                        "status": status.HTTP_400_BAD_REQUEST,
                        "error": "key email not provided in request",
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

            user = User.objects.filter(username=data.get("username")).first()
            if user is not None:
                return Response(
                    {
                        "status": status.HTTP_400_BAD_REQUEST,
                        "error": "username already taken",
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )
            user = User.objects.filter(email=data.get("email")).first()
            if user is not None:
                return Response(
                    {
                        "status": status.HTTP_400_BAD_REQUEST,
                        "error": "email already taken",
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

            user = User.objects.create_user(
                username=data.get("username"),
                email=data.get("email"),
                password=data.get("password"),
            )
            user.save()
            token = generate_random_string(20)
            profile = Profile.objects.create(user=user, token=token)
            profile.save()
            return Response(
                {
                    "status": status.HTTP_201_CREATED,
                    "message": "User created successfully",
                    "data": {
                        "username": user.username,
                        "email": user.email,
                        "is_active": user.is_active,
                        "is_staff": user.is_staff,
                        "is_superuser": user.is_superuser,
                    },
                    "token": token,
                },
                status=status.HTTP_201_CREATED,
            )
        except Exception as e:
            print(e)
            return Response(
                {"message": "something went wrong ", "error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class UserView(APIView):
    def get(self, request):
        try:
            users = User.objects.all()
            response = []
            if users is None:
                return Response(
                    {"message": "No user found"}, status=status.HTTP_404_NOT_FOUND
                )
            for user in users:
                response.append(
                    {
                        "username": user.username,
                        "email": user.email,
                        "is_active": user.is_active,
                        "is_staff": user.is_staff,
                        "is_superuser": user.is_superuser,
                        "password": user.password,
                    }
                )
            return Response(response, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response(
                {"message": "something went wrong ", "error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


RegisterView = RegisterView.as_view()
