from dataclasses import dataclass
from typing import List, Optional
from enum import Enum


class SiigoErrorCode(Enum):
    ALREADY_EXISTS = 'already_exists'
    COMPANY_SETTINGS = 'company_settings'
    DELETE_NOT_ALLOWED = 'delete_not_allowed'
    DOCUMENT_SETTINGS = 'document_settings'
    INVALID_ARRAY = 'invalid_array'
    INVALID_AMOUNT = 'invalid_amount'
    INVALID_CODE = 'invalid_code'
    INVALID_COST_CENTER = 'invalid_cost_center'
    INVALID_CURRENCY = 'invalid_currency'
    INVALID_DATE = 'invalid_date'
    INVALID_DESCRIPTION = 'invalid_description'
    INVALID_DOCUMENT = 'invalid_document'
    INVALID_EMAIL = 'invalid_email'
    INVALID_IDENTIFICATION = 'invalid_identification'
    INVALID_NAME = 'invalid_name'
    INVALID_PAYMENT = 'invalid_payment'
    INVALID_RANGE = 'invalid_range'
    INVALID_REFERENCE = 'invalid_reference'
    INVALID_TOTAL_PAYMENTS = 'invalid_total_payments'
    INVALID_RETENTIONS = 'invalid_retentions'
    INVALID_TYPE = 'invalid_type'
    INVALID_URL = 'invalid_url'
    INVALID_VALUE = 'invalid_value'
    LENGTH_MAX = 'length_max'
    LENGTH_MIN = 'length_min'
    NOT_FOUND = 'not_found'
    PARAMETER_EMPTY = 'parameter_empty'
    PARAMETER_INACTIVE = 'parameter_inactive'
    PARAMETER_REQUIRED = 'parameter_required'
    PARAMETERS_EXCLUSIVE = 'parameters_exclusive'
    PRODUCT_SETTINGS = 'product_settings'
    REQUESTS_LIMIT = 'requests_limit'
    UNAUTHORIZED = 'unauthorized'
    UNHANDLED_ERROR = 'unhandled_error'
    WAREHOUSE_SETTINGS = 'warehouse_settings'
    INVALID_BALANCE = 'invalid_balance'
    VALUES_LIMIT = 'values_limit'
    INVALID_DATE_RANGE = 'invalid_date_range'
    DATE_SETTINGS = 'date_settings'
    PARAMETER_NOT_ALLOWED = 'parameter_not_allowed'
    NON_EDITABLE = 'non_editable'
    ENTRY_SERVICE = 'entry_service'
    GENERAL_SERVICE = 'general_service'


@dataclass
class SiigoError:
    code: str
    message: str
    params: Optional[List[str]] = None
    deatil: Optional[str] = None

    def to_str(self) -> str:
        return f'{self.code}: {self.message}'
