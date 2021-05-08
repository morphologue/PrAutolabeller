class StrategyBase:
    def __init__(self, config):
        self.config = config

    def calc_labels(self, pr):
        if self.config == None:
            return {}

        if pr['draft']:
            return { label: False for label in self.config.values() }

        # The subclass will need to do some work
        return None
