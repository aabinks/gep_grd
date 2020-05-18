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

def get_ground_task(domain_filepath, problem_filepath):
    parser = Parser(domain_filepath, problem_filepath)
    domain = parser.parse_domain()
    problem = parser.parse_problem(domain)
    task = grounding.ground(problem)
    return task

def gep_number(domain_filepath, problem_filepath):

    task = get_ground_task(domain_filepath, problem_filepath)
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

if __name__=="__main__": 
    if len(sys.argv) < 2:
        print("Usage: gep_number domain_folder")
        sys.exit()
    else:
        domain_folder = sys.argv[1]
        
        gep_results_df = pd.Dataframe()
        
        #check output dir
        #TODO for each problem
        #TODO for each domain in each problem
        gep_number = gep_number(domain_filepath, problem_filepath)
        gep_results_df = pd.concat([gep_results_df, pd.Dataframe(data=[domain_filepath, problem_filepath, gep_number])])
        
