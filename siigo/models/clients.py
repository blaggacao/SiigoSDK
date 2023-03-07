from dataclasses import dataclass
from enum import Enum
from typing import List, Optional
from siigo.utils.utils import opt_dict


class ClientType(Enum):
    CUSTOMER = 'Customer'
    SUPPLIER = 'Supplier'
    OTHER = 'Other'


class PersonType(Enum):
    PERSON = 'Person'
    COMPANY = 'Company'


class DocType(Enum):
    CC = '13'
    NIT = '31'
    CE = '22'
    FOREIGN_ID = '42'
    FOREIGN_NIT = '50'
    NO_RUT = 'R-00-PN'
    NUIP = '91'
    PASSPORT = '41'
    PEP = '14'
    CIVIL_REG = '11'
    NO_DIAN_ID = '43'
    FOREIGN_CARD = '21'
    TI = '12'


class Responsibility(Enum):
    NA = 'R-99-PN'
    GRAN_CONTRIBUYENTE = 'O-13'
    AUTORRETENEDOR = 'O-15'
    AGENTE_RETENCION_IVA = 'O-23'
    REGIMEN_SIMPLE = 'O-47'


@dataclass
class ID:
    type: DocType
    id: str
    check_digit: Optional[str] = None
    name: Optional[str] = None

    @staticmethod
    def from_dict(res: dict) -> 'ID':
        return ID(
            type=DocType(str(res['id_type'].get('code', DocType.CC.value)).strip()),
            check_digit=res['check_digit'],
            id=res['identification'],
            name=res['id_type'].get('name'),
        )


@dataclass
class Entity:
    type: PersonType
    name: List[str]
    responsibility: List[Responsibility]
    commercial_name: Optional[str] = None
    vat_responsible: Optional[bool] = False

    def __post_init__(self):
        if self.type is PersonType.COMPANY and len(self.name) != 1:
            raise Exception('Company type must contain only one value for name array')
        if self.type is PersonType.PERSON and len(self.name) != 2:
            raise Exception('Person type must contain two values for name array')

    @staticmethod
    def from_dict(res: dict) -> 'Entity':
        return Entity(
            type=PersonType(res.get('person_type', PersonType.PERSON.value)),
            name=res.get('name', ['', '']),
            commercial_name=res.get('commercial_name'),
            vat_responsible=res['vat_responsible'],
            responsibility=[Responsibility(r['code']) for r in res.get('fiscal_responsibilities', [])],
        )


@dataclass
class City:
    country_code: str
    state_code: str
    city_code: str

    def to_dict(self) -> dict:
        return opt_dict(
            country_code=self.country_code,
            state_code=self.state_code,
            city_code=self.city_code,
        )


@dataclass
class Address:
    address: str
    city: City
    postal_code: Optional[str] = None

    def to_dict(self) -> dict:
        return opt_dict(
            address=self.address,
            postal_code=self.postal_code,
            city=self.city.to_dict(),
        )


@dataclass
class Phone:
    number: str
    indicative: Optional[str] = None
    extension: Optional[str] = ''

    def to_dict(self) -> dict:
        return opt_dict(
            indicative=self.indicative,
            number=self.number,
            extension=self.extension,
        )


@dataclass
class ContactPerson:
    first_name: str
    last_name: str
    email: str
    phone: Optional[Phone] = None

    def to_dict(self) -> dict:
        return opt_dict(
            first_name=self.first_name,
            last_name=self.last_name,
            email=self.email,
            phone=self.phone.to_dict() if self.phone else None,
        )


@dataclass
class Contact:
    address: Address
    phones: List[Phone]
    contacts: List[ContactPerson]

    @staticmethod
    def from_dict(res: dict) -> 'Contact':
        return Contact(
            address=Address(**res['address']),
            phones=[Phone(**p) for p in res.get('phones', [])],
            contacts=[ContactPerson(**c) for c in res['contacts']],
        )


@dataclass
class Client:
    _id: str
    type: ClientType
    id: ID
    entity: Entity
    active: bool
    contact: Contact

    @staticmethod
    def from_dict(res: dict) -> 'Client':
        return Client(_id=res['id'],
                      type=ClientType(res.get('type', ClientType.OTHER.value)),
                      active=res['active'],
                      id=ID.from_dict(res),
                      entity=Entity.from_dict(res),
                      contact=Contact.from_dict(res))
