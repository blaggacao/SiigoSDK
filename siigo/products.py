import requests
from siigo.models.auth import AuthToken
from siigo.models.products import Item
from siigo.utils.constants import BASE_URL
from siigo.utils.utils import form_headers, paginate

URL = f'{BASE_URL}/v1/products'


@paginate(parse_response=Item.from_dict, delay=5)
def list_products(token: AuthToken, page: int):
    req = requests.get(URL, params={
        'page': page,
        'page_size': 25,
    }, headers=form_headers(token))
    return req.json()


def get_product(id: str, token: AuthToken):
    req = requests.get(f'{URL}/{id}', headers=form_headers(token))
    return Item.from_dict(req.json())
