import pytest
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token


user_data = {
    'email': 'jara@sparcs.org',
    'password': 'paperpaper'
}

client = APIClient()
token = client.post('/api-token-auth/',user_data, format='json')
client.credentials(HTTP_AUTHORIZATION='PAPER ' + token.key)

def test_get_list_case():
    response = client.get('/api/users/')
    assert response.status_code == 200


def test_get_single_case():
    pass


def test_post_case():
    pass


def test_put_case():
    pass


def test_patch_case():
    pass
