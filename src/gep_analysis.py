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
import io

def get_ground_task(domain_filename, problem_filename):
    parser = Parser(domain_filename, problem_filename)
    domain = parser.parse_domain()
    problem = parser.parse_problem(domain)
    task = grounding.ground(problem)
    return task

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

def analyze_wcd(col_names, problem_folder, data_filepath, domain_filename, problem_filename, task):
    
    #Get load the grd intermediate output data from csv

    wcd_df = load_data(data_filepath, col_names)
    
    #parse and extract the action removal design modification from the unholy mess
    action_remove_index = 0
    wcd_df["action_removed"] = "(" + wcd_df["op_comb.getString()"].str.replace("[","").str.replace("]","").str.split("--", expand=True)[action_remove_index].str.strip() + ")"
    wcd_df["problem"] = os.path.basename(problem_folder)
    wcd_df["domain"] = os.path.basename(os.path.dirname(problem_folder))
    wcd_df["domain_filename"] = domain_filename
    wcd_df["problem_filename"] = problem_filename
    wcd_df["gep_number"] = get_gep_number(task)
    
    #extract hypothesis
    wcd_df[["hyp_A","hyp_B"]] =  wcd_df["init_wcd_hyps"].str.split("'", expand=True)[[1,3]]
    
    #get the goal from the planning problem
    #problem_goals = get_problem_goals(os.path.join(data_folder, problem_filename))
    
    #only return rows that have an action removal design mod
    return_df = wcd_df[ (wcd_df["action_removed"] != "()")]
    
    #TODO may want to filter out action removals that are equal to the min WCD for this problem
    return return_df

def load_data(data_filepath, col_names):
    
    df = pd.read_csv(data_filepath, sep = ";", names = col_names)
    
    return df

def format_pddl_to_filename(pddl):
    return pddl.replace("(", "").replace(")", "").strip().replace(" ","_")

def get_gep_number(task):

    #iterate through ground actions (operators)
#    for operator in task.operators:
        #if we have found the removed operator, concatenate its preconditions in a string
#        if (operator.name == action_removed):
#            found_operator = True
#            for precondition in operator.preconditions:

    print("Number of ground actions is: " + str(len(task.operators)))
    return str(len(task.operators))

def generate_gep_problem(row, output_folder, problem_folder):
    
    domain_filename = os.path.join(problem_folder, row[0])
    problem_filename = os.path.join(problem_folder, row[1])
    gep_action_removed  = row[2]
    gep_problem_filestring_prefix = "gep_hyp_" + format_pddl_to_filename(row[3]) + "_" + format_pddl_to_filename(row[4]) + "_act_" + format_pddl_to_filename(gep_action_removed)
    #gep_problem_filestrings = []
    in_init = True
    gep_problem_precondition_filestring_pairs = []
    
    #loop through each line in the problem file and add it to a file buffer as we may need to make multiple gep problem files
    with open(problem_filename) as problem_file:
            file_buff = io.StringIO()
            for line in problem_file:

                #If we arrive at the goal, it is now time to generate one gep problem file per negated precondition of the removed action
                if( "(:goal" in line):
                    in_init = False
                    file_buff.write(line)
                    file_buff.write("(and")
                    gep_problem_goals = negated_action_preconditions_to_pddl_string(gep_action_removed, domain_filename, problem_filename)

                    #for each negated precondition, setup the excessively long filename
                    for gep_problem_goal in gep_problem_goals:
                        gep_problem_filestring = gep_problem_filestring_prefix + "_pre_" + format_pddl_to_filename(gep_problem_goal) + ".pddl"
                        gep_problem_filename = os.path.join(output_folder, gep_problem_filestring)
                        gep_problem_precondition_filestring_pairs.append([gep_problem_goal, gep_problem_filestring])

                        #create a new gep problem file and write the file buff contents and the unique precondition
                        with open(gep_problem_filename, "w") as gep_problem_file:
                            print(file_buff.getvalue(), file = gep_problem_file)
                            print(gep_problem_goal + "\n)\n)\n)\n", file = gep_problem_file)

                #for all other line sbeside the goal, just copy into file buffer
                elif (in_init):
                    file_buff.write(line)
            file_buff.close()
                        
    return gep_problem_precondition_filestring_pairs


def negated_action_preconditions_to_pddl_string(action_removed, domain_filename, problem_filename):
    
    neg_pre_pddl_strings = []
    found_operator = False

    #Ground the problem (e.g. generate all ground actions from lifted actions in domain)
    #Note: do not use directly from pyperplan, something weird on the imports and it won't compile
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
                neg_pre_pddl_strings.append("(not " + precondition + ")")

    #for some reason, operator not found in domain
    if not found_operator:
        #TODO something more elegant
        neg_pre_pddl_strings.append( "ERROR - Probably wrong problem")
        print(neg_pre_pddl_strings)
    return neg_pre_pddl_strings


def generate_gep_solution(row, output_folder, problem_folder):

    domain_filename = os.path.join(problem_folder, row[0])
    gep_problem_filename = os.path.join(output_folder, row[1])
    
    #use grd_planning.py to call fast-downward planner
    plan_cmd, planning_failed, signal = grd_planning.perform_planning(output_folder, domain_filename, gep_problem_filename, time_limit = grd_defs.DEFAULT_TIME_LIMIT, heuristic = 'lmcut()') #:#heuristic = 'ipdb()'):
    
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
        gep_solution_filename = "NA"#"No Solution Found"

    return gep_solution_filename

