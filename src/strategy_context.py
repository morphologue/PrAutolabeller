from os import environ
from team_strategy import TeamStrategy
from path_strategy import PathStrategy

def _get_config(section):
    if section not in environ:
        return None
    pairs = environ[section].split(',')
    return { splat[0]: splat[1] for splat in [ pair.split('=') for pair in pairs ] }

_instances = [
    TeamStrategy(_get_config('TEAM_STRATEGY')),
    PathStrategy(_get_config('PATH_STRATEGY'))
]

def calc_labels(pr):
    return { label for s in _instances for label in s.calc_labels(pr) }
