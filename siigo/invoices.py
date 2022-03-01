import requests
from typing import List, Optional, Union
from siigo.models.auth import AuthToken
from siigo.models.core import CurrencyCode
from siigo.models.invoices import Currency, Invoice, InvoiceCustomer, Payment, Retention
from siigo.models.products import Item
from siigo.utils.constants import BASE_URL
from siigo.utils.requests import check_for_errors
from siigo.utils.utils import form_headers, paginate, parse_date

URL = f'{BASE_URL}/v1/invoices'


@paginate(parse_response=Invoice.from_dict)
def list_invoices(token: AuthToken, page: int):
    req = requests.get(URL, params={
        'page': page,
        'page_size': 25,
    }, headers=form_headers(token=token))

    return req.json()


def get_invoice(id: str, token: AuthToken):
    req = requests.get(f'{URL}/{id}', headers=form_headers(token))
    res = req.json()

    return Invoice.from_dict(res)


def create_invoice(*,
                   token: AuthToken,
                   doc_id: int,
                   date: Union[float, int],
                   customer: InvoiceCustomer,
                   seller: str,
                   items: List[Item],
                   payments: List[Payment],
                   currency: Optional[Currency] = None,
                   cost_center: Optional[str] = None,
                   observations: Optional[str] = None,
                   retentions: Optional[List[Retention]] = None) -> Invoice:
    data = dict(document={'id': doc_id},
                date=parse_date(date),
                customer=customer.to_dict(),
                cost_center=cost_center,
                currency=currency.to_dict() if currency and currency.code is not CurrencyCode.COLOMBIAN_PESO else None,
                seller=seller,
                observations=observations,
                items=[i.to_dict() for i in items],
                payments=[p.to_dict() for p in payments],
                retentions=[r.to_dict() for r in retentions] if retentions else None)
    req = requests.post(URL, headers=form_headers(token), json=data)
    res = req.json()
    check_for_errors(req=req, res=res)

    return Invoice.from_dict(res)
