import requests
from siigo.models.auth import AuthToken
from siigo.models.clients import ID, ClientType, Contact, Entity, Client
from siigo.models.exceptions import SiigoError
from siigo.utils.constants import BASE_URL
from siigo.utils.exceptions import SiigoException
from siigo.utils.requests import check_for_errors
from siigo.utils.utils import form_headers, paginate

URL = f'{BASE_URL}/v1/customers'


def create_client(*,
                  entity: Entity,
                  id: ID,
                  client_type: ClientType = ClientType.CUSTOMER,
                  contact: Contact,
                  token: AuthToken) -> Client:
    data = dict(
        type=client_type.value,
        person_type=entity.type.value,
        id_type=id.type.value,
        identification=id.id,
        check_digit=id.check_digit,
        name=entity.name,
        commercial_name=entity.commercial_name,
        vat_responsible=entity.vat_responsible,
        fiscal_responsibilities=[{
            'code': r.value
        } for r in entity.responsibility],
        address=contact.address.to_dict(),
        phones=[p.to_dict() for p in contact.phones],
        contacts=[c.to_dict() for c in contact.contacts],
    )

    req = requests.post(URL, headers=form_headers(token=token), json=data)
    res = req.json()
    check_for_errors(req=req, res=res)

    return Client.from_dict(res)


@paginate(parse_response=Client.from_dict)
def list_clients(token: AuthToken, page: int):
    req = requests.get(URL, params={
        'page': page,
        'page_size': 25,
    }, headers=form_headers(token=token))

    return req.json()


def get_client(*, _id: str, token: AuthToken):
    req = requests.get(f'{URL}/{_id}', headers=form_headers(token=token))
    res = req.json()
    check_for_errors(req=req, res=res)
    return Client.from_dict(res)


def delete_client(*, _id: str, token: AuthToken):
    req = requests.delete(f'{URL}/{_id}', headers=form_headers(token))
    res = req.json()

    if not res['deleted']:
        raise SiigoException(errors=[SiigoError(code='unknown', message='Client could not be deleted')])

    return res['id']
