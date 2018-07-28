from rest_framework.routers import DefaultRouter
from api.answers.views import ParticipateViewSet

participate_router = DefaultRouter()

participate_router.register(
    prefix=r'participates',
    viewset=ParticipateViewSet,
)
