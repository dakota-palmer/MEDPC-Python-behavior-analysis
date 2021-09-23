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
import shelve
import seaborn as sns

#%% About:

#this script will load your medpc data from spreadsheets generated by the mpctoexcel python package.
#it will also associate this data with 1) subject and 2) session metadata from spreadsheets manually created by you.
#data is imported and put into a pandas dataframe, df
#the dataframe is then "tidied" so that each column is one variable and each row is an observation (one observation=1 event timestamp)
#result is the dataframe dfTidy

#hierarchical data structure (subject, session, trial, event) is retained using labels for each event  

#finally, dfTidy is exported as .csv so it can be rapidly loaded later on without running this script.

# TODO: consider alternative organization like 'epoch' labels (e.g. DS, NS, in port, laser on, etc) 

#%% Things to manually change based on your data:
    
#datapath= path to your folder containing excel files

#colToImport= columns in your excel sheets to include (manually defined this so that I could exclude a specific variable that was huge)
#TODO: this might need to change based on stage/MPC code (perhaps variables are introduced in different .MPCs that mess with the order of things)

#metapath= paths to 1) subject metadata spreadsheet (e.g. virus type, sex) and 2) session metadata spreadsheet (e.g. laser parameters, DREADD manipulations)
#excludeDate= specific date you might want to exclude

#eventVars= event type labels for recorded timestamps
#idVars=  subject & session metadata labels for recorded timestamps 

#TODO: may consider adding subjVars and sessionVars depending on your experiment 

#experimentType= just a gate now for opto-specific code. = 'Opto' for opto specific code
experimentType= 'gadOpto'

#%% ID and import raw data .xlsx
# your path to folder containing excel files 
datapath = r'C:\Users\Dakota\Desktop\Opto DS Task Test- Laser Manipulation\_dataRaw\\'#dp opto

datapath= r'C:\Users\Dakota\Desktop\gad-vp-opto\\' #dp gad-vp-opto

# datapath= r'C:\Users\Dakota\Desktop\_example_gaddreadd\MED-PC Files July-TBD 2021\All\\' #ally dreadd

# set all .xls files in your folder to list
allfiles = glob.glob(datapath + "*.xls*")

#initialize list to store data from each file
dfRaw = pd.DataFrame()

#define columns in your .xlsx for specific variables you want (e.g. A:Z for all)
colToImport= 'F:S,U:X' #dp opto 

colToImport= 'A:Q' #ally dreadd

#for loop to aquire all excel files in folder
for excelfiles in allfiles:
    #read all sheets by specifying sheet_name = None
    #Remove any variables you don't want now before appending!
    #there was an issue with (W)trialState so leaving that out (col T)
    #Also leaving out first few columns
    raw_excel = pd.read_excel(excelfiles, sheet_name= None, usecols=colToImport)
    
    dfRaw = dfRaw.append(raw_excel, ignore_index=True)
    
#dfRaw is now nested df, each column is a subject and each row is a session

#eliminate data from 'MSNs' sheets for now, not informative currently
#TODO: this could be nice to get, but requires changing the mpc2excel scripts
dfRaw.drop('MSNs',axis=1,inplace=True)

#loop through nested df and append data. Now we have all data in one df
df= pd.DataFrame()

for subject in dfRaw.columns:
    print('loading'+subject)
    for file in range(len(dfRaw)):
        # print(allfiles[file]+subject)
        try:
            #add file label to each nested raw_excel before appending
            #assume fileName is yyyymmdd.xlsx (total of 13 characters at end of path. 5 are '.xlsx')
            dfRaw.loc[file,subject]['file']=allfiles[file][-13:]
            
            #add date too
            dfRaw.loc[file,subject]['date']= allfiles[file][-13:-5]
            
            
            #add subject label before appending
            dfRaw.loc[file,subject]['subject']=subject
            
            df= df.append(dfRaw.loc[file,subject])
            
        except: 
            print(allfiles[file]+'_'+subject+' has no data')

#%% ID and import metadata .xlsx
#TODO: for now assuming separate excel files for these data

