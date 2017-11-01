
export FCCDATASETS=$PWD
export PATH=$FCCDATASETS/bin:$PATH
export PYTHONPATH=$PWD/..:$PYTHONPATH
export EOSCONDOR=/eos/experiment/fcc/ee/datasets/papas/

# set up executable directory
cp htcondor/*.py bin/
chmod +x bin/*.py 



