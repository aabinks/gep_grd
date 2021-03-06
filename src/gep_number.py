__author__ = 'Anonymous for peer review'

'''
Created on May 18, 2020
Utility to investigate how domain changes affect GEP number
@author: anon
'''

#imports
import pandas as pd
import sys
import os
import grd_planning
from pddl.parser import Parser
import grounding
import time

def get_ground_task(domain_filepath, problem_filepath):
    parser = Parser(domain_filepath, problem_filepath)
    domain = parser.parse_domain()
    problem = parser.parse_problem(domain)
    task = grounding.ground(problem)
    
    return task

def get_gep_number(task):
    
    effects = {}
    gep_number = 0
    already_counted = False
  
    #iterate through ground actions (operators)
    for operator in task.operators:
        for effect in operator.del_effects:
            if (effect in effects.keys()):
                effects[effect].add(operator)
            else:
                effects[effect] = {operator}

    for operator in task.operators:
        already_counted = False
        for precondition in operator.preconditions:
            if (not(already_counted) and precondition in effects and operator not in effects[precondition]):
                gep_number += 1
                already_counted = True

    return gep_number

def gep_number_matrix(domain_path):
    dirs = [x[1] for x in os.walk(os.path.dirname(domain_path))][0]
    problem_names = [directory for directory in dirs if directory.startswith("p") ]
    #problem_dirs.remove("results")
    #problem_dirs.remove("domains")
    gep_results_df = pd.DataFrame(columns=["domain", "problem", "gep_number"])

    #check output dir
    for domain_file in os.listdir(domain_path):
        if (domain_file.endswith(".pddl")):
            for problem_name in problem_names:
                problem_filepath = os.path.join(*[os.path.dirname(domain_path),problem_name,"hyp_0_problem.pddl" ])
                task = get_ground_task(os.path.join(domain_path,domain_file), problem_filepath)
                gep_number = get_gep_number(task)
                d = {"domain":[domain_file.split(".")[0]], "problem":[problem_name], "gep_number":[gep_number]}
                gep_number_df = pd.DataFrame(data=d)
                gep_results_df = pd.concat([gep_results_df, gep_number_df])

    print(gep_results_df.reset_index(drop=True))
    gep_matrix_df = gep_results_df.reset_index(drop=True).pivot(index='domain', columns="problem", values="gep_number").reset_index()
    
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