#convert subject and date variables to string datatype to ensure easy matching (excel number formatting can be weird)
df.subject= df.subject.astype('str')
df.date= df.date.astype('str')

# Match and insert subject metadata based on subject
metaPath= r"C:\Users\Dakota\Desktop\Opto DS Task Test- Laser Manipulation\_metadata\vp-vta-stgtacr_subj_metadata.xlsx" #dp opto

metaPath= r'C:\Users\Dakota\Desktop\gad-vp-opto\_metadata\subj_metadata.xlsx' #gad-vp-opto

dfRaw= pd.read_excel(metaPath).astype('str') 

df= df.merge(dfRaw.astype('str'), how='left', on=['subject'])

# Match and insert session metadata based on date and subject

metaPath= r"C:\Users\Dakota\Desktop\Opto DS Task Test- Laser Manipulation\_metadata\vp-vta-stgtacr_session_metadata.xlsx" #dp opto

metaPath= r"C:\Users\Dakota\Desktop\gad-vp-opto\_metadata\ses_metadata.xlsx" #gad-vp-opto

#ensure that date is read as string
dfRaw= pd.read_excel(metaPath, converters={'date': str}).astype('str') 

df= df.merge(dfRaw.astype('str'), how='left', on=['subject','date'])

# %% Exclude data

excludeDate= ['20210604']

# Exclude specific date(s)
df= df[~df.date.isin(excludeDate)]


# %% Remove parentheses from variable names 

import re
#use regex to replace text between () with empty string
#loop through each column name, remove characters between () and collect into list 'labels'
labels= []
for col in df.columns:
    labels.append(re.sub(r" ?\([^)]+\)", "", col))
#rename columns to labels
df.columns= labels

#%% Add unique fileID for each session (subject & date )

df.loc[:,'fileID'] = df.groupby(['date', 'subject']).ngroup()

# %% Add other variables if necessary before tidying

# calculate port exit time estimate using PEtime and peDur, save this as a new variable
df = df.assign(PExEst=df.PEtime + df.PEdur)

# save cue duration (in DS task this is A(2))
#TODO: may be better to put this in session metadata.xlsx? just to keep things parallel with photometry TDT data analysis (assume we won't import MPC as well)

#group by fileID then retrieve the 2nd value in stageParams 
grouped= df.groupby('fileID')

df.loc[:,'cueDur']= grouped.stageParams.transform('nth',2)

grouped.stageParams.nth(2)

#convert 'date' to datetime format
df.date= pd.to_datetime(df.date)


#%% Define Event variables for your experiment 
#make a list of all of the Event Types so that we can melt them together into one variable
#instead of one column for each event's timestamps, will get one single column for timestamps and another single column for the eventType label

#these should match the labels in your .MPC file

## e.g. for DS task with no Opto  
eventVars= ['PEtime', 'PExEst', 'lickTime', 'DStime', 'NStime', 'UStime']

#e.g. for DS task with Opto
if experimentType== 'Opto':
    eventVars= ['PEtime', 'PExEst', 'lickTime', 'laserTime', 'DStime', 'NStime', 'UStime','laserOffTime']

#%% Define ID variables for your sessions
#these are identifying variables per sessions that should be matched up with the corresponding event variables and timestamps
#they should variables in your session and subject metadata spreadsheets

## e.g. for DS task with no Opto
idVars= ['fileID','subject', 'virus', 'sex', 'date', 'stage', 'cueDur', 'note']

#e.g. for DS task with Opto
if experimentType== 'Opto':
    idVars= ['fileID','subject', 'virus', 'sex', 'date', 'stage', 'cueDur', 'laserDur', 'note']


#%% Define Trial variables for your experiment
# If you have variables corresponding to each individual trial 
#e.g. different trial types in addition to DS vs NS (e.g. laser ON vs laser OFF trials; TODO: variable reward outcome)

trialVars= []

#e.g. for Opto:
if experimentType=='Opto':
    trialVars= ['laserDStrial','laserNStrial']
    #the laserDStrial and laserNS trial variables will later be melted() into a new variable called 'laserState' with their values


