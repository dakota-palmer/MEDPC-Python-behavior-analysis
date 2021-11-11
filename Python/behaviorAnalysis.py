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
    plt.gcf().set_size_inches((20,10), forward=False) # ~monitor size
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

#fixed order of trialType to plot (so consistent between figures)
#for comparison of trial types (e.g. laser on vs laser off, good to have these in paired order for paired color palettes)
trialOrder= ['DStime','NStime','Pre-Cue', 'ITI']

#DS PE probability criteria (for visualization)
criteriaDS= 0.6

if experimentType=='Opto':
    # trialOrder= ['laserDStrial_0', 'laserDStrial_1', 'laserNStrial_0', 'laserNStrial_1', 'Pre-Cue', 'ITI']
    # trialOrder= [trialOrder, 'laserDStrial_0', 'laserDStrial_1', 'laserNStrial_0', 'laserNStrial_1']
    trialOrder= (['DStime', 'DStime_laser', 'NStime', 'NStime_laser', 'Pre-Cue','ITI'])

# %% Preliminary data analyses
# Event latency, count, and behavioral outcome for each trial

#TODO: Lick 'cleaning' to eliminate invalid licks (are they in port, is ILI within reasonable range)


# #Calculate latency to each event in trial (from cue onset). based on trialEnd to keep it simple
#   # trialEnd is = cue onset + cueDur. So just subtract cueDur for cue onset time  
# dfTidy.loc[dfTidy.trialID>=0, 'eventLatency'] = (
#     (dfTidy.eventTime)-(dfTidy.trialEnd-dfTidy.cueDur)).copy()

#DP 9/28/21:
#have trial start now, subtract trialStart from eventTime to get latency per trial
#no need for -trialID exception
dfTidy.loc[:,'eventLatency']= ((dfTidy.eventTime)-(dfTidy.trialStart)).copy()
# 
# dfTidy.loc[dfTidy.trialID>=0,'eventLatency']= ((dfTidy.eventTime)-(dfTidy.trialStart))

# dfTidy.loc[dfTidy.trialID<0, 'eventLatency'] = ((dfTidy.eventTime)-(dfTidy.trialStart)).copy()

#TODO: exception needs to be made for first ITI; for now fill w nan
dfTidy.loc[dfTidy.trialID== -999, 'eventLatency']= np.nan

#Count events in each trial 
#use cumcount() of event times within file & trial 

#converting to float for some reason
dfTidy['trialPE'] = dfTidy.loc[(dfTidy.eventType == 'PEtime')].groupby([
'fileID', 'trialID'])['eventTime'].cumcount().copy()

# #try transform
# dfTidy.loc[:,'trialPE'] = dfTidy.loc[(dfTidy.eventType == 'PEtime')].groupby([
# 'fileID', 'trialID'])['eventTime'].transform('cumcount').copy()


dfTidy['trialLick'] = dfTidy.loc[(dfTidy.eventType == 'lickTime')].groupby([
    'fileID', 'trialID']).cumcount().copy()

# Add trainDay variable (cumulative count of sessions within each subject)
dfGroup= dfTidy.loc[dfTidy.groupby(['subject','fileID']).cumcount()==0]
# test= dfGroup.groupby(['subject','fileID']).transform('cumcount')
dfTidy.loc[:,'trainDay']= dfGroup.groupby(['subject'])['fileID'].transform('cumcount')
dfTidy.loc[:,'trainDay']= dfTidy.groupby(['subject','fileID']).fillna(method='ffill')


#%% TODO: count events within 10s of cue onset (cue duration in final stage)  
#this is mainly for comparing progression/learning between stages since cueDuration varies by stage

dfTemp=  dfTidy.loc[((dfTidy.eventLatency<= 10) & (dfTidy.eventLatency>0))].copy()

dfTidy['trialPE10s'] = dfTemp.loc[(dfTemp.eventType == 'PEtime')].groupby([
'fileID', 'trialID'])['eventTime'].cumcount().copy()

dfTidy['trialLick10s'] = dfTemp.loc[(dfTemp.eventType == 'lickTime')].groupby([
'fileID', 'trialID'])['eventTime'].cumcount().copy()

#%% Define behavioral (pe,lick) outcome for each trial. For my lick+laser sessions I need 
#to isolate trials with both a PE+lick to measure effect of laser

