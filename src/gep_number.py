__author__ = 'Adam Amos-Binks'

'''
Created on May 18, 2020
Utility to investigate how domain changes affect GEP number
@author: adamab
'''

#imports
import pandas as pd
import sys
import os
import grd_planning, grd_defs
#import pyperplan._parse, pyperplan._ground
from pddl.parser import Parser
import grounding
import time

def get_ground_task(domain_filepath, problem_filepath):
    parser = Parser(domain_filepath, problem_filepath)
    domain = parser.parse_domain()
    problem = parser.parse_problem(domain)
    task = grounding.ground(problem)
    
    return task

def get_gep_number(ground_task):
    
    effects = []
    gep_number = 0
    already_counted = False
  
    #iterate through ground actions (operators)
    for operator in task.operators:
        for effect in operator.preconditions:
            effects.append()
  
    for operator in task.operators:
        already_counted = False
        for precondition in operator.preconditions:
            if (precondition in effects and not(already_counted)):
                gep_number += 1
                already_counted = True

    return gep_number

def gep_number_matrix(domain_path):
    dirs = [x[1] for x in os.walk(os.path.dirname(domain_path))][0]
    problem_names = [dir if dir.beginswith("p") for dir in dirs]
    #problem_dirs.remove("results")
    #problem_dirs.remove("domains")
    gep_results_df = pd.Dataframe()

    #check output dir
    for domain_file in os.listdir(domain_path):
        if (domain_file.endswith(".pddl")):
            for problem_name in problem_names:
                problem_filepath = os.path.join(*[os.path.dirname(domain_path),problem_name,"hyp_0.pddl" ])
                task = get_ground_task(domain_filepath, problem_filepath)
                gep_number = gep_number(task)      
                gep_results_df = pd.concat([gep_results_df, pd.Dataframe(data={"domain":domain_file.split(".")[0], "problem":problem_name, "gep_number":gep_number})])

    gep_matrix_df = gep_results_df.pivot(columns="problem", values="gep_number")
    
    return gep_matrix_df
    
if __name__=="__main__": 
    if len(sys.argv) < 2:
        print("Usage: gep_number domain_path")
        sys.exit()
    else:
        domain_path = sys.argv[1]
        output_filename = "_".join([time.strftime("%Y%m%d_%H%M%S"), "all_probs_gep_numbers.csv"])
        gep_matrix_df = gep_number_matrix(domain_path)
        print(gep_matrix_df)
        
        gep_matrix_df.to_csv( os.path.join(domain_path, output_filename) )
