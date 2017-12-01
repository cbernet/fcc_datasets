# fcc_datasets

Tools to manage event datasets stored in ROOT format. 

High-energy physics analyses typically process a large number of datasets.
A dataset comprises a set of ROOT files, each containing a number of events. 

To reduce the probability of human errors, this package makes it easy to find the datasets that can be used and, for each dataset, to: 

* list the good files in the dataset for further processing 
* keep track of various dataset information: 
  * parent (or mother) dataset 
  * total number of events 
  * computing efficiency 
  * version of the software used to produce the dataset
  * etc.

This information is stored in a yaml file like this one: 

```yaml

sample:
  id: !!python/object:uuid.UUID
    int: 164332393679473591140683890003054440774
  jobtype: heppy
  mother: papas/ee_to_ZZ_condor_A_703
  nevents: 100
  nfiles: 1
  ngoodfiles: 1
  pattern: heppy.analyzers.JetTreeProducer.JetTreeProducer_1/jet_tree.root
software:
  heppy: !!python/unicode '5dd9d9828fe4e79dc3c71b0119edc1b322882edd'
```

## Prerequisites

To use this package, you need: 

* python 2.7 (might work with other versions)
* [GitPython](http://gitpython.readthedocs.io/en/stable/) - you'll need to install it
* [ROOT](https://root.cern.ch/)

## Installation

Clone this package and do the following: 

```bash
cd fcc_datasets
export PYTHONPATH=$PWD/..:$PYTHONPATH
source ./init.sh
```

Make sure the test suite runs: 

```bash
python test/suite.py
```

Messages of the following type can be safely ignored: 

```
TClass::Init:0: RuntimeWarning: no dictionary for class fcc::BareParticle is available
```

## Dataset area

All datasets should be stored in the same directory of your choice, called the base directory. 

Create your base directory, e.g. `$HOME/datasets`:

```bash
mkdir ~/datasets
```

Keep track of this directory as the `FCCDATASETBASEOUT` environment variable. In bash: 

```bash
export FCCDATASETBASEOUT=$HOME/datasets
```

You may add this line to your `.bashrc` if you wish. 
You may also have several base directories for different projects, and switch between them by resetting the environment variable. 

## Dataset publication

Create a dataset in your base directory. For simplicity, you may just copy one of the test datasets available in this package: 

```bash 
cp -r test/papas/ee_to_ZZ_condor_A_703/ $FCCDATASETBASEOUT/test_dataset
```

This dataset contains the following files: 

```
info.yaml           papasout_2.0_2.root papasout_2.0_5.root papasout_2.0_8.root
papasout_2.0_0.root papasout_2.0_3.root papasout_2.0_6.root papasout_2.0_9.root
papasout_2.0_1.root papasout_2.0_4.root papasout_2.0_7.root
```

The `info.yaml file`, if there, is a remnant of a previous publication. Just remove it if you want, it will be re-created in the next step anyway.  

Publish the dataset: 

```bash
publish.py -e -v -w 'papasout*.root' test_dataset
```

This produces the following output: 

```
TClass::Init:0: RuntimeWarning: no dictionary for class fcc::MCParticleData is available
TClass::Init:0: RuntimeWarning: no dictionary for class fcc::BareParticle is available
TClass::Init:0: RuntimeWarning: no dictionary for class fcc::LorentzVector is available
TClass::Init:0: RuntimeWarning: no dictionary for class fcc::Point is available
TClass::Init:0: RuntimeWarning: no dictionary for class podio::ObjectID is available
TClass::Init:0: RuntimeWarning: no dictionary for class fcc::GenVertexData is available
TClass::Init:0: RuntimeWarning: no dictionary for class fcc::ParticleData is available
TClass::Init:0: RuntimeWarning: no dictionary for class fcc::ParticleMCParticleAssociationData is available
TClass::Init:0: RuntimeWarning: no dictionary for class podio::CollectionIDTable is available
test_dataset
/Users/cbernet/Tmp/datasets//test_dataset
papasout_2.0_8.root            : {'good': True, 'n_events': 10, 'zero_size': False}
papasout_2.0_2.root            : {'good': True, 'n_events': 10, 'zero_size': False}
papasout_2.0_5.root            : {'good': True, 'n_events': 10, 'zero_size': False}
papasout_2.0_1.root            : {'good': True, 'n_events': 10, 'zero_size': False}
papasout_2.0_7.root            : {'good': True, 'n_events': 10, 'zero_size': False}
papasout_2.0_6.root            : {'good': True, 'n_events': 10, 'zero_size': False}
papasout_2.0_9.root            : {'good': True, 'n_events': 10, 'zero_size': False}
papasout_2.0_3.root            : {'good': True, 'n_events': 10, 'zero_size': False}
papasout_2.0_4.root            : {'good': True, 'n_events': 10, 'zero_size': False}
papasout_2.0_0.root            : {'good': True, 'n_events': 10, 'zero_size': False}
{'sample': {'id': UUID('d22af90f-4e76-4aee-97aa-c7c44cd7f4b5'),
            'jobtype': 'fccsw',
            'mother': None,
            'nevents': 100,
            'nfiles': 10,
            'ngoodfiles': 10,
            'pattern': 'papasout*.root'},
 'software': {}}
```

Again, the `RunTimeWarning` messages can be ignored. 

## Dataset listing 

Datasets are simply identified with respect to their path relative to the base directory. 
For example, the dataset we have just published is `test_dataset`

To list this dataset, you can do: 

```bash
lsdataset.py test_dataset

test_dataset
/Users/cbernet/Tmp/datasets//test_dataset
papasout_2.0_8.root            : {'good': True, 'n_events': 10, 'zero_size': False}
papasout_2.0_2.root            : {'good': True, 'n_events': 10, 'zero_size': False}
papasout_2.0_5.root            : {'good': True, 'n_events': 10, 'zero_size': False}
papasout_2.0_1.root            : {'good': True, 'n_events': 10, 'zero_size': False}
papasout_2.0_7.root            : {'good': True, 'n_events': 10, 'zero_size': False}
papasout_2.0_6.root            : {'good': True, 'n_events': 10, 'zero_size': False}
papasout_2.0_9.root            : {'good': True, 'n_events': 10, 'zero_size': False}
papasout_2.0_3.root            : {'good': True, 'n_events': 10, 'zero_size': False}
papasout_2.0_4.root            : {'good': True, 'n_events': 10, 'zero_size': False}
papasout_2.0_0.root            : {'good': True, 'n_events': 10, 'zero_size': False}
{'sample': {'id': UUID('d22af90f-4e76-4aee-97aa-c7c44cd7f4b5'),
            'jobtype': 'fccsw',
            'mother': None,
            'nevents': 100,
            'nfiles': 10,
            'ngoodfiles': 10,
            'pattern': 'papasout*.root'},
 'software': {}}

```

## Using a dataset in a python script

Write and run this example script in python:

```python
from dataset import Dataset

ds = Dataset('test_dataset')

for fname in ds.list_of_good_files():
    print fname
```

And have a look at the [Dataset](dataset.py) class for more information.


## More advanced features

### Keeping track of the software version or other information

At publication, all yaml files in the dataset directory are aggregated into `info.yaml`, and their content is thus added to the dataset information. 

To test this, create a file `software.yaml` containing: 

```yaml
software:
  my_package: 13f8b64  # this may be a git commit id
```

Rerun the publication command. The information is added: 

```
papasout_2.0_8.root            : {'good': True, 'n_events': 10, 'zero_size': False}
papasout_2.0_2.root            : {'good': True, 'n_events': 10, 'zero_size': False}
papasout_2.0_5.root            : {'good': True, 'n_events': 10, 'zero_size': False}
papasout_2.0_1.root            : {'good': True, 'n_events': 10, 'zero_size': False}
papasout_2.0_7.root            : {'good': True, 'n_events': 10, 'zero_size': False}
papasout_2.0_6.root            : {'good': True, 'n_events': 10, 'zero_size': False}
papasout_2.0_9.root            : {'good': True, 'n_events': 10, 'zero_size': False}
papasout_2.0_3.root            : {'good': True, 'n_events': 10, 'zero_size': False}
papasout_2.0_4.root            : {'good': True, 'n_events': 10, 'zero_size': False}
papasout_2.0_0.root            : {'good': True, 'n_events': 10, 'zero_size': False}
{'sample': {'id': UUID('9e6fa105-19f1-4791-93df-eca61edb6b32'),
            'jobtype': 'fccsw',
            'mother': None,
            'nevents': 100,
            'nfiles': 10,
            'ngoodfiles': 10,
            'pattern': 'papasout*.root'},
 'software': {'mypackage': '13f8b64'}}
```

If you use [heppy](https://github.com/HEP-FCC/heppy) to produce your dataset, the `software.yaml` file will be created for you automatically. 

You may want to add yaml files to store custom information. 

### Handle the cache

to be written


