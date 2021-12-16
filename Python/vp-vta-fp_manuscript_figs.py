# -*- coding: utf-8 -*-
"""
Created on Thu Dec 16 11:55:32 2021

@author: Dakota
"""

import customFunctions

import shelve
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt


# #%% Load previously saved dfTidyAnalyzed (and other vars) from pickle
dataPath= r'./_output/' #'r'C:\Users\Dakota\Documents\GitHub\DS-Training\Python\\'

dfTidy= pd.read_pickle(dataPath+'dfTidyAnalyzed.pkl')

#load any other variables saved during the import process ('dfTidymeta' shelf)
my_shelf = shelve.open(dataPath+'dfTidymeta')
for key in my_shelf:
    globals()[key]=my_shelf[key]
my_shelf.close()

#%% Set plot options
sns.set_style("darkgrid")
sns.set_context('notebook')
sns.set_palette('tab10')

# sns.palplot(sns.light_palette("purple"))
# sns.palplot(sns.diverging_palette(150, 275, s=80, l=55, n=9))



#%% Exclude data if necessary
dfTemp= dfTidy.copy()

#subset subjects to plot (for training should we just show the n=9 or all?)
subjectsToExclude= ['VP-VTA-FP10', 'VP-VTA-FP16', 'VP-VTA-FP20', 'VP-VTA-FP220', 'VP-VTA-FP']
dfTemp= dfTemp.loc[dfTemp.subject.isin(subjectsToExclude)==False]

#%% Calculate PE probability
#Probability of PE within 10s of cue 
criteriaDS= 0.6

# declare hierarchical grouping variables (how should observations be separated)
# groupers= ['virus', 'sex', 'stage', 'laserDur', 'subject', 'trainDayThisStage', 'trialType'] #Opto
groupers= ['virus', 'sex', 'stage', 'subject', 'trainDayThisStage', 'trialType'] #Photometry

#here want percentage of each behavioral outcome per trialType per above groupers
observation= 'trialOutcomeBeh10s'

#Now calculate PE Probability using fxn:    
test= customFunctions.percentPortEntryCalc(dfTemp, groupers, observation)

test= test.reset_index()

#merge back into dataframe
dfTemp= dfTemp.merge(test, how='left', on=groupers).copy()

#then resample only valid observations (for this it's one PE probability per trialType per fileID)
dfPlot= dfTemp.loc[dfTemp.groupby(['fileID','trialType']).cumcount()==0].copy()

#%% Figure of Training Data, all individual subjects, all stages

#subset specific trialTypes to include!
trialTypesToPlot= pd.Series(dfPlot.loc[dfPlot.trialType.notnull(),'trialType'].unique())
trialTypesToPlot= trialTypesToPlot.loc[((trialTypesToPlot.str.contains('Pre-Cue')|(trialTypesToPlot.str.contains('DS')) | (trialTypesToPlot.str.contains('NS'))))]
dfPlot= dfPlot.loc[dfPlot.trialType.isin(trialTypesToPlot)]
dfPlot.trialType= dfPlot.trialType.cat.remove_unused_categories()

trialOrder= ['DStime','NStime', 'Pre-Cue']


#% THIS is probably the most informative individual subject training visualization
g= sns.relplot(data=dfPlot, x= 'trainDay', y='PE', col='subject', col_wrap=3, style='stage', hue='trialType', hue_order=trialOrder, kind='line', markers=True)
g.fig.suptitle('VP-VTA-FP DS Task Training Data')
g.set_ylabels('Probability of port entry within 10s cue onset')
    # criteria line overlaid
g.map(plt.axhline, y=criteriaDS, color=".2", linewidth=3, dashes=(3,1), zorder=0)

customFunctions.saveFigCustom(g, 'vp-vta-fp_individual_PEprob', close=False)

#%% Figure of Training data, group average, specific stage subset
#Probability of PE within 10s of cue 

#then resample only valid observations (for this it's one PE probability per trialType per fileID)
dfPlot= dfTemp.loc[dfTemp.groupby(['fileID','trialType']).cumcount()==0].copy()

#subset only stages 1-5
# stagesToPlot= ['1.0','2.0','3.0','4.0','5.0']
stagesToPlot= ['4.0', '5.0', '6.0', '7.0']

dfPlot= dfPlot.loc[dfPlot.stage.isin(stagesToPlot)].copy()
dfPlot.stage= dfPlot.stage.cat.remove_unused_categories()

#subset specific trialTypes to plot!
trialTypesToPlot= pd.Series(dfPlot.loc[dfPlot.trialType.notnull(),'trialType'].unique())
trialTypesToPlot= trialTypesToPlot.loc[((trialTypesToPlot.str.contains('DS')) | (trialTypesToPlot.str.contains('NS')))]
dfPlot= dfPlot.loc[dfPlot.trialType.isin(trialTypesToPlot)]
dfPlot.trialType= dfPlot.trialType.cat.remove_unused_categories()

trialOrder= ['DStime','NStime']
 

# #group mean with individual subjects overlaid
# g = sns.FacetGrid(data=dfPlot, row='stage')
# g.fig.suptitle('Probability of port entry within 10s cue onset')
# g.map_dataframe(sns.lineplot, x= 'trainDayThisStage', y='PE', hue='trialType', hue_order=trialOrder)
# g.map_dataframe(sns.lineplot,x='trainDayThisStage', y='PE', units='subject', estimator=None, palette=('muted'), hue='trialType', hue_order=trialOrder, style='subject', markers=True, dashes=True, linewidth=1, markersize=5)
# g.set_ylabels('Probability of PE within 10s cue onset') 
# g.set_xlabels('trainDayThisStage')
# g.legend
#    # criteria line overlaid
# g.map(plt.axhline, y=criteriaDS, color=".2", linewidth=3, dashes=(3,1), zorder=0)

#THIS seems like best way to compare across stages for whole group
#Facet stage, trialType. group mean with individual subjects overlaid
g = sns.FacetGrid(data=dfPlot, col='stage', row='trialType')
g.fig.suptitle('Probability of port entry within 10s cue onset')
g.map_dataframe(sns.lineplot, x= 'trainDayThisStage', y='PE', hue='trialType', hue_order=trialOrder, linewidth=2, zorder=0)
g.map_dataframe(sns.lineplot,x='trainDayThisStage', y='PE', units='subject', estimator=None, palette=('muted'), hue='trialType', hue_order=trialOrder, style='subject', markers=True, dashes=True, linewidth=1, markersize=5)

g.set_ylabels('Probability of PE within 10s cue onset') 
g.set_xlabels('trainDayThisStage')
g.legend
   # criteria line overlaid
g.map(plt.axhline, y=criteriaDS, color=".2", linewidth=3, dashes=(3,1), zorder=0)

customFunctions.saveFigCustom(g, 'vp-vta-fp_group_PEprob', close=False)

#%% TODO: Facet by Cue Identity- does siren vs. white noise differ?
