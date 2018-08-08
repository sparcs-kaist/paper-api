from django.conf.urls import include, url
from django.urls import path, re_path
from rest_framework_swagger.views import get_swagger_view
from api.users.routers import paperuser_router
from api.papers.routers import paper_router
from api.answers.routers import participate_router
from api.mails.routers import mail_router

swagger_view = get_swagger_view(title="Pastebian API")
urlpatterns = (

    url(r'^api/', include(paperuser_router.urls)),
    url(r'^api/', include(paper_router.urls)),
    url(r'^api/', include(participate_router.urls)),
    url(r'^api/', include(mail_router.urls)),

    url(r'^api/login/$', views.login),
    url(r'^api/login/callback/$', views.login_callback),
    url(r'^api/logout/$', views.logout),
    url(r'^api/unregister/$', views.unregister),

    url(r'^swagger/$', swagger_view),
)
