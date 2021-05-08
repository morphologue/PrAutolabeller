from strategy_base import StrategyBase

class ConstStrategy(StrategyBase):
    def __init__(self, config):
        super().__init__(config)

    def calc_labels(self, pr):
        basic = super().calc_labels(pr)
        if basic != None:
            return basic

        return { label: value == 'true' for label, value in self.config.items() }