def analyze_gep_solution(row, output_folder):
    
    gep_solution_filename = os.path.join(output_folder,row[0])
    action_count = -1
    action_cost = -1
    in_actions = True
    
    if (os.path.exists(gep_solution_filename)):
        action_count = 0
        action_cost = 0
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


def gep_wcd_analysis(output_folder, problem_folder, data_filepath, domain_filename, problem_filename):
    
    task = get_ground_task(os.path.join(problem_folder, domain_filename), os.path.join(problem_folder, problem_filename))
    # Obtained from grd git repo
    col_names = ["cur_grd_task.full_template_file_name","cur_grd_task.hyps_file_name","wcd_calc_method","budget_string","init_wcd","min_wcd","init_wcd_hyps"," opt_op_comb.getString()","wcd_calc_time","optimal_costs"," cur_exec_time"," explored_op_comb"," total_num_of_nodes_explored"," total_num_of_states_explored","reduction_per_budget_exhausted","curResFindWcd.wcd_value","op_comb.getString()","design_budget_array_string","cur_grd_task.observability_file_name","cur_grd_task.action_tokens_file_name","cur_grd_task.get_sub_optimal_bound_array_string()"]

    #   2.  parse GRD output to find get a list of action/reductions
    grd_df = analyze_wcd(col_names, problem_folder, data_filepath, domain_filename, problem_filename, task)
    print("Analyzing GRD output with length: " + str(len(grd_df)))
    
    #   3.  generate a gep problem with init state from problem and goal state as disjunction of removed action’s (negated) preconditions.
    grd_df['gep_problem_pre_file'] = grd_df[['domain_filename',"problem_filename",'action_removed', "hyp_A", "hyp_B"]].apply(generate_gep_problem, args=(output_folder, problem_folder,), axis=1)
    
    # since we have multiple gep_problems stored in the same column entry per action removal, expand it out
    grd_df = grd_df.explode('gep_problem_pre_file')

    # now expand out the negated precondition and problem filename
    grd_df[["gep_problem_precondition", "gep_problem"]] = pd.DataFrame(grd_df["gep_problem_pre_file"].values.tolist(), index = grd_df.index)
    
    #   4.  solve the GEP problem (ie generate a plan)
    grd_df['gep_solution'] = grd_df[['domain_filename','gep_problem','action_removed']].apply(generate_gep_solution, args=(output_folder, problem_folder,), axis=1)

    #   5.  analyze the GEP solution (ie. number of steps)
    grd_df[['gep_solution_action_count','gep_solution_action_cost']] = grd_df[["gep_solution"]].apply(analyze_gep_solution, args=(output_folder,), axis=1, result_type='expand')
    
    return grd_df

if __name__=="__main__": 
    if len(sys.argv) < 2:
        print("Usage: gep_analysis grd_results_folder")
        sys.exit()
    else:
        grd_results_folder = sys.argv[1]

        #infer domain-problem directories and the params below
        #domain_name = os.path.basename(grd_results_folder).split("_")[0]
        domain_folder = os.path.dirname(os.path.dirname(grd_results_folder))
        domain_filename = "domain.pddl"
        hyp_problem_prefix = "hyp"

        output_folder = os.path.join(grd_results_folder, "gep_problems")
        if (not(os.path.exists(output_folder))):
                os.mkdir(output_folder)

        budget = 0
        hyp_opts = "max"

        gep_wcd_analysis_df = pd.DataFrame()
        for grd_results in os.listdir(grd_results_folder):
                if (grd_results.endswith("_grd_log_reduction.txt")):
                    budget = grd_results.split("_")[3]
                    hyp_opts = grd_results.split("_")[4]
                    found_problem_file = False
                    problem_name = grd_results.split("_")[2]
                    problem_folder = os.path.join(domain_folder, problem_name)
                    #iterate through all the hypothesis problem files to get one that we can ground
                    for problem_filename in os.listdir(problem_folder):
                        if(problem_filename.endswith("pddl") and problem_filename[:len(hyp_problem_prefix)] == hyp_problem_prefix and not(found_problem_file) ):
                            found_problem_file = True
                            #run the gep analysis pipeline
                            problem_df = gep_wcd_analysis(output_folder, problem_folder, os.path.join(grd_results_folder, grd_results), domain_filename, problem_filename)
                            gep_wcd_analysis_df = pd.concat([gep_wcd_analysis_df, problem_df])         
        #Output to csv
	#filter columns
        gep_wcd_analysis_df["budget"] = budget
        gep_wcd_analysis_df["hyp_opts"] = hyp_opts

        output_cols = ["domain", "problem", "gep_number", "budget", "hyp_opts", "hyp_A", "hyp_B", "gep_solution_action_count", "gep_solution_action_cost", "curResFindWcd.wcd_value", "init_wcd", "min_wcd", "action_removed", "gep_problem_precondition", "gep_problem", "gep_solution", "wcd_calc_method"]
        output_filename = "_".join(grd_results.split("_")[:2]) + "_gep_all_probs.csv"
        gep_wcd_analysis_df[output_cols].to_csv( os.path.join(grd_results_folder, output_filename) )

        print("-----------------------------------------------------------\n")
        print("GEP analysis finished, check out the results here:\n" + os.path.join(grd_results_folder, output_filename))
        print("-----------------------------------------------------------\n")       
