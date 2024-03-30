from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework.reverse import reverse
from django.contrib.auth.models import User
from .models import Novel
from users.models import Author
from users.authentication import generate_access_token


class NovelCreateTest(APITestCase):
    def setUp(self):
        # Create a user for testing
        author_id = Author.generate_unique_author_id()
        self.author = Author.objects.create(
            email="test_author@gmail.com", password="Author123", author_id=author_id
        )
        self.author.save()

    def get_token(self):
        # Get JWT token for the test user
        token = generate_access_token(self.author).decode()
        return token

    def test_novel_create_view(self):
        # Authenticate the request with JWT token
        token = self.get_token()
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + token)

        # Create a novel
        data = {
            "title": "Test Novel",
            "body": "Test Body",
            "summary": "Test Summary",
            "categories": [],
        }
        response = self.client.post(reverse("author-novels"), data)

        # Check response status code and data
        self.assertEqual(response.data["status"], "success")
        self.assertEqual(response.data["payload"]["title"], "Test Novel")


class AuthorNovelReadUpdataDeleteTest(APITestCase):
    def setUp(self):
        # Create a user for testing
        author_id = Author.generate_unique_author_id()
        self.author = Author.objects.create(
            email="test2_author@gmail.com", password="Author123", author_id=author_id
        )
        novel_id = Novel.generate_unique_author_id()
        self.novel = Novel.objects.create(
            novel_id=novel_id,
            title="Test title",
            body="Test Body",
            summary="Test Summary",
            author=self.author,
        )

    def get_token(self):
        # Get JWT token for the test user
        token = generate_access_token(self.author).decode()
        return token

    def test_novel_read_view(self):
        # Authenticate the request with JWT token
        token = self.get_token()
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + token)

        # Read the novel
        response = self.client.get(
            reverse("author-novel-detail", kwargs={"novel_id": self.novel.novel_id})
        )

        self.assertEqual(response.data["status"], "success")
        self.assertEqual(response.data["payload"]["title"], "Test title")

    def test_novel_update_view(self):
        token = self.get_token()
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + token)

        data = {"title": "New Test Title"}

        # update the title
        response = self.client.patch(
            reverse("author-novel-detail", kwargs={"novel_id": self.novel.novel_id}),
            data,
        )
        self.assertEqual(response.data["status"], "success")
        self.assertEqual(response.data["payload"]["title"], "New Test Title")

    def test_novel_delete_view(self):
        token = self.get_token()
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + token)

        response = self.client.delete(
            reverse("author-novel-detail", kwargs={"novel_id": self.novel.novel_id})
        )
        count = Novel.objects.count()
        self.assertEqual(response.data["status"], "success")
        self.assertEqual(count, 0)
