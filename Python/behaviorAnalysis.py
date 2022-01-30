# -*- coding: utf-8 -*-
"""
Created on Tue Aug 31 16:09:42 2021

@author: Dakota
"""

# %% Load dependencies
import pandas as pd
import shelve
import os

import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

# script ('module') containing custom fxns
from customFunctions import saveFigCustom
from customFunctions import subsetData
from customFunctions import subsetLevelObs
from customFunctions import percentPortEntryCalc
from customFunctions import groupPercentCalc

# %$ Things to change manually for your data:

# plot settings in section below

# %% define a function to save and close figures


# def saveFigCustom(figure, figName):
#     plt.gcf().set_size_inches((20, 10), forward=False)  # ~monitor size
#     # creates legend ~right of the last subplot
#     plt.legend(bbox_to_anchor=(1.01, 1), borderaxespad=0)

#     plt.gcf().tight_layout()
#     plt.savefig(r'./_output/_behaviorAnalysis/' +
#                 figName+'.png', bbox_inches='tight')
#     plt.close()


# %% Load previously saved dfTidy (and other vars) from pickle
dataPath = r'./_output/'  # 'r'C:\Users\Dakota\Documents\GitHub\DS-Training\Python\\'

# dfTidy = pd.read_pickle(dataPath+'dfTidy.pkl')

#note if .pkl saved in an older python version, may need to use pickle5:
import pickle5 as pickle
with open(dataPath+'dfTidy.pkl', "rb") as fh:
  dfTidy = pickle.load(fh)

# load any other variables saved during the import process ('dfTidymeta' shelf)
my_shelf = shelve.open(dataPath+'dfTidymeta')
for key in my_shelf:
    globals()[key] = my_shelf[key]
my_shelf.close()


# %% Plot settings
sns.set_style("darkgrid")
sns.set_context('notebook')

savePath= r'./_output/_behaviorAnalysis/'


# fixed order of trialType to plot (so consistent between figures)
# for comparison of trial types (e.g. laser on vs laser off, good to have these in paired order for paired color palettes)
trialOrder = ['DStime', 'NStime', 'Pre-Cue', 'ITI']

# DS PE probability criteria (for visualization)
criteriaDS = 0.6

if experimentType.__contains__('Opto'):
    # trialOrder= ['laserDStrial_0', 'laserDStrial_1', 'laserNStrial_0', 'laserNStrial_1', 'Pre-Cue', 'ITI']
    # trialOrder= [trialOrder, 'laserDStrial_0', 'laserDStrial_1', 'laserNStrial_0', 'laserNStrial_1']
    trialOrder = (['DStime', 'DStime_laser', 'NStime',
                  'NStime_laser', 'Pre-Cue', 'ITI'])




# %%For Opto, combine make each laserDur its own unique stage
if experimentType.__contains__('Opto'):
    #find non-nan laserDur entires and combine with 
    ind= ~dfTidy.laserDur.str.contains('nan')
    
    dfTidy.stage= dfTidy.stage.astype(str)
    dfTidy.laserDur= dfTidy.laserDur.astype(str)
    
    dfTidy.loc[ind,'stage']= dfTidy.stage+'-laser-'+dfTidy.laserDur

    dfTidy.stage=dfTidy.stage.astype('category')



# %% Preliminary data analyses
# Event latency, count, and behavioral outcome for each trial

# TODO: Lick 'cleaning' to eliminate invalid licks (are they in port, is ILI within reasonable range)


# #Calculate latency to each event in trial (from cue onset). based on trialEnd to keep it simple
#   # trialEnd is = cue onset + cueDur. So just subtract cueDur for cue onset time
# dfTidy.loc[dfTidy.trialID>=0, 'eventLatency'] = (
#     (dfTidy.eventTime)-(dfTidy.trialEnd-dfTidy.cueDur)).copy()

# have trial start now, subtract trialStart from eventTime to get latency per trial
# no need for -trialID exception
dfTidy.loc[:, 'eventLatency'] = ((dfTidy.eventTime)-(dfTidy.trialStart)).copy()
#
# dfTidy.loc[dfTidy.trialID>=0,'eventLatency']= ((dfTidy.eventTime)-(dfTidy.trialStart))

# dfTidy.loc[dfTidy.trialID<0, 'eventLatency'] = ((dfTidy.eventTime)-(dfTidy.trialStart)).copy()

# TODO: exception needs to be made for first ITI; for now fill w nan
dfTidy.loc[dfTidy.trialID == -999, 'eventLatency'] = np.nan

# Count events in each trial
# use cumcount() of event times within file & trial

# converting to float for some reason
dfTidy['trialPE'] = dfTidy.loc[(dfTidy.eventType == 'PEtime')].groupby([
    'fileID', 'trialID'])['eventTime'].cumcount().copy()

# #try transform
# dfTidy.loc[:,'trialPE'] = dfTidy.loc[(dfTidy.eventType == 'PEtime')].groupby([
# 'fileID', 'trialID'])['eventTime'].transform('cumcount').copy()


