import modulefinder
import git
import sys
import fnmatch
import pprint

########################################################################
class Versions(object):
    """"""

    #----------------------------------------------------------------------
    def __init__(self, scriptfname, to_track):
        """Analyze the script scriptfname to find the version of the
        packages matching the patterns in to_track
        """
        # remove standard python2 path to speed things up
        exclude = 'python2'
        path = [p for p in sys.path if 'python2' not in p]
        self.scriptfname = scriptfname
        self.finder = modulefinder.ModuleFinder(path)
        self.finder.run_script(scriptfname)
        # self.finder.report()
        self.tracked = dict()
        for key, mod in self.finder.modules.iteritems():
            for pattern in to_track:
                if fnmatch.fnmatch(key, pattern):
                    self._analyze(key, mod)
                    break
        
    def _analyze(self, key, module):
        info = dict()
        repo = git.Repo(module.__path__[0])
        info['commitid'] = repo.head.commit.hexsha
        self.tracked[key] = info
        print
    
    def __str__(self):
        return pprint.pformat(self.tracked)
    
