from functools import reduce


class Benefit():

    def __init__(self, name, rates, *args, **kwargs):
        self.name = name
        self.rates = rates
        self.amounts = kwargs.get("amounts")
        self.claimCost = rates['claimCost']
        self.claimCostUnit = rates['unit']
        self.durations = kwargs.get('durations', {}).get('values')
        self.factors = {}
        self.factorApplicability = {
            tuple([factor['name'], factor['type']]): factor['applicability'] for factor in kwargs.get("factorApplicability", [])}

    def setSelections(self, state, amount, *args, **kwargs):
        self.state = state
        self.selectedAmount = self._validate_amount(amount, self.amounts)
        self.selectedDuration = kwargs.get("duration")
        self.selectedBenefitFactor = self._get_benefit_factor(
            self.selectedDuration, self.durations)

    def update(self, factor):
        """
        Add a factor to the factor dictionary
        """
        self.factors[factor.name] = factor

    def _validate_amount(self, amount, configAmounts, minVal=0, maxVal=1e10, stepVal=1):
        """
        Validate that the selected amount is valid for the provided configuration
        """
        minAmt = configAmounts.get('min', minVal)
        maxAmt = configAmounts.get('max', maxVal)
        step = configAmounts.get('step', stepVal)

        if amount == 0:
            return amount
        if amount < minAmt:
            raise Exception("Amount selected is less than the minimum")
        if amount > maxAmt:
            raise Exception("Amount selected is greater than the maximum")
        if amount % step != 0:
            raise Exception(f"Amount selected must be a multiple of {step}")
        return amount

    def _get_benefit_factor(self, selectedDuration, durations):
        """
        Return the benefit factor for the selected duration
        """
        if selectedDuration:
            return list(filter(lambda x: x['time'] == selectedDuration, durations))[
                0]['factor']
        return 1.0

    def _validate_factor_applicability(self, factorName, type):
        """
        Return a boolean for whether a specific type of factor is applicable
        to this benefit. 
        """
        applicability = self.factorApplicability.get(
            tuple([factorName, type]), "included")
        if applicability == "prohibited":
            return False
        return True

    def calculatePremium(self):
        """
        Calculate premium for this benefit for the specific selections
        """
        factor_product = reduce(lambda x, fct: x *
                                fct.value, self.factors.values(), 1)
        return factor_product * self.claimCost * self.selectedBenefitFactor * self.selectedAmount / self.claimCostUnit
