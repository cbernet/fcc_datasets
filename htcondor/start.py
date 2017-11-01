import os
from fcc_datasets.env_versions import EnvVersions
from filename_handler import FilenameHandler
from condor_parameters import CondorParameters

from subprocess import call


def setup_condor_parser():
    from optparse import OptionParser
    
    parser = OptionParser(
        usage='%prog  [options]',
        description='set up ready for condor dag run'
    ) 
    parser.add_option(
        "-e","--eosdir", dest="eosdir",
        #default="//eos/experiment/fcc/ee/datasets/papas/new",
        default="/Users/alice/ee/datasets/papas/",
        help="eos directory for outputs"
    )
    parser.add_option(
        "-i","--input" ,dest="input",
        default="/afs/cern.ch/work/a/alrobson/fcc_datasets/htcondor/pythiafiles/ee_ZZ.txt",
        help="input file"
    )    
    parser.add_option(
        "-s","--script", dest="script",
        default="/afs/cern.ch/work/a/alrobson/fcc_datasets/htcondor/scripts/simple_papas_condor.py",
        help="fccsw script to run"
    ) 
    parser.add_option(
        "-n","--nevents", dest="nevents",
        default="10",
        help="number of events"
    ) 
    parser.add_option(
        "-r","--runs", dest="runs",
        default="3",
        help="number of htcondor runs"
    )         
    return parser


def setup_condor_directories(outdir, eosdir):
    call(["mkdir", outdir])
    print "made subdirectory " +  outdir   
    basedir = ''.join((eosdir, outdir))
    call(["mkdir", outdir+"/log"]) 
    call(["mkdir", outdir+"/output"]) 
    call(["mkdir", outdir+"/error"]) 
    call(["mkdir", basedir])     
    os.system("cp ./base/* " + outdir)
      

def write_condor_software_yaml(outdir, filename="software.yaml"):
    env_versions =EnvVersions({ 'fccsw': "FCCSWBASEDIR",
                                'fccedm': "FCCEDM",
                                'fccswstack': "FCCSWPATH",
                                'fccphysics': "FCCPHYSICS",
                                'pythia8': "PYTHIA8_DIR",
                                'podio': "PODIO",
                                'fccdag': "FCCDAG",
                                'junk': 'FCCJUNK',
                                'root': 'ROOTSYS',
                                'fccpapas':'FCCPAPASCPP'})
    #print env_versions
    env_versions.write_yaml('/'.join([outdir,filename]))
    
def write_condor_parameters_yaml(outdir, filename="parameters.yaml"):
    
    parameters = Parameters()
    parameters.add("eosdir",eosdir)
    parameters.add("pythiafile",options.pythia)
    parameters.add("subdirectory",outdir)
    parameters.add("script",options.script) 
    parameters.add("nevents",options.nevents) 
    parameters.add("nruns",options.nruns) 
    parameters.write_yaml('/'.join([outdir,fname]))
    parameters.write_yaml('/'.join([basedir,fname]))
    
    
def setup_condor_dag_files(outdir, nevents, runs, rate = 100000):
    #create all the jobs needed in dag file
    outfile =  outdir + "\/run.dag"
    for c in range(runs):
        os.system("echo Job A" + str(c) + " run.sub >> " + outfile)
        os.system("echo Vars A" + str(c) + " runnumber=\\\"" + str(c) + "\\\"  >> " + outfile)
    os.system("echo FINAL FO finish.sub >> " + outfile)
    
    #automatically choose queue based on rate
    flavour="expresso"  
    if nevents>8*rate:
        flavour="tomorrow"
    elif nevents>2*rate:
        flavour="workday"
    elif nevents>rate:
        flavour="longlunch"
    elif nevents>rate/3:
        flavour="microcentury"
    
    print "job is flavour: " + flavour
    outfile =  outdir + "\/run.sub"
    os.system("echo +JobFlavour = " + flavour +" >> " + outfile)
    os.system("echo Queue >> " + outfile)
      


if __name__ == '__main__':
    
    parser = setup_condor_parser()
    (options,args) = parser.parse_args()
    if len(args) != 0:
        parser.print_usage()
        sys.exit(1)

    #extract options
    condor_parameters = CondorParameters(options)
    setup_condor_directories(condor_parameters["subdirectory"], condor_parameters["eosdir"])
    setup_condor_dag_files(condor_parameters["subdirectory"], condor_parameters["nevents"], condor_parameters["runs"])
    write_condor_software_yaml(condor_parameters["subdirectory"] )
    condor_parameters.write_yaml(condor_parameters["subdirectory"])
    condor_parameters.write_yaml(condor_parameters["eosdir"])
    os.chdir(condor_parameters["subdirectory"])
    os.system( "condor_submit_dag -update_submit run.dag ; touch startdag.txt")
    os.chdir("..")
    print os.getcdw()
    print "finished setup"
