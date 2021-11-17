class ValidationError(Exception):
    def __init__(self, message="Custom validation failed"):
        super().__init__(message)


class StateValidationError(ValidationError):
    def __init__(self, message="State is not approved"):
        super().__init__(message)


class PolicyValidationError(ValidationError):
    def __init__(self, message="Selection invalid for this policy"):
        super().__init__(message)
