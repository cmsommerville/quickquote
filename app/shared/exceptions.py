class StateValidationError(Exception):
    def __init__(self, message="State is not approved"):
        super().__init__(message)


class PolicyValidationError(Exception):
    def __init__(self, message="Selection invalid for this policy"):
        super().__init__(message)
