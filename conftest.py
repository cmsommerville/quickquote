import datetime
import json
import pytest

from app.models.GroupModel import GroupModel
from app.models.PlanModel import PlanModel
from app.models.ProvisionModel import ProvisionModel
from app.models.FactorModel import FactorModel

from app.schemas.GroupSchema import GroupSchema
from app.schemas.PlanSchema import PlanSchema
from app.schemas.ProvisionSchema import ProvisionSchema
from app.schemas.FactorSchema import FactorSchema


@pytest.fixture(scope='module')
def new_group_data1():
    group_data = {
        "group_name": "Barrel and Bull",
        "group_size": 2400,
        "sic_code": '9876',
        "tax_id": "123456789"
    }

    return group_data


@pytest.fixture(scope='module')
def new_plan_data1():
    plan_data = {
        "plan_number": 1,
        "group_id": 1,
        "product_name": "Accident",
        "rating_state": "CA",
        "plan_effective_date": "2018-01-01",
        "plan_status": "Quoting"
    }
    return plan_data


@pytest.fixture(scope='module')
def new_provision_data1():
    data = {
        "plan_id": 1,
        "provision_code": "prex",
        "provision_name": "Pre-Existing Condition Limitation",
        "provision_value": str(100),
        "provision_data_type": "number"
    }
    return data


@pytest.fixture(scope='module')
def new_factor_data1():
    data = {
        "plan_id": 1,
        "factor_type": "product",
        "factor_name": "groupsize",
        "factor_selection": "<1000",
        "factor_value": 0.95
    }
    return data


@pytest.fixture(scope='module')
def new_group1(new_group_data1):
    group_schema = GroupSchema()
    group1 = group_schema.load(new_group_data1)
    return group1


@pytest.fixture(scope='module')
def new_plan1(new_plan_data1):
    plan_schema = PlanSchema()
    plan1 = plan_schema.load(new_plan_data1)
    return plan1


@pytest.fixture(scope='module')
def new_provision1(new_provision_data1):
    schema = ProvisionSchema()
    provision = schema.load(new_provision_data1)
    return provision


@pytest.fixture(scope='module')
def new_factor1(new_factor_data1):
    schema = FactorSchema()
    factor = schema.load(new_factor_data1)
    return factor
