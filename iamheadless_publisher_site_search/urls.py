from django.urls import path

from .conf import settings
from .viewsets import SearchViewSet


urlpatterns = [
    path(r'<str:language>/search/', SearchViewSet.as_view(), name=settings.URLNAME_SEARCH),
]
