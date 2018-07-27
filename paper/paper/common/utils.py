from api.users.serializers import PaperuserSerializer


def jwt_response_payload_handler(token, user=None, request=None):
    return {
        'token': token,
        'user': PaperuserSerializer(user, context={'request': request}).data
    }