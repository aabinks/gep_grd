__author__ = 'Adam Amos-Binks'

'''
Created on March 25, 2020
Analyze contents of a WCD results file and compare against GEP method
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

def get_problem_goals(problem_filepath):
    in_goal = False
    goal_tokens = []
    with open(problem_filepath, "r") as problem_file:
        for line in problem_file:
            line = line.strip()
            if( "(:goal" in line or in_goal):
                in_goal = True
                line_tokens = line.replace(")","),").split(",")
                goal_tokens.extend(line_tokens)
                #TODO filter out '', and, or, ), goal tokens
    return goal_tokens

def analyze_wcd(col_names, data_folder, data_filename, domain_filename, problem_filename):
    
    #Get load the grd intermediate output data from csv
    data_filepath = os.path.join(data_folder, data_filename)
    wcd_df = load_data(data_filepath, col_names)
    
    #parse and extract the action removal design modification from the unholy mess
    action_remove_index = 0
    wcd_df['action_removed'] = wcd_df["op_comb.getString()"].str.replace("[","").str.replace("]","").str.split("--", expand=True)[action_remove_index].str.strip()
    wcd_df["domain"] = domain_filename
    wcd_df["problem"] = problem_filename
    
    #extract hypothesis
    wcd_df[["hyp_0","hyp_1"]] =  wcd_df["init_wcd_hyps"].str.split("'", expand=True)[[1,3]]
    
    #get the goal from the planning problem
    #problem_goals = get_problem_goals(os.path.join(data_folder, problem_filename))
    
    #TODO make sure remainder of logical statement is needed/works
    #only return rows that have an action removal design mod for the correct hypothesis-problem combination
    return_df = wcd_df[ (wcd_df["action_removed"] != "")]# & ((wcd_df["hyp_0"].isin(problem_goals)) | (wcd_df["hyp_1"].isin(problem_goals))) ]
    
    #TODO may want to filter out action removals that are equal to the min WCD for this problem
    return return_df

def load_data(data_filepath, col_names):
    
    df = pd.read_csv(data_filepath, sep = ";", names = col_names)
    
    return df


def generate_gep_problem(row, data_folder):
    
    domain_filename = os.path.join(data_folder, row[0])
    problem_filename = os.path.join(data_folder, row[1])
    gep_action_removed  = row[2]
    
    gep_problem_filestring = "gep_" + gep_action_removed.strip().replace(" ","_") + "_" + row[1]
    gep_problem_filename = os.path.join(data_folder, gep_problem_filestring)
    in_init = True
    
    with open(problem_filename) as problem_file:
        with open(gep_problem_filename, "w") as gep_problem_file:
            for line in problem_file:
                line = line.strip()
                if( "(:goal" in line):
                    in_init = False
                    print(line, file = gep_problem_file)
                    print("(and", file = gep_problem_file)
                    gep_problem_goals = negated_action_preconditions_to_pddl_string(gep_action_removed, domain_filename, problem_filename) + "\n)\n)\n)\n"
                    print(gep_problem_goals, file = gep_problem_file)
                elif (in_init):
                    print(line, file= gep_problem_file)
                        
    return gep_problem_filestring


def negated_action_preconditions_to_pddl_string(action, domain_filename, problem_filename):
    
    pddl_string = ""
    found_operator = False
    #TODO add brackets in stored action name?
    action_removed = "(" + action + ")"

    #Ground the problem (e.g. generate all ground actions from lifted actions in domain)
    #Note do not use directly from pyperplan, something weird on the imports and it won't compile
    parser = Parser(domain_filename, problem_filename)
    domain = parser.parse_domain()
    problem = parser.parse_problem(domain)
    task = grounding.ground(problem)

    
    #iterate through ground actions (operators)
    for operator in task.operators:
        #if we have found the removed operator, concatenate its preconditions in a string
        if (operator.name == action_removed):
            found_operator = True
            for precondition in operator.preconditions:
		#TODO hack until figure this out, need new plannign problem per precondition?
                if(precondition.split(" ")[0] == "(is_free"):
                    pddl_string += "(not" + precondition + ") "

    #for some reason, operator not found in domain
    if not found_operator:
        #TODO something more elegant
        pddl_string = "ERROR - Probably wrong problem for this hypothesis"
        print(pddl_string)
    return pddl_string


def generate_gep_solution(row, data_folder):

    domain_filename = os.path.join(data_folder, row[0])
    gep_problem_filename = os.path.join(data_folder, row[1])
    
    #use grd_planning.py to call fast-downward planner
    plan_cmd, planning_failed, signal = grd_planning.perform_planning(data_folder, domain_filename, gep_problem_filename, time_limit = grd_defs.DEFAULT_TIME_LIMIT, heuristic = 'lmcut()') #:#heuristic = 'ipdb()'):
    
    #Change the solution plan name
    if (signal == 0):
        gep_solution_filename = os.path.basename(row[1]).split(".")[0] + ".plan"
        gep_solution_filepath = os.path.join(plan_cmd.destination_folder_name, gep_solution_filename)
        solution_filename = os.path.join(plan_cmd.destination_folder_name,'sas_plan')
        print(gep_problem_filename)
        print(solution_filename)
        print(gep_solution_filepath)
        os.renames(solution_filename, gep_solution_filepath)
    else:
        gep_solution_filename = "NA"#os.path.join(data_folder,'sas_plan1')#"NA"

    return gep_solution_filename

def analyze_gep_solution(row, data_folder):
    
    gep_solution_filename = os.path.join(data_folder,row[0])
    action_count = 0
    action_cost = 0
    in_actions = True
    
    if (os.path.exists(gep_solution_filename)):   
        with open(gep_solution_filename) as file:
            for line in file:
            
                #TODO this is a bit hacky, clean up later lol
                #if we are in the final line of the plan and action cost is explicitely calculated, parse it out
                if (in_actions and line[0] == ";"):
                    in_actions = False
                    line_tokens = line.split("=")
                    action_cost = int(line_tokens[1].strip().split(" ")[0])
            
                #action counter
                else:
                    action_count += 1
    
    return [action_count, action_cost]


def gep_wcd_analysis(data_folder, data_file, domain_file, problem_file):
    
    # Obtained from grd git repo
    col_names = ["cur_grd_task.full_template_file_name","cur_grd_task.hyps_file_name","wcd_calc_method","budget_string","init_wcd","min_wcd","init_wcd_hyps"," opt_op_comb.getString()","wcd_calc_time","optimal_costs"," cur_exec_time"," explored_op_comb"," total_num_of_nodes_explored"," total_num_of_states_explored","reduction_per_budget_exhausted","curResFindWcd.wcd_value","op_comb.getString()","design_budget_array_string","cur_grd_task.observability_file_name","cur_grd_task.action_tokens_file_name","cur_grd_task.get_sub_optimal_bound_array_string()"]

    #   2.  parse GRD output to find get a list of action/reductions
    grd_df = analyze_wcd(col_names, data_folder, data_file, domain_file, problem_file)
    print(len(grd_df))
    #   3.  generate a gep problem with init state from problem and goal state as disjunction of removed action’s (negated) preconditions.
    grd_df['gep_problem'] = grd_df[['domain','problem','action_removed']].apply(generate_gep_problem, args=(data_folder,), axis=1)
        
    #   4.  solve the GEP problem (ie generate a plan)
    grd_df['gep_solution'] = grd_df[['domain','gep_problem','action_removed']].apply(generate_gep_solution, args=(data_folder,), axis=1)

    #   5.  analyze the GEP solution (ie. number of steps)
    grd_df[['gep_solution_action_count','gep_solution_action_cost']] = grd_df[["gep_solution"]].apply(analyze_gep_solution, args=(data_folder,), axis=1, result_type='expand')
    
    return grd_df

if __name__=="__main__": 
    if False:#len(sys.argv) < 5:
        print("Usage: gep_analysis data_folder data_filename domain_filename hyp_problem_prefix")
        sys.exit()
    else:
        data_folder = sys.argv[1]
        data_filename = sys.argv[2]
        domain_filename = sys.argv[3]
        hyp_problem_prefix = sys.argv[4]

        gep_wcd_analysis_df = pd.DataFrame()
	#iterate through all the hypothesis problem files
        for problem_filename in os.listdir(data_folder):
            if(problem_filename.endswith("pddl") and problem_filename[:len(hyp_problem_prefix)] == hyp_problem_prefix):
                #run the gep analysis pipeline
                single_hyp_gep_wcd_analysis = gep_wcd_analysis(data_folder, data_filename, domain_filename, problem_filename)
                gep_wcd_analysis_df = pd.concat([gep_wcd_analysis_df, single_hyp_gep_wcd_analysis])

        #Output to csv
	#TODO filter columns, too much junk there now
        output_filename = "gep_" + hyp_problem_prefix + "_all.csv"
        print(os.path.join(data_folder, output_filename))
        gep_wcd_analysis_df.to_csv( os.path.join(data_folder, output_filename) )        