dfTidy['trialLick'] = dfTidy.loc[(dfTidy.eventType == 'lickTime')].groupby([
    'fileID', 'trialID']).cumcount().copy()

# Add trainDay variable (cumulative count of sessions within each subject)
dfGroup = dfTidy.loc[dfTidy.groupby(['subject', 'fileID']).cumcount() == 0]
# test= dfGroup.groupby(['subject','fileID']).transform('cumcount')
dfTidy.loc[:, 'trainDay'] = dfGroup.groupby(
    ['subject'])['fileID'].transform('cumcount')
dfTidy.loc[:, 'trainDay'] = dfTidy.groupby(
    ['subject', 'fileID']).fillna(method='ffill')

# Add cumulative count of training day within-stage (so we can normalize between subjects appropriately)
# very important consideration!! Different subjects can run different programs on same day, which can throw plots/analysis off when aggregating data by date.
dfGroup = dfTidy.loc[dfTidy.groupby('fileID').transform(
    'cumcount') == 0, :].copy()  # one per session
dfTidy['trainDayThisStage'] = dfGroup.groupby(
    ['subject', 'stage']).transform('cumcount')
dfTidy.trainDayThisStage = dfTidy.groupby(
    ['fileID'])['trainDayThisStage'].fillna(method='ffill').copy()
# #QC visualizations
# g= sns.relplot(data=dfTidy, col='subject', col_wrap=4, x='date', y='trainDayThisStage', hue='stage', kind='scatter')
# g= sns.relplot(data=dfTidy, col='subject', col_wrap=4, x='date', y='trainDay', hue='stage', kind='scatter')
# g= sns.relplot(data=dfTidy, col='subject', col_wrap=4, x='date', y='date', hue='stage', kind='scatter')


#Correct dtypes
dfTidy.eventLatency = dfTidy.eventLatency.astype('float')  # TODO: correct dtypes early in code


# %% Declare hierarchical grouping variables for analysis
# e.g. for aggregated measures, how should things be calculated and grouped?

# examples of different measures @ different levels:
# consider within-file (e.g. total PEs per session)
# within-trialType (e.g. Probability of PEs during all DS vs. all NS)
# within-trialID measures (e.g. Latency to enter port all individual trials)
# within virus, cue identity, subject, stage, etc.

if experimentType.__contains__('Opto'):
    # groupHierarchyFileID = ['virus', 'sex', 'stage',
    #                         'laserDur', 'subject', 'trainDayThisStage', 'fileID']
    # groupHierarchyTrialType = ['virus', 'sex', 'stage', 'laserDur',
    #                            'subject', 'trainDayThisStage', 'fileID', 'trialType']
    # groupHierarchyTrialID = ['virus', 'sex', 'stage', 'laserDur',
    #                          'subject', 'trainDayThisStage', 'trialType', 'fileID', 'trialID']
   #taking out laserDur, combining into stage
    groupHierarchyFileID = ['virus', 'sex', 'stage',
                            'subject', 'trainDayThisStage', 'fileID']
    groupHierarchyTrialType = ['virus', 'sex', 'stage',
                               'subject', 'trainDayThisStage', 'fileID', 'trialType']
    groupHierarchyTrialID = ['virus', 'sex', 'stage',
                             'subject', 'trainDayThisStage', 'trialType', 'fileID', 'trialID']
    
    groupHierarchyEventType = ['virus', 'sex', 'stage',
                             'subject', 'trainDayThisStage', 'trialType', 'fileID', 'trialID', 'eventType']


else:
    groupHierarchyFileID = ['sex', 'stage',
                            'subject', 'trainDayThisStage', 'fileID']
    groupHierarchyTrialType = ['sex', 'stage', 'subject',
                               'trainDayThisStage', 'fileID', 'trialType']
    groupHierarchyTrialID = ['sex', 'stage', 'subject',
                             'trainDayThisStage', 'trialType', 'fileID', 'trialID']

    groupHierarchyEventType = ['sex', 'stage',
                             'subject', 'trainDayThisStage', 'trialType', 'fileID', 'trialID', 'eventType']


#%% Consider saving specific ind for different level of observations 
#e.g. trial, file, could very quickly subset data or store alt dataframe

#index of first entry per file
obsFile= dfTidy.groupby(groupHierarchyFileID).cumcount()==0

#e.g. 
# dfFile= dfTidy[obsFile].copy()

#index of first entry per trialType
obsTrialType= dfTidy.groupby(groupHierarchyTrialType).cumcount()==0

#index of first entry per trial
obsTrial= dfTidy.groupby(groupHierarchyTrialID).cumcount()==0


#index of first event per type per trial (e.g. mean latency of each event)
obsEventType= dfTidy.groupby(groupHierarchyEventType).cumcount()==0


# %% Count events within 10s of cue onset (cue duration in final stage)
# this is mainly for comparing progression/learning between stages since cueDuration varies by stage

dfTemp = dfTidy.loc[((dfTidy.eventLatency <= 10) &
                     (dfTidy.eventLatency > 0))].copy()

