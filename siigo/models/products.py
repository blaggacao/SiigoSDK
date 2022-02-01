from dataclasses import dataclass
from enum import Enum
from typing import List, Optional
from siigo.utils.utils import get_or_default


class TaxType(Enum):
    Retefuente = 'Retefuente'
    ReteIVA = 'ReteIVA'
    ReteICA = 'ReteICA'
    Impoconsumo = 'Impoconsumo'
    AdValorem = 'AdValorem'
    Autorretencion = 'Autorretencion'
    IVA = 'IVA'


@dataclass
class ItemDiscount:
    percentage: float
    value: float

    def to_dict(self) -> dict:
        return {
            'percentage': self.percentage,
            'value': self.value,
        }

    @staticmethod
    def from_dict(data: Optional[dict]) -> Optional['ItemDiscount']:
        if not data:
            return None

        return ItemDiscount(
            percentage=data['percentage'],
            value=data['value'],
        )


@dataclass
class ItemTax:
    id: int
    name: str
    type: TaxType
    percentage: float
    value: Optional[float] = None

    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'name': self.name,
            'percentage': self.percentage,
            'value': self.value,
            'type': self.type.value,
        }

    @staticmethod
    def from_dict(data: dict) -> 'ItemTax':
        return ItemTax(id=data['id'], name=data['name'], type=TaxType(data['type']), percentage=data['percentage'])


@dataclass
class Item:
    id: str
    code: str
    description: str
    quantity: float
    price: float
    taxes: List[ItemTax]
    discount: Optional[ItemDiscount] = None

    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'code': self.code,
            'description': self.description,
            'quantity': self.quantity,
            'price': self.price,
            'taxes': [t.to_dict() for t in self.taxes],
            'discount': self.discount.to_dict() if self.discount else None,
        }

    @staticmethod
    def from_dict(data: dict) -> 'Item':
        price = data.get('price')
        if price is None:
            prices = get_or_default(data, 'prices', [{}])[0]
            price = get_or_default(prices, 'price_list', [{}])[0].get('value', 0)

        return Item(id=data['id'],
                    code=data['code'],
                    description=data['description'],
                    quantity=data.get('quantity', 0),
                    price=price,
                    discount=ItemDiscount.from_dict(data.get('discount')),
                    taxes=[ItemTax.from_dict(t) for t in data['taxes']])
