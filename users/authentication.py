import jwt
from django.conf import settings
from datetime import datetime, timedelta
from users.models import Author, TOKEN_TYPE
from common import exceptions


class ValidateJwtToken:
    def validate_jwt_from_headers(self, request, _token_type: TOKEN_TYPE) -> Author:
        if "Authorization" in request.headers:
            auth_header = request.headers["Authorization"]

            # Check if the header has the correct format
            if auth_header.startswith("Bearer "):
                token = auth_header.split(" ")[1]

                # Validate the JWT token and return user object
                author = self.validate_jwt(self, token, _token_type)
                return author

            else:
                raise exceptions.InvalidAuthorizationHeaderFormatException
        else:
            raise exceptions.AuthorizationHeaderMissingException

    def validate_jwt(self, token: str, _token_type: TOKEN_TYPE) -> Author:
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            author_id = payload["user_id"]
            token_type = payload["token_type"]

            if token_type != _token_type:
                raise exceptions.InvalidTokenTypeException

            author = Author.objects.get(author_id=author_id)
            return author

        except jwt.ExpiredSignatureError:
            raise exceptions.TokenExpiredException
        except jwt.InvalidTokenError:
            raise exceptions.InvalidTokenException
        except Author.DoesNotExist:
            raise exceptions.AuthorUserNotFoundException


def generate_access_token(author: Author):
    access_token_payload = {
        "user_id": author.author_id,
        "token_type": TOKEN_TYPE.ACCESS,
        "exp": datetime.utcnow() + timedelta(minutes=30),
        "iat": datetime.utcnow(),
    }

    access_token = jwt.encode(
        access_token_payload, settings.SECRET_KEY, algorithm="HS256"
    )
    return access_token


def generate_refresh_token(author: Author):
    refresh_token_payload = {
        "user_id": author.author_id,
        "token_type": TOKEN_TYPE.REFRESH,
        "exp": datetime.utcnow() + timedelta(minutes=30),
        "iat": datetime.utcnow(),
    }

    refresh_token = jwt.encode(
        refresh_token_payload, settings.SECRET_KEY, algorithm="HS256"
    )
    return refresh_token
