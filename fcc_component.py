import heppy.framework.config as cfg
from fcc_datasets.dataset import Dataset

class FCCComponent(cfg.MCComponent):
    
    #----------------------------------------------------------------------
    def __init__(self, name, pattern=None, cache=True,
                 cfg=None, xsection=None, **kwargs):
        """"""
        dataset = Dataset(name, pattern, cache, cfg, xsection)
        super(FCCComponent, self).__init__(
            dataset.name,
            dataset.list_of_good_files(),
            xSection=dataset.xsection(), 
            **kwargs
        )
