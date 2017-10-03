import basedir

import glob
import os

class File(object):

    def __init__(self, path):
        self.path = path
        self.name = os.path.basename(path) 
        self._check()

    def check(self):
        pass

    def __str__(self):
        return self.name
        

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

    def __str__(self):
        lines = [self.name]
        lines.append(self.path)
        return '\n'.join(lines)