#For each trial (trialID >=0),
#count the number of PEs per trial. if >0, they entered the port and earned sucrose. If=0, they did not.
#since groupby counting methods don't work well with nans, using nunique() 
# peOutcome= dfTidy.loc[dfTidy.trialID>=0].groupby(['fileID','trialID'],dropna=False)['trialPE'].nunique()
#do for all trials
outcome= dfTidy.groupby(['fileID','trialID'],dropna=False)['trialPE'].nunique()

#naming "trialOutcomeBeh" for now to distinguish between behavioral outcome and reward outcome if needed later
trialOutcomeBeh= outcome.copy()

trialOutcomeBeh.loc[outcome>0]='PE'
trialOutcomeBeh.loc[outcome==0]='noPE'

#now do the same for licks
outcome= dfTidy.groupby(['fileID','trialID'],dropna=False)['trialLick'].nunique()

#add lick outcome + PE outcome for clarity #if it doesn't say '+lick', then none was counted
trialOutcomeBeh.loc[outcome>0]=trialOutcomeBeh.loc[outcome>0]+ '+' + 'lick'

#set index to file,trial and
#fill in matching file,trial with trialOutcomeBeh
#TODO: I think there is a more efficient way to do this assignment, doens't take too long tho

dfTidy= dfTidy.reset_index().set_index(['fileID','trialID'])

dfTidy.loc[trialOutcomeBeh.index,'trialOutcomeBeh']= trialOutcomeBeh

#reset index to eventID
dfTidy= dfTidy.reset_index().set_index(['eventID'])

#%% same as above but behavioral outcome within first 10s of each trial
outcome= dfTidy.groupby(['fileID','trialID'],dropna=False)['trialPE10s'].nunique()

#naming "trialOutcomeBeh" for now to distinguish between behavioral outcome and reward outcome if needed later
#10s = within 10s of epoch start
trialOutcomeBeh= outcome.copy()

trialOutcomeBeh.loc[outcome>0]='PE'
trialOutcomeBeh.loc[outcome==0]='noPE'

#now do the same for licks
outcome= dfTidy.groupby(['fileID','trialID'],dropna=False)['trialLick10s'].nunique()

#add lick outcome + PE outcome for clarity #if it doesn't say '+lick', then none was counted
trialOutcomeBeh.loc[outcome>0]=trialOutcomeBeh.loc[outcome>0]+ '+' + 'lick'

#set index to file,trial and
#fill in matching file,trial with trialOutcomeBeh
#TODO: I think there is a more efficient way to do this assignment, doens't take too long tho

dfTidy= dfTidy.reset_index().set_index(['fileID','trialID'])

dfTidy.loc[trialOutcomeBeh.index,'trialOutcomeBeh10s']= trialOutcomeBeh

#reset index to eventID
dfTidy= dfTidy.reset_index().set_index(['eventID'])

#%% Calculate Probability of behavioral outcome for each trial type. 
#This is normalized so is more informative than simple count of trials. 

#calculate Proportion of trials with PE out of all trials for each trial type
#can use nunique() to get count of unique trialIDs with specific PE outcome per file
#given this, can calculate Probortion as #PE/#PE+#noPE
   
#subset data and save as intermediate variable dfGroup
#get only one entry per trial
dfGroup= dfTidy.loc[dfTidy.groupby(['fileID','trialID']).cumcount()==0].copy()

#for Lick+laser sessions, retain only trials with PE+lick for comparison (OPTO specific)
# dfGroup.loc[dfGroup.laserDur=='Lick',:]= dfGroup.loc[(dfGroup.laserDur=='Lick') & (dfGroup.trialOutcomeBeh=='PE+lick')].copy()
   
dfPlot= dfGroup.copy() 

#for each unique behavioral outcome, loop through and get count of trials in file
#fill null counts with 0
dfTemp=dfPlot.groupby(
        ['fileID','trialType','trialOutcomeBeh'],dropna=False)['trialID'].nunique(dropna=False).unstack(fill_value=0)


##calculate proportion for each trial type: num trials with outcome/total num trials of this type

trialCount= dfTemp.sum(axis=1)


outcomeProb= dfTemp.divide(dfTemp.sum(axis=1),axis=0)

#melt() into single column w label
dfTemp= outcomeProb.reset_index().melt(id_vars=['fileID','trialType'],var_name='trialOutcomeBeh',value_name='outcomeProbFile')

#assign back to df by merging
#TODO: can probably be optimized. if this section is run more than once will get errors due to assignment back to dfTidy
# dfTidy.reset_index(inplace=True) #reset index so eventID index is kept

