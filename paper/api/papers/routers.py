from rest_framework.routers import DefaultRouter
from api.papers.views import PaperViewSet

paper_router = DefaultRouter()

paper_router.register(
    prefix=r'papers',
    viewset=PaperViewSet,
)
