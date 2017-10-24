import os
import pprint
import fnmatch
import re
import git
import yaml
import sys
import fnmatch


########################################################################
class EnvVersions(object):
    """
    Look in specified environment variables to find out which software version was used
    If it has a git repository then record the commit id.
    """

    #----------------------------------------------------------------------
    def __init__(self, to_track_dict):
   
        self.tracked = dict()
        self.environ = os.environ
        for key, envname in to_track_dict.iteritems():
            envval =self._get_env(envname)
            if envval:
                envval =envval.split("/install")[0]
                self._analyze(key, envval)

        
    def _analyze(self, key, envval):
        info = envval
        if self._is_git_repo(envval):        
            repo = git.Repo(envval)
            if not repo.bare:
                info = dict()
                info['commitid'] = repo.head.commit.hexsha  
        self.tracked[key] = info
        print
    
    def _is_git_repo(self, path):
        try:
            _ = git.Repo(path).git_dir
            return True
        except git.exc.InvalidGitRepositoryError:
            return False    
        
    def _get_envs(self, name):
        paths= os.environ[name].split(':')
        set = {}
        map(set.__setitem__, paths, [])
        return set.keys()  
        
    def _get_env(self, name):
        if name in self.environ:
            return self.environ[name]
        return None
       
    
    #----------------------------------------------------------------------
    def write_yaml(self, path):
        '''write the versions to a yaml file'''
        data = dict(software=dict())
        # write out either the directory or the git commit if this was found
        for package, info in self.tracked.iteritems():
            if isinstance(info, dict) and 'commitid' in info:
                data['software'][package] = info['commitid']
            else:
                data['software'][package] = info
        with open(path, mode='w') as outfile:
                yaml.dump(data, outfile,
                          default_flow_style=False)    

    def __str__(self):
        return pprint.pformat(self.tracked)
