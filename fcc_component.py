import heppy.framework.config as cfg
from fcc_datasets.dataset import Dataset

class FCCComponent(cfg.MCComponent):
    
    #----------------------------------------------------------------------
    def __init__(self, name, pattern='*.root', cache=True,
                 cfg=None, xsection=None, **kwargs):
        """"""
        self.dataset = Dataset(name, pattern, cache, cfg, xsection)
        super(FCCComponent, self).__init__(
            self.dataset.name,
            self.dataset.list_of_good_files(),
            xSection=self.dataset.xsection(), 
            **kwargs
        )
