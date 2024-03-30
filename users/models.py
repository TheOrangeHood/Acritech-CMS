from django.db import models
from django.core.validators import RegexValidator, EmailValidator
from .utils import random_alphanumeric_generator

# Create your models here.


class TOKEN_TYPE(models.TextChoices):
    ACCESS = ("access",)
    REFRESH = "refresh"


class Author(models.Model):
    author_id = models.CharField(max_length=13, unique=True)
    email = models.EmailField(
        unique=True,
        validators=[EmailValidator(message="Please enter a valid email address")],
    )
    password = models.CharField(
        max_length=128,
        validators=[
            RegexValidator(
                regex="^(?=.*[a-z])(?=.*[A-Z]).{8,}$",
                message="Password must be at least 8 characters with 1 uppercase and 1 lowercase letter",
            )
        ],
    )
    full_name = models.CharField(max_length=255)
    phone = models.CharField(
        max_length=10,
        validators=[
            RegexValidator(
                regex="^[0-9]{10}$", message="Phone number must be 10 digits numeric"
            )
        ],
    )
    address = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=255, blank=True)
    state = models.CharField(max_length=255, blank=True)
    country = models.CharField(max_length=255, blank=True)
    pincode = models.CharField(
        max_length=6,
        validators=[
            RegexValidator(
                regex="^[0-9]{6}$", message="Pincode must be 6 digits numeric"
            )
        ],
    )

    def __str__(self) -> str:
        return self.full_name

    @classmethod
    def generate_unique_author_id(cls):
        author_id = "author_" + random_alphanumeric_generator()
        while cls.objects.filter(author_id=author_id).exists():
            return cls.generate_unique_option_id()
        return author_id
