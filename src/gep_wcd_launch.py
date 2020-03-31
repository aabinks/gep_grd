__author__ = 'Adam Amos-Binks'

'''
Created on March 25, 2020
Launch WCD for a all problems of a domain and save output in GEP locations
@author: adamab
'''

import os
import time
import shutil
import sys
import grd_evaluator
import grd_options

def gep_wcd_launch(grd_dir, domain_name):

    #setup filenames and directories for output and copying
    gep_data_path = os.path.join(*[grd_dir, "gep", "data", domain_name])
    gen_files_path = os.path.join(grd_dir, "gen_files")
    log_files_path = os.path.join(grd_dir, "log_files")
    wcd_results_filename = "grd_log_reduction.txt"
    wcd_results_filepath = os.path.join(log_files_path, wcd_results_filename)

    #exit if we can't find the GEP destination for all WCD output
    if (not(os.path.exists(gep_data_path))):
        print("Exiting, can't find: " + gep_data_path)
        sys.exit(0)

    #get all the problems in the domain's directory
    problem_dirs = [x[1] for x in os.walk(gep_data_path)][0]
    print("Running grd_evaluator_reduce for domain: " + domain_name + " and problems: " + ", ".join(problem_dirs))

    #loop through each problem and call run the GRD process for WCD
    for problem_dir in problem_dirs:
        problem_name = os.path.basename(problem_dir).split(".")[0]
        problem_path = os.path.join(gep_data_path, problem_name)
        
	#TODO check the harded coded params below to make sure they are correct, we may want "all_pairs" instead of "max" for -v
        exec_array = [ "-o", os.path.join(gep_data_path, "domain.pddl"), "-p", os.path.join(problem_path, "template.pddl"), "-y", os.path.join(problem_path, "hyps.dat"), "-c", "WcdReduce-LatestSplit", "-g", "1", "-b", "NA", "-u", "NA", "-f", "True", "-v", "all_pairs", "-a", "NA"]

	#For easy reference above
	#print ( "-e  --experiment <file or folder>  Plan Recognition experiment files (tar'ed)",file =  sys.stderr)
	#print ( "-d  --destination folder (the subfolder of pgrd_defs.gen_files where the files are generated)",file = sys.stderr )
	#print ( "-c  --calculation method    the method to be applied",file =  sys.stderr)
	#print ( "-v  --combinations examined - either max over all pairs or the wcd of each pair",file =  sys.stderr)
	#print ( "-h  --help                       Get Help",file =  sys.stderr)
	#print ( "-t  --max-time <time>            Maximum allowed execution time (defaults to 1800 secs)",file =  sys.stderr)
	#print ( "-m  --max-memory <time>          Maximum allowed memory consumption (defaults to 1Gb)",file =  sys.stderr)
	#print ( "-x  --done-file-name          task names that need not be calculated",file =  sys.stderr)
	#print ( "-o  --domain-file-name         grd domain file name(when specifing files instead of folder)",file =  sys.stderr)
	#print ( "-p  --temPlate-file-name        grd template file name(when specifing files instead of folder)",file =  sys.stderr)
	#print ( "-y  --hyps-file-name        grd hyps file name(when specifing files instead of folder)",file =  sys.stderr)
	#print ( "-b  --obs-file-name        grd non-observable actions file name(when specifing files instead of folder)",file =  sys.stderr)
	#print ( "-a  --action-tokens-file-name      grd action token file name(when specifing files instead of folder)",file =  sys.stderr)
	#print ( "-u  --sub-optimal-bound-array",file =  sys.stderr)
	#print ( "-f  --delete-log-folders  should the log folders be deleted",file =  sys.stderr)
	#print ( "-r  --rec-obs-file-name     reciproce-observability actions file name(when specifing files instead of folder)",file =  sys.stderr)
	#print ( "-g  --design-budget-array",file =  sys.stderr)
	#print ( "-k  --token-file-string",file =  sys.stderr)
	#print ( "-i  --actions-to-remove",file =  sys.stderr)
	#print ( "-z  --actions-constraints",file =  sys.stderr)
	#print ( "-n  --domain",file = sys.stderr)
        
        #Error when calling main in grd_evaluator, so just running the contents
        #grd_evaluator.main(exec_array)
        options = grd_options.Program_Options( exec_array )
        grd_evaluator.evaluate(options)

        #move results and rename with timestamp
        timestr = time.strftime("%Y%m%d_%H%M%S")
        shutil.copyfile(wcd_results_filepath, os.path.join(problem_path, timestr + "_" + wcd_results_filename) )
        shutil.make_archive(os.path.join(problem_path, timestr + "_gen"), 'zip', gen_files_path)
        shutil.make_archive(os.path.join(problem_path, timestr + "_log"), 'zip', log_files_path)

if __name__=="__main__":

    if len(sys.argv) < 3:
        print("Usage: gep_wcd_launch grd_path domain_name")
        sys.exit()
    else:
        grd_path = sys.argv[1]
        domain_name = sys.argv[2]

        gep_wcd_launch(grd_path, domain_name)