#%% Change dtypes of variables if necessary (might help with grouping & calculations later on)

#binary coded 0/1 laser variables were being imported as floats, converting them to pandas dtype Int64 which supports NA values
if experimentType=='Opto':
    df.loc[:,(trialVars)]= df.loc[:,(trialVars)].astype('Int64')

#%% Tidying: All events in single column, add trialID and trialType that matches trial 1-60 through each session.

#First, am melting columns of behavioral events into single column of event label and column of individual timestamps (value_vars= want to melt)
dfEventAll = df.melt(id_vars=idVars, value_vars=eventVars, var_name='eventType', value_name='eventTime') #, ignore_index=False)

#Remove all rows with NaN eventTimes (these are just placeholders, not valid observations) 
dfEventAll= dfEventAll[dfEventAll.eventTime.notna()]

# remove invalid/placeholder 0s
# TODO: seem to be removing legitimate port exits with peDur==0, not sure how to deal with this so just excluding
dfEventAll = dfEventAll[dfEventAll.eventTime != 0]

# add trialID column by cumulative counting each DS or NS within each file
# now we have ID for trials 0-59 matching DS or NS within each session, nan for other events
dfEventAll['trialID'] = dfEventAll[(dfEventAll.eventType == 'DStime') | (
    dfEventAll.eventType == 'NStime')].groupby('fileID').cumcount()

#add trialType label using eventType (which will be DS or NS for valid trialIDs)
dfEventAll['trialType']= dfEventAll[dfEventAll.trialID.notna()].eventType

#%% Assign more specific trialTypes based on trialVars (OPTO ONLY specific for now)
if experimentType=='Opto':
    # melt() trialVars, get trialID for each trial and use this to merge label back to df 
    dfTrial = df.melt(id_vars= idVars, value_vars=trialVars, var_name='laserType', value_name='laserState')#, ignore_index=False)
    #remove nan placeholders
    dfTrial= dfTrial[dfTrial.laserState.notna()]
    
    #get trialID
    dfTrial['trialID'] = dfTrial.groupby('fileID').cumcount() 
    
    #merge trialType data back into df on matching fileID & trialID
    dfEventAll= dfEventAll.merge(dfTrial[['trialID', 'fileID', 'laserType', 'laserState']], on=[
        'fileID', 'trialID'], how='left')#.drop('trialID', axis=1)
    
    #combine laserState and laserType into one variable for labelling each trial: trialType
    #Exclude the Lick-paired laser sessions. We will label those using a different method below  
    dfEventAll.loc[dfEventAll.laserDur!='Lick', 'trialType'] = dfEventAll.laserType + \
        '_'+dfEventAll.laserState.astype(str).copy()
    
    #now drop redundant columns
    # dfEventAll= dfEventAll.drop(['laserType','laserState'], axis=1)
     
#%% DS training code error fix
#need to get rid of false first cue onsets
#code error caused final cue time to overwrite first cue time (dim of array needed to be +1)

#simply exclude very high values
dfEventAll.loc[((dfEventAll.trialID==0) & (dfEventAll.eventTime>=2500)),'eventTime']= pd.NA

# idx = (dfTidy.groupby(['fileID'])['trialID'].transform('cumcount').copy() == dfTidy['trialID'].copy())
# # dfTidy.loc[idx,'nextTrialStart']= pd.NA
# dfTest= dfTidy.loc[idx]

# #for last trial set next trial start to nan
# idx = (dfTidy.groupby(['fileID'])['trialID'].transform(max).copy() == dfTidy['trialID'].copy()) 

# dfTest=dfTidy.copy()
# dfTest.loc[idx,'nextTrialStart']= pd.NA
# # dfTest= dfTidy.loc[idx]


# # test= dfTidy.set_index('fileID')
# # test.loc[((test.eventType=='DStime') | (test.eventType=='NStime'))]

# # dfTidy.loc[dfTidy.groupby(['fileID','trialID']).cumcount()==0]

# test= dfEventAll.set_index('fileID')
# test2= test.loc[test.loc[test.trialID==0].eventTime >= test.loc[test.trialID==1].eventTime]

