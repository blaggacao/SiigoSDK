import requests
from siigo.models.auth import AuthToken
from siigo.utils.constants import BASE_URL

URL = f'{BASE_URL}/auth'


def get_token(username: str, access_key: str) -> AuthToken:
    res = requests.post(URL, json={'username': username, 'access_key': access_key})
    data = res.json()
    return AuthToken(type=data['token_type'], token=data['access_token'])
