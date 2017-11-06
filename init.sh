
export FCCDATASETS=$PWD
export PATH=$FCCDATASETS/bin:$PATH
export PYTHONPATH=$PWD/..:$PYTHONPATH
unamestr=`uname`

if [[ "$unamestr" == 'Linux' ]]; then
    export EOSCONDOR=/eos/experiment/fcc/ee/datasets/papas/
else
    export EOSCONDOR=~/ee/datasets/papas
fi

#mkdir ~/ee
#export EOS_MGM_URL=root://eospublic.cern.ch//eos/experiment/fcc/ee/
#eos fuse mount ~/ee

export EOS_MGM_URL=root://eosuser.cern.ch//eos/user/a/alrobson
eos fuse mount /Users/alice/eos
# set up executable directory
#cp htcondor/*.py bin/
#chmod +x bin/*.py



