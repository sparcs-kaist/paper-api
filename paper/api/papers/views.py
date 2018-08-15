from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.response import Response
from rest_framework import viewsets
from apps.papers.models import Paper, Question, Choice
from api.papers.serializers import PaperSerializer, PaperListSerializer, PaperCreateSerializer
from .admin_serializers import PaperAdminSerializer
from django.shortcuts import get_object_or_404
from rest_framework import permissions
from paper.common.permissions import IsOwnerOrIsAuthenticatdThenCreateOnlyOrReadOnly
from rest_framework import status
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAdminUser
from api.common.viewset import ActionAPIViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from paper.common.permissions import IsOwnerOrIsAuthenticatdThenCreateOnlyOrReadOnly, PaperPermission


class PaperViewSet(viewsets.ModelViewSet, ActionAPIViewSet):
    """
        This viewset automatically provides `list`, `create`, `retrieve`,
        `update` and `destroy` actions.
    """
    serializer_class = PaperSerializer
    queryset = Paper.objects.all()
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    search_fields = ('title', 'content',)
    # 나중에 검색 결과 순서에 대해 이야기 해보아야 함
    ordering_fields = ('created_time',)
    filter_fields = ('author', )


    action_serializer_class = {
        'create': PaperCreateSerializer,
        'list': PaperListSerializer,
        'retrieve': PaperSerializer,
        "update": PaperCreateSerializer,
        "admin": PaperAdminSerializer,
    }
    permission_classes = (PaperPermission, )

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        paper = self.perform_create(serializer)
        response_dict = {'paper': paper.id}
        response_dict.update(serializer.data)
        headers = self.get_success_headers(serializer.data)
        return Response(response_dict, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        paper = serializer.save(
            author=self.request.user
        )
        return paper


    @action(methods=['get'], detail=False)
    def created(self, request):
        if request.user.is_anonymous:
            return Response({'Message': 'You are unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)
        user = request.user
        queryset = Paper.objects.filter(author=user).order_by('updated_time')
        page = self.paginate_queryset(queryset)
        serializer = PaperListSerializer(page, many=True, context={
            'request': request,
        })
        if page is not None:
            return self.get_paginated_response(serializer.data)
        return Response(serializer.data)

    @action(methods=['get'], detail=True)
    def admin(self, request, pk=None):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