dfTidy['trialPE10s'] = dfTemp.loc[(dfTemp.eventType == 'PEtime')].groupby([
    'fileID', 'trialID'])['eventTime'].cumcount().copy()

dfTidy['trialLick10s'] = dfTemp.loc[(dfTemp.eventType == 'lickTime')].groupby([
    'fileID', 'trialID'])['eventTime'].cumcount().copy()

# %% Define behavioral (pe,lick) outcome for each trial.
# For my lick+laser sessions I need
# to isolate trials with both a PE+lick to measure effect of laser

# For each trial (trialID >=0),
# count the number of PEs per trial. if >0, they entered the port and earned sucrose. If=0, they did not.
# since groupby counting methods don't work well with nans, using nunique()
# peOutcome= dfTidy.loc[dfTidy.trialID>=0].groupby(['fileID','trialID'],dropna=False)['trialPE'].nunique()
# do for all trials
outcome = dfTidy.groupby(['fileID', 'trialID'], dropna=False)[
    'trialPE'].nunique()

# naming "trialOutcomeBeh" for now to distinguish between behavioral outcome and reward outcome if needed later
trialOutcomeBeh = outcome.copy()

trialOutcomeBeh.loc[outcome > 0] = 'PE'
trialOutcomeBeh.loc[outcome == 0] = 'noPE'

# now do the same for licks
outcome = dfTidy.groupby(['fileID', 'trialID'], dropna=False)[
    'trialLick'].nunique()

# add lick outcome + PE outcome for clarity #if it doesn't say '+lick', then none was counted
trialOutcomeBeh.loc[outcome >
                    0] = trialOutcomeBeh.loc[outcome > 0] + '+' + 'lick'

# set index to file,trial and
# fill in matching file,trial with trialOutcomeBeh
# TODO: I think there is a more efficient way to do this assignment, doens't take too long tho

dfTidy = dfTidy.reset_index().set_index(['fileID', 'trialID'])

dfTidy.loc[trialOutcomeBeh.index, 'trialOutcomeBeh'] = trialOutcomeBeh

# reset index to eventID
dfTidy = dfTidy.reset_index().set_index(['eventID'])

# %% same as above but behavioral outcome within first 10s of each trial
outcome = dfTidy.groupby(['fileID', 'trialID'], dropna=False)[
    'trialPE10s'].nunique()

# naming "trialOutcomeBeh" for now to distinguish between behavioral outcome and reward outcome if needed later
# 10s = within 10s of epoch start
trialOutcomeBeh = outcome.copy()

trialOutcomeBeh.loc[outcome > 0] = 'PE'
trialOutcomeBeh.loc[outcome == 0] = 'noPE'

# now do the same for licks
outcome = dfTidy.groupby(['fileID', 'trialID'], dropna=False)[
    'trialLick10s'].nunique()

# add lick outcome + PE outcome for clarity #if it doesn't say '+lick', then none was counted
trialOutcomeBeh.loc[outcome >
                    0] = trialOutcomeBeh.loc[outcome > 0] + '+' + 'lick'

# set index to file,trial and
# fill in matching file,trial with trialOutcomeBeh
# TODO: I think there is a more efficient way to do this assignment, doens't take too long tho

dfTidy = dfTidy.reset_index().set_index(['fileID', 'trialID'])

dfTidy.loc[trialOutcomeBeh.index, 'trialOutcomeBeh10s'] = trialOutcomeBeh

# reset index to eventID
dfTidy = dfTidy.reset_index().set_index(['eventID'])

# %% Calculate Probability of behavioral outcome for each trial type.
# This is normalized so is more informative than simple count of trials.

# declare hierarchical level of analysis for the analysis we are doing (here there is one outcome per trial per file)
levelOfAnalysis = ['fileID', 'trialID']

# First we need to subset only one outcome per level of analysis (trial)
dfGroup = dfTidy.loc[dfTidy.groupby(levelOfAnalysis).cumcount() == 0].copy()

#alternatively, this is the same as:
# dfGroup= dfTidy[obsTrial]

# declare hierarchical grouping variables (how should the observations be separated)
groupHierarchy = groupHierarchyTrialType

# here want percentage of each behavioral outcome per trialType per above groupers
colToCalc = 'trialOutcomeBeh10s'

dfTemp = groupPercentCalc(dfGroup, levelOfAnalysis, groupHierarchy, colToCalc)

#instead of 1 col per probability, melt into single column that matches up to outcome
dfTemp= dfTemp.reset_index().melt(
    id_vars=groupHierarchy, value_name='trialTypeOutcomeBehProb10s')

#merge to save as new column in dfTidy
dfTidy = dfTidy.merge(dfTemp, how='left', on=groupHierarchy+[colToCalc])

#%% Calculate PE probability for each trialType
#(combines all outcomes with PE vs all outcomes with no PE)

dfTemp= dfTidy.copy()


# declare hierarchical grouping variables (how should the observations be separated)
groupHierarchy = groupHierarchyTrialType


# here want percentage of each behavioral outcome per trialType per above groupers
colToCalc = 'trialOutcomeBeh10s'

