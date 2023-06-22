# -*- coding: utf-8 -*-
"""
Created on Thu Dec 16 13:50:19 2021

@author: Dakota
"""

import pandas as pd
import matplotlib.pyplot as plt

 #%% define a function to save and close figures
def saveFigCustom(figure, figName,savePath, close=True):
    plt.gcf().set_size_inches((20,10), forward=False) # ~monitor size
    plt.legend(bbox_to_anchor=(1.01, 1), borderaxespad=0) #creates legend ~right of the last subplot
    
    plt.gcf().tight_layout()
    plt.savefig(savePath+figName+'.png', bbox_inches='tight')
    
    if close==True:
        plt.close()
    
    
#%% define a function to subset data at correct level of observation for variable
def subsetLevelObs(df, groupers, n=0):
    
    #get first n observations at this groupby level
    #(probably just want the first @ n=0)
    ind= df.groupby(groupers).cumcount()<=n

    df= df.loc[ind]

    return df
    
    
#%% define a function to subset data for plotting
#--!Assumes that you will subset data at correct level of observation for given variable first
def subsetData(df, stagesToPlot, trialTypesToPlot, eventsToPlot):
    
    #subset trialTypes to plot
    df= df.loc[df.stage.isin(stagesToPlot)]
  
    #subset trialTypes to plot
    df= df.loc[df.trialType.isin(trialTypesToPlot)]
    
    #subset events to plot
    df= df.loc[df.eventType.isin(eventsToPlot)]
    
    #after subsetting data
    #remove all unused categories from vars (so sns doesn't plot empty labels)
    ind= df.dtypes=='category'
    ind= df.columns[ind]
    
    for col in ind:
        df[col]= df[col].cat.remove_unused_categories()
    
    return df
#%% define a function to calculate PE probability
def percentPortEntryCalc(df, groupHierarchy, colToCalc):
    #First we need to subset only one observation per level of analysis
    dfSubset= df.loc[df.groupby(['fileID','trialID']).cumcount()==0].copy()
      
    #build a list of groupers to be used as hierarchical index for crosstabs, just because this works a bit differently than other methods
    xTabInd= []
    for grouper in groupHierarchy:
        xTabInd.append(dfSubset[grouper]) 
    
    #combine all outcomes with PE before making crosstab and running calculation
    dfSubset.loc[((dfSubset[colToCalc]=='PE') | (dfSubset[colToCalc]=='PE+lick')),colToCalc]= 'PE'
    dfSubset.loc[((dfSubset[colToCalc]=='noPE') | (dfSubset[colToCalc]=='noPE+lick')),colToCalc]= 'noPE'
    
    
    test= pd.crosstab(index=xTabInd, columns=dfSubset[colToCalc], margins=True)

    #normalizing over index (row) should return proportion of each outcome for each trialType 
    result= pd.crosstab(index=xTabInd, columns=dfSubset[colToCalc], margins=False, normalize='index')
    
    #retain only PE column
    result= result.drop('noPE',axis=1)
        
    return result
 
#%% define a function to calculate % of each observation in group (more generalizable verison of above PE probability fxn)    
def groupPercentCalc(df, levelOfAnalysis, groupHierarchy, colToCalc):
    #First we need to subset only one observation per level of analysis
    dfSubset= df.loc[df.groupby(levelOfAnalysis).cumcount()==0].copy()
      
    #build a list of groupers to be used as hierarchical index for crosstabs, just because this works a bit differently than other methods
    xTabInd= []
    for grouper in groupHierarchy:
        xTabInd.append(dfSubset[grouper]) 
    
    # test= pd.crosstab(index=xTabInd, columns=dfSubset[colToCalc], margins=True)
    
    #normalizing over index (row) should return proportion of each outcome for each trialType 
    result= pd.crosstab(index=xTabInd, columns=dfSubset[colToCalc], margins=False, normalize='index')
    return result