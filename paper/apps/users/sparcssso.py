import binascii
import requests
import hmac
import time
import os
import urllib
import json


# SPARCS sso v2 Client Version 1.1
# VALID ONLY AFTER
# Made by SPARCS SSO Team

class Client:
    SERVER_DOMAIN = 'https://sparcssso.kaist.ac.kr/'
    BETA_DOMAIN = 'https://ssobeta.sparcs.org/'
    DOMAIN = None

    API_PREFIX = 'api/'
    VERSION_PREFIX = 'v2/'

    URLS = {
        'token_require': 'token/require/',
        'token_info': 'token/info/',
        'logout': 'logout/',
        'unregister': 'unregister/',
        'point': 'point/',
        'notice': 'notice/',
    }

    def __init__(self, client_id, secret_key, is_beta=False, server_addr=''):
        self.DOMAIN = self.BETA_DOMAIN if is_beta else self.SERVER_DOMAIN
        self.DOMAIN = server_addr if server_addr else self.DOMAIN

        BASE_URL = '%s%s%s' % (self.DOMAIN, self.API_PREFIX, self.VERSION_PREFIX)

        tmp_URLS = dict()
        for k in self.URLS:
            tmp_URLS[k] = '%s%s' % (BASE_URL, self.URLS[k])
        self.URLS = tmp_URLS

        self.client_id = client_id
        self.secret_key = secret_key

    def _post_data(self, url, data):
        r = requests.post(url, data, verify=True)

        if r.status_code == 400:
            raise RuntimeError('INVALID_REQUEST')
        elif r.status_code == 403:
            raise RuntimeError('NO_PERMISSION')
        elif r.status_code != 200:
            raise RuntimeError('UNKNOWN_ERROR')

        try:
            return r.json()
        except:
            raise RuntimeError('NOT_JSON_OBJECT')

    def get_login_params(self):
        state = binascii.hexlify(os.urandom(10))
        newstate = json.dumps(state.decode('utf-8'))
        params = {
            'client_id': self.client_id,
            'state': newstate,
        }
        return ['%s?%s' % (self.URLS['token_require'], urllib.parse.urlencode(params)), newstate]

    def get_user_info(self, code):
        timestamp = str(int(time.time()))
        msg = '%s%s' % (code, timestamp)
        sign = hmac.new(str(self.secret_key).encode('utf-8'),
                        msg.encode('utf-8')).hexdigest()

        params = {
            'client_id': self.client_id,
            'code': code,
            'timestamp': timestamp,
            'sign': sign,
        }
        return self._post_data(self.URLS['token_info'], params)

    def get_logout_url(self, sid, redirect_uri):
        timestamp = int(time.time())
        msg = '%s%s%s' % (sid, redirect_uri, timestamp)
        sign = hmac.new(str(self.secret_key).encode('utf-8'),
                        msg.encode('utf-8')).hexdigest()

        params = {
            'client_id': self.client_id,
            'sid': sid,
            'timestamp': timestamp,
            'redirect_uri': redirect_uri,
            'sign': sign,
        }
        return '%s?%s' % (self.URLS['logout'], urllib.parse.urlencode(params))

    def do_unregister(self, sid):
        timestamp = int(time.time())
        msg = '%s%s' % (sid, timestamp)
        sign = hmac.new(str(self.secret_key).encode('utf-8'),
                        msg.encode('utf-8')).hexdigest()

        params = {
            'client_id': self.client_id,
            'sid': sid,
            'timestamp': timestamp,
            'sign': sign,
        }
        return self._post_data(self.URLS['unregister'], params)['success']

    def get_point(self, sid):
        return self.modify_point(sid, 0, '')['point']

    def modify_point(self, sid, delta, message, lower_bound=0):
        timestamp = int(time.time())
        msg = '%s%s%s%s' % (sid, delta, lower_bound, timestamp)
        sign = hmac.new(str(self.secret_key).encode('utf-8'),
                        msg.encode('utf-8')).hexdigest()

        params = {
            'client_id': self.client_id,
            'sid': sid,
            'delta': delta,
            'message': message,
            'lower_bound': lower_bound,
            'timestamp': timestamp,
            'sign': sign,
        }
        return self._post_data(self.URLS['point'], params)

    def get_notice(self, offset=0, limit=3, date_after=0):
        params = {
            'offset': offset,
            'limit': limit,
            'date_after': date_after,
        }
        r = requests.get(self.URLS['notice'], data=params, verify=True)
        return r.json()

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
    #print(sso_profile)
    email = sso_profile['email']
    user_list = ZaboUser.objects.filter(email=email)

    if len(user_list) == 0:
        user = ZaboUser.objects.create_user(email=email, password=email)
        user.first_name = sso_profile['first_name']
        user.last_name = sso_profile['last_name']
        user.gender = sso_profile['gender']
        user.sid = sso_profile['sid']
        #TODO sso유저 닉네임 설정
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
@permission_classes([IsAuthenticated,])
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