dfTemp= percentPortEntryCalc(dfTemp, groupHierarchy, colToCalc)

dfTemp= dfTemp.reset_index()

dfTemp= dfTemp.rename(columns= {'PE':'trialTypePEProb10s'})

dfTidy= dfTidy.merge(dfTemp, how='left', on=groupHierarchy)

# # %% old code
# # calculate Proportion of trials with PE out of all trials for each trial type
# # can use nunique() to get count of unique trialIDs with specific PE outcome per file
# # given this, can calculate Probortion as #PE/#PE+#noPE

# # subset data and save as intermediate variable dfGroup
# # get only one entry per trial
# dfGroup = dfTidy.loc[dfTidy.groupby(
#     ['fileID', 'trialID']).cumcount() == 0].copy()

# # for Lick+laser sessions, retain only trials with PE+lick for comparison (OPTO specific)
# # dfGroup.loc[dfGroup.laserDur=='Lick',:]= dfGroup.loc[(dfGroup.laserDur=='Lick') & (dfGroup.trialOutcomeBeh=='PE+lick')].copy()

# dfPlot = dfGroup.copy()

# # for each unique behavioral outcome, loop through and get count of trials in file
# # fill null counts with 0
# dfTemp = dfPlot.groupby(
#     ['fileID', 'trialType', 'trialOutcomeBeh'], dropna=False)['trialID'].nunique(dropna=False).unstack(fill_value=0)


# # calculate proportion for each trial type: num trials with outcome/total num trials of this type

# trialCount = dfTemp.sum(axis=1)


# outcomeProb = dfTemp.divide(dfTemp.sum(axis=1), axis=0)

# # melt() into single column w label
# dfTemp = outcomeProb.reset_index().melt(id_vars=[
#     'fileID', 'trialType'], var_name='trialOutcomeBeh', value_name='outcomeProbFile')

# # assign back to df by merging
# # TODO: can probably be optimized. if this section is run more than once will get errors due to assignment back to dfTidy
# # dfTidy.reset_index(inplace=True) #reset index so eventID index is kept

# dfTidy = dfTidy.reset_index().merge(
#     dfTemp, 'left', on=['fileID', 'trialType', 'trialOutcomeBeh']).copy()

# # %% Same as above but probability of behavioral outcome within first 10s of trial
# # This is normalized so is more informative than simple count of trials.

# # calculate Proportion of trials with PE out of all trials for each trial type
# # can use nunique() to get count of unique trialIDs with specific PE outcome per file
# # given this, can calculate Probortion as #PE/#PE+#noPE

# # subset data and save as intermediate variable dfGroup
# # get only one entry per trial
# dfGroup = dfTidy.loc[dfTidy.groupby(
#     ['fileID', 'trialID']).cumcount() == 0].copy()

# # for Lick+laser sessions, retain only trials with PE+lick for comparison (OPTO specific)
# # dfGroup.loc[dfGroup.laserDur=='Lick',:]= dfGroup.loc[(dfGroup.laserDur=='Lick') & (dfGroup.trialOutcomeBeh=='PE+lick')].copy()

# dfPlot = dfGroup.copy()

# # for each unique behavioral outcome, loop through and get count of trials in file
# # fill null counts with 0
# dfTemp = dfPlot.groupby(
#     ['fileID', 'trialType', 'trialOutcomeBeh10s'], dropna=False)['trialID'].nunique(dropna=False).unstack(fill_value=0)


# # calculate proportion for each trial type: num trials with outcome/total num trials of this type

# trialCount = dfTemp.sum(axis=1)


# outcomeProb = dfTemp.divide(dfTemp.sum(axis=1), axis=0)

# # melt() into single column w label
# dfTemp = outcomeProb.reset_index().melt(id_vars=[
#     'fileID', 'trialType'], var_name='trialOutcomeBeh10s', value_name='trialTypeOutcomeBehProb10s')

# # assign back to df by merging
# # TODO: can probably be optimized. if this section is run more than once will get errors due to assignment back to dfTidy
# # dfTidy.reset_index(inplace=True) #reset index so eventID index is kept

# dfTidy = dfTidy.reset_index().merge(
#     dfTemp, 'left', on=['fileID', 'trialType', 'trialOutcomeBeh10s']).copy()




# %%----- PLOTS:

# %% Plot event counts across sessions (check for outlier sessions/event counts)
sns.set_palette('tab20')  # good for plotting by many subj


# I know that lick count was absurdly high (>9000) due to liquid shorting lickometer on at least 1 session
# visualize event counts by session to ID outliers
# not interested in some events (e.g. # cues is fixed), remove those
dfPlot = dfTidy.loc[(dfTidy.eventType != 'NStime') & (dfTidy.eventType != 'DStime') & (
    dfTidy.eventType != 'PExEst') & (dfTidy.eventType != 'laserOffTime')].copy()

# count of each event type by date and subj
dfPlot = dfPlot.groupby(['subject', 'date', 'eventType'])[
    'eventTime'].count().reset_index()