# dfEventAll= dfEventAll.set_index('fileID')

# dfTemp= dfEventAll.loc[dfEventAll.trialID==0].eventTime >= dfEventAll.loc[dfEventAll.trialID==1].eventTime
# dfTemp= dfTemp.reset_index()

# # dfEventAll.reset_index(inplace=True,drop=False)

# #remove this cue's timestamp (we don't know when the cue came on)
# dfEventAll.loc[(dfEventAll.fileID==dfTemp.fileID) & (dfEventAll.trialID==0)]= pd.NA

# #
# dfGroup= dfEventAll.groupby(['fileID','trialID'], as_index=False).first()
# idx= dfGroup.loc[dfGroup.trialID==0].eventTime >= dfGroup.loc[dfGroup.trialID==1].eventTime

# #
# dfTemp= dfEventAll.set_index('fileID')
# test= dfTemp.loc[(dfTemp.loc[dfTemp.trialID==0].eventTime)>= (dfTemp.loc[dfTemp.trialID==1].eventTime)]
# test.reset_index(inplace=True, drop=False)

# dfTemp.loc[dfTemp.fileID==test.fileID]


#%% Sort events by chronological order within-file, correct trialID, and save as dfTidy
dfTidy = dfEventAll.sort_values(by=['fileID', 'eventTime'])

#drop old, unsorted eventID
dfTidy= dfTidy.reset_index(drop=True)
dfTidy.index.name= 'eventID'

#reset_index so we have new, sorted eventID in a column
dfTidy.reset_index(inplace=True)

#recompute trialID now that everything is sorted chronologically
dfTidy.trialID= dfTidy[dfTidy.trialID.notna()].groupby('fileID').cumcount()


#%% Add trialID & trialType labels to other events (events during trials and ITIs) 
 
# fill in intermediate trialID values... We have absolute trialIDs now for each Cue but other events have trialID=nan
# we can't tell for certain if events happened during a trial or ITI at this point but we do have all of the timestamps
# and we know the cue duration, so we can calculate and assign events to a trial using this.

# To start, fill in these values between each trialID as -trialID (could also use decimal like trial 1.5) between each actual Cue
# Get the values and index of nan trialIDs
# this returns a series of each nan trialID along with its index.
indNan = dfTidy.trialID[dfTidy.trialID.isnull()].copy()


#Need to group by file, otherwise the ffill method here will contaminate between files (events before trial 0 in fileB are filled as 59 from fileA)
# pandas has a function for this- groupby().ffill or .backfill or .fillna
# this fills nan trialID
dfTidy.trialID= dfTidy.groupby('fileID')['trialID'].fillna(method='ffill').copy()

#Add 1 to each trialID to avoid trialID==0. 
#Don't allow trialIDs=0, so we can avoid issues with -0 trialIDs later (-0 will equate to 0 and we don't want to mix them up)
dfTidy.trialID= dfTidy.trialID+1

# do the same for trialType
dfTidy.trialType= dfTidy.groupby('fileID')['trialType'].fillna(method='ffill').copy()


# now multiply previously nan trialIDs by -1 so we can set them apart from the valid trialIDs
dfTidy.loc[indNan.index, 'trialID'] = dfTidy.trialID[indNan.index].copy()*-1

#Fill nan trialIDs (first ITI) with a placeholder. Do this because groupby of trialID with nan will result in contamination between sessions
#don't know why this is, but I'm guessing if any index value==nan then the entire index likely collapses to nan
dfTidy.loc[dfTidy.trialID.isnull(),'trialID']= -999#-0.5


# Can get a trial end time based on cue onset, then just check
# event times against this

dfTidy = dfTidy.sort_values(by=['fileID', 'eventTime']).copy()

# dfTidy.loc[:, 'trialStart'] = dfTidy.eventTime[dfTidy.trialID >= 0].copy()
    
# dfTidy.loc[:, 'trialStart'] = dfTidy.fillna(method='ffill').copy()

dfTidy.loc[:, 'trialEnd'] = dfTidy.eventTime[dfTidy.trialID >= 0].copy() + \
    dfTidy.cueDur
    