dfTidy= dfTidy.reset_index().merge(dfTemp,'left', on=['fileID','trialType','trialOutcomeBeh']).copy()

#%% Same as above but probability of behavioral outcome within first 10s of trial 
#This is normalized so is more informative than simple count of trials. 

#calculate Proportion of trials with PE out of all trials for each trial type
#can use nunique() to get count of unique trialIDs with specific PE outcome per file
#given this, can calculate Probortion as #PE/#PE+#noPE
   
#subset data and save as intermediate variable dfGroup
#get only one entry per trial
dfGroup= dfTidy.loc[dfTidy.groupby(['fileID','trialID']).cumcount()==0].copy()

#for Lick+laser sessions, retain only trials with PE+lick for comparison (OPTO specific)
# dfGroup.loc[dfGroup.laserDur=='Lick',:]= dfGroup.loc[(dfGroup.laserDur=='Lick') & (dfGroup.trialOutcomeBeh=='PE+lick')].copy()
   
dfPlot= dfGroup.copy() 

#for each unique behavioral outcome, loop through and get count of trials in file
#fill null counts with 0
dfTemp=dfPlot.groupby(
        ['fileID','trialType','trialOutcomeBeh10s'],dropna=False)['trialID'].nunique(dropna=False).unstack(fill_value=0)


##calculate proportion for each trial type: num trials with outcome/total num trials of this type

trialCount= dfTemp.sum(axis=1)


outcomeProb= dfTemp.divide(dfTemp.sum(axis=1),axis=0)

#melt() into single column w label
dfTemp= outcomeProb.reset_index().melt(id_vars=['fileID','trialType'],var_name='trialOutcomeBeh10s',value_name='outcomeProbFile10s')

#assign back to df by merging
#TODO: can probably be optimized. if this section is run more than once will get errors due to assignment back to dfTidy
# dfTidy.reset_index(inplace=True) #reset index so eventID index is kept

dfTidy= dfTidy.reset_index().merge(dfTemp,'left', on=['fileID','trialType','trialOutcomeBeh10s']).copy()


#%% PLOTS:
    
#%% Plot event counts across sessions (check for outlier sessions/event counts)
sns.set_palette('tab20')  #good for plotting by many subj


#I know that lick count was absurdly high (>9000) due to liquid shorting lickometer on at least 1 session
#visualize event counts by session to ID outliers
#not interested in some events (e.g. # cues is fixed), remove those
dfPlot= dfTidy.loc[(dfTidy.eventType!='NStime') & (dfTidy.eventType!='DStime') & (dfTidy.eventType!='PExEst') & (dfTidy.eventType!='laserOffTime')].copy()

#count of each event type by date and subj
dfPlot= dfPlot.groupby(['subject','date', 'eventType'])['eventTime'].count().reset_index()

g= sns.relplot(data=dfPlot, col='eventType', x='date', y='eventTime', hue='subject', kind='line', style='subject', markers=True, dashes=False,
                facet_kws={'sharey': False, 'sharex': True})
g.fig.subplots_adjust(top=0.9)  # adjust the figure for title
g.fig.suptitle('Total event count across sessions by type- check for outliers')
g.set_ylabels('# of events')
g.set_ylabels('session')

saveFigCustom(g, 'individual_eventCounts_line')

#%% Plot PE probability by trialType (within 10s of trial start)
sns.set_palette('Paired') #default  #tab10
#subset data and save as intermediate variable dfGroup
dfGroup= dfTidy.copy()
 


#cumulative count of training day within-stage (so we can normalize between subjects appropriately)
dfGroup= dfTidy.loc[dfTidy.groupby('fileID').transform('cumcount')==0,:].copy() #one per session
dfTidy['trainDayThisStage']=  dfGroup.groupby(['subject', 'stage']).transform('cumcount')
dfTidy.trainDayThisStage= dfTidy.groupby(['fileID'])['trainDayThisStage'].fillna(method='ffill').copy()




#select data
#all trialTypes excluding ITI     
# dfPlot = dfGroup[(dfGroup.trialType != 'ITI')].copy()

#all trialTypes excluding ITI     
# dfPlot = dfGroup[(dfGroup.trialType != 'ITI') & (dfGroup.trialType !='Pre-Cue')].copy()
# trialOrderPlot= ['DStime','DStime_laser','NStime','NStime_laser']

