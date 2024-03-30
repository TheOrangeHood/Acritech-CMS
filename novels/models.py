from django.db import models
from users.models import Author  # Import the Author model
from users.utils import random_alphanumeric_generator


class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Novel(models.Model):
    novel_id = models.CharField(max_length=13, unique=True)
    title = models.CharField(max_length=30)
    body = models.TextField(max_length=300)
    summary = models.CharField(max_length=60)
    document = models.FileField(
        upload_to="novels/", help_text="Upload PDF document", blank=True, null=True
    )
    categories = models.ManyToManyField(Category)
    author = models.ForeignKey(
        Author, on_delete=models.CASCADE, related_name="novels"
    )  # Foreign key relationship to Author model

    def __str__(self):
        return self.title

    @classmethod
    def generate_unique_author_id(cls):
        novel_id = "novel_" + random_alphanumeric_generator()
        while cls.objects.filter(novel_id=novel_id).exists():
            return cls.generate_unique_option_id()
        return novel_id
