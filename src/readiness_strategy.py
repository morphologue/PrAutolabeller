class ReadinessStrategy:
    def __init__(self, config):
        self._config = config

    def calc_labels(self, pr):
        return [(label, _reviewabilityMatches(pr, value)) for value, label in self._config]

def _reviewabilityMatches(pr, readiness):
    if readiness == 'draft':
        return pr['draft']
    if readiness == 'pr':
        return not pr['draft']
    if readiness == 'true':
        return True
    return False
