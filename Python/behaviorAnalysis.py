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

#%% Load previously saved dfTidy (and other vars) from pickle
dataPath= r'C:\Users\Dakota\Documents\GitHub\DS-Training\Python\dfTidy.pkl'

dfTidy= pd.read_pickle(dataPath)

#load any other variables saved during the import process ('dfTidymeta' shelf)
my_shelf = shelve.open(r'C:\Users\Dakota\Documents\GitHub\DS-Training\Python\dfTidymeta')
for key in my_shelf:
    globals()[key]=my_shelf[key]
my_shelf.close()


# %% Preliminary data analyses
# Event latency, count, and behavioral outcome for each trial

#TODO: Lick 'cleaning' to eliminate invalid licks (are they in port, is ILI within reasonable range)


#Calculate latency to each event in trial (from cue onset). based on trialEnd to keep it simple
  # trialEnd is = cue onset + cueDur. So just subtract cueDur for cue onset time  
dfTidy.loc[dfTidy.trialID>=0, 'eventLatency'] = (
    (dfTidy.eventTime)-(dfTidy.trialEnd-cueDur)).copy()

#for 'ITI' events, calculate latency based on last trial end (not cue onset)
dfTidy.loc[dfTidy.trialID<0, 'eventLatency'] = (
    (dfTidy.eventTime)-(dfTidy.trialEnd)).copy()

#TODO: exception needs to be made for first ITI
#for now fill w nan
dfTidy.loc[dfTidy.trialID== -0.5, 'eventLatency']= np.nan

#Count events in each trial 
#use cumcount() of event times within file & trial 
dfTidy['trialPE'] = dfTidy.loc[(dfTidy.eventType == 'x_K_PEtime')].groupby([
'fileID', 'trialID'])['eventTime'].cumcount().copy()

dfTidy['trialLick'] = dfTidy.loc[(dfTidy.eventType == 'x_S_lickTime')].groupby([
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
