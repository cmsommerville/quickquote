from app.extensions import ma

class Schema_QueryAgeBands_AgeBand(ma.Schema): 
    age_band_id = ma.Integer(data_key="config_age_band_id")
    age_band_lower = ma.Integer()
    age_band_upper = ma.Integer()

class Schema_QueryAgeBands(ma.Schema):
    age_band_set_id = ma.Integer(data_key="config_age_band_set_id")
    product_variation_id = ma.Integer(data_key="config_product_variation_id")
    state_id = ma.Integer()
    age_band_effective_date = ma.Date()
    age_band_expiration_date = ma.Date()

    age_bands = ma.List(ma.Nested(Schema_QueryAgeBands_AgeBand))