g = sns.relplot(data=dfPlot, col='eventType', x='date', y='eventTime', hue='subject', kind='line', style='subject', markers=True, dashes=False,
                facet_kws={'sharey': False, 'sharex': True})
g.fig.subplots_adjust(top=0.9)  # adjust the figure for title
g.fig.suptitle('Total event count across sessions by type- check for outliers')
g.set_ylabels('# of events')
g.set_ylabels('session')

saveFigCustom(g, 'individual_eventCounts_line', savePath)

# %% Plot PE probability by trialType (within 10s of trial start)
sns.set_palette('Paired')  # default  #tab10

# subset data corresponding to apprpriate level of observation for variable
dfPlot = dfTidy.loc[obsTrialType].copy()

# define subset further based on stage, trialTypes, eventTypes
stagesToPlot= dfPlot.stage.unique()
trialTypesToPlot= ['DStime','NStime']
eventsToPlot= dfPlot.eventType.unique()

##use custom fxn to subset
# dfPlot= subsetData(dfPlot, stagesToPlot, trialTypesToPlot, eventsToPlot)

# g = sns.relplot(data=dfPlot, x='trainDay', y='trialTypeOutcomeBehProb10s', hue='subject',
#                 row='trialType', kind='line', style='stage', markers=True, dashes=True)
# g.map(plt.axhline, y=criteriaDS, color=".2",
#       linewidth=3, dashes=(3, 1), zorder=0)

# g.map(sns.lineplot, data=dfPlot, x='trainDay', y='trialTypeOutcomeBehProb10s', color='black')

# saveFigCustom(g, 'training_peProb', savePath)


#--Training: DS PE Prob+latency in 1 fig

dfPlot= dfTidy.copy()

#subset with customFunction
stagesToPlot= dfPlot.stage.unique()
trialTypesToPlot= ['DStime']
eventsToPlot= ['PEtime']
dfPlot= subsetData(dfPlot, stagesToPlot, trialTypesToPlot, eventsToPlot)


#subset data at correct level of observation for variable    
groupHierarchy= groupHierarchyTrialType
dfPlot= subsetLevelObs(dfPlot, groupHierarchy)


#subset data further to correct level of observation for variable
dfPlot2= dfTidy[obsEventType].copy()

#subset with customFunction
stagesToPlot= dfPlot2.stage.unique()
trialTypesToPlot= ['DStime']
eventsToPlot= ['PEtime']
dfPlot2= subsetData(dfPlot2, stagesToPlot, trialTypesToPlot, eventsToPlot)

#subset data further to correct level of observation
groupHierarchy= groupHierarchyEventType
dfPlot2= subsetLevelObs(dfPlot2, groupHierarchy)

#make figure
f, ax= plt.subplots(2,1)

g= sns.lineplot(ax=ax[0], data=dfPlot, x='trainDay', y='trialTypeOutcomeBehProb10s', hue='subject', style='stage')
ax[0].axhline(y=criteriaDS, color=".2", linewidth=3, dashes=(3, 1), zorder=0)
g.set(title=('Training: 10s PE probability, DS trials'))
g.set( ylabel='PE probability (10s)')

g= sns.lineplot(ax=ax[1], data=dfPlot2, x='trainDay', y='eventLatency', hue='subject', style='trialType')
g.set(title=('Training: PE latency, DS trials'))
g.set( ylabel='latency to first PE (s)')

saveFigCustom(f, 'training_PE_Prob+Latency_DS', savePath)


# #define specific trialTypes to plot!
# trialTypesToPlot= pd.Series(dfTidy.loc[dfTidy.trialType.notnull(),'trialType'].unique())
# trialTypesToPlot= trialTypesToPlot.loc[((trialTypesToPlot.str.contains('DS')) | (trialTypesToPlot.str.contains('NS')))]

# dfPlot= dfPlot.loc[dfPlot.trialType.isin(trialTypesToPlot)]
# dfPlot.trialType= dfTidy.trialType.cat.remove_unused_categories()

## late stages only
# g = sns.relplot(data=dfPlot, x='trainDayThisStage', y='trialTypeOutcomeBehProb10s', col='subject', col_wrap=4,
#                 hue='trialType', hue_order=trialOrder, kind='line', style='stage', markers=True, dashes=True)
# g.map(plt.axhline, y=criteriaDS, color=".2",
#       linewidth=3, dashes=(3, 1), zorder=0)
# g.fig.suptitle('Evolution of the trialTypeOutcomeBehProb10s in subjects by trialType')
# saveFigCustom(g, 'training_peProb_10s_lateStages_individual')

# g = sns.relplot(data=dfPlot, x='trainDayThisStage', y='trialTypeOutcomeBehProb10s', col='subject', col_wrap=4,
#                 hue='trialType', hue_order=trialOrder, kind='line', style='stage', markers=True, dashes=True)
# g.map(plt.axhline, y=criteriaDS, color=".2",
#       linewidth=3, dashes=(3, 1), zorder=0)
# g.fig.suptitle('Evolution of the trialTypeOutcomeBehProb10s in subjects by trialType')
# saveFigCustom(g, 'training_peProb_10s_lateStages_individual_trainDay')


