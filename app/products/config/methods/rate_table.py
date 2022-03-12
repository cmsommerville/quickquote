import pandas as pd 
from io import StringIO

from app.extensions import db, ma
from ..models import Model_ConfigProduct, Model_ConfigProductVariation, Model_ConfigBenefit, Model_ConfigBenefitProductVariation, Model_RefStates



class Schema_RateTableValidation(ma.Schema):
    product_id = ma.Integer()
    product_variation_id = ma.Integer()
    benefit_id = ma.Integer()
    product_code = ma.String()
    product_variation_code = ma.String()
    benefit_code = ma.String()


class Schema_States(ma.Schema):
    state_id = ma.Integer()
    state_code = ma.String()


class Schema_RateTable(ma.Schema):
    product_id = ma.Integer()
    product_variation_id = ma.Integer()
    benefit_id = ma.Integer()
    state_id = ma.Integer()
    age = ma.Integer()
    family_code = ma.String()
    smoker_status_code = ma.String()
    gender_code = ma.String()
    family_code = ma.String()
    annual_rate_per_unit = ma.Float()
    unit_value = ma.Float()




_schema_list = Schema_RateTableValidation(many=True)
_schema_state_list = Schema_States(many=True)
_schema_rate_table_list = Schema_RateTable(many=True)


def process_rate_table(file): 
    df = pd.read_csv(file)
    df = _validate_columns(df)
    df = _validate_fields(df)
    return _serialize(df.to_dict('records'))


def _query_for_ids(): 
    """
    Query for the benefit, product, and product variation IDs
    """
    qry = db.session.query(
        Model_ConfigBenefit.benefit_id, Model_ConfigBenefit.benefit_code, 
        Model_ConfigBenefitProductVariation.product_variation_id, Model_ConfigProductVariation.product_variation_code, 
        Model_ConfigProduct.product_id, Model_ConfigProduct.product_code)
    qry = qry.join(Model_ConfigBenefitProductVariation.benefit)
    qry = qry.join(Model_ConfigProductVariation)
    qry = qry.join(Model_ConfigProduct)

    data = qry.all()
    return _schema_list.dump(data)


def _query_for_state_ids(): 
    """
    Query for the state IDs
    """
    qry = db.session.query(Model_RefStates.state_code, Model_RefStates.state_id)
    data = qry.all()
    return _schema_state_list.dump(data)


def _validate_columns(df): 
    """
    Validate that all the required columns are present
    """
    VALID_COLUMNS = {'product_code', 'product_variation_code', 'benefit_code', 'state_code', 'family_code', 'smoker_status_code', 'gender_code', 'age', 'annual_rate_per_unit', 'unit_value'}
    for col in VALID_COLUMNS:
        if col not in df.columns: 
            raise Exception(f'Column, {col}, not in input file.')
    return df


def _validate_fields(df): 
    """
    Return a dataframe with all the valid IDs
    Raise errors if validation fails
    """
    data_ids = _query_for_ids()
    state_ids = _query_for_state_ids()
    VALID_DATA = pd.DataFrame(data_ids)
    VALID_DATA_STATES = pd.DataFrame(state_ids)

    VALID_STATES = set(VALID_DATA_STATES['state_code'].tolist())
    VALID_PRODUCTS = set(VALID_DATA['product_code'].tolist())
    VALID_PRODUCT_VARIATIONS = set(VALID_DATA['product_variation_code'].tolist())
    VALID_BENEFITS = set(VALID_DATA['benefit_code'].tolist())

    for row in df.to_dict('records'): 
        if row['product_code'] not in VALID_PRODUCTS: 
            raise Exception(f"Product code, `{row['product_code']}`, has not been configured yet")
        if row['product_variation_code'] not in VALID_PRODUCT_VARIATIONS: 
            raise Exception(f"Product variation code, `{row['product_variation_code']}`, has not been configured yet")
        if row['benefit_code'] not in VALID_BENEFITS: 
            raise Exception(f"Benefit code, `{row['benefit_code']}`, has not been configured yet")
        if row['state_code'] not in VALID_STATES: 
            raise Exception(f"State code, `{row['state_code']}`, has not been configured yet")

    try: 
        df_joined = pd\
            .merge(df, VALID_DATA, on=["product_code", "product_variation_code", "benefit_code"], how="left")
    except: 
        raise Exception("Could not join uploaded rate table to product surrogate keys")

    try: 
        df_joined = pd.merge(df_joined, VALID_DATA_STATES, on=['state_code'], how='left')
    except: 
        raise Exception("Could not join uploaded rate table to state reference table")

    try: 
        if any(pd.isna(df_joined['product_id'])): 
            raise Exception("Please make sure that all benefits are configured and attached to product variations")
        if any(pd.isna(df_joined['product_variation_id'])): 
            raise Exception("Please make sure that all benefits are configured and attached to product variations")
        if any(pd.isna(df_joined['benefit_id'])): 
            raise Exception("Please make sure that all benefits are configured and attached to product variations")
    except: 
        raise Exception("Couldn't evaluate if any cells are null")

    return df_joined


def _serialize(data): 
    return _schema_rate_table_list.dump(data)