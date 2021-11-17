import datetime
from typing import List

from .exceptions import ValidationError
from ..errors import ERR1001, ERR1002


def stateValidator(rating_state: str,
                   plan_effective_date: datetime.date,
                   state_applicability: List[dict]) -> bool:
    """
    Validate that the state and effective date of the plan
    is supported by the state applicability array
    """

    state_obj = [
        state for state in state_applicability if state['code'] == rating_state]

    # validate that the policy allows state/effective date
    if len(state_obj) < 1:
        raise ValidationError(ERR1001)
    elif plan_effective_date < dateFormat(state_obj[0].get('effectiveDate', '1900-01-01')):
        raise ValidationError(ERR1002.format({
            "rating_state": rating_state,
            "effective_date": plan_effective_date.strftime('%Y-%m-%d')
        }))
    elif plan_effective_date > dateFormat(state_obj[0].get('expiryDate', '1900-01-01')):
        raise ValidationError(ERR1002.format({
            "rating_state": rating_state,
            "effective_date": plan_effective_date.strftime('%Y-%m-%d')
        }))

    return True


def dateFormat(dateString: str, dateFormat: str = "%Y-%m-%d"):
    return datetime.datetime.strptime(dateString, dateFormat).date()