# g = sns.relplot(data=dfPlot, x='trainDayThisStage', y='trialTypeOutcomeBehProb10s', row='stage', col='virus',
#                 hue='trialType', hue_order=trialOrder, kind='line', style='virus', markers=True, dashes=True)
# g.map(plt.axhline, y=criteriaDS, color=".2",
#       linewidth=3, dashes=(3, 1), zorder=0)
# saveFigCustom(g, 'training_peProb_10s_lateStages_virus')


# g = sns.relplot(data=dfPlot, x='trainDayThisStage', y='trialTypeOutcomeBehProb10s', row='stage', col='virus',
#                 hue='trialType', hue_order=trialOrder, kind='line', style='virus', markers=True, dashes=True)
# g.map(plt.axhline, y=criteriaDS, color=".2",
#       linewidth=3, dashes=(3, 1), zorder=0)
# saveFigCustom(g, 'training_peProb_10s_lateStages_virus_trainDay')

# g= sns.relplot(data=dfPlot, x='trainDayThisStage', y='trialTypeOutcomeBehProb10s', row='trialType', hue='virus', kind='line', style='virus', markers=True, dashes=False)
# g.map(plt.axhline, y=criteriaDS, color=".2", linewidth=3, dashes=(3,1), zorder=0)

# individual subj lines
# g= sns.relplot(data=dfPlot, x='trainDayThisStage', y='trialTypeOutcomeBehProb10s', row='trialType', units='subject', estimator=None, hue='virus', kind='line', style='stage', markers=True, dashes=False, palette='tab10')
# g.map(plt.axhline, y=criteriaDS, color=".2", linewidth=3, dashes=(3,1), zorder=0)
# g.fig.suptitle('Evolution of the trialTypeOutcomeBehProb10s in subjects by trialType')


# %% TODO: ECDF of behavioral outcome (PE) would be nice to view compared to latency ECDFs?

#not sure how to do best with binary outcome?

# %% Plot PE latency by trialType

#--Distribution: Stage 5 PE latency by trialType across trainDay
#ECDF plot of latency shows discrimination between trialTypes

dfPlot= dfTidy.copy()

#subset with customFunction
stagesToPlot= ['Stage 5']
trialTypesToPlot= ['DStime', 'NStime', 'Pre-Cue']
eventsToPlot= ['PEtime']
dfPlot= subsetData(dfPlot, stagesToPlot, trialTypesToPlot, eventsToPlot)


# #subset data at correct level of observation for variable    
# subset to first event per trial
groupHierarchy= groupHierarchyEventType
dfPlot= subsetLevelObs(dfPlot, groupHierarchy)


g= sns.displot(data=dfPlot, kind='ecdf', col='trainDayThisStage', x='eventLatency', hue='trialType', hue_order=trialOrder)




# # select data corresponding to first PE from valid trials, excluding ITI
# dfPlot = dfTidy[(dfTidy.trialType != 'ITI') & (dfTidy.trialPE10s == 0)].copy()

# # PE latency: virus
# g = sns.displot(data=dfPlot, x='eventLatency', hue='trialType',
#                 row='virus', kind='ecdf', hue_order=trialOrder)
# g.fig.suptitle('First PE latency by trial type')
# g.set_ylabels('First PE latency from epoch start (s)')
# saveFigCustom(g, 'virus_peLatency_10s_ecdf',savePath)

# # PE latency:  individual subj
# g = sns.displot(data=dfPlot, col='subject', col_wrap=4, x='eventLatency',
#                 hue='trialType', kind='ecdf', hue_order=trialOrder)
# g.fig.suptitle('First PE latency by trial type (within 10s)')
# g.set_ylabels('Probability: first PE latency from epoch start')
# saveFigCustom(g, 'individual_peLatency_10s_ecdf',savePath)

# # training across stages

# g = sns.relplot(data=dfPlot, x='trainDayThisStage', y='eventLatency', col='subject', col_wrap=4,
#                 hue='trialType', hue_order=trialOrder, kind='line', style='stage', markers=True, dashes=True)
# g.fig.suptitle('Evolution of first PE latency by trialType')
# saveFigCustom(g, 'training_peLatency_10s_individual',savePath)


# g = sns.relplot(data=dfPlot, x='trainDayThisStage', y='eventLatency', row='virus',
#                 hue='trialType', hue_order=trialOrder, kind='line', style='stage', markers=True, dashes=True)
# g.fig.suptitle('Evolution of first PE latency by trialType')
# saveFigCustom(g, 'training_peLatency_10s_virus+sex',savePath)


# # late stages plots
# dfPlot = dfPlot.loc[dfPlot.stage.isin(stagesToPlot)]

# g = sns.displot(data=dfPlot, x='eventLatency', hue='trialType',
#                 row='virus', col='stage', kind='ecdf', hue_order=trialOrder)
# g.fig.suptitle('First PE latency by trial type, late stages')
# g.set_ylabels('Probability: first PE latency from epoch start')
# saveFigCustom(g, 'dist_peLatency_10s_lateStages_virus_ecdf',savePath)


