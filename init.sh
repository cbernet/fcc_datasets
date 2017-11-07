export PATH=$PWD/scripts:$PATH
export FCCDATASETS=$PWD
export PATH=$FCCDATASETS:$PATH
export PYTHONPATH=$FCCDATASETS:$PYTHONPATH
unamestr=`uname`
echo $unamestr
if [[ "$unamestr" == 'Linux' ]]; then
    export EOSCONDOR=/eos/experiment/fcc/ee/datasets/papas/
else
    export EOSCONDOR=~/ee/
fi
#TODO discuss with colin best way to deal with EOS and with filepaths
#Mac osx command for linking eos after a kinit token is setup
#mkdir ~/ee
#export EOS_MGM_URL=root://eospublic.cern.ch//eos/experiment/fcc/ee/
#eos fuse mount ~/ee

#export EOS_MGM_URL=root://eosuser.cern.ch//eos/user/a/alrobson
#cd ..eos fuse mount /Users/alice/eos





