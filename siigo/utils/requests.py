from siigo.utils.exceptions import SiigoException, SiigoError


def check_for_errors(*, req, res):
    if req.status_code >= 400:
        if res.get('Errors'):
            raise SiigoException(errors=[
                SiigoError(
                    code=e['Code'],
                    deatil=e['Detail'],
                    message=e['Message'],
                    params=e['Params'],
                ) for e in res['Errors']
            ])
        raise Exception(res.get('Errors', f'Unkwnon Siigo error occured: {str(res)}'))
