import datetime

from app.models.GroupModel import GroupModel
from app.models.PlanModel import PlanModel
from app.models.ProvisionModel import ProvisionModel
from app.models.FactorModel import FactorModel

from app.schemas.GroupSchema import GroupSchema
from app.schemas.PlanSchema import PlanSchema
from app.schemas.ProvisionSchema import ProvisionSchema
from app.schemas.FactorSchema import FactorSchema


def test_group_model(new_group1):
    assert new_group1.group_name == "Barrel and Bull"
    assert new_group1.sic_code == "9876"
    assert new_group1.group_size == 2400
    assert new_group1.tax_id == "123456789"


def test_plan_model(new_plan1):
    assert new_plan1.rating_state == "CA"
    assert new_plan1.plan_effective_date == datetime.date(2018, 1, 1)


def test_provision_model(new_provision1):
    assert new_provision1.provision_code == "prex"
    assert new_provision1.provision_value == "100"
    assert new_provision1.provision_data_type == "number"
    assert new_provision1.getValue() == 100


def test_factor_model(new_factor1):
    assert new_factor1.factor_type == "product"
    assert new_factor1.factor_selection == "<1000"
    assert new_factor1.factor_value == 0.95