# g = sns.relplot(data=dfPlot, x='trainDayThisStage', y='eventLatency', row='virus',
#                 hue='trialType', hue_order=trialOrder, kind='line', style='stage', markers=True, dashes=True)
# g.fig.suptitle('Evolution of first PE latency by trialType, late stages')
# saveFigCustom(g, 'training_peLatency_10s_lateStages_virus',savePath)


# %% TODO: Custom Ridge Plot to show changes in distribution over time

dfPlot= dfTidy.copy()

#subset with customFunction
stagesToPlot= ['Stage 5']
trialTypesToPlot= ['DStime', 'NStime', 'Pre-Cue']
eventsToPlot= ['PEtime']
dfPlot= subsetData(dfPlot, stagesToPlot, trialTypesToPlot, eventsToPlot)


# #subset data at correct level of observation for variable    
# subset to first event per trial
groupHierarchy= groupHierarchyEventType
dfPlot= subsetLevelObs(dfPlot, groupHierarchy)

# Initialize the FacetGrid object
pal = sns.cubehelix_palette(10, rot=-.25, light=.7)
# g = sns.FacetGrid(dfPlot, row="trainDayThisStage", hue="trainDayThisStage", col='subject', aspect=15, height=10, palette=pal)
g = sns.FacetGrid(dfPlot, row="trainDayThisStage", hue="trainDayThisStage", col='subject')#, aspect=15, height=10, palette=pal)

# Draw the densities in a few steps
g.map(sns.kdeplot, "eventLatency",
      bw_adjust=.5, clip_on=False,
      fill=True, alpha=1, linewidth=1.5)
# g.map(sns.kdeplot, "eventLatency", clip_on=False, color="w", lw=2, bw_adjust=.5)

# passing color=None to refline() uses the hue mapping
# g.refline(y=0, linewidth=2, linestyle="-", color=None, clip_on=False)


# Define and use a simple function to label the plot in axes coordinates
def label(x, color, label):
    ax = plt.gca()
    ax.text(0, .2, label, fontweight="bold", color=color,
            ha="left", va="center", transform=ax.transAxes)


g.map(label, "eventLatency")

# Set the subplots to overlap
# g.figure.subplots_adjust(hspace=-.25)

# Remove axes details that don't play well with overlap
g.set_titles("")
g.set(yticks=[], ylabel="")
g.despine(bottom=True, left=True)


# %% Plot First lick latencies (time from cue or trialEnd if ITI events) by trialType (within 10s)
# should represent "baseline" behavior  without laser

# trial-based, ignoring ITI
dfPlot = dfTidy[(dfTidy.trialType != 'ITI')].copy()
# trial-based, including ITI
# dfPlot= dfTidy.copy()

# All subj distribution of ILI (inter-lick interval)
# only include first trialLick ==0
dfPlot = dfPlot[dfPlot.trialLick10s == 0].copy()

# box- all subj
g = sns.catplot(data=dfPlot, y='eventLatency',
                x='trialType',  kind='box', order=trialOrder)
g.fig.subplots_adjust(top=0.9)  # adjust the figure for title
g.fig.suptitle('First Lick latencies by trial type; all subj')
g.set_ylabels('lick latency from epoch start (s)')
saveFigCustom(g, 'all_lickLatency_10s_box',savePath)


# ecdf- all subj'[]
g = sns.displot(data=dfPlot, x='eventLatency', hue='trialType',
                kind='ecdf', hue_order=trialOrder)
g.fig.subplots_adjust(top=0.9)  # adjust the figure for title
g.fig.suptitle('First Lick latencies by trial type; all subj')
g.set_xlabels('lick latency from epoch start (s)')
saveFigCustom(g, 'all_lickLatency_10s_ecdf',savePath)


# Individual distribution of ILI (inter-lick interval)
# only include trialLick~=nan
# bar- individual subj
g = sns.catplot(data=dfPlot, y='eventLatency', x='subject',
                hue='trialType',  kind='bar', hue_order=trialOrder)
g.fig.subplots_adjust(top=0.9)  # adjust the figure for title
g.fig.suptitle('First Lick latencies by trial type; individual subj')
g.set_ylabels('lick latency from epoch start (s)')
saveFigCustom(g, 'individual_lickLatency_10s_bar',savePath)


# %% Plot inter-lick interval (ILI) by trialType (within 10s)

# trial-based, ignoring ITI
dfPlot = dfTidy[(dfTidy.trialType != 'ITI')].copy()
# trial-based, including ITI
# dfPlot = dfTidy.copy()

# All subj distribution of ILI (inter-lick interval)
# only include trialLick~=nan (lick timestamps within trials)
dfPlot = dfPlot[dfPlot.trialLick10s.notnull()].copy()

# calculate ILI by taking diff() of latencies
ili = dfPlot.groupby(['fileID', 'trialID', 'trialType'])['eventLatency'].diff()

