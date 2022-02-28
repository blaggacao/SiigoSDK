import requests
from time import time
from siigo.models.auth import AuthToken
from siigo.models.core import CurrencyCode
from siigo.utils.constants import BASE_URL
from siigo.utils.utils import form_headers, parse_date


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


def get_exchange_rate(token: AuthToken, source: CurrencyCode, target: CurrencyCode) -> float:
    req = requests.get('https://services.siigo.com/ACGeneralApi/api/v1/Money/GetExchangeValue',
                       params={
                           'sourceMoney': source.value,
                           'targetMoney': target.value,
                           'sDate': parse_date(timestamp=time(), format='%Y%m%d'),
                       },
                       headers=form_headers(token))
    return req.json()
