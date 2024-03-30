from django.shortcuts import render
from users.authentication import ValidateJwtToken
from rest_framework.views import APIView
from users.models import TOKEN_TYPE
from .serializers import NovelCreateSerializer, NovelDetailSerializer
from common.utils import custom_fail_response, custom_success_response
from .models import Novel
from common.exceptions import NovelNotFoundException
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.db.models import Q


# Create your views here.
class AuthorNovelListOrCreateView(APIView):
    def get(self, request):
        """
        A function to retrieve novels belonging to the authenticated author and serialize them.

        Returns:
            A custom success response containing serialized data of the novels.
        """
        author = ValidateJwtToken.validate_jwt_from_headers(
            ValidateJwtToken, request, TOKEN_TYPE.ACCESS
        )
        novels = author.novels.all()
        serializer = NovelDetailSerializer(novels, many=True)
        return custom_success_response(serializer.data)

    def post(self, request):
        """
        Handles the POST request to create a new novel. Validates the JWT token from the request headers,
        then creates a new novel using the provided data. Returns a success response with the novel data if
        the serializer is valid, otherwise returns a fail response with the serializer errors.
        """
        author = ValidateJwtToken.validate_jwt_from_headers(
            ValidateJwtToken, request, TOKEN_TYPE.ACCESS
        )
        serializer = NovelCreateSerializer(data=request.data)
        if serializer.is_valid(raise_exception=False):
            serializer.validated_data["author"] = author
            novel = serializer.save()
            novel_data = NovelDetailSerializer(novel).data
            return custom_success_response(novel_data)
        else:
            return custom_fail_response(serializer.errors)


class AuthorNovelDetailUpdateDeleteView(APIView):
    def get(self, request, novel_id):
        """
        Get the novel details for the given novel_id.

        Parameters:
            request: The request object.
            novel_id: The ID of the novel.

        Returns:
            If the novel is found, returns the serialized novel details.
            If the novel is not found, returns a custom fail response.
        """
        author = ValidateJwtToken.validate_jwt_from_headers(
            ValidateJwtToken, request, TOKEN_TYPE.ACCESS
        )
        try:
            novel = author.novels.get(novel_id=novel_id, author=author)
            serializer = NovelDetailSerializer(novel)
            return custom_success_response(serializer.data)
        except Novel.DoesNotExist:
            return NovelNotFoundException

    def patch(self, request, novel_id):
        author = ValidateJwtToken.validate_jwt_from_headers(
            ValidateJwtToken, request, TOKEN_TYPE.ACCESS
        )
        try:
            novel = author.novels.get(novel_id=novel_id, author=author)
            serializer = NovelDetailSerializer(novel, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return custom_success_response(serializer.data)
            else:
                return custom_fail_response(serializer.errors)
        except Novel.DoesNotExist:
            raise NovelNotFoundException

    def delete(self, request, novel_id):
        author = ValidateJwtToken.validate_jwt_from_headers(
            ValidateJwtToken, request, TOKEN_TYPE.ACCESS
        )
        try:
            novel = author.novels.get(novel_id=novel_id, author=author)
            novel.delete()
            return custom_success_response("Novel deleted successfully")
        except Novel.DoesNotExist:
            raise NovelNotFoundException


class AdminNovelDetailUpdateDeleteView(APIView):
    permission_classes = (IsAuthenticated, IsAdminUser)
    authentication_classes = (JWTAuthentication,)

    def get(self, request, novel_id):
        try:
            novel = Novel.objects.get(novel_id=novel_id)
            serializer = NovelDetailSerializer(novel)
            return custom_success_response(serializer.data)
        except Novel.DoesNotExist:
            return NovelNotFoundException

    def patch(self, request, novel_id):
        try:
            novel = Novel.objects.get(novel_id=novel_id)
            serializer = NovelDetailSerializer(novel, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return custom_success_response(serializer.data)
            else:
                return custom_fail_response(serializer.errors)
        except Novel.DoesNotExist:
            raise NovelNotFoundException

    def delete(self, request, novel_id):
        try:
            novel = Novel.objects.get(novel_id=novel_id)
            novel.delete()
            return custom_success_response("Novel deleted successfully")
        except Novel.DoesNotExist:
            raise NovelNotFoundException


class PublicNovelListView(APIView):
    def get(self, request):
        """
        Retrieves novels based on a search query parameter in the request and serializes them using NovelDetailSerializer.

        Parameters:
        - request: Request object containing query parameters

        Returns:
        - Response containing serialized novel data
        """
        search_query = request.query_params.get("search", None)
        novels = Novel.objects.all()
        if search_query:
            novels = novels.filter(
                Q(title__icontains=search_query)
                | Q(summary__icontains=search_query)
                | Q(body__icontains=search_query)
                | Q(categories__name__icontains=search_query)
            )
        serializer = NovelDetailSerializer(novels, many=True)
        return custom_success_response(serializer.data)
