from typing import List, Optional
import requests
from siigo.models.auth import AuthToken
from siigo.models.products import Item
from siigo.utils.constants import BASE_URL
from siigo.utils.requests import check_for_errors
from siigo.utils.utils import form_headers, paginate

URL = f'{BASE_URL}/v1/products'


@paginate(parse_response=Item.from_dict, delay=5)
def list_products(token: AuthToken, page: int, ids: Optional[List[str]] = None):
    ids_query = ({'ids': ','.join(ids)} if ids else {})
    req = requests.get(URL, params={
        'page': page,
        'page_size': 25,
        **ids_query,
    }, headers=form_headers(token))
    return req.json()


def get_product(id: str, token: AuthToken):
    req = requests.get(f'{URL}/{id}', headers=form_headers(token))
    res = req.json()
    check_for_errors(req=req, res=res)
    return Item.from_dict(res)
