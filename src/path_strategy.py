import github
from fnmatch import fnmatch

class PathStrategy:
    def __init__(self, config):
        self._config = config

    def calc_labels(self, pr):
        needed_labels = set()
        if self._config == None:
            return needed_labels

        for file in github.get_paginated(pr['url'] + '/files'):
            file_name = '/' + file['filename']
            for pattern, label in self._config.items():
                if (fnmatch(file_name, pattern)):
                    needed_labels.add(label)

        return needed_labels
