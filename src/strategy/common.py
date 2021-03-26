import os

def get_settings(section):
    pairs = os.environ[section].split(',')
    return { splat[0]: splat[1] for pair in pairs for splat in pair.split('=') }
