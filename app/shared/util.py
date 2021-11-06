import functools
import datetime
from .exceptions import StateValidationError


def list_to_dict(l, key):
    return {item['key'] for item in l}


def deep_getattr(obj: dict, attr: str | tuple):
    return functools.reduce(getattr, attr.split("."), obj)


def dateFormat(dateString: str, dateFormat: str = "%Y-%m-%d"):
    return datetime.datetime.strptime(dateString, dateFormat)


def validateStates(rating_state: str, effective_date: str, state_availability: List[dict]) -> None:
    for state in state_availability:
        if state['code'] != rating_state:
            continue

        if effective_date < dateFormat(state.get('effectiveDate', '1900-01-01')):
            raise StateValidationError

        if effective_date > dateFormat(state.get('expiryDate', '1900-01-01')):
            raise StateValidationError
