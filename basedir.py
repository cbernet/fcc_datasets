import os
import fcc_datasets

_basename_default = '/'.join([fcc_datasets.__path__[0], 'test'])
_basename = _basename_default
_basecache= '/'.join([os.environ['HOME'],'.fcc_datasets'])


def basename():
    envbasename = os.environ.get('FCCDATASETBASEOUT', None)
    if envbasename:
        return envbasename
    else:
        return _basename

def basecache():
    return _basecache
    
def abspath(name):
    return '/'.join([basename(), name])

def abscache(name):
    return '/'.join([_basecache, name])

def set_basename(name=None):
    global _basename
    if not name:
        name = _basename_default
    _basename = name
    if 'FCCDATASETBASEOUT' in os.environ:
        del os.environ['FCCDATASETBASEOUT']