#Only DS & NS trialTypes
dfGroup= dfTidy.copy()
dfPlot = dfGroup[(dfGroup.trialType == 'DStime') | (dfGroup.trialType =='NStime')].copy()
trialOrderPlot= ['DStime','NStime']


#define stages for 'early' and 'late' subplotting
#TODO: consider groupby() stage and counting day within each stage to get the first x sessions of stage 5 compared to last?
earlyStages= ['Stage 1','Stage 2','Stage 3','Stage 4']
lateStages= ['Stage 5', 'Stage 5+tether']
earlyStages= ['Stage 4']
lateStages= ['Stage 5+tether']
testStages= ['Cue Manipulation']
dfPlot['stageType']= pd.NA #dfPlot.stage.astype('str').copy()

dfPlot.loc[dfPlot.stage.isin(earlyStages), 'stageType']= 'early'
dfPlot.loc[dfPlot.stage.isin(lateStages), 'stageType']= 'late'
dfPlot.loc[dfPlot.stage.isin(testStages), 'stageType']= 'test'

dfGroup= dfTidy.loc[dfTidy.groupby('fileID').transform('cumcount')==0,:].copy() #one per session
test= dfGroup.groupby(['subject', 'stage']).transform('cumcount')

# dfPlot.stageType= dfPlot.stageType.astype('category')

#exclude test sessions
# dfPlot= dfPlot.loc[dfPlot.stageType != 'test',:].copy()


 
#get only PE outcomes
# dfPlot.reset_index(inplace=True)
dfPlot= dfPlot.loc[(dfPlot.trialOutcomeBeh10s=='PE') | (dfPlot.trialOutcomeBeh10s=='PE+lick')].copy()
 
#since we calculated aggregated proportion across all trials in session,
#take only first index. Otherwise repeated observations are redundant
dfPlot= dfPlot.groupby(['fileID','trialType','trialOutcomeBeh10s']).first().copy()
 
#sum together both PE and PE+lick for total overall PE prob
# dfPlot['outcomeProbFile']= dfPlot.groupby(['fileID'])['outcomeProbFile'].sum().copy()
 
dfPlot['probPE']= dfPlot.groupby(['fileID','trialType'])['outcomeProbFile10s'].sum().copy()

#get an aggregated x axis for files per subject
fileAgg= dfPlot.reset_index().groupby(['subject','fileID','trialType']).cumcount().copy()==0
 
#since grouping PE and PE+lick, we still have redundant observations
#retain only 1 per trial type per file
dfPlot= dfPlot.reset_index().loc[fileAgg]

#subjects may run different session types on same day (e.g. different laserDur), so shouldn't plot simply by date across subjects
#individual plots by date is ok
# sns.set_palette('Paired')

#a few examples of options here
# g= sns.relplot(data=dfPlot, x='date', y='probPE', col='subject', col_wrap=4, hue='trialType', hue_order=trialOrder, kind='line', style='subject', markers=True, dashes=False)
# g= sns.relplot(data=dfPlot, x='date', y='probPE', col='subject', col_wrap=4, hue='trialType', hue_order=trialOrder, kind='line', size='stage')
# g= sns.relplot(data= dfPlot, x='date', y='probPE', hue='subject', kind='line', style='trialType', markers=True)

# g= sns.relplot(data= dfPlot, x='date', y='probPE', hue='subject', kind='line', style='trialType', markers=True, row='stage')
# g.set_titles('{row_name}')
g= sns.relplot(data=dfPlot, x='date', y='probPE', col='subject', col_wrap=4, hue='trialType', hue_order=trialOrder, kind='line', style='stage', markers=True, dashes=True)
g.map(plt.axhline, y=criteriaDS, color=".2", linewidth=3, dashes=(3,1), zorder=0)
g.fig.suptitle('Evolution of the probPE in subjects by trialType')
saveFigCustom(g, 'training_peProb_10s_individual')


#virus , sex facet 
#only DS and NS
g= sns.relplot(data=dfPlot, x='date', y='probPE', col='sex', row='virus', hue='trialType', hue_order=trialOrder, kind='line', style='stage', markers=True, dashes=True)
g.map(plt.axhline, y=criteriaDS, color=".2", linewidth=3, dashes=(3,1), zorder=0)
saveFigCustom(g, 'training_peProb_10s_virus+sex')

