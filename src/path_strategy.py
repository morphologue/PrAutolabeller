import github
from fnmatch import fnmatch

class PathStrategy:
    def __init__(self, config):
        self._config = config

    def calc_labels(self, pr):
        label_requirements = []
        for file in github.get_paginated(pr['url'] + '/files'):
            file_name = '/' + file['filename']
            for pattern, label in self._config:
                label_requirements.append((label, fnmatch(file_name, pattern)))

        return label_requirements
