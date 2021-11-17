def min(x, y):
    return x if x < y else y


def max(x, y):
    return x if x > y else y


class Rating_ConfigPolicyReducer:

    def __init__(self, config, policy):
        self.config = config
        self.policy = policy
        self.output_config = config

    def stateReducer(self):
        # if policy does not restrict states, then do not modify output_config.states
        if not self.policy.get('states'):
            return

        states = []
        # make dictionary for easy config lookup
        cfg = {state['code']: state for state in self.config.get('states', [])}

        for state in self.policy.get('states', []):
            code = state['code']

            # if state not in config, then skip it
            if not cfg.get(code):
                continue

            # append the adjusted state configuration
            states.append({
                "code": code,
                "effectiveDate": max(state['effectiveDate'], cfg[code]['effectiveDate']),
                "expiryDate": min(state['expiryDate'], cfg[code]['expiryDate'])
            })

        self.output_config = {**self.output_config, "states": states}

    def benefitsReducer(self):

        # if policy does not restrict benefits, then do not modify output_config.benefits
        if not self.policy.get('benefits'):
            return

        benefits = []
        # make dictionary for easy config lookup
        cfg = {bnft['code']: bnft for bnft in self.config.get('benefits', [])}

        for bnft in self.policy.get('benefits', []):
            code = bnft['code']

            # if benefit not in config, then skip it
            if not cfg.get(code):
                continue

            # append the adjusted state configuration
            benefits.append({
                "code": code,
                "effectiveDate": max(state['effectiveDate'], cfg[code]['effectiveDate']),
                "expiryDate": min(state['expiryDate'], cfg[code]['expiryDate'])
            })

        self.output_config = {**self.output_config, "states": states}
