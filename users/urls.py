from django.urls import path
from .views import *

# BASE URL = api/auth/

urlpatterns = [
    path("admin/login", AdminUserLoginView.as_view(), name="admin-login"),
    path("author/login", AuthorUserLoginView.as_view(), name="author-login"),
    path("author/signup", AuthorUserCreateView.as_view(), name="author-signup"),
    # these can be added later
    # path("author/refresh", AuthorUserRefreshTokenView.as_view(), name="author-refresh"),
    # path("admin/refresh", AdminUserRefreshTokenView.as_view(), name="admin-refresh"),
]
