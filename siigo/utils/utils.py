import time
from functools import wraps
from typing import Any, Callable, Generic, TypeVar, Generator, Union, Protocol
from siigo.models.auth import AuthToken


def form_headers(token: AuthToken) -> dict:
    return {
        'Content-Type': 'application/json',
        'Authorization': token.form(),
    }


T = TypeVar('T')


class Paginable(Protocol, Generic[T]):

    def __call__(self, token: AuthToken, **kwargs) -> Generator[T, None, None]:
        ...


def paginate(*, parse_response: Callable[[dict], T] = lambda x: x, delay=10, verbose=False):

    def inner(func) -> Paginable[T]:

        @wraps(func)
        def wrapper(*args, **kwargs) -> Generator[T, None, None]:
            res = None
            try:
                consumed_total = False
                page = 0

                while not consumed_total:
                    page += 1
                    res = func(*args, **kwargs, page=page)

                    pagination = res['pagination']
                    consumed_total = pagination['page'] * pagination['page_size'] >= pagination['total_results']
                    if verbose:
                        print(page, 'out of', int(pagination['total_results'] / pagination['page_size']))

                    for r in res['results']:
                        yield parse_response(r)

                    if delay:
                        time.sleep(delay)
            except Exception as e:
                if verbose:
                    print(res)
                raise e

        return wrapper

    return inner


def parse_date(timestamp: Union[float, int], format: str = '%Y-%m-%d') -> str:
    return time.strftime(format, time.gmtime(timestamp))


def get_or_default(data: dict, key: Any, default):
    return data.get(key) or default


def opt_dict(**entries):
    return {k: v for k, v in entries.items() if v is not None}
