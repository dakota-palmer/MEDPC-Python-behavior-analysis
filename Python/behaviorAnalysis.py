# -*- coding: utf-8 -*-
"""
Created on Tue Aug 31 16:09:42 2021

@author: Dakota
"""

#%% Load dependencies
import pandas as pd
import shelve

import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

#%$ Things to change manually for your data:
    
#dataPath= path to folder containing dfTidy.pkl
#

#%% Load previously saved dfTidy (and other vars) from pickle
dataPath= r'C:\Users\Dakota\Documents\GitHub\DS-Training\Python\\'

dfTidy= pd.read_pickle(dataPath+'dfTidy.pkl')

#load any other variables saved during the import process ('dfTidymeta' shelf)
my_shelf = shelve.open(dataPath+'dfTidymeta')
for key in my_shelf:
    globals()[key]=my_shelf[key]
my_shelf.close()


#%% Plot settings
sns.set_style("darkgrid")

#fixed order of trialType to plot (so consistent between figures)
#for comparison of trial types (e.g. laser on vs laser off, good to have these in paired order for paired color palettes)
trialOrder= ['DStime','NStime','ITI']

if experimentType=='Opto':
    trialOrder= ['laserDStrial_0', 'laserDStrial_1', 'laserNStrial_0', 'laserNStrial_1','ITI']


# %% Preliminary data analyses
# Event latency, count, and behavioral outcome for each trial

#TODO: Lick 'cleaning' to eliminate invalid licks (are they in port, is ILI within reasonable range)


#Calculate latency to each event in trial (from cue onset). based on trialEnd to keep it simple
  # trialEnd is = cue onset + cueDur. So just subtract cueDur for cue onset time  
dfTidy.loc[dfTidy.trialID>=0, 'eventLatency'] = (
    (dfTidy.eventTime)-(dfTidy.trialEnd-dfTidy.cueDur)).copy()

#for 'ITI' events, calculate latency based on last trial end (not cue onset)
dfTidy.loc[dfTidy.trialID<0, 'eventLatency'] = (
    (dfTidy.eventTime)-(dfTidy.trialEnd)).copy()

#TODO: exception needs to be made for first ITI
#for now fill w nan
dfTidy.loc[dfTidy.trialID== -0.5, 'eventLatency']= np.nan

#Count events in each trial 
#use cumcount() of event times within file & trial 

#converting to float for some reason
dfTidy['trialPE'] = dfTidy.loc[(dfTidy.eventType == 'PEtime')].groupby([
'fileID', 'trialID'])['eventTime'].cumcount().copy()

#try transform
dfTidy.loc[:,'trialPE'] = dfTidy.loc[(dfTidy.eventType == 'PEtime')].groupby([
'fileID', 'trialID'])['eventTime'].transform('cumcount').copy()




dfTidy['trialLick'] = dfTidy.loc[(dfTidy.eventType == 'lickTime')].groupby([
    'fileID', 'trialID']).cumcount().copy()

#Define behavioral (pe,lick) outcome for each trial. For my lick+laser sessions I need 
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


#%% Calculate Probability of behavioral outcome for each trial type. 
#This is normalized so is more informative than simple count of trials. 

#calculate Proportion of trials with PE out of all trials for each trial type
#can use nunique() to get count of unique trialIDs with specific PE outcome per file
#given this, can calculate Probortion as #PE/#PE+#noPE
   
#subset data and save as intermediate variable dfGroup
dfGroup= dfTidy.copy()

#for Lick+laser sessions, retain only trials with PE+lick for comparison (OPTO specific)
# dfGroup.loc[dfGroup.laserDur=='Lick',:]= dfGroup.loc[(dfGroup.laserDur=='Lick') & (dfGroup.trialOutcomeBeh=='PE+lick')].copy()
   
dfPlot= dfGroup.copy() 

#get unique outcomes. excluded trials are all nan- don't include them
# outcomes= dfTidy.loc[dfTidy.trialOutcomeBeh.notnull()].trialOutcomeBeh.unique()

#TODO: optimize this- combine outcomes here into one variable
#using apply() might help? or pivot?

