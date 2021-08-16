# -*- coding: utf-8 -*-
"""
Created on Mon Aug 16 12:01:47 2021

@author: Dakota
"""
#%% 
import pandas as pd
import glob
import os
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
    raw_excel = pd.read_excel(excelfiles, sheet_name= None, usecols='A:S,U:X')
    
    dfRaw = dfRaw.append(raw_excel, ignore_index=True)
    
#dfRaw is now nested df, each column is a subject and each row is a session

#eliminate data from 'MSNs' sheets for now, not informative currently
dfRaw.drop('MSNs',axis=1,inplace=True)

#loop through nested df and append data
df2= pd.DataFrame()

for subject in dfRaw.columns:
    print(subject)
    for file in range(len(dfRaw)):
        # print(allfiles[file]+subject)
        
        #add fileID label to each nested raw_excel before appending
        #assume fileName is yyyymmdd.xlsx (total of 13 characters at end of path)
        dfRaw.loc[file,subject]['fileName']=allfiles[file][-13:]
        
        #add subject label before appending
        dfRaw.loc[file,subject]['subject']=subject

        
        df2= df2.append(dfRaw.loc[file,subject])


# place dataframe into list
# raw_data = raw_data.append(raw_excel)

#%% ID and import metadata .xlsx

# Match and insert subject metadata

# Match and insert session metadata based on date