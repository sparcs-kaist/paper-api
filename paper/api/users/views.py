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
from paper.common.permissions import IsOwnerOrIsAuthenticatdThenCreateOnlyOrReadOnly


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = PaperuserSerializer
    queryset = PaperUser.objects.all()
    filter_fields = ("nickName",)

    @action(methods=['get'], detail=False)
    def myInfo(self, request):
        user = request.user
        serializer = self.get_serializer(user)
        return Response(serializer.data)


# front end base url
base_url = "http://ssal.sparcs.org:16140"
# url after login
url_after_login = base_url + "/login/"
# url when get error
url_when_error = base_url + "/error/"
# url after logout
url_after_logout = base_url


def login(request):
    user = request.user
    if user.is_authenticated:
        return redirect(url_after_login)

    login_url, state = sso_client.get_login_params()
    request.session['sso_state'] = state
    return redirect(login_url)


@require_http_methods(['GET'])
def login_callback(request):
    state_before = request.session.get('sso_state', 'default before state')
    state = request.GET.get('state', 'default state')
    if state_before != state:
        return redirect(url_when_error)

    code = request.GET.get('code')
    sso_profile = sso_client.get_user_info(code)
    # print(sso_profile)
    email = sso_profile['email']
    user_list = ZaboUser.objects.filter(email=email)

    if len(user_list) == 0:
        user = ZaboUser.objects.create_user(email=email, password=email)
        user.first_name = sso_profile['first_name']
        user.last_name = sso_profile['last_name']
        user.gender = sso_profile['gender']
        user.sid = sso_profile['sid']
        # TODO sso유저 닉네임 설정
        user.nickName = email[0:15]
        print("user's sid: {sid}".format(sid=user.sid))
        user.save()

        return redirect(url_after_login + email)
    else:
        print("user exists")
        user = user_list[0]
        user.first_name = sso_profile['first_name']
        user.last_name = sso_profile['last_name']
        user.sid = sso_profile['sid']
        user.save()

        return redirect(url_after_login + email)

    return JsonResponse(status=200,
                        data={'error_title': "Login Error",
                              'error_message': "No such that user"})


@api_view(['GET'])
def logout(request):
    print("logout")
    email = request.GET.get('email')
    sid = ZaboUser.objects.get(email=email).sid
    logout_url = sso_client.get_logout_url(sid, url_after_logout)
    return redirect(logout_url)

    if request.user.is_authenticated:
        sid = ZaboUser.objects.get(email=request.GET.get('email')).sid
        logout_url = sso_client.get_logout_url(sid, url_after_logout)
        request.session['visited'] = True
        return redirect(logout_url)
    return redirect(url_after_logout)


@csrf_exempt
@api_view(['POST'])
@permission_classes([IsAuthenticated, ])
def unregister(request):
    if request.method != 'POST':
        return JsonResponse(status=200,
                            data={'error_title': "Unregister Error",
                                  'error_message': "please try again1"})
    zabo_user = ZaboUser.objects.get(email=request.user)

    sid = zabo_user.sid
    result = sso_client.do_unregister(sid)
    if not result:
        return JsonResponse(status=200,
                            data={'error_title': "Unregister Error",
                                  'error_message': "please try again2"})

    zabo_user.delete()
    request.user.delete()

    return JsonResponse(status=200,
                        data={'message': "Unregister successfully"})