g= sns.relplot(data=dfPlot, x='trainDay', y='probPE', col='sex', row='virus', hue='trialType', hue_order=trialOrder, kind='line', style='stage', markers=True, dashes=True)
g.map(plt.axhline, y=criteriaDS, color=".2", linewidth=3, dashes=(3,1), zorder=0)
saveFigCustom(g, 'training_peProb_10s_virus+sex_trainDay')

g= sns.relplot(data=dfPlot, x='date', y='probPE', row='virus', hue='trialType', hue_order=trialOrder, kind='line', style='stage', markers=True, dashes=True)
g.map(plt.axhline, y=criteriaDS, color=".2", linewidth=3, dashes=(3,1), zorder=0)
saveFigCustom(g, 'training_peProb_10s_virus')

#facet early v late stages #for iris like christelle's opto plot
g= sns.relplot(data=dfPlot, x='trainDayThisStage', y='probPE', col='stageType', hue='trialType', hue_order=trialOrderPlot, kind='line', style='sex', markers=True, dashes=True
               , facet_kws={'sharey': True, 'sharex': False}, palette= 'tab10')
g.map(plt.axhline, y=criteriaDS, color=".2", linewidth=3, dashes=(3,1), zorder=0)
saveFigCustom(g, 'training_peProb_10s_early_vs_late_trainDay')


#training across stages
#%% define specific stages to plot!
stagesToPlot= pd.Series(dfTidy.loc[dfTidy.stage.notnull(),'stage'].unique())
stagesToPlot= stagesToPlot.loc[((stagesToPlot.str.contains('5')) | (stagesToPlot.str.contains('Manipulation')))]

dfPlot= dfPlot.loc[dfPlot.stage.isin(stagesToPlot)].copy()
dfPlot.stage= dfPlot.stage.cat.remove_unused_categories()


# #define specific trialTypes to plot!
# trialTypesToPlot= pd.Series(dfTidy.loc[dfTidy.trialType.notnull(),'trialType'].unique())
# trialTypesToPlot= trialTypesToPlot.loc[((trialTypesToPlot.str.contains('DS')) | (trialTypesToPlot.str.contains('NS')))]

# dfPlot= dfPlot.loc[dfPlot.trialType.isin(trialTypesToPlot)]
# dfPlot.trialType= dfTidy.trialType.cat.remove_unused_categories()

#late stages only
g= sns.relplot(data=dfPlot, x='date', y='probPE', col='subject', col_wrap=4, hue='trialType', hue_order=trialOrder, kind='line', style='stage', markers=True, dashes=True)
g.map(plt.axhline, y=criteriaDS, color=".2", linewidth=3, dashes=(3,1), zorder=0)
g.fig.suptitle('Evolution of the probPE in subjects by trialType')
saveFigCustom(g, 'training_peProb_10s_lateStages_individual')

g= sns.relplot(data=dfPlot, x='trainDay', y='probPE', col='subject', col_wrap=4, hue='trialType', hue_order=trialOrder, kind='line', style='stage', markers=True, dashes=True)
g.map(plt.axhline, y=criteriaDS, color=".2", linewidth=3, dashes=(3,1), zorder=0)
g.fig.suptitle('Evolution of the probPE in subjects by trialType')
saveFigCustom(g, 'training_peProb_10s_lateStages_individual_trainDay')


g= sns.relplot(data=dfPlot, x='date', y='probPE', row='stage', col='virus', hue='trialType', hue_order=trialOrder, kind='line', style='virus', markers=True, dashes=True)
g.map(plt.axhline, y=criteriaDS, color=".2", linewidth=3, dashes=(3,1), zorder=0)
saveFigCustom(g, 'training_peProb_10s_lateStages_virus')


g= sns.relplot(data=dfPlot, x='trainDay', y='probPE', row='stage', col='virus', hue='trialType', hue_order=trialOrder, kind='line', style='virus', markers=True, dashes=True)
g.map(plt.axhline, y=criteriaDS, color=".2", linewidth=3, dashes=(3,1), zorder=0)
saveFigCustom(g, 'training_peProb_10s_lateStages_virus_trainDay')

# g= sns.relplot(data=dfPlot, x='date', y='probPE', row='trialType', hue='virus', kind='line', style='virus', markers=True, dashes=False)
# g.map(plt.axhline, y=criteriaDS, color=".2", linewidth=3, dashes=(3,1), zorder=0)

#individual subj lines
# g= sns.relplot(data=dfPlot, x='date', y='probPE', row='trialType', units='subject', estimator=None, hue='virus', kind='line', style='stage', markers=True, dashes=False, palette='tab10')
# g.map(plt.axhline, y=criteriaDS, color=".2", linewidth=3, dashes=(3,1), zorder=0)
# g.fig.suptitle('Evolution of the probPE in subjects by trialType')


