import json

from Benefit import Benefit
from ProductFactor import ProductFactor

with open("database.json") as f:
    productConfig = json.load(f)

# configure all benefits from the database
benefits = {}
benefitConfig = productConfig['benefits']

for b in benefitConfig:
    benefit = Benefit(**b)
    benefits[benefit.name] = benefit

# load the benefit selections
with open("input_data.json") as f:
    inputData = json.load(f)

benefitSelections = inputData['benefits']
factorSelections = inputData['factors']

if __name__ == "__main__":

    # instantiate each selected factor
    product_factors = []
    for fctr in factorSelections:
        product_factors.append(ProductFactor(name=fctr['name']))

    # instantiate each selected benefit
    for b in benefitSelections:
        selectedBenefit = benefits[b['name']]
        selectedBenefit.setSelections(**b, **{"state": inputData['state']})

        # establish observation pattern for product factors
        for pf in product_factors:
            if selectedBenefit._validate_factor_applicability(pf.name, 'product'):
                pf.attach(selectedBenefit)

    # set the product factors
    product_factors[0].set(1.7)

    # calculate premium for each benefit
    for k, b in benefits.items():
        print(b.name, b.calculatePremium())
