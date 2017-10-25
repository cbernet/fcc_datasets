import os
import fcc_datasets

basename = '/'.join([fcc_datasets.__path__[0], 'test'])
envbasename = os.environ.get('FCCDATASETS', None)
if envbasename:
    basename = envbasename

basecache = '/'.join([os.environ['HOME'],'.fcc_datasets']) 

def abspath(name):
    return '/'.join([basename,name])

def abscache(name):   
    return '/'.join([basecache,name])

