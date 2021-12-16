# -*- coding: utf-8 -*-
"""
Created on Thu Dec 16 13:50:19 2021

@author: Dakota
"""

import pandas as pd
import matplotlib.pyplot as plt

 #%% define a function to save and close figures
def saveFigCustom(figure, figName, close=True):
    plt.gcf().set_size_inches((20,10), forward=False) # ~monitor size
    plt.legend(bbox_to_anchor=(1.01, 1), borderaxespad=0) #creates legend ~right of the last subplot
    
    plt.gcf().tight_layout()
    plt.savefig(r'./_output/_behaviorAnalysis/'+figName+'.png', bbox_inches='tight')
    
    if close==True:
        plt.close()
    
    
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
    
    
    result= pd.crosstab(index=xTabInd, columns=dfSubset[colToCalc], margins=False, normalize='index')
        
    return result
 
#%% define a function to calculate % of each observation in group (more generalizable verison of above PE probability fxn)    
def groupPercentCalc(df, levelOfAnalysis, groupHierarchy, colToCalc):
    #First we need to subset only one observation per level of analysis
    dfSubset= df.loc[df.groupby(levelOfAnalysis).cumcount()==0].copy()
      
    #build a list of groupers to be used as hierarchical index for crosstabs, just because this works a bit differently than other methods
    xTabInd= []
    for grouper in groupHierarchy:
        xTabInd.append(dfSubset[grouper]) 
    
    result= pd.crosstab(index=xTabInd, columns=dfSubset[colToCalc], margins=False, normalize='index')
    return result