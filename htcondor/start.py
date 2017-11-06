import os
from fcc_datasets.env_versions import EnvVersions
from filename_handler import FilenameHandler
from condor_parameters import CondorParameters
from subprocess import call

''' Start.py is used to setup all files and directories needed for a condor batch run

    Usage: python $FCCDATASETS/htcondor/start.py -e baseoutdir -i inputfile -s script -n nevents -r runs
    
    example
    python $FCCDATASETS/htcondor/start.py -e $EOSCONDOR -i ee_ZZ.txt -s simple_papas_cms.py -n 100 -r 4
    
    A subdirectory name will be automatically created based on the run parameters.
    A working subdirectory of this name will be created in the current directory. 
    Log/output/error subdirectories needed for condor are created in the working directory.
    The working directory will receive outputs/logs/errors 
    from the condor_dag and condor submissions, and can be referred to uncover any issues.
    Some scipts and sub files are copied into the working directory from $FCCSDATASET/htcondor/base
    Some sub files are written/added to according to run parameters
    
    An output subdirectory of this name will be created in the base output directory (usually EOS) to hold root and yaml outputs
    
    The run is submitted to condor. This executes run.dag which will execute the individual runs and, when these have completed, a finish.sub which 
    creates a final info.yaml summary.
    
'''


def setup_condor_parser():
    ''' Reads in options from the line command line:
    The options are
    -e base_outputdir -i inputfile -s script -n nevents -r runs
    '''
    from optparse import OptionParser
    #defaults are in FCCDATASETS directory
    environ = os.environ
    datasetsdir = ""
    eosdir=""
    if "FCCDATASETS" in environ:
        datasetsdir = environ["FCCDATASETS"] 
    else:
        print "FCCDATASETS environment variable is missing - call init.sh"
    if "EOSCONDOR" in environ:
        eosdir = environ["EOSCONDOR"] 
    else:
        print "EOSCONDOR environment variable is missing - call/read init.sh"    
        
    parser = OptionParser(
        usage='%prog  [options]',
        description='set up ready for condor dag run'
    ) 
    parser.add_option(
        "-e","--base_outputdir", dest="base_outputdir",
        default=eosdir,
        help="directory for outputs"
    )
    parser.add_option(
        "-i","--input" ,dest="input",
        default=datasetsdir + "/htcondor/pythiafiles/ee_ZZ.txt",
        help="input file"
    )    
    parser.add_option(
        "-s","--script", dest="script",
        default=datasetsdir + "/htcondor/scripts/simple_papas_condor.py",
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

def setup_condor_directories(subdir, base_outputdir):
    '''Creates a subdirectory in the current directory and in the output directory.
    The subdirectory in the current directory will be used to contain:-
        various scripts such as finish.sh, finish.sub etc
        the dag log and output files
        output/log/error directories used for the condor runs,
    @param: the nameof the subdirectory which will be used to contain the errors and logs etc
    @param: the name of the output directory (base) where a subdir will also be created to hold 
    the outputs.
    '''
    #make the working directory (inside the current directory)
    call(["mkdir", subdir])
    print "made subdirectory " +  subdir 
    #make the log output and error directories needed for condor
    call(["mkdir", subdir+"/log"]) 
    call(["mkdir", subdir+"/output"]) 
    call(["mkdir", subdir+"/error"]) 
    #create a subdirectory in the outputs directory
    basedir = ''.join((base_outputdir, subdir))
    call(["mkdir", basedir])

    #copy the files in $FCCDATASETS/htcondor/base/ into the working directory to be used for the condor run
    os.system("cp $FCCDATASETS/htcondor/base/* " + subdir)

def write_condor_software_yaml(subdir, filename="software.yaml"):
    ''' works out and writes a software.yaml file containing 
    details of software versions
    It uses the env variables to search for software.
    For software on fcc stack the stack path will be used.
    For software with a git version, the git details will be used
    '''
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
    env_versions.write_yaml('/'.join([subdir,filename]))
    
def write_condor_parameters_yaml(subdir, filename="parameters.yaml"):
    ''' writes the parameters.yaml file to both the work and output directories
    @param subdir: the name of the subdirectory
    @param filename: the name of the output yaml file
    '''
    parameters = Parameters()
    parameters.add("base_outputdir", base_outputdir) # the base eos path (the subdirectory below will be appended to this)
    parameters.add("pythiafile", options.pythia) # full path to the pythia file
    parameters.add("subdirectory", subdir) # subdirectory name for this run, there will be a dir with this name in the work and output locations
    parameters.add("script", options.script) #fccsw script to be run
    parameters.add("nevents", options.nevents) #number of events
    parameters.add("nruns", options.nruns) #number of runs
    #create a parameters yaml in the working directory
    parameters.write_yaml('/'.join([subdir,fname]))
    #also make one in the output directory
    parameters.write_yaml('/'.join([basedir,fname]))
    
    
def setup_condor_dag_files(subdir, nevents, runs, rate = 50000):
    '''
    writes dag job information to the run.dag file
    @param nevents: how many events per fcc papas run
    @param runs: how many fcc papas runs
    @param rate: number of events that could (easily) be run in a hour
       
    '''
    #create a dag file which will list all the jobs needed
    outfile =  subdir + "\/run.dag"
    for c in range(runs):
        os.system('echo Job A{} run.sub >> {} '.format(str(c), outfile))
        os.system('echo Vars A{} runnumber=\\\"{}\\\"  >> {}' .format( str(c) , str(c) , outfile))
    os.system('echo FINAL FO finish.sub >> {}'.format(outfile))
    
    #automatically choose queue based on rate,
    flavour="expresso"  
    if nevents>16*rate: #
        flavour="tomorrow" # 1 day
    elif nevents>4*rate:
        flavour="workday" # 8 hours
    elif nevents>2*rate:
        flavour="longlunch" # 2 hours
    elif nevents>rate:
        flavour="microcentury"  # 1 hour
    
    print "job is flavour: " + flavour
    outfile =  subdir + "\/run.sub"
    os.system("echo +JobFlavour = " + flavour +" >> " + outfile)
    os.system("echo Queue >> " + outfile)
      


if __name__ == '__main__':
    ''' 
    Usage: python $FCCDATASETS/htcondor/start.py -e base_outputdir -i inputfile -s script -n nevents -r runs
    '''    
    
    #read in the command line options
    parser = setup_condor_parser()
    (options,args) = parser.parse_args()
    if len(args) != 0:
        parser.print_usage()
        sys.exit(1)

    #extract options and create condor_parameters class to hold the run parameters
    #this will also construct a unique subdirectory name
    condor_parameters = CondorParameters(options)
   
    #create work and output directories 
    setup_condor_directories(condor_parameters["subdirectory"], condor_parameters["base_outputdir"])
    #create the dag files needed for the run
    setup_condor_dag_files(condor_parameters["subdirectory"], condor_parameters["nevents"], condor_parameters["runs"])
    #write parameters to working directory
    condor_parameters.write_yaml(condor_parameters["subdirectory"])    
    #write software and paramater yaml files to the output location 
    outputsub= condor_parameters["base_outputdir"] + "/" + condor_parameters["subdirectory"]    
    write_condor_software_yaml(outputsub )
    condor_parameters.write_yaml(outputsub)
    print "wrote yaml files to: " + outputsub
    os.system( "ls -l " + outputsub  )
    
    # move to the working directory and launch the dag job
    os.chdir(condor_parameters["subdirectory"])
    exit=1
    from sys import platform
    print platform
    while platform == "linux2" and exit<>0:
        print "submit to condor"
        exit = os.system( "condor_submit_dag -update_submit run.dag ; touch startdag.txt")

    #return to original directory
    os.chdir("..")
    print "finished setup"
