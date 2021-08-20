# -*- coding: utf-8 -*-
"""
Created on Mon Aug 16 12:01:47 2021

@author: Dakota
"""
#%% import dependencies
import pandas as pd
import glob
import os
import numpy as np
#%% ID and import raw data .xlsx
# your path to folder containing excel files
datapath = r'C:\Users\Dakota\Desktop\Opto DS Task Test- Laser Manipulation\_dataRaw\\'


# set all .xls files in your folder to list
allfiles = glob.glob(datapath + "*.xls*")

#initialize list to store data from each file
dfRaw = pd.DataFrame()


#for loop to aquire all excel files in folder
for excelfiles in allfiles:
    #read all sheets by specifying sheet_name = None
    #Remove any variables you don't want now before appending!
    #there was an issue with (W)trialState so leaving that out (col T)
    #Also leaving out first few columns
    raw_excel = pd.read_excel(excelfiles, sheet_name= None, usecols='F:S,U:X')
    
    dfRaw = dfRaw.append(raw_excel, ignore_index=True)
    
#dfRaw is now nested df, each column is a subject and each row is a session

#eliminate data from 'MSNs' sheets for now, not informative currently
dfRaw.drop('MSNs',axis=1,inplace=True)

#loop through nested df and append data. Now we have all data in one df
df= pd.DataFrame()

for subject in dfRaw.columns:
    print('loading'+subject)
    for file in range(len(dfRaw)):
        # print(allfiles[file]+subject)
        
        #add file label to each nested raw_excel before appending
        #assume fileName is yyyymmdd.xlsx (total of 13 characters at end of path. 5 are '.xlsx')
        dfRaw.loc[file,subject]['file']=allfiles[file][-13:]
        
        #add date too
        dfRaw.loc[file,subject]['date']= allfiles[file][-13:-5]
        
        
        #add subject label before appending
        dfRaw.loc[file,subject]['subject']=subject

        
        df= df.append(dfRaw.loc[file,subject])

#%% ID and import metadata .xlsx

# Match and insert subject metadata based on subject
metaPath= r"C:\Users\Dakota\Desktop\Opto DS Task Test- Laser Manipulation\_metadata\vp-vta-stgtacr_subj_metadata.xlsx"

dfRaw= pd.read_excel(metaPath).astype('object') 

df= df.astype('object').merge(dfRaw.astype('object'), how='left', on=['subject'])

# Match and insert session metadata based on date and subject

metaPath= r"C:\Users\Dakota\Desktop\Opto DS Task Test- Laser Manipulation\_metadata\vp-vta-stgtacr_session_metadata.xlsx"

dfRaw= pd.read_excel(metaPath).astype('object') 

df= df.astype('object').merge(dfRaw.astype('object'), how='left', on=['subject','date'])

# %% Exclude data

# Exclude specific date
df = df[df.date != 20210604]

# %% Remove parentheses from variable names 

import re
#use regex to replace text between () with empty string
#loop through each column name, remove characters between () and collect into list 'labels'
labels= []
for col in df.columns:
    labels.append(re.sub(r" ?\([^)]+\)", "", col))
#rename columns to labels
df.columns= labels

# %% Add other variables if necessary before tidying

# calculate port exit time estimate using PEtime and peDur, save this as a new variable
df = df.assign(PExEst=df.PEtime + df.PEdur)

#%% Custom method of groupby subsetting, manipulations, and reassignment to df

#May be interchangable with groupby.transform() Call function producing a like-indexed DataFrame on each group and return a DataFrame having the same indexes as the original object filled with the transformed values
def groupbyCustom(df, grouper):
    #df= dataframe ; grouper= list of columns to groupby (e.g.) grouper= ['subject','date'] 
    
    grouped= df.groupby(grouper)
    
    #get the unique groups
    groups= grouped.groups
    
        
    #Each group in groups contains index of items belonging to said group
    #so we can loop through each group, use that as a key for the groups dict to get index
    #then retrieve or alter values as needed by group with this index using df.iloc  
    # dfGroup= pd.DataFrame()
    #initialize dfGroup as all nan copy of original df. Then we'll get values by group
    dfGroup= df.copy()
    dfGroup[:]= np.nan
    
    #collection using loop takes too long. would be nice to vectorize (need to find a way to use the dict int64 ind as index in df I think)
    for group in groups:
        #index corresponding to this group in the df
        groupInd= groups[group]
        
        #extract values from df
        dfGroup.loc[groupInd,:]= df.loc[groupInd,:]
        
        #add label for this group
        # dfGroup.loc[groupInd,'groupID']= [group]
        dfGroup.loc[groupInd,'groupID']= str(group)
        
    # for group in groups:
    #     #use key and get_group
    #     #this approach isolates values but loses original index
    #     dfGroup= grouped.get_group(group)

        #here you could run a function on dfGroup
        return dfGroup
