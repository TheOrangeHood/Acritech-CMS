from rest_framework import serializers
from .models import Novel, Category


class CategoryDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["name", "id"]


class NovelCreateSerializer(serializers.ModelSerializer):
    categories = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Category.objects.all()
    )

    class Meta:
        model = Novel
        fields = ["title", "body", "summary", "categories", "document"]

    def create(self, validated_data):
        novel_id = Novel.generate_unique_author_id()
        validated_data["novel_id"] = novel_id
        categories = validated_data.pop("categories")
        novel = Novel.objects.create(**validated_data)
        for category in categories:
            novel.categories.add(category)

        novel.save()
        return novel


class NovelDetailSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()
    categories = serializers.SerializerMethodField()

    class Meta:
        model = Novel
        fields = [
            "title",
            "body",
            "summary",
            "novel_id",
            "author",
            "categories",
            "document",
        ]
        read_only_fields = ["novel_id", "author"]

    def get_author(self, instance):
        return instance.author.full_name

    def get_categories(self, instance):
        category_qs = instance.categories.all()
        return CategoryDetailSerializer(category_qs, many=True).data
