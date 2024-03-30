# Generated by Django 5.0.3 on 2024-03-29 09:31

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Author",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("author_id", models.CharField(max_length=13, unique=True)),
                (
                    "email",
                    models.EmailField(
                        max_length=254,
                        unique=True,
                        validators=[
                            django.core.validators.EmailValidator(
                                message="Please enter a valid email address"
                            )
                        ],
                    ),
                ),
                (
                    "password",
                    models.CharField(
                        max_length=128,
                        validators=[
                            django.core.validators.RegexValidator(
                                message="Password must be at least 8 characters with 1 uppercase and 1 lowercase letter",
                                regex="^(?=.*[a-z])(?=.*[A-Z]).{8,}$",
                            )
                        ],
                    ),
                ),
                ("full_name", models.CharField(max_length=255)),
                (
                    "phone",
                    models.CharField(
                        max_length=10,
                        validators=[
                            django.core.validators.RegexValidator(
                                message="Phone number must be 10 digits numeric",
                                regex="^[0-9]{10}$",
                            )
                        ],
                    ),
                ),
                ("address", models.CharField(blank=True, max_length=255)),
                ("city", models.CharField(blank=True, max_length=255)),
                ("state", models.CharField(blank=True, max_length=255)),
                ("country", models.CharField(blank=True, max_length=255)),
                (
                    "pincode",
                    models.CharField(
                        max_length=6,
                        validators=[
                            django.core.validators.RegexValidator(
                                message="Pincode must be 6 digits numeric",
                                regex="^[0-9]{6}$",
                            )
                        ],
                    ),
                ),
            ],
        ),
    ]
