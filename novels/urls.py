from django.urls import path
from .views import *

# BASE URL = api/novels/

urlpatterns = [
    path("", PublicNovelListView.as_view(), name="novels"),
    path("author", AuthorNovelListOrCreateView.as_view(), name="author-novels"),
    path(
        "author/<str:novel_id>",
        AuthorNovelDetailUpdateDeleteView.as_view(),
        name="author-novel-detail",
    ),
    path(
        "admin/<str:novel_id>",
        AdminNovelDetailUpdateDeleteView.as_view(),
        name="author-novel-detail",
    ),
]
