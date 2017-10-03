import os

basename = '/eos/experiment/fcc/ee/datasets'
basecache = '/'.join([os.environ['HOME'],'.fcc_datasets']) 

def abspath(name):
    return '/'.join([basename,name])

def abscache(name):
    return '/'.join([basecache,name])