dfTidy.loc[:, 'trialEnd'] = dfTidy.fillna(method='ffill').copy()


#also get start of next trial (by indexing by file,trial and then shifting by 1)
#will be used to define preCue trialTypes
dfGroup= dfTidy.loc[dfTidy.trialID>=0].copy()
#index by file, trial
dfGroup.set_index(['fileID','trialID'], inplace=True)
#get time of next trial start by shifting by 1 trial #shift data within file (level=0)
dfGroup.loc[:, 'nextTrialStart'] = dfGroup.groupby(level=0)['eventTime'].shift(-1).copy()
dfGroup.reset_index(inplace=True) #reset index so eventID index is kept
dfGroup.set_index('eventID', inplace=True)
#merge back on eventID
dfTidy.set_index('eventID',inplace=True,drop=False)
dfTidy= dfTidy.merge(dfGroup, 'left').copy()

#ffill for negative trialIDs
dfTidy.nextTrialStart= dfTidy.nextTrialStart.fillna(method='ffill').copy()

#SIMPLE GROUPBY INDEXING!
#for last trial set next trial start to nan
idx = (dfTidy.groupby(['fileID'])['trialID'].transform(max).copy() == dfTidy['trialID'].copy()) | (-dfTidy.groupby(['fileID'])['trialID'].transform(max).copy() == dfTidy['trialID'].copy())
dfTidy.loc[idx,'nextTrialStart']= pd.NA
dfTest= dfTidy.loc[idx]

dfTidy.trialID.max() #good here

# Add trialType for pre-cue period 
#this is a useful epoch to have identified; can be a good control time period vs. cue presentation epoch
preCueDur= 10 
dfTest= dfTidy.copy()
dfTest2= dfTest.loc[(dfTidy.nextTrialStart-dfTidy.eventTime <= preCueDur)]

dfTidy.loc[(dfTidy.nextTrialStart-dfTidy.eventTime <= preCueDur),'trialType'] = 'Pre-Cue'#'Pre-'+dfTidy.trialType.copy()

#make pre-cue trialIDs intervals of .5
dfTidy.loc[(dfTidy.nextTrialStart-dfTidy.eventTime <= preCueDur),'trialID'] = dfTidy.trialID.copy()-0.5
dfTest= dfTidy.loc[dfTidy.trialID==-31]

dfTidy.trialID.max() #good here

#Special exceptions for events before first trial starts, need to be manually assigned (bc ffill method above won't work)
#get the time of the first event in the first trial (equivalent to trial start time)
dfTidy.loc[dfTidy.trialID== -999, 'nextTrialStart'] = dfTidy.loc[dfTidy.trialID==1].eventTime.iloc[0] 
#make trialEnd for the first ITI the start of the recording, keeping with scheme of other ITIs which reflect "end" of last cue
dfTidy.loc[dfTidy.trialID== -999, 'trialEnd'] = 0

##ID events in the first preCue period
dfTidy.set_index('fileID', drop=False)

dfTidy.loc[((dfTidy.trialID== -999) & (dfTidy.nextTrialStart-dfTidy.eventTime <= preCueDur)),'trialType']= 'Pre-Cue'#+ dfTidy.loc[(dfTidy.trialID==1) | (dfTidy.trialID==-0.5)].trialType.fillna(method='bfill').copy()

dfTest= dfTidy.copy()
dfTest2= dfTest.loc[((dfTest.trialID== -999) & (dfTest.nextTrialStart-dfTidy.eventTime <= preCueDur))]

##TODO: for first ILI, make trial end the first cue onset
# dfTidy.loc[dfTidy.trialID== -0.5,'trialEnd']= dfTidy.loc[dfTidy.loc[dfTidy.trialID==1].groupby(['fileID','trialID'])['eventTime'].cumcount()==0]

# find events that occur after cue start but before cue duration end.
# remaining events with negative trialIDs must have occurred somewhere in that ITI (or 'pre/post cue')

