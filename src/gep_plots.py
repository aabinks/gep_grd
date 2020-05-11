__author__ = 'Adam Amos-Binks'

'''
Created on April 3, 2020
Analyze contents of a WCD results file and compare against GEP method
@author: adamab
'''

#imports__author__ = 'Adam Amos-Binks'

'''
Created on April 3, 2020
Analyze contents of a WCD results file and compare against GEP method
@author: adamab
'''

#imports
import pandas as pd
import sys
import os
from matplotlib import pyplot as plt
import matplotlib as mpl
import seaborn as sns
%matplotlib inline
import numpy as np
pd.set_option('display.max_rows', None)

def gep_overall_min_wcd_hist(gep_df, output_filepath_prefix, budget):

    #filter out GEP plans that are not GEP solutions (they would not 'arrrive' in time)
    plot_df = gep_df[gep_df["gep_solution_action_cost"] <= (gep_df["curResFindWcd.wcd_value"] + budget)]

    #Group by as an action removal may have several GEP solution plans
    min_df = plot_df[["problem", "hyp_A", "hyp_B","min_wcd", "init_wcd",
                      "gep_min_wcd"]].groupby(by=["problem", "hyp_A", "hyp_B"]).min().reset_index()
    
    #transform and sort dataframe to make it easy to plot with sns
    melt_df = pd.melt(min_df, id_vars=["problem", "hyp_A", "hyp_B"], value_vars=["min_wcd", "init_wcd","gep_min_wcd"],
        var_name='method', value_name='action_cost')
    melt_df.sort_values(by=["problem", "method"], inplace=True)
    
    #Set general plot properties
    sns.set_style("white")
    sns.set_context({"figure.figsize": (14, 5)})
    
    #plot
    gep_grd_init_bar_plot = sns.barplot(x = melt_df["problem"], y = melt_df["action_cost"], hue=melt_df["method"], hue_order=["min_wcd", "gep_min_wcd", "init_wcd"])    

    #Optional code - Make plot look nicer
    h, l = gep_grd_init_bar_plot.get_legend_handles_labels()
    gep_grd_init_bar_plot.legend(h, ['GRD WCD Reduction', 'GEP WCD Reduction', 'Initial (No Reduction)'], prop={'size':24})
    sns.despine(left=True)
    gep_grd_init_bar_plot.set_ylabel("Minimum WCD")
    gep_grd_init_bar_plot.set_xlabel("Problems in easy-grid$^{\prime}$")

    #Again, optional - set fonts to consistent 16pt size
    for item in ([gep_grd_init_bar_plot.xaxis.label, gep_grd_init_bar_plot.yaxis.label] +
                 gep_grd_init_bar_plot.get_xticklabels() + gep_grd_init_bar_plot.get_yticklabels()):
        item.set_fontsize(24)

    output_filepath = output_filepath_prefix + "_budget_" + str(non_opt_budget) + "_overall_min_wcd.png"
    fig = gep_grd_init_bar_plot.get_figure()
    fig.savefig(output_filepath, dpi=400)
    print("Just saved: " + output_filepath)
    
    return output_filepath
    ######################
