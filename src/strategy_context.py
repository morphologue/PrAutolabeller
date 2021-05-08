from os import environ
from const_strategy import ConstStrategy
from team_strategy import TeamStrategy
from path_strategy import PathStrategy

def _get_config(section):
    if section not in environ:
        return None
    pairs = environ[section].split(',')
    return { splat[0]: splat[1] for splat in [ pair.split('=') for pair in pairs ] }

_instances = [
    ConstStrategy(_get_config('CONST_STRATEGY')),
    TeamStrategy(_get_config('TEAM_STRATEGY')),
    PathStrategy(_get_config('PATH_STRATEGY'))
]

def calc_labels(pr):
    all_pairs = [(k, v) for s in _instances for k, v in s.calc_labels(pr).items()]
    consolidated = {}
    for label, requirement in all_pairs:
        consolidated[label] = consolidated.get(label, False) or requirement
    return consolidated