#% TODO: ECDF of behavioral outcome (PE) would be nice to view compared to latency ECDFs?

#%% Plot PE latency by trialType
            
#select data corresponding to first PE from valid trials, excluding ITI
dfPlot = dfTidy[(dfTidy.trialType!='ITI') & (dfTidy.trialPE10s == 0)].copy()

# PE latency: virus
g = sns.displot(data=dfPlot, x='eventLatency', hue='trialType',
                row='virus', kind='ecdf', hue_order= trialOrder)
g.fig.suptitle('First PE latency by trial type')
g.set_ylabels('First PE latency from epoch start (s)')
saveFigCustom(g, 'virus_peLatency_10s_ecdf')

  #PE latency:  individual subj 
g=sns.displot(data=dfPlot, col='subject', col_wrap=4, x='eventLatency',hue='trialType', kind='ecdf', hue_order=trialOrder)
g.fig.suptitle('First PE latency by trial type (within 10s)')
g.set_ylabels('Probability: first PE latency from epoch start')
saveFigCustom(g, 'individual_peLatency_10s_ecdf')


 #training across stages
dfPlot.eventLatency= dfPlot.eventLatency.astype('float') #TODO: correct dtypes early in code

g= sns.relplot(data=dfPlot, x='date', y='eventLatency', col='subject', col_wrap=4, hue='trialType', hue_order=trialOrder, kind='line', style='stage', markers=True, dashes=True)
g.fig.suptitle('Evolution of first PE latency by trialType')
saveFigCustom(g, 'training_peLatency_10s_individual')


g= sns.relplot(data=dfPlot, x='date', y='eventLatency', row='virus', hue='trialType', hue_order=trialOrder, kind='line', style='stage', markers=True, dashes=True)
g.fig.suptitle('Evolution of first PE latency by trialType')
saveFigCustom(g, 'training_peLatency_10s_virus+sex')


# late stages plots
dfPlot= dfPlot.loc[dfPlot.stage.isin(stagesToPlot)]

g = sns.displot(data=dfPlot, x='eventLatency', hue='trialType',
                row='virus', col='stage', kind='ecdf', hue_order= trialOrder)
g.fig.suptitle('First PE latency by trial type, late stages')
g.set_ylabels('Probability: first PE latency from epoch start')
saveFigCustom(g, 'dist_peLatency_10s_lateStages_virus_ecdf')


g= sns.relplot(data=dfPlot, x='date', y='eventLatency', row='virus', hue='trialType', hue_order=trialOrder, kind='line', style='stage', markers=True, dashes=True)
g.fig.suptitle('Evolution of first PE latency by trialType, late stages')
saveFigCustom(g, 'training_peLatency_10s_lateStages_virus')




#%% TODO: Custom Ridge Plot to show changes in distribution over time

# # Initialize the FacetGrid object
# pal = sns.cubehelix_palette(10, rot=-.25, light=.7)
# # g = sns.FacetGrid(dfPlot, row="date", hue="date", col='subject', aspect=15, height=10, palette=pal)
# g = sns.FacetGrid(dfPlot, row="date", hue="date", col='subject')#, aspect=15, height=10, palette=pal)


# # Draw the densities in a few steps
# g.map(sns.kdeplot, "eventLatency",
#       bw_adjust=.5, clip_on=False,
#       fill=True, alpha=1, linewidth=1.5)
# # g.map(sns.kdeplot, "eventLatency", clip_on=False, color="w", lw=2, bw_adjust=.5)

# # passing color=None to refline() uses the hue mapping
# # g.refline(y=0, linewidth=2, linestyle="-", color=None, clip_on=False)


# # Define and use a simple function to label the plot in axes coordinates
# def label(x, color, label):
#     ax = plt.gca()
#     ax.text(0, .2, label, fontweight="bold", color=color,
#             ha="left", va="center", transform=ax.transAxes)


# g.map(label, "eventLatency")

# # Set the subplots to overlap
# # g.figure.subplots_adjust(hspace=-.25)

# # Remove axes details that don't play well with overlap
# g.set_titles("")
# g.set(yticks=[], ylabel="")
# g.despine(bottom=True, left=True)


#%% Plot First lick latencies (time from cue or trialEnd if ITI events) by trialType (within 10s)
# should represent "baseline" behavior  without laser
      
