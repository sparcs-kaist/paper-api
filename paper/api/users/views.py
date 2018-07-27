from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import RetrieveAPIView
from api.users.serializers import PaperuserSerializer
from apps.papers.models import PaperUser

class UserViewSet(viewsets.ModelViewSet):

    serializer_class = PaperuserSerializer
    queryset = PaperUser.objects.all()
    filter_fields = ("nickName")