from os import environ
from team_strategy import TeamStrategy
from path_strategy import PathStrategy

def _get_config(section):
    if section not in environ:
        return None
    pairs = environ[section].split(',')
    return { splat[0]: splat[1] for splat in [ pair.split('=') for pair in pairs ] }

instances = [
    TeamStrategy(_get_config('TEAM_STRATEGY')),
    PathStrategy(_get_config('PATH_STRATEGY'))
]
