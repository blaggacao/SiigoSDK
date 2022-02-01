import requests
from siigo.models.auth import AuthToken
from siigo.utils.constants import BASE_URL
from siigo.utils.utils import form_headers


def list_users(token: AuthToken):
    req = requests.get(f'{BASE_URL}/v1/users', headers=form_headers(token))
    return req.json()


def get_docs(token: AuthToken):
    req = requests.get(f'{BASE_URL}/v1/document-types', params={'type': 'FV'}, headers=form_headers(token))
    return req.json()


def get_payments(token: AuthToken):
    req = requests.get(f'{BASE_URL}/v1/payment-types', params={'document_type': 'FV'}, headers=form_headers(token))
    return req.json()


def get_cost_centers(token: AuthToken):
    req = requests.get(f'{BASE_URL}/v1/cost-centers', headers=form_headers(token))
    return req.json()


def get_taxes(token: AuthToken):
    req = requests.get(f'{BASE_URL}/v1/taxes', headers=form_headers(token))
    return req.json()


def get_users(token: AuthToken):
    req = requests.get(f'{BASE_URL}/v1/users', headers=form_headers(token))
    return req.json()
