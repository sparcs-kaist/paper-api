from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework import viewsets
from apps.mails.models import PaperMail
from apps.mails.helpers import MailHelpers
from api.mails.serializers import PaperMailCreateSerializer
from api.common.viewset import ActionAPIViewSet
from paper.common.permissions import IsOwnerOrIsAuthenticatdThenCreateOnlyOrReadOnly


class PaperMailViewSet(viewsets.ModelViewSet, ActionAPIViewSet):
    """
        This viewset automatically provides `list`, `create`, `retrieve`,
        `update` and `destroy` actions.
    """
    serializer_class = PaperMailCreateSerializer
    queryset = PaperMail.objects.all()
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    search_fields = ('sender_address', 'message',)
    # 나중에 검색 결과 순서에 대해 이야기 해보아야 함
    ordering_fields = ('created_time',)
    permission_classes = (IsOwnerOrIsAuthenticatdThenCreateOnlyOrReadOnly,)

    def perform_create(self, serializer):
        paperMail = serializer.save(
            author=self.request.user
        )
        MailHelpers(paperMail).sendMail()