dfTidy.loc[(dfTidy.trialEnd-dfTidy.eventTime >= 0) & ((dfTidy.trialEnd -
                                                      dfTidy.eventTime).apply(np.round) < dfTidy.cueDur), 'trialID'] = dfTidy.trialID.copy()*-1
dfTest= dfTidy.loc[dfTidy.trialID==-999].copy()

# remove trialType labels from events outside of cueDur (- trial ID or nan trialID)

#add 'ITI' trialType label for remaining events in ITI. This gets the first ITI
dfTidy.loc[(((dfTidy.trialID < 0) & (dfTidy.trialType.isnull()))), 'trialType'] = 'ITI'
# keep trialIDs in between integers (preCue period) by checking for nonzero modulo of 1
#for now labelling with "ITI"
dfTidy.loc[((dfTidy.trialID < 0) & (dfTidy.trialID % 1 == 0)), 'trialType'] = 'ITI'

#good here

#%% add "dummy" placeholder entries for any  missing trialIDs 
#since ITI/pre-cue trial definitions are contingent on behavioral events, if no events occur during a particular ITI 
#then that epoch won't be included in calculations later on (e.g. probability calculations based on total count of each trialType)

#find the max integer trialID (the highest numbered trial in session)
trialsToAdd= dfTidy.loc[(dfTidy.trialID % 1 == 0)].groupby('fileID').trialID.max().reset_index().copy()

#there should be 1 pre-Cue trialID (- intervals of .5) and 1 ITI (- integers) per trial
#plus an additional ITI for time after the final cue
#so total number is = #trials * 3 + 1

# trialsToAdd= np.array(trialsToAdd.values)

# trialIDs = np.empty([round(trialsToAdd.trialID.max()*3), trialsToAdd.shape[0]], dtype=object)    
# trialIDs[:]= np.nan
# 
# trialIDs = np.empty([round(trialsToAdd.shape[0]),2], dtype=object)
# trialIDs= pd.DataFrame(dtype=object)    
# trialIDs.trialID= []

#initialize list for trialIDs and trialTypes for each file, will iteratively add to it
trialRange= []
trialID= []
fileID= []

for file in trialsToAdd.fileID:#range(0,trialsToAdd.shape[0]):
    
    trialRange= np.arange(-trialsToAdd.loc[file].trialID,trialsToAdd.loc[file].trialID,0.5)   
    
    #eliminate trialIDs with + non integers
    trialRange[(trialRange>=0) & (trialRange %1 !=0)] = np.nan
    
    #eliminate 0 trialIDs
    trialRange= trialRange[trialRange !=0]
    
    #remove nans
    trialRange= trialRange[pd.notnull(trialRange)]
    
    #add placeholder trialID for first ITI
    trialRange= np.append(-999,trialRange)
     
    # trialIDs[0:trialRange.shape[0],file]= trialRange
    # trialIDs.loc[file:,'fileID']= file
    # trialIDs.loc[file,'trialID']= trialRange
    # # trialIDs.loc[file,'fileID']=file
    # trialIDs.trialID= trialIDs.trialID.append(trialRange)

    # trialID.append(trialRange)
    # fileID.append([file]*len(trialRange))
    
    trialID= np.append(trialID,trialRange, axis=0)
    fileID= np.append(fileID,[file]*len(trialRange))



    
#save in dataframe format, add trialType labels for the ITIs and Pre-Cue periods
dfTemp= pd.DataFrame()
dfTemp.loc[:,'trialID']= trialID
dfTemp.loc[:,'fileID']= fileID
dfTemp.loc[(dfTemp.trialID<=0),'trialType']= 'ITI'
dfTemp.loc[((dfTemp.trialID<=0)&(dfTemp.trialID %1 !=0)),'trialType']= 'Pre-Cue'

#remove duplicate trialIDs that are already present in dfTidy (only add placeholders for epochs without events already)
#maybe a right merge would work
# dfTest= dfTidy.set_index(['fileID','trialID']).copy()
# dfTemp= dfTemp#.set_index(['fileID','trialID'])
# dfMerged= dfTest.merge(dfTemp,'right', on=['fileID','trialID'])

