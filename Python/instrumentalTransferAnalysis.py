# -*- coding: utf-8 -*-
"""
Created on Thu Nov 11 16:39:52 2021

@author: Dakota
"""

# -*- coding: utf-8 -*-
"""
Created on Tue Aug 31 16:09:42 2021

@author: Dakota
"""

#%% Load dependencies
import pandas as pd
import shelve
import os

import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

#%$ Things to change manually for your data:
    
#plot settings in section below


 #%% define a function to save and close figures
def saveFigCustom(figure, figName):
    plt.legend(bbox_to_anchor=(1.01, 1), borderaxespad=0) #creates legend ~right of the last subplot
    
    plt.gcf().tight_layout()
    plt.savefig(r'./_output/_behaviorAnalysis/'+figName+'.png', bbox_inches='tight')
    plt.close()
         
         

#%% Load previously saved dfTidy (and other vars) from pickle
dataPath= r'./_output/' #'r'C:\Users\Dakota\Documents\GitHub\DS-Training\Python\\'

dfTidy= pd.read_pickle(dataPath+'dfTidy.pkl')

#load any other variables saved during the import process ('dfTidymeta' shelf)
my_shelf = shelve.open(dataPath+'dfTidymeta')
for key in my_shelf:
    globals()[key]=my_shelf[key]
my_shelf.close()


#%% Plot settings
sns.set_style("darkgrid")
sns.set_context('notebook')
sns.set_palette('Paired')

#fixed order of trialType to plot (so consistent between figures)
#for comparison of trial types (e.g. laser on vs laser off, good to have these in paired order for paired color palettes)
trialOrder= ['DStime','NStime','Pre-Cue', 'ITI']

#DS PE probability criteria (for visualization)
criteriaDS= 0.6

if experimentType.__contains__('Opto'):
    # trialOrder= ['laserDStrial_0', 'laserDStrial_1', 'laserNStrial_0', 'laserNStrial_1', 'Pre-Cue', 'ITI']
    # trialOrder= [trialOrder, 'laserDStrial_0', 'laserDStrial_1', 'laserNStrial_0', 'laserNStrial_1']
    trialOrder= (['DStime', 'DStime_laser', 'NStime', 'NStime_laser', 'Pre-Cue','ITI'])
    
#%% trying stuff with data hierarchy grouping

#%% subset test day, compare LPs by trialType
#todo: debug; something takes awhile

#define specific set of behavioral events to examine
eventsBeh= 'inactiveLPtime', 'activeLPtime', 'PEtime', 'lickTime'

dfGroup= dfTidy.loc[dfTidy.stage=='test'].copy()
dfGroup= dfGroup.loc[dfGroup.trialType!= 'ITI']
dfGroup= dfGroup.loc[dfGroup.eventType.isin(eventsBeh)]
  # by_many<- group_by(py_data, virus, sex, stage, laserDur, subject, fileID, trialType, trialOutcomeBeh10s)

groupers= ['virus','sex','stage','laserDur', 'subject', 'date', 'trialType', 'epoch']

#hierarchy should be something like groupVars -> stageVars -> subjVars-> sessionVars -> date -> fileID -> trialType/trialVars -> trialID -> eventVars

#seems that the grouping here is using all possible combos (e.g. creating entries for F Sex even for subjects that are M)
dfGroup= dfGroup.groupby(groupers)

#observed=True parameter only includes observed categories
# dfGroup= dfTidy.copy().groupby(['virus','sex','stage','laserDur', 'subject', 'date', 'trialType'], observed=True)


dfGroupComp= pd.DataFrame()
dfGroupComp['trialCount']= dfGroup['trialID'].nunique()
dfGroupComp.reset_index(inplace=True)

# dfGroupComp2= dfTidy.copy()
# dfGroupComp2['trialCount']= dfGroup['trialID'].transform('nunique')


sns.catplot(data= dfGroupComp, row='virus', col='sex', x='stage', y='trialCount', hue='trialType', hue_order=trialOrder, kind='bar')
sns.catplot(data= dfGroupComp, row='virus', col='sex', x='stage', y='trialCount', hue='trialType', hue_order=trialOrder, kind='bar')


#dp 11/11/21
#TODO: laser on vs laser off epochs within trial
#TODO: measure transfer by LP per minute**  throughout session or LP in 30s cue vs 30s pre-cue (normalized to full amount of time)


#first) individual event counts by trial for each subject
test= dfTidy.groupby(['subject','fileID', 'trialType', 'trialID','eventType'])['eventTime'].transform('count').reset_index().copy()
test= dfTidy.groupby(['subject','fileID','trialType', 'trialID','eventType']).transform('count')
#transform('count') loses index but retains group info... idk how to deal with this best, could be merged() back into df on groupers
dfPlot= pd.DataFrame()
dfPlot['eventCount']= dfTidy.groupby(['virus','subject','date', 'trialType', 'trialID','eventType'])['eventTime'].count().copy()
dfPlot= dfPlot.reset_index()

