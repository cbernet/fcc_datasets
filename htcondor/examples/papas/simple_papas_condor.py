## Simple Papas Run
## Runs papas using as a sequence of tools
## The reconstructed particles are written to a ROOT file
#
#  To run 
#  > ./run gaudirun.py Sim/SimPapas/options/simple_papas_condor.py

import argparse
recoparser = argparse.ArgumentParser()
recoparser.add_argument('-o','--routput', type=str, default='output.root', help='output.root')
recoparser.add_argument('-i','--rpythiainput', type=str, default='./ee_ZZ.txt', help='ee_ZZ.txt')
recoparser.add_argument('-n','--rmaxevents', type=int,default = 10, help='10')
recoargs, _ = recoparser.parse_known_args()

outputfilename = recoargs.routput
pythiafile = recoargs.rpythiainput
rmaxevents = recoargs.rmaxevents

print "=================================="
print "input = ", pythiafile
print "output = ", outputfilename
print "maxevents = ", rmaxevents
print "=================================="
from Gaudi.Configuration import *
from Configurables import ApplicationMgr, FCCDataSvc, PodioOutput
from GaudiKernel import SystemOfUnits as units


#### Data service
podioevent = FCCDataSvc("EventDataSvc")

from Configurables import  HepMCFileReader
from Configurables import PythiaInterface, GenAlg
### PYTHIA algorithm
pythia8gentool = PythiaInterface("Pythia8Interface", Filename=pythiafile)
pythia8gen = GenAlg("Pythia8", SignalProvider=pythia8gentool)
pythia8gen.hepmc.Path = "hepmcevent"

from Configurables import HepMCToEDMConverter
### Reads an HepMC::GenEvent from the data service and writes a collection of EDM Particles
hepmc_converter = HepMCToEDMConverter("Converter")
hepmc_converter.hepmc.Path="hepmcevent"
hepmc_converter.genparticles.Path="GenParticle"
hepmc_converter.genvertices.Path="GenVertex"

from CMS_detector_cfg import detservice
from papas_cfg import papasalg

#output fcc particles to root
from Configurables import PodioOutput
out = PodioOutput("out",
                  OutputLevel=WARNING, filename=outputfilename)
out.outputCommands = ["keep *"]

from Configurables import ApplicationMgr
ApplicationMgr(
    ## all algorithms should be put here
    TopAlg=[pythia8gen, hepmc_converter, papasalg, out],
    EvtSel='NONE',
    ## number of events
    EvtMax=rmaxevents,
    ## all services should be put here
    ExtSvc = [podioevent, detservice],
    OutputLevel = WARNING
 )
