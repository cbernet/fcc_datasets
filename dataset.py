import basedir

import glob
import os
import pprint

class File(object):

    def __init__(self, path):
        self.path = path
        self.name = os.path.basename(path) 
        self._check()

    def _check(self):
        self.flags = dict()
        to_check = ['zero_size', 
                    'n_events']
        for testname in to_check:
            method = getattr(self, '_check_{}'.format(testname))
            self.flags[testname] = method()
  
    def _check_zero_size(self):
        statinfo = os.stat(self.path)
        return statinfo.st_size==0

    def _check_n_events(self):
        return 100
        
    def __str__(self):
        return '{:<30} : {}'.format(self.name, pprint.pformat(self.flags))
        

class Directory(object):

    def __init__(self, path):
        self.path = path

    def abspath(self, fname):
        return '/'.join([self.path, fname])


class Dataset(Directory):

    def __init__(self, name):
        self.name = name
        self.path = basedir.abspath(name)
        self.all_files = dict()
        self._build_list_of_files()

    def _build_list_of_files(self):
        print self.abspath('*.root')
        for path in glob.glob(self.abspath('*.root')):
            the_file = File(path)
            self.all_files[the_file.name] = the_file
            print the_file

    def __str__(self):
        lines = [self.name]
        lines.append(self.path)
        return '\n'.join(lines)
