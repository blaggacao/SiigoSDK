import json
from typing import List
from siigo.models.exceptions import SiigoError


class SiigoException(Exception):
    errors: List[SiigoError]

    def __init__(self, errors: List[SiigoError]) -> None:
        self.errors = errors

        errors_str = json.dumps({e.code: e.message for e in errors})
        super().__init__(f'One or more errors occurred while calling Siigo API. Check errors attribute: {errors_str}')
