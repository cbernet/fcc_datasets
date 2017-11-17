import os

class FilenameHandler(object):
    ''' Class for extracting parts of a filename'''
    
    def __init__(self, filename):
        self.filename = filename
    
    def absolute_path(self):
        return os.path.abspath(self.filename)
    
    def extension(self):
        return os.path.splitext(self.basename())[1] 
    
    def core(self):
        return os.path.splitext(self.basename())[0]          
    
    def basename(self):
        return os.path.basename(self.filename)  
    
    def path(self):
        return os.path(self.filename)   
    
    def filename(self):
        return self.filename    
    
    def __str__(self):
        return self.filename