from django.shortcuts import render
from .models import Author
from rest_framework.views import APIView
from .serializers import (
    AuthorUserLoginSerializer,
    AdminUserLoginSerializer,
    AuthorUserCreateSerializer,
)
from common.exceptions import (
    AuthorUserNotFoundException,
    UserWithEmailAlreadyExistsException,
    UserWithPhoneAlreadyExistsException,
)
from common.utils import custom_fail_response, custom_success_response
from django.contrib.auth import authenticate
from django.contrib.auth.models import update_last_login
from rest_framework_simplejwt.tokens import RefreshToken


from .authentication import (
    generate_access_token,
    generate_refresh_token,
)

# Create your views here.


class AuthorUserLoginView(APIView):
    def post(self, request):
        serializer = AuthorUserLoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=False):
            data = serializer.validated_data
            email = data["email"]
            password = data["password"]
            try:
                author = Author.objects.get(email=email)
                if author.password == password:
                    access_token = generate_access_token(author)
                    refresh_token = generate_refresh_token(author)

                    response = {
                        "access": access_token,
                        "refresh": refresh_token,
                    }

                    return custom_success_response(response)
            except Author.DoesNotExist:
                raise AuthorUserNotFoundException
        else:
            return custom_fail_response(serializer.errors)


class AuthorUserLogoutView(APIView):
    def post(self, request):
        pass


class AuthorUserRefreshTokenView(APIView):
    def post(self, request):
        pass


class AuthorUserCreateView(APIView):
    def validate_if_user_exists(self, email, phone):
        if Author.objects.filter(email=email).exists():
            raise UserWithEmailAlreadyExistsException

        if Author.objects.filter(phone=phone).exists():
            raise UserWithPhoneAlreadyExistsException

    def post(self, request):
        serializer = AuthorUserCreateSerializer(data=request.data)
        if serializer.is_valid(raise_exception=False):
            data = serializer.validated_data
            email = data["email"]
            phone = data["phone"]
            self.validate_if_user_exists(email, phone)
            serializer.save()
            return custom_success_response(serializer.data)
        else:
            return custom_fail_response(serializer.errors)


class AdminUserLoginView(APIView):
    def post(self, request):
        serializer = AdminUserLoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=False):
            data = serializer.validated_data
            username = data["username"]
            password = data["password"]
            user = authenticate(username=username, password=password)

            if user is not None:
                tokens = get_tokens_for_user(user)
                update_last_login(None, user)
                payload = {
                    "username": user.username,
                    "access": tokens["access"],
                    "refresh": tokens["refresh"],
                }
                return custom_success_response(payload)
            else:
                return custom_fail_response("Invalid credentials")
        else:
            return custom_fail_response(serializer.errors)


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        "refresh": str(refresh),
        "access": str(refresh.access_token),
    }


class AdminUserLogoutView(APIView):
    def post(self, request):
        pass


class AdminUserRefreshTokenView(APIView):
    def post(self, request):
        pass