dfTest=dfTidy.set_index('fileID').copy()
# dfTemp= dfTemp.set_index('fileID')

test1= dfTemp.groupby('fileID').trialID.unique().explode()
test2= dfTidy.groupby('fileID').trialID.unique().explode()

test3= dfTemp.groupby('fileID').trialID.unique().isin(dfTidy.groupby('fileID').trialID.unique())

test4= dfTemp.groupby('fileID').trialID.unique().explode().isin(dfTidy.groupby('fileID').trialID.unique().explode())

test6= dfTidy.groupby('fileID').trialID.unique().explode().isin(dfTemp.groupby('fileID').trialID.unique().explode())

test8= dfTemp.groupby('fileID').trialID.unique().explode().reset_index().isin(dfTidy.groupby('fileID').trialID.unique().explode().reset_index())

test9= test1.any()==test2

test10= test1.reset_index().set_index(['fileID','trialID'])
test11= test2.reset_index().set_index(['fileID','trialID'])

test12= test10.index.isin(test11.index)

#how is .isin actually working
#maybe unique() is sorting or something causing index could be off?
# test7= dfTemp.loc[test4==False]

dfTemp= dfTemp.loc[test12==False]

dfTemp= dfTemp.set_index('fileID')

dfTest= dfTidy.set_index('fileID').copy()

dfCat= pd.concat([dfTest, dfTemp], axis=0)
test5= dfCat.groupby('fileID').trialID.unique().explode().copy()

# dfTidy= dfCat.reset_index(drop=False).copy()

#% visualize trialIDs now- there should be same amount per session (depending on stage)
dfCat= dfCat.reset_index(drop=False) 
dfTemp=dfCat.groupby(
        ['fileID','trialType'],dropna=False,as_index=False)['trialID'].nunique(dropna=False)#.unstack(fill_value=0)
# dfTemp=dfPlot.groupby(
#         ['fileID','trialType','trialOutcomeBeh'],dropna=False)['trialID'].unique().unstack(fill_value=0)
# dfTemp=dfPlot.groupby(
#         ['fileID','trialType','trialOutcomeBeh'],dropna=False)['trialID'].groups
# dfTemp=dfPlot.groupby(
#         ['fileID','trialType','trialOutcomeBeh'],dropna=False)['trialID'].unique().nth(0).unstack(fill_value=0)


##calculate proportion for each trial type: num trials with outcome/total num trials of this type

#%TODO: for pre- cue trialTypes, can't curently just divide by count since their current definition is contingent on behavior.
# should divide by # of total trials of the corresponding cue...or create dummy pre-cue entries for every trial
#I guess this theoretically applies to ITIs as well, if there's no event in the ITI it won't be included in the count
# #trialCount= dfTemp.sum(axis=1)


# outcomeProb= dfTemp.divide(dfTemp.sum(axis=1),axis=0)
# dfTemp.loc[:,'outcomeProb']= dfTemp.trialID.divide(dfTemp.trialID.sum(),axis=0)

# trialOrder= ['DStime','NStime','ITI','Pre-Cue']

test= dfCat.groupby('fileID')['trialID'].nunique()


dfTidy= dfCat.copy()

#%works?
# # #concat back into dfTidy
# dfTidy.set_index('fileID',inplace=True)
# dfTemp.set_index('fileID', inplace=True)
# # test= test.merge(dfTemp, 'left').copy()
# dfTidy= pd.concat([dfTidy, dfTemp], axis=0)

# dfTidy.reset_index(inplace=True,drop=False)
# # test= dfTidy.merge(dfTemp,'left',on='fileID') 

test= dfTidy.groupby('fileID')['trialID'].unique().explode()


#%% Add trialType for pre-cue period 
#this is a useful epoch to have identified; can be a good control time period vs. cue presentation epoch

# #define time window in seconds
# preCueEpoch= 10

# dfTemp= dfTidy.copy()

# #find events that occur before cue start within preCueEpoch
# test= dfTidy.loc[(dfTidy.trialEnd-dfTidy.eventTime <= 0) & ((dfTidy.trialEnd -
#                                                       dfTidy.eventTime).apply(np.round) >preCueEpoch), 'trialID']