#individual subj count over time
sns.relplot(data= dfPlot, col='subject', col_wrap=4, x='date', y='eventCount', hue='eventType', kind='line', palette='tab20')

#%% TEST day only!
#virus event count by trialtype
dfGroup= dfTidy.loc[dfTidy.stage=='test'].copy()
dfGroup= dfGroup.loc[dfGroup.trialType!= 'ITI']
dfGroup= dfGroup.loc[dfGroup.eventType.isin(eventsBeh)]


dfPlot= pd.DataFrame()
dfPlot['eventCount']= dfGroup.groupby(['virus','subject','date', 'trialType', 'trialID','eventType'])['eventTime'].count().copy()
dfPlot= dfPlot.reset_index()

sns.catplot(data= dfPlot, row='virus', x='date', y='eventCount', hue='trialType', hue_order=trialOrder, kind='bar', palette='Paired')



#second) aggregation by subject
dfGroupComp2= pd.DataFrame() #A
dfGroupComp2['eventCount']= dfGroup['eventType'].value_counts()
dfGroupComp2.index.name= 'eventType'
# dfGroupComp2= dfTidy.copy() #B
# dfGroupComp2['eventCount']= dfTidy.groupby(groupers)['eventType'].transform('count')
# dfGroupComp2= pd.DataFrame() #C
# dfGroupComp2['eventCount']= dfTidy.groupby(groupers)['eventType'].count().reset_index()
# dfGroupComp2= dfTidy.copy() #D
# dfGroupComp2['Counts'] = dfTidy.copy().groupby(groupers)['eventType'].transform('count')
dfGroupComp2= pd.DataFrame() #E!!
dfGroupComp2['eventCount']= dfGroup.copy().groupby(groupers)['eventType'].value_counts()
# dfGroupComp2.index.name= 'eventType'

dfGroupComp2.reset_index(drop=False, inplace=True)
# sns.catplot(data= dfGroupComp2, row='virus', col='sex', x='eventType', y='eventCount', hue='trialType', hue_order=trialOrder, kind='bar')
sns.catplot(data= dfGroupComp2, row='virus', x='eventType', y='eventCount', hue='epoch', kind='bar')


#%% #^this was just example, now do something more relevant to behavior analysis

# dfGroup= dfTidy.copy().groupby(['virus','sex','stage','laserDur', 'subject', 'date', 'trialType'])


# dfGroupComp= pd.DataFrame()
# # dfGroupComp['outcomeBehCount']= dfGroup['trialOutcomeBeh10s'].value_counts()
# # dfGroupComp['outcomeBehCount']= dfGroup['trialOutcomeBeh10s'].transform(pd.Series.mode)
# # dfGroupComp['outcomeBehCount']= dfGroup['trialOutcomeBeh10s'].transform(dfTidy.trialOutcomeBeh10s.mode)


# # dfGroupComp.reset_index(inplace=True)


# # sns.catplot(data= dfGroupComp, row='virus', col='sex', x='trialOutcomeBeh10s', y='outcomeBehCount', hue='trialType', hue_order=trialOrder, kind='bar')


# #^ can calculate proportion more efficiently?
# # dfGroup= dfTidy.copy().groupby(['virus','sex','stage','laserDur', 'subject', 'date', 'trialType'])

# #subset to one event per trial, then groupby()
# dfGroup= dfTidy.copy().loc[dfTidy.groupby(['fileID','trialID']).cumcount()==0].groupby(groupers)

# dfGroupComp= pd.DataFrame()
# dfGroupComp['trialCount']= dfGroup['trialID'].nunique()
# dfGroupComp= dfGroupComp.reset_index(drop=False).set_index(groupers)

# # dfGroupComp2= pd.DataFrame()
# # dfGroupComp2['outcomeBehCount']= dfGroup['trialOutcomeBeh10s'].value_counts()
# # dfGroupComp2= dfGroupComp2.reset_index(drop=False).set_index(groupers)

# # #issue now would be dividing appropriately with non-unique index
# # #could try using transform() operation?
# # # dfGroupComp2['outcomeProb']= dfGroupComp2.outcomeBehCount/dfGroupComp.trialCount

# # #do division while indexed by groupers, then reset index for reassignment of result
# # outcomeProb= dfGroupComp2.outcomeBehCount/dfGroupComp.trialCount

# # dfGroupComp.reset_index(inplace=True, drop=False)
# # outcomeProb= outcomeProb.reset_index().copy()

# # # dfGroupComp['outcomeProb']= outcomeProb.copy()



# #can imagine doing peri-event analyses like so
# dfGroup= dfTidy.copy().groupby(['virus','sex','stage','laserDur', 'subject', 'date', 'trialType', 'eventType'])

# dfGroupComp= pd.DataFrame()
# dfGroupComp['eventOnsets']= dfGroup['eventTime'].value_counts()
