__author__ = 'Adam Amos-Binks'

'''
Created on March 25, 2020
Launch WCD for a all problems of a domain and save output in GEP locations
@author: adamab
'''

import subprocess
import os
import time
import shutil
import sys
#import grd_evaluator

def gep_wcd_launch(grd_dir, domain_name):

    gep_data_path = os.path.join(*[grd_dir, "gep", "data", domain_name])
    #domain_path = os.path.join(*[grd_dir,"benchmarks", domain_name])
    gen_files_path = os.path.join(grd_dir, "gen_files")
    log_files_path = os.path.join(grd_dir, "log_files")

    problem_dirs = [x[1] for x in os.walk(gep_data_path)][0]

    #problem_dirs = ['p01', 'p02', 'p03', 'p04', 'p05']
    wcd_results_filename = "grd_log_reduction.txt"
    wcd_results_filepath = os.path.join(log_files_path, wcd_results_filename)

    for problem_dir in problem_dirs:
	#print(problem_dirs)
        problem_name = os.path.basename(problem_dir).split(".")[0]
        problem_path = os.path.join(gep_data_path, problem_name)

        #TODO this block can probably be removed
	#execute string
        exec_string = "./scripts/grd_evaluator_reduce " + os.path.join(gep_data_path, "domain.pddl") +" "+ os.path.join(problem_path, "template.pddl") + " " + os.path.join(problem_path, "hyps.dat") + " LatestSplit 1 NA NA True max NA"
	#grd_evaluator.main(["grd_evaluator_reduce", os.path.join(gep_data_path, "domain.pddl"), os.path.join(problem_path, "template.pddl"), os.path.join(problem_path, "hyps.dat"), "LatestSplit", "1", "NA", "NA", "True", "max", "NA"])
        #exec_string = ["grd_evaluator_reduce", os.path.join(gep_data_path, "domain.pddl"), os.path.join(problem_path, "template.pddl"), os.path.join(problem_path, "hyps.dat"), "LatestSplit", "1", "NA", "NA", "True", "max", "NA"]
        print(exec_string)
        #subprocess.call(exec_string,cwd=grd_dir+"/scripts")
        
	#TODO below doesn't work and issue #1 on this repo refers to the error from .main() below
	#TODO also check the harded coded params below to make sure they are correct, we may want "all_pairs" instead of "max" for -v
        #python3 ./src/grd_evaluator.py -o $1 -p $2 -y $3 -c $4 -g $5 -b $6 -u $7 -f $8 -v $9 -a ${10}
        exec_array = ["WcdReduce", "-o", os.path.join(gep_data_path, "domain.pddl"), "-p", os.path.join(problem_path, "template.pddl"), "-y", os.path.join(problem_path, "hyps.dat"), "-c", "LatestSplit", "-g", "1", "-b", "NA", "-u", "NA", "-f", "True", "-v", "max", "-a", "NA"]
        grd_evaluator.main(exec_array)

        #move results and rename with timestamp
        timestr = time.strftime("%Y%m%d_%H%M%S")
	#dest_filepath = os.path.join(*[gep_data_path, domain_name, problem_name])
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
#         grd_path = "\home\aamosbinks\git\goal-recognition-design"
#         domain_name = "easy-grid"
        gep_wcd_launch(grd_path, domain_name)
