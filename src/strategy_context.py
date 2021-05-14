from os import environ
from readiness_strategy import ReadinessStrategy
from team_strategy import TeamStrategy
from path_strategy import PathStrategy

def _get_config(section):
    if section not in environ:
        return None
    pairs = environ[section].split(',')
    return [(splat[0], splat[1]) for splat in [pair.split('=') for pair in pairs]]

_types = {
    ReadinessStrategy: _get_config('READINESS_STRATEGY'),
    TeamStrategy: _get_config('TEAM_STRATEGY'),
    PathStrategy: _get_config('PATH_STRATEGY')
}

_instances = [
    Ctor(config) for Ctor, config in _types.items() if config != None
]

def calc_labels(pr):
    all_pairs = [pair for s in _instances for pair in s.calc_labels(pr)]
    consolidated = {}
    for label, requirement in all_pairs:
        consolidated[label] = consolidated.get(label, False) or requirement
    return consolidated