#%% Add unique fileID for each session (subject & date )

df.loc[:,'fileID'] = df.groupby(['subject', 'date']).ngroup()


#%% Tidy df org: All events in single column, sort by time by file, with fileID column and trialID column that matches trial 1-60 through each session.
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   
#First, am melting columns of behavioral events into single column of event label and column of individual timestamps (value_vars= want to melt)

dfEventAll = df.melt(id_vars=['subject', 'RatID', 'Virus', 'Sex', 'date', 'laserDur', 'note'], value_vars=[

                     'PEtime', 'PExEst', 'lickTime', 'laserTime', 'DStime', 'NStime', 'UStime',
                     'laserOffTime'], var_name='eventType', value_name='eventTime')#, ignore_index=False)

# remove invalid/placeholder 0s
# TODO: seem to be removing legitimate port exits with peDur==0, not sure how to deal with this so just excluding
dfEventAll = dfEventAll[dfEventAll.eventTime != 0]


# before any removal/sorting is done, next issue is to match up laser state with cues.
dfLaser = df.melt(id_vars=['subject', 'RatID', 'Virus', 'Sex', 'date', 'laserDur', 'note'], value_vars=[
   'laserDStrial', 'laserNStrial'], var_name='laserType', value_name='laserState', ignore_index=False)


# use cumcount() of DS & NS to match up laser status with cue time (redundant since we have a timestamp of laser on, but good verification still and easy grouping by trial)
dfEventAll.index.name = 'fileID'
dfEventAll.reset_index(inplace=True)
dfEventAll.index.name= 'eventID'
dfEventAll['g'] = dfEventAll[(dfEventAll.eventType == 'DStime') | (
dfEventAll.eventType == 'NStime')].groupby('fileID').cumcount()  # .index

dfLaser.index.name = 'fileID'
dfLaser.reset_index(inplace=True)
dfLaser['g'] = dfLaser[(dfLaser.laserType == 'laserDStrial') | (
dfLaser.laserType == 'laserNStrial')].groupby('fileID').cumcount()

 # print(dfLaser['g'].shape, dfLaser['g'].max(), dfEventAll['g'].shape, dfEventAll['g'].max())

dfEventAll = pd.merge(dfEventAll, dfLaser[['g', 'fileID', 'laserType', 'laserState']], on=[
    'fileID', 'g'], how='left').drop('g', axis=1)

# sort all event times by file and timestamp
# set index name so we can sort by it easily
# dfEventAll.index.name= 'fileID'
dfEventAll = dfEventAll.sort_values(by=['fileID', 'eventTime'])

 # need to reset_index before assigning values back to dfEventAll (this is because the fileID index repeats so assignment is ambiguous)
dfEventAll.reset_index(drop=True,inplace=False) #dropping old unsorted eventID
dfEventAll.index.name= 'eventID'


 # add trialID column by cumulative counting each DS or NS within each file
 # now we have ID for trials 0-59 matching DS or NS within each session, nan for other events
dfEventAll['trialID'] = dfEventAll[(dfEventAll.eventType == 'DStime') | (
    dfEventAll.eventType == 'NStime')].groupby('fileID').cumcount()

# combine laserState and laserType into one variable for labelling each trial: trialType
#Exclude the Lick-paired laser sessions. We will label those using a different method below  
dfEventAll.loc[dfEventAll.laserDur!='Lick', 'trialType'] = dfEventAll.laserType + \
    '_'+dfEventAll.laserState.astype(str).copy()

 
#sort again by file & event timestamp before saving to new df
dfEventAll = dfEventAll.sort_values(by=['fileID', 'eventTime'])
 
#reset index so that eventIDs are in chronological order
#for some reason inplace=true isn't working here so just reassign
dfEventAll= dfEventAll.reset_index(drop=True)
dfEventAll.index.name= 'eventID'


dfTidy = dfEventAll.copy()

