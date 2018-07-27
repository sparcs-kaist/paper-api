from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
from api.users.views import UserViewSet

paperuser_router = DefaultRouter()

paperuser_router.register(
    prefix=r'users',
    viewset=UserViewSet,
)
