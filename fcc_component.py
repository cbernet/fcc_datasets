import heppy.framework.config as cfg
from fcc_datasets.dataset import Dataset

class FCCComponent(cfg.MCComponent):
    
    #----------------------------------------------------------------------
    def __init__(self, name, **kwargs):
        """"""
        dataset = Dataset(name, extract_info=False, cache=True)
        super(FCCComponent, self).__init__(
            dataset.name,
            dataset.list_of_good_files(),
            **kwargs
        )