# ecdf- all subj
g = sns.displot(data=dfPlot, x=ili, hue='trialType',
                kind='ecdf', hue_order=trialOrder)
g.fig.subplots_adjust(top=0.9)  # adjust the figure for title
g.fig.suptitle('ILI by trial type; all subj')
g.set_xlabels('ILI (s)')
g.set(xlim=(0, 1))
saveFigCustom(g, 'all_ILI_ecdf',savePath)


# Individual distribution of ILI (inter-lick interval)
# only include trialLick~=nan
dfPlot = dfPlot[dfPlot.trialLick10s.notnull()].copy()
# calculate ILI by taking diff() of latencies
ili = dfPlot.groupby(['fileID', 'trialID', 'trialType'])['eventLatency'].diff()
# bar- individual subj
g = sns.catplot(data=dfPlot, y=ili, x='subject',
                hue='trialType',  kind='bar', hue_order=trialOrder)
g.fig.subplots_adjust(top=0.9)  # adjust the figure for title
g.fig.suptitle('ILI by trial type; individual subj')
g.set_ylabels('ILI (s)')
g.set(ylim=(0, 1))
saveFigCustom(g, 'individual_ILI_10s_bar',savePath)



# %% Illustration of groupby() calculations based on date vs trainDayThisStage vs normalized trainDay hierarchies

# #declare hierarchical grouping variables (how should observations be separated)
# # groupers= ['virus', 'sex', 'stage', 'laserDur', 'subject', 'date', 'trialType'] #Opto
# groupers= ['virus', 'sex', 'stage', 'subject', 'date', 'trialType'] #photometry


# #here want percentage of each behavioral outcome per trialType per above groupers
# observation= 'trialOutcomeBeh10s'

# test= percentPortEntryCalc(dfTidy, groupers, observation)

# #test visualization
# dfPlot= test.reset_index().copy()
# g= sns.relplot(data=dfPlot, x= 'date', y='PE', row='stage', hue='trialType', hue_order=trialOrder, kind='line')
# g.fig.suptitle('PE probability: computed by date')


# #declare hierarchical grouping variables (how should observations be separated)
# # groupers= ['virus', 'sex', 'stage', 'laserDur', 'subject', 'trainDay', 'trialType'] #Opto
# groupers= ['virus', 'sex', 'stage', 'subject', 'trainDay', 'trialType'] #photometry


# #here want percentage of each behavioral outcome per trialType per above groupers
# observation= 'trialOutcomeBeh10s'

# test= percentPortEntryCalc(dfTidy, groupers, observation)

# #test visualization
# dfPlot= test.reset_index().copy()
# g= sns.relplot(data=dfPlot, x= 'trainDay', y='PE', row='stage', hue='trialType', hue_order=trialOrder, kind='line')
# g.fig.suptitle('PE probability: computed by raw trainDay')


# #declare hierarchical grouping variables (how should observations be separated)
# # groupers= ['virus', 'sex', 'stage', 'laserDur', 'subject', 'trainDayThisStage', 'trialType'] #Opto
# groupers= ['virus', 'sex', 'stage', 'subject', 'trainDayThisStage', 'trialType'] #photometry


# #here want percentage of each behavioral outcome per trialType per above groupers
# observation= 'trialOutcomeBeh10s'

# test= percentPortEntryCalc(dfTidy, groupers, observation)

# #test visualization
# dfPlot= test.reset_index().copy()
# g= sns.relplot(data=dfPlot, x= 'trainDayThisStage', y='PE', row='stage', hue='trialType', hue_order=trialOrder, kind='line')
# g.fig.suptitle('PE probability: computed by normalized trainDayThisStage')


# %% Save dfTidy so it can be loaded quickly for subesequent analysis

dfTidyAnalyzed = dfTidy.copy()

savePath = r'./_output/'  # r'C:\Users\Dakota\Documents\GitHub\DS-Training\Python'

print('saving dfTidyAnalyzed to file')

# Save as pickel
dfTidyAnalyzed.to_pickle(savePath+'dfTidyAnalyzed.pkl')


# Save as .CSV
# dfTidyAnalyzed.to_csv('dfTidyAnalyzed.csv')


# %% Use pandas profiling on event counts
# This might be a decent way to quickly view behavior session results/outliers if automated
# note- if you are getting errors with ProfileReport() and you installed using conda, remove and reinstall using pip install

# from pandas_profiling import ProfileReport

# #Unstack() the groupby output for a dataframe we can profile
# dfPlot= dfTidy.copy()
# dfPlot= dfPlot.groupby(['subject','date','eventType'])['eventTime'].count().unstack()
# #add trialType counts
# dfPlot= dfPlot.merge(dfTidy.loc[(dfTidy.eventType=='NStime') | (dfTidy.eventType=='DStime')].groupby(['subject','date','trialType'])['eventTime'].count().unstack(),left_index=True,right_index=True)


# profile = ProfileReport(dfPlot, title='Event Count by Session Pandas Profiling Report', explorative = True)

# # save profile report as html
# profile.to_file('pandasProfileEventCounts.html')

# %% all done
print('all done')