# tester[outcomes]= dfPlot[(dfPlot.trialOutcomeBeh==outcomes)].reset_index().groupby(
#     ['fileID','trialType','trialOutcomeBeh'])['trialID'].nunique()


# tester=pd.DataFrame()
# tester2= tester.copy()
# for outcome in outcomes:
#     # tester.loc[:,outcome]= dfPlot.loc[(dfPlot.trialOutcomeBeh==outcome)].reset_index().groupby(
#     #     ['fileID','trialType','trialOutcomeBeh'])['trialID'].nunique()
#     tester.loc[:,outcome]= dfPlot.loc[(dfPlot.trialOutcomeBeh==outcome)].groupby(
#         ['fileID','trialType'],dropna=False)['trialID'].nunique(dropna=False).unstack(fill_value=0).stack()
#     tester2.loc[:,outcome]= dfPlot.loc[(dfPlot.trialOutcomeBeh==outcome)].groupby(
#       ['fileID','trialType'],dropna=False, as_index=False)['trialID'].nunique(dropna=False).unstack(fill_value=0)#.stack()
#     groups= dfPlot.groupby(
#         ['fileID','trialType'],dropna=False)['trialID'].groups
#     groups2= dfPlot.loc[(dfPlot.trialOutcomeBeh==outcome)].groupby(
#         ['fileID','trialType'],dropna=False)['trialID'].groups
#     #seems that indexing conditionallyh with .loc before groupby constrains groups?
#     groups3= dfPlot.groupby(
#         ['fileID','trialType','trialOutcomeBeh'],dropna=False)['trialID'].groups
# tester.fillna(0,inplace=True)

 #still missing some sessions somehow...

#for each unique behavioral outcome, loop through and get count of trials in file
#fill null counts with 0
dfTemp=dfPlot.groupby(
        ['fileID','trialType','trialOutcomeBeh'],dropna=False)['trialID'].nunique(dropna=False).unstack(fill_value=0)

##calculate proportion for each trial type: num trials with outcome/total num trials of this type
outcomeProb= dfTemp.divide(dfTemp.sum(axis=1),axis=0)

#melt() into single column w label
dfTemp= outcomeProb.reset_index().melt(id_vars=['fileID','trialType'],var_name='trialOutcomeBeh',value_name='outcomeProbFile')

#assign back to df by merging
#TODO: can probably be optimized. if this section is run more than once will get errors due to assignment back to dfTidy
# dfTidy.reset_index(inplace=True) #reset index so eventID index is kept

dfTidy= dfTidy.reset_index().merge(dfTemp,'left', on=['fileID','trialType','trialOutcomeBeh']).copy()

dfTidy.loc[:,'outcomeProbFile']= dfTemp.outcomeProbFile




#%% PLOTS:
#%% Plot event counts across sessions (check for outlier sessions/event counts)
sns.set_palette('tab20')  #good for plotting by many subj


#I know that lick count was absurdly high (>9000) due to liquid shorting lickometer on at least 1 session
#visualize event counts by session to ID outliers
#not interested in some events (e.g. # cues is fixed), remove those
dfPlot= dfTidy.loc[(dfTidy.eventType!='NStime') & (dfTidy.eventType!='DStime') & (dfTidy.eventType!='PExEst') & (dfTidy.eventType!='laserOffTime')] 

#count of each event type by date and subj
dfPlot= dfPlot.groupby(['subject','date', 'eventType'])['eventTime'].count().reset_index()


g= sns.relplot(data=dfPlot, col='eventType', x='date', y='eventTime', hue='subject', kind='line',
                facet_kws={'sharey': False, 'sharex': True})
g.fig.subplots_adjust(top=0.9)  # adjust the figure for title
g.fig.suptitle('Total event count across sessions by type- check for outliers')
g.set_ylabels('# of events')
g.set_ylabels('session')

#%% Plot port entry latency by trialType
            
#select data corresponding to first PE from valid trials
dfPlot = dfTidy[(dfTidy.trialID >= 0) & (dfTidy.trialPE == 0)].copy()

