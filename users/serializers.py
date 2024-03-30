from rest_framework import serializers
from .models import Author


class AuthorUserLoginSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField()


class AdminUserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()


class AuthorUserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = [
            "email",
            "password",
            "full_name",
            "phone",
            "address",
            "city",
            "state",
            "country",
            "pincode",
        ]

    def create(self, validated_data):
        validated_data["author_id"] = Author.generate_unique_author_id()
        return Author.objects.create(**validated_data)