#trial-based, ignoring ITI
dfPlot = dfTidy[(dfTidy.trialType !='ITI')].copy()
#trial-based, including ITI
# dfPlot= dfTidy.copy()

#All subj distribution of ILI (inter-lick interval)
#only include first trialLick ==0
dfPlot = dfPlot[dfPlot.trialLick10s==0].copy()

#box- all subj
g= sns.catplot(data=dfPlot, y='eventLatency', x='trialType',  kind='box', order=trialOrder)
g.fig.subplots_adjust(top=0.9)  # adjust the figure for title
g.fig.suptitle('First Lick latencies by trial type; all subj')
g.set_ylabels('lick latency from epoch start (s)')
saveFigCustom(g, 'all_lickLatency_10s_box')



#ecdf- all subj'[]
g= sns.displot(data=dfPlot, x='eventLatency', hue='trialType',  kind='ecdf', hue_order=trialOrder)
g.fig.subplots_adjust(top=0.9)  # adjust the figure for title
g.fig.suptitle('First Lick latencies by trial type; all subj')
g.set_xlabels('lick latency from epoch start (s)')
saveFigCustom(g, 'all_lickLatency_10s_ecdf')



#Individual distribution of ILI (inter-lick interval)
#only include trialLick~=nan 
#bar- individual subj
g= sns.catplot(data=dfPlot, y='eventLatency', x='subject', hue='trialType',  kind='bar', hue_order=trialOrder)
g.fig.subplots_adjust(top=0.9)  # adjust the figure for title
g.fig.suptitle('First Lick latencies by trial type; individual subj')
g.set_ylabels('lick latency from epoch start (s)')
saveFigCustom(g, 'individual_lickLatency_10s_bar')


    
# %% Plot inter-lick interval (ILI) by trialType (within 10s)

#trial-based, ignoring ITI
dfPlot = dfTidy[(dfTidy.trialType!= 'ITI')].copy()
#trial-based, including ITI
# dfPlot = dfTidy.copy()

#All subj distribution of ILI (inter-lick interval)
#only include trialLick~=nan (lick timestamps within trials)
dfPlot = dfPlot[dfPlot.trialLick10s.notnull()].copy()

#calculate ILI by taking diff() of latencies
ili= dfPlot.groupby(['fileID','trialID','trialType'])['eventLatency'].diff()

#ecdf- all subj
g= sns.displot(data=dfPlot, x=ili, hue='trialType',  kind='ecdf', hue_order=trialOrder)
g.fig.subplots_adjust(top=0.9)  # adjust the figure for title
g.fig.suptitle('ILI by trial type; all subj')
g.set_xlabels('ILI (s)')
g.set(xlim=(0,1))
saveFigCustom(g, 'all_ILI_ecdf')



#Individual distribution of ILI (inter-lick interval)
#only include trialLick~=nan
dfPlot = dfPlot[dfPlot.trialLick10s.notnull()].copy()
#calculate ILI by taking diff() of latencies
ili= dfPlot.groupby(['fileID','trialID','trialType'])['eventLatency'].diff()
#bar- individual subj
g= sns.catplot(data=dfPlot, y=ili, x='subject', hue='trialType',  kind='bar', hue_order=trialOrder)
g.fig.subplots_adjust(top=0.9)  # adjust the figure for title
g.fig.suptitle('ILI by trial type; individual subj')
g.set_ylabels('ILI (s)')
g.set(ylim=(0,1))
saveFigCustom(g, 'individual_ILI_10s_bar')


#%% trying stuff with data hierarchy grouping

  # by_many<- group_by(py_data, virus, sex, stage, laserDur, subject, fileID, trialType, trialOutcomeBeh10s)

groupers= ['virus','sex','stage','laserDur', 'subject', 'date', 'trialType']

#hierarchy should be something like groupVars -> stageVars -> subjVars-> sessionVars -> date -> fileID -> trialType/trialVars -> trialID -> eventVars

#seems that the grouping here is using all possible combos (e.g. creating entries for F Sex even for subjects that are M)
dfGroup= dfTidy.copy().groupby(['virus','sex','stage','laserDur', 'subject', 'date', 'trialType'])

#observed=True parameter only includes observed categories
# dfGroup= dfTidy.copy().groupby(['virus','sex','stage','laserDur', 'subject', 'date', 'trialType'], observed=True)