def gep_action_min_wcd_hist(gep_df, output_filepath_prefix, budget):

    sns.set_context({"figure.figsize": (14, 5)})
    chart2, ax2 = plt.subplots()
        
    #Groupby to get the min WCD for each action removal (removes multiple GEP problems/solutions)
    plot_df = gep_df[["problem", "action_removed", "min_wcd", "init_wcd", "curResFindWcd.wcd_value",
                      "gep_min_wcd"]].groupby(by=["problem", "action_removed", "min_wcd", "init_wcd", "curResFindWcd.wcd_value"]).min().reset_index()
    
    #transform dataframe to make it easier to plot
    min_melt_df = pd.melt(plot_df, id_vars=["problem", "action_removed", "min_wcd", "init_wcd"], 
                          value_vars=["curResFindWcd.wcd_value", "gep_min_wcd"], var_name='method', value_name='wcd_reduction')

    #filter out the actions that achieve the minimum WCD when the WCD is different from the initial
    count_min_melt_df = min_melt_df.loc[ (min_melt_df["wcd_reduction"] == min_melt_df["min_wcd"]) & 
                                        (min_melt_df["wcd_reduction"] < min_melt_df["init_wcd"]), ["problem", "method"]]    
    
    #groupby to count the actions that achieve the minimum WCD
    count_min_melt_df_grouped = count_min_melt_df.groupby(by=["problem","method"]).size().reset_index()
    
    #add in some filler data
    #TODO fix this hack into somethign more generic
    d = {'problem': ["p02", "p03"], "method":["gep_min_wcd","gep_min_wcd"], 0:[0,0]}
    df_suppl = pd.DataFrame(data=d)
    count_min_melt_df_grouped = count_min_melt_df_grouped.append(df_suppl)
    count_min_melt_df_grouped.columns = ["problem", "method", "actions"]
    count_min_melt_df_grouped.sort_values(by=["problem"], inplace=True)
    
    #plot
    gep_grd_action_hist = sns.barplot(x = count_min_melt_df_grouped["problem"], y = count_min_melt_df_grouped["actions"], hue=count_min_melt_df_grouped["method"], ax=ax2)
    
    #Optional code - Make plot look nicer
    h, l = gep_grd_action_hist.get_legend_handles_labels()
    gep_grd_action_hist.legend(h, ['GRD WCD Reduction', 'GEP WCD Reduction'], prop={'size':24})
    sns.despine(left=True)
    gep_grd_action_hist.set_ylabel("Min WCD Action Removals")
    gep_grd_action_hist.set_xlabel("Problems in easy-grid$^{\prime}$")

    #Again, optional - set fonts to consistent 16pt size
    for item in ([gep_grd_action_hist.xaxis.label, gep_grd_action_hist.yaxis.label] +
                 gep_grd_action_hist.get_xticklabels() + gep_grd_action_hist.get_yticklabels()):
        item.set_fontsize(24)    
    
    output_filepath = output_filepath_prefix+ "_budget_" + str(non_opt_budget) + "_action_min_wcd.png"
    fig = gep_grd_action_hist.get_figure()
    fig.savefig(output_filepath, dpi=400)
    print("Just saved: " + output_filepath)
    
    return output_filepath

def gep_plot(data_filepath, output_filepath_prefix, budget=0):

    #read in raw data and filter out action removals without a GEP solution
    raw_df = pd.read_csv(data_filepath)
    gep_df = raw_df[(raw_df["gep_solution_action_count"] > -1)]
    gep_df["gep_min_wcd"] = np.where( (gep_df["curResFindWcd.wcd_value"] == 12072) | (gep_df["gep_solution_action_count"] > (gep_df["curResFindWcd.wcd_value"] + budget)), 
                            gep_df["init_wcd"], gep_df["curResFindWcd.wcd_value"])

    plot_names = []
    plot_names.append(gep_overall_min_wcd_hist(gep_df, output_filepath_prefix, budget))
    plot_names.append(gep_action_min_wcd_hist(gep_df, output_filepath_prefix, budget))
    
    return plot_names
    
if __name__=="__main__": 
    if len(sys.argv) < 3:
        print("Usage: gep_plots data_filepath non_opt_budget" )
        sys.exit()
    else:
        data_filepath = sys.argv[1]
        non_opt_budget = sys.argv[2]

        if (not(os.path.exists(data_filepath))):
            print("ERROR: Couldn't find " + data_filepath )
            sys.exit()
            
        output_folder = os.path.join( os.path.dirname(data_filepath), "fig" )
        if (not(os.path.exists(output_folder))):
            os.mkdir(output_folder)

        output_filepath_prefix = os.path.join(output_folder, os.path.basename(data_filepath).split(".")[0])
        output_filenames = gep_plot(data_filepath, output_filepath_prefix, non_opt_budget)

        print("-----------------------------------------------------------\n")
        print("GEP plots finished, check out the results here:\n" + output_folder)
        print("-----------------------------------------------------------\n")
