from django.conf.urls import include, url
from django.urls import path, re_path
from rest_framework_swagger.views import get_swagger_view
from api.users.routers import paperuser_router
from api.papers.routers import paper_router
from api.answers.routers import participate_router

swagger_view = get_swagger_view(title="Pastebian API")
urlpatterns = (

    url(r'^api/', include(paperuser_router.urls)),
    url(r'^api/', include(paper_router.urls)),
    url(r'^api/', include(participate_router.urls)),

    url(r'^swagger/$', swagger_view),

)
