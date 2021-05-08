import github
from fnmatch import fnmatch
from strategy_base import StrategyBase

class PathStrategy(StrategyBase):
    def __init__(self, config):
        super().__init__(config)

    def calc_labels(self, pr):
        basic = super().calc_labels(pr)
        if basic != None:
            return basic

        label_requirements = {}
        for file in github.get_paginated(pr['url'] + '/files'):
            file_name = '/' + file['filename']
            for pattern, label in self.config.items():
                label_requirements[label] = label_requirements.get(label, False) or fnmatch(file_name, pattern)

        return label_requirements
