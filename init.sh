
export FCCDATASETS=$PWD
export PATH=$FCCDATASETS/bin:$PATH
export PYTHONPATH=$PWD/..:$PYTHONPATH

# set up executable directory
cp htcondor/*.py bin/
chmod +x bin/*.py 