# test= dfTidy.loc[(dfTidy.trialID<=0)]-dfT

#%% for lick-paired laser sessions, classify trials as laser on vs. laser off
#since laser delivery in these sessions is contingent on lick behavior
#use actual laser on & off times to define trials where laser delivered
   
if experimentType== 'Opto': 
    #cumcount each laser onsets per trial
    dfTidy['trialLaser'] = dfTidy[(dfTidy.laserDur=='Lick') & (dfTidy.eventType == 'laserTime')].groupby([
        'fileID', 'trialID']).cumcount().copy()
    
    #relabel trialType based on presence or absence of laser onset
    laserCount= dfTidy[dfTidy.laserDur=='Lick'].groupby(['fileID','trialID'],dropna=False)['trialLaser'].nunique()
    
    #make 0 or 1 to match trialType labels of Cue laser sessions
    laserCount.loc[laserCount>0]='1' 
    laserCount.loc[laserCount==0]='0'
    
    #so  we have a laser state for each trial, but dfTidy has many entries for each trial.
    #get the first value, then we'll use ffill to fill in other entries later
    #using  reset_index() then set_index() keeps the original named index as a column
    
    laserCount= laserCount.loc[laserCount.index.get_level_values(1)>=0]
    
    ## index by file, trial and get total count of lasers onsets per trial
    #we will use this to match up values with the original dfTidy
    dfLaser= dfTidy[((dfTidy.laserDur=='Lick') & ((dfTidy.eventType=='DStime') | (dfTidy.eventType=='NStime')))].reset_index().set_index(['fileID','trialID'])
    
    # combine laserState and laserType into one variable for labelling each trial: trialType
    # #only include the laser sessions
    dfLaser.trialType= dfLaser.laserType + '_' + laserCount.astype(str).copy()
    
    #set index to eventID before assignment
    # dfLaser= dfLaser.reset_index().set_index('eventID')
    # dfLaser= dfLaser.set_index('fileID','trialID')s
    
    #index by fileID, trialID and overwrite previous trialType labels
    dfTidy.set_index(['fileID','trialID'],inplace=True)
    
    dfTidy.loc[dfLaser.index, 'trialType']= dfLaser.trialType
    
    dfTidy.reset_index(inplace=True)    

    #insert trialTypes using eventID as index
    
    #ffill trialType for each trial
    #already filled nan so fillna wont work
    # dfTidy.loc[dfTidy.trialID>=0,'trialType']= dfTidy[dfTidy.trialID>=0].groupby('fileID')['trialType'].fillna(method='ffill').copy()
    
    #%%  drop any redundant columns remaining
    if experimentType== 'Opto':
        dfTidy = dfTidy.drop(columns=['laserType', 'laserState']).copy()


#%% Save dfTidy so it can be loaded quickly for subesequent analysis

savePath= r'./_output/' #r'C:\Users\Dakota\Documents\GitHub\DS-Training\Python' 

print('saving dfTidy to file')

#Save as pickel
dfTidy.to_pickle(savePath+'dfTidy.pkl')

#also save other variables e.g. eventVars, idVars, trialVars for later recall (without needing to run this script again)
# pickle.dump([idVars, eventVars, trialVars], savePath+'dfTidyMeta.pkl')

saveVars= ['idVars', 'eventVars', 'trialVars', 'experimentType']

#use shelve module to save variables as dict keys
my_shelf= shelve.open(savePath+'dfTidyMeta', 'n') #start new file

for key in saveVars:
    try:
        my_shelf[key]= globals()[key] 
    except TypeError:
        #
        # __builtins__, my_shelf, and imported modules can not be shelved.
        #
        print('ERROR shelving: {0}'.format(key))
my_shelf.close()


#Could save as .csv, but should also save dtypes because they should be manually defined when imported
# dfTidy.to_csv('dfTidy.csv')




#%% Custom method of groupby subsetting, manipulations, and reassignment to df
#TODO: in progress...
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
    dfGroup[:]= pd.NA #np.nan
    
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