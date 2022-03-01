from dataclasses import dataclass
from typing import List, Optional, Union
from siigo.core import get_exchange_rate
from siigo.models.auth import AuthToken
from siigo.models.core import CurrencyCode
from .products import Item


@dataclass
class InvoiceCustomer:
    identification: str
    id: Optional[str] = None
    branch_office: Optional[int] = None

    def to_dict(self) -> dict:
        return {
            'identification': self.identification,
            'id': self.id,
            'branch_office': self.branch_office,
        }

    @staticmethod
    def from_dict(res: dict) -> 'InvoiceCustomer':
        return InvoiceCustomer(
            id=res['id'],
            identification=res['identification'],
        )


@dataclass
class Currency:
    code: CurrencyCode
    exchange_rate: Optional[float] = None
    token: Optional[AuthToken] = None

    def __post_init__(self):
        if self.code.value not in CurrencyCode._value2member_map_:
            raise Exception('Currency code not accepted')
        if self.exchange_rate is None and self.token is None:
            raise Exception('Exchange rate cannot be None. Set token to query Siigo exchange rate service')

        if self.exchange_rate is None and self.token and self.code is not CurrencyCode.COLOMBIAN_PESO:
            self.exchange_rate = get_exchange_rate(token=self.token,
                                                   source=self.code,
                                                   target=CurrencyCode.COLOMBIAN_PESO)

    def to_dict(self) -> dict:
        return {
            'code': self.code.value,
            'exchange_rate': self.exchange_rate,
        }

    @staticmethod
    def from_dict(res: Optional[dict]) -> Optional['Currency']:
        return Currency(code=CurrencyCode(res['code']), exchange_rate=res['exchange_rate']) if res else None


@dataclass
class Payment:
    id: int
    value: float
    name: Optional[str] = None
    due_date: Optional[str] = None

    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'name': self.name,
            'value': self.value,
            'due_date': self.due_date,
        }

    @staticmethod
    def from_dict(res: dict) -> 'Payment':
        return Payment(
            id=res['id'],
            name=res['name'],
            value=res['value'],
            due_date=res.get('due_date'),
        )


@dataclass
class Retention:
    id: int
    name: Optional[str] = None
    type: Optional[str] = None
    percentage: Optional[float] = None
    value: Optional[float] = None

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'type': self.type,
            'percentage': self.percentage,
            'value': self.value,
        }

    @staticmethod
    def from_dict(data):
        return Retention(
            id=data['id'],
            name=data.get('name'),
            type=data.get('type'),
            percentage=data.get('percentage'),
            value=data.get('value'),
        )


@dataclass
class Invoice:
    id: str
    document_id: int
    number: int
    name: str
    date: str
    customer: InvoiceCustomer
    currency: Optional[Currency]
    total: float
    balance: float
    seller: int
    items: List[Item]
    payments: List[Payment]
    cost_center: Optional[Union[bool, int]] = None
    observations: Optional[str] = None
    retentions: Optional[List[Retention]] = None

    @staticmethod
    def from_dict(res: dict) -> 'Invoice':
        return Invoice(
            id=res['id'],
            document_id=res['document']['id'],
            number=res['number'],
            name=res['name'],
            date=res['date'],
            customer=InvoiceCustomer.from_dict(res['customer']),
            cost_center=res.get('cost_center'),
            currency=Currency.from_dict(res.get('currency')),
            total=res['total'],
            balance=res['balance'],
            seller=res['seller'],
            items=[Item.from_dict(i) for i in res['items']],
            observations=res.get('observations'),
            payments=[Payment.from_dict(p) for p in res['payments']],
            retentions=[Retention.from_dict(r) for r in res.get('retentions', [])],
        )
