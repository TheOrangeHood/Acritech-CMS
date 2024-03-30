from rest_framework import status
from django.utils.translation import gettext_lazy as _
from rest_framework.exceptions import APIException


class AdminUserNotFoundException(APIException):
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = _("User not found")
    default_code = "user_not_found"


class AuthorUserNotFoundException(APIException):
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = _("User not found")
    default_code = "user_not_found"


class InvalidTokenTypeException(APIException):
    status_code = status.HTTP_401_UNAUTHORIZED
    default_detail = _("Inavlid token type")
    default_code = "invalid_token_type"


class TokenExpiredException(APIException):
    status_code = status.HTTP_401_UNAUTHORIZED
    default_detail = _("Token expired")
    default_code = "token_expired"


class InvalidTokenException(APIException):
    status_code = status.HTTP_401_UNAUTHORIZED
    default_detail = _("Invalid Token")
    default_code = "invalid_token"


class InvalidTokenException(APIException):
    status_code = status.HTTP_401_UNAUTHORIZED
    default_detail = _("Invalid Token")
    default_code = "invalid_token"


class InvalidAuthorizationHeaderFormatException(APIException):
    status_code = status.HTTP_401_UNAUTHORIZED
    default_detail = _("Invalid authorization header format")
    default_code = "invalid_header_format"


class AuthorizationHeaderMissingException(APIException):
    status_code = status.HTTP_401_UNAUTHORIZED
    default_detail = _("Authorization header missing")
    default_code = "auth_header_missing"


class UserWithEmailAlreadyExistsException(APIException):
    status_code = status.HTTP_409_CONFLICT
    default_detail = _("User with email exists")
    default_code = "user_exists"


class UserWithPhoneAlreadyExistsException(APIException):
    status_code = status.HTTP_409_CONFLICT
    default_detail = _("User with phone exists")
    default_code = "user_exists"


class NovelNotFoundException(APIException):
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = _("Novel not found")
    default_code = "novel_not_found"