dfGroupComp= pd.DataFrame()
dfGroupComp['trialCount']= dfGroup['trialID'].nunique()
dfGroupComp.reset_index(inplace=True)

# dfGroupComp2= dfTidy.copy()
# dfGroupComp2['trialCount']= dfGroup['trialID'].transform('nunique')


sns.catplot(data= dfGroupComp, row='virus', col='sex', x='stage', y='trialCount', hue='trialType', hue_order=trialOrder, kind='bar')


#^this was just example, now do something more relevant to behavior analysis

dfGroup= dfTidy.copy().groupby(['virus','sex','stage','laserDur', 'subject', 'date', 'trialType'])

dfGroupComp= pd.DataFrame()
# dfGroupComp['outcomeBehCount']= dfGroup['trialOutcomeBeh10s'].value_counts()
# dfGroupComp['outcomeBehCount']= dfGroup['trialOutcomeBeh10s'].transform(pd.Series.mode)
# dfGroupComp['outcomeBehCount']= dfGroup['trialOutcomeBeh10s'].transform(dfTidy.trialOutcomeBeh10s.mode)


# dfGroupComp.reset_index(inplace=True)


# sns.catplot(data= dfGroupComp, row='virus', col='sex', x='trialOutcomeBeh10s', y='outcomeBehCount', hue='trialType', hue_order=trialOrder, kind='bar')


#^ can calculate proportion more efficiently?
# dfGroup= dfTidy.copy().groupby(['virus','sex','stage','laserDur', 'subject', 'date', 'trialType'])

#subset to one event per trial, then groupby()
dfGroup= dfTidy.copy().loc[dfTidy.groupby(['fileID','trialID']).cumcount()==0].groupby(groupers)

dfGroupComp= pd.DataFrame()
dfGroupComp['trialCount']= dfGroup['trialID'].nunique()
dfGroupComp= dfGroupComp.reset_index(drop=False).set_index(groupers)



dfGroupComp2= pd.DataFrame()
dfGroupComp2['outcomeBehCount']= dfGroup['trialOutcomeBeh10s'].value_counts()
dfGroupComp2= dfGroupComp2.reset_index(drop=False).set_index(groupers)

#issue now would be dividing appropriately with non-unique index
#could try using transform() operation?
# dfGroupComp2['outcomeProb']= dfGroupComp2.outcomeBehCount/dfGroupComp.trialCount

#do division while indexed by groupers, then reset index for reassignment of result
outcomeProb= dfGroupComp2.outcomeBehCount/dfGroupComp.trialCount

dfGroupComp.reset_index(inplace=True, drop=False)
outcomeProb= outcomeProb.reset_index().copy()

# dfGroupComp['outcomeProb']= outcomeProb.copy()



#can imagine doing peri-event analyses like so
dfGroup= dfTidy.copy().groupby(['virus','sex','stage','laserDur', 'subject', 'date', 'trialType', 'eventType'])

dfGroupComp= pd.DataFrame()
dfGroupComp['eventOnsets']= dfGroup['eventTime'].value_counts()


#%% Save dfTidy so it can be loaded quickly for subesequent analysis

dfTidyAnalyzed= dfTidy.copy()

savePath= r'./_output/' #r'C:\Users\Dakota\Documents\GitHub\DS-Training\Python' 

print('saving dfTidyAnalyzed to file')

#Save as pickel
dfTidyAnalyzed.to_pickle(savePath+'dfTidyAnalyzed.pkl')


# Save as .CSV
# dfTidyAnalyzed.to_csv('dfTidyAnalyzed.csv')


#%% Use pandas profiling on event counts
##This might be a decent way to quickly view behavior session results/outliers if automated
## note- if you are getting errors with ProfileReport() and you installed using conda, remove and reinstall using pip install

# from pandas_profiling import ProfileReport

# #Unstack() the groupby output for a dataframe we can profile
# dfPlot= dfTidy.copy()
# dfPlot= dfPlot.groupby(['subject','date','eventType'])['eventTime'].count().unstack()
# #add trialType counts
# dfPlot= dfPlot.merge(dfTidy.loc[(dfTidy.eventType=='NStime') | (dfTidy.eventType=='DStime')].groupby(['subject','date','trialType'])['eventTime'].count().unstack(),left_index=True,right_index=True)


# profile = ProfileReport(dfPlot, title='Event Count by Session Pandas Profiling Report', explorative = True)

# # save profile report as html
# profile.to_file('pandasProfileEventCounts.html')

#%% all done
print('all done')