# PE latency: virus x laserDur
g = sns.displot(data=dfPlot, x='eventLatency', hue='trialType',
                row='virus', kind='ecdf', hue_order= trialOrder)
g.fig.suptitle('First PE latency by trial type')
g.set_ylabels('First PE latency from epoch start (s)')

#PE latency: virus individual subj
g=sns.catplot(data=dfPlot,y='eventLatency',hue='trialType', x='subject', kind='bar', hue_order=trialOrder)
g.fig.suptitle('First PE latency by trial type')
g.set_ylabels('First PE latency from epoch start (s)')

  #PE latency:  individual subj 
g=sns.displot(data=dfPlot, col='subject', col_wrap=4, x='eventLatency',hue='trialType', kind='ecdf', hue_order=trialOrder)
g.fig.suptitle('First PE latency by trial type')
g.set_ylabels('First PE latency from epoch start (s)')

#%% Plot First lick latencies (time from cue or trialEnd if ITI events) by trialType
# should represent "baseline" behavior  without laser
      
#trial-based, ignoring ITI
# dfPlot = dfTidy[(dfTidy.trialID >= 0)].copy()
#trial-based, including ITI
dfPlot= dfTidy.copy()

#All subj distribution of ILI (inter-lick interval)
#only include first trialLick ==0
dfPlot = dfPlot[dfPlot.trialLick==0].copy()

#box- all subj
g= sns.catplot(data=dfPlot, y='eventLatency', x='trialType',  kind='box', order=trialOrder)
g.fig.subplots_adjust(top=0.9)  # adjust the figure for title
g.fig.suptitle('First Lick latencies by trial type; all subj')
g.set_ylabels('lick latency from epoch start (s)')


#ecdf- all subj'[]
g= sns.displot(data=dfPlot, x='eventLatency', hue='trialType',  kind='ecdf', hue_order=trialOrder)
g.fig.subplots_adjust(top=0.9)  # adjust the figure for title
g.fig.suptitle('First Lick latencies by trial type; all subj')
g.set_xlabels('lick latency from epoch start (s)')


#Individual distribution of ILI (inter-lick interval)
#only include trialLick~=nan 
#bar- individual subj
g= sns.catplot(data=dfPlot, y='eventLatency', x='subject', hue='trialType',  kind='bar', hue_order=trialOrder)
g.fig.subplots_adjust(top=0.9)  # adjust the figure for title
g.fig.suptitle('First Lick latencies by trial type; individual subj')
g.set_ylabels('lick latency from epoch start (s)')

    
# %% Plot inter-lick interval (ILI) by trialType

#trial-based, ignoring ITI
# dfPlot = dfTidy[(dfTidy.trialID >= 0)].copy()
#trial-based, including ITI
dfPlot = dfTidy.copy()

#All subj distribution of ILI (inter-lick interval)
#only include trialLick~=nan (lick timestamps within trials)
dfPlot = dfPlot[dfPlot.trialLick.notnull()].copy()

#calculate ILI by taking diff() of latencies
ili= dfPlot.groupby(['fileID','trialID','trialType'])['eventLatency'].diff()

#ecdf- all subj
g= sns.displot(data=dfPlot, x=ili, hue='trialType',  kind='ecdf', hue_order=trialOrder)
g.fig.subplots_adjust(top=0.9)  # adjust the figure for title
g.fig.suptitle('ILI by trial type; all subj')
g.set_xlabels('ILI (s)')
g.set(xlim=(0,1))


#Individual distribution of ILI (inter-lick interval)
#only include trialLick~=nan
dfPlot = dfPlot[dfPlot.trialLick.notnull()].copy()
#calculate ILI by taking diff() of latencies
ili= dfPlot.groupby(['fileID','trialID','trialType'])['eventLatency'].diff()
#bar- individual subj
g= sns.catplot(data=dfPlot, y=ili, x='subject', hue='trialType',  kind='bar', hue_order=trialOrder)
g.fig.subplots_adjust(top=0.9)  # adjust the figure for title
g.fig.suptitle('ILI by trial type; individual subj')
g.set_ylabels('ILI (s)')
g.set(ylim=(0,1))

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
