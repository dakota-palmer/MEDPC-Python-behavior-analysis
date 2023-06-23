# -*- coding: utf-8 -*-
"""
Created on Fri Jan  6 13:46:56 2023

@author: Dakota
"""

import pandas as pd
import numpy as np

import matplotlib
import seaborn as sns

import statsmodels.api as sm
import statsmodels.formula.api as smf
#%% Import data tables (generated in matlab Figure code) and run stats here in python so can do more complex stats than matlab

#using statsmodels package
#note that statsmodels documentation frequently mentions using patsy to create design matrices. 

#formulaic seems better long term successor to patsy
# https://github.com/matthewwardrop/formulaic

#but formulaic support for mixed effects unclear as of late 2022 https://github.com/matthewwardrop/formulaic/pull/34

#here am just going to just use pandas dataframes and prep the data myself, best for mixed effects


#%% Really nice notes on categorical data / dummy & contrast coding
# https://www.statsmodels.org/stable/examples/notebooks/generated/contrasts.html

# The dummy coding is not wrong per se. It captures all of the coefficients, but it complicates matters when the model assumes independence of the coefficients such as in ANOVA.
#Linear regression models do not assume independence of the coefficients and thus dummy coding is often the only coding that is taught in this context.


#% Example LME- examining how variables are coded 
#% https://www.statsmodels.org/dev/examples/notebooks/generated/mixed_lm_example.html
# data = sm.datasets.get_rdataset("dietox", "geepack").data
# md = smf.mixedlm("Weight ~ Time", data, groups=data["Pig"])
# mdf = md.fit(method=["lbfgs"])
# print(mdf.summary())

#%% Environmetn for R?
#- pandas version needs to match R environment version to load the pickle!
# activate R environment for pickling (to make env management/consistency easier)
# conda activate r-env 


#%% ---- FIGURE 2B STATS ---------------------------------------
#Figure 2B- compare AUC of DS vs NS
    
#%%--Load the data
datapath= r"C:\Users\Dakota\Documents\GitHub\FP-analysis\matlabVPFP\_dp_manuscript\vp-vta-fp_stats_fig2bTable.parquet"

dfFig2B= pd.read_parquet(datapath)


df= dfFig2B.copy()


#Defining model variables here to help automate data prep (thinking want dummy coding of categorical fixed effects but not random effects)
yVar= ['periCueBlueAUC']

fixedEffectVars= ['trialType','sesSpecialLabel']

randomEffectVars= ['subject']


#%%-- Isolate only data you want
#to save time/memory, pare down dataset to vars we are interested in

y= 'periCueBlueAuc'

varsToInclude= ['subject','trialType','stage','sesSpecialLabel']

varsToInclude.append(y)

df= df[varsToInclude]

#%%--Prepare data for stats

# #--remove missing/invalid observations

# #-can only do stat comparison for DS vs NS in stages/sessions where NS auc is present
# #so subset to stages >=5
# ind= []
# ind= df.stage>=5

# df= df.loc[ind,:]

#-- Fix dtypes - explicitly assign categorical type to categorical vars
# note can use C() in statsmodels formula to treat as categorical tho good practice to change in df 

catVars= ['subject','trialType','stage','sesSpecialLabel']

df[catVars]= df[catVars].astype('category')

#%%-- Export to R.

# save to pickle
#- pandas version needs to match R environment version to load the pickle!
# # activate R environment for pickling (to make env management/consistency easier)
# conda activate r-env 

df= df.copy()

savePath= r'./_output/' #r'C:\Users\Dakota\Documents\GitHub\DS-Training\Python' 

print('saving fig2b df to file')

#Save as pickel
df.to_pickle(savePath+'fig2b.pkl')



#%% ------Figure 2D stats ------------------
# Figure 2D- compare AUC of PE vs no PE DS trials

    
#%%--Load the data
datapath= r"C:\Users\Dakota\Documents\GitHub\FP-analysis\matlabVPFP\_dp_manuscript\vp-vta-fp_stats_fig2dTable.parquet"

dfFig2D= pd.read_parquet(datapath)


df= dfFig2D.copy()


#Defining model variables here to help automate data prep (thinking want dummy coding of categorical fixed effects but not random effects)
yVar= ['periCueBlueAUC']

# if wanted to look at effect across sessions, would want to keep trainDay or add a fileID
fixedEffectVars= ['trialOutcome']

randomEffectVars= ['subject']


#%%-- Isolate only data you want
#to save time/memory, pare down dataset to vars we are interested in

y= 'periCueBlueAuc'

varsToInclude= ['subject','trialOutcome','trialIDcum']

varsToInclude.append(y)

df= df[varsToInclude]

#%%--Prepare data for stats

# #--remove missing/invalid observations

# #-can only do stat comparison for DS vs NS in stages/sessions where NS auc is present
# #so subset to stages >=5
# ind= []
# ind= df.stage>=5

# df= df.loc[ind,:]

#-- Fix dtypes - explicitly assign categorical type to categorical vars
# note can use C() in statsmodels formula to treat as categorical tho good practice to change in df 

catVars= ['subject','trialOutcome', 'trialIDcum']

df[catVars]= df[catVars].astype('category')

#%%-- Export to R.

# save to pickle
#- pandas version needs to match R environment version to load the pickle!
# # activate R environment for pickling (to make env management/consistency easier)
# conda activate r-env 

df= df.copy()

savePath= r'./_output/' #r'C:\Users\Dakota\Documents\GitHub\DS-Training\Python' 

print('saving fig2d df to file')

#Save as pickel
df.to_pickle(savePath+'fig2d.pkl')

#%%--------- FIG 3 ENCODING MODEL PREDICTED VS ACTUAL ----


#%% ---------------------------FIG 3 LATENCY CORRELATION ---------------



#%%--Load the data
datapath= r"C:\Users\Dakota\Documents\GitHub\FP-analysis\matlabVPFP\_dp_manuscript\vp-vta-fp_stats_fig3_latencyCorr_Table.parquet"

dfFig3_latencyCorr= pd.read_parquet(datapath)


df= dfFig3_latencyCorr.copy()


#%%-- Isolate only data you want
#to save time/memory, pare down dataset to vars we are interested in


varsToInclude= df.columns

# varsToInclude.append(y)

df= df[varsToInclude]


#%%--Prepare data for stats

# #--remove missing/invalid observations

# #-can only do stat comparison for DS vs NS in stages/sessions where NS auc is present
# #so subset to stages >=5
# ind= []
# ind= df.stage>=5

# df= df.loc[ind,:]

#-- Fix dtypes - explicitly assign categorical type to categorical vars
# note can use C() in statsmodels formula to treat as categorical tho good practice to change in df 

catVars= ['subject', 'stage', 'timeLock', 'latencyOrder']

df[catVars]= df[catVars].astype('category')



#%%-- Export to R.

# save to pickle
#- pandas version needs to match R environment version to load the pickle!
# # activate R environment for pickling (to make env management/consistency easier)
# conda activate r-env 

df= df.copy()

savePath= r'./_output/' #r'C:\Users\Dakota\Documents\GitHub\DS-Training\Python' 

print('saving df Fig3_latencyCorr to file')

#Save as pickel
df.to_pickle(savePath+'Fig3_latencyCorr.pkl')


# # Save an df with session-level observations (active proportion)
# df2= df[df.groupby(['Subject','Session']).cumcount()==0]


# print('saving fig6sessionLevel df to file')

# #Save as pickel
# df.to_pickle(savePath+'fig6sessionLevel.pkl')



#%% ----- FIG 4 C/D Stats -------

# OPTO DS TASK

#%%--Load the data
datapath= r"C:\Users\Dakota\Documents\GitHub\DS-Training\Matlab\vp-vta-fp_stats_fig4CDTable.parquet"

dfFig4CD= pd.read_parquet(datapath)


df= dfFig4CD.copy()


#%%-- Isolate only data you want
#to save time/memory, pare down dataset to vars we are interested in

#multiply y vars in this table

# y= ['ResponseProb', 'RelLatency']

varsToInclude= ['Subject', 'Projection', 'StimLength', 'CueID','LaserTrial', 'ResponseProb', 'RelLatency']

# varsToInclude.append(y)

df= df[varsToInclude]

#%%--Prepare data for stats

# #--remove missing/invalid observations

# #-can only do stat comparison for DS vs NS in stages/sessions where NS auc is present
# #so subset to stages >=5
# ind= []
# ind= df.stage>=5

# df= df.loc[ind,:]

#-- Fix dtypes - explicitly assign categorical type to categorical vars
# note can use C() in statsmodels formula to treat as categorical tho good practice to change in df 

catVars= ['Subject', 'Projection', 'StimLength', 'CueID','LaserTrial']

df[catVars]= df[catVars].astype('category')

#%%-- Export to R.

# save to pickle
#- pandas version needs to match R environment version to load the pickle!
# # activate R environment for pickling (to make env management/consistency easier)
# conda activate r-env 

df= df.copy()

savePath= r'./_output/' #r'C:\Users\Dakota\Documents\GitHub\DS-Training\Python' 

print('saving fig4CD df to file')

#Save as pickel
df.to_pickle(savePath+'fig4cd.pkl')


#%% ---------------------------FIG 5 Choice Task ---------------



#%%--Load the data
datapath= r"C:\Users\Dakota\Documents\GitHub\DS-Training\Matlab\vp-vta-fp_stats_fig5Table.parquet"

dfFig5= pd.read_parquet(datapath)


df= dfFig5.copy()


#%%-- Isolate only data you want
#to save time/memory, pare down dataset to vars we are interested in

#multiply y vars in this table

# y= ['ResponseProb', 'RelLatency']

varsToInclude= ['Subject', 'Projection', 'TotalStimulations', 'TotalPE', 'ActiveLicks', 'InactiveLicks', 'Session', 'Sex', 'Proportion', 'LicksPerReward', 'LicksPerRewardInactive', 'trainPhase', 'trainPhaseLabel', 'trainDayThisPhase', 'probActiveLP', 'probInactiveLP', 'leverPressTotal', 'typeLP', 'countLP']

# varsToInclude.append(y)

df= df[varsToInclude]


#%%--Prepare data for stats

#% -Subset only Initial Phase
phaseToInclude= 1

df= df[df.trainPhase==phaseToInclude]


# #--remove missing/invalid observations

# #-can only do stat comparison for DS vs NS in stages/sessions where NS auc is present
# #so subset to stages >=5
# ind= []
# ind= df.stage>=5

# df= df.loc[ind,:]

#- Stack licksPerReward and licksPerRewardInactive by typeLP
# test= df.melt(id_vars= 'typeLP', value_vars=['LicksPerReward','LicksPerRewardInactive'], value_name='rewardLicks')

#melt() and merge by setting index subject,session,typeLP

# df.reset_index(inplace=True)

test= df.melt(id_vars= ['Subject','Session'], value_vars=['LicksPerReward','LicksPerRewardInactive'], var_name= 'typeLP', value_name='licksPerRewardTypeLP')

# make typeLP labels identical
test.loc[(test.typeLP=='LicksPerReward'), 'typeLP']= 'ActiveLeverPress'
test.loc[(test.typeLP=='LicksPerRewardInactive'), 'typeLP']= 'InactiveLeverPress'



#already was melted/stacked by typeLP in matlab so redundant rows here added
test= test[test.groupby(['Subject','Session','typeLP']).cumcount()==0]


test.set_index(['Subject','Session','typeLP'], inplace=True)

df.set_index(['Subject','Session','typeLP'], inplace=True)


# test2= df.copy()
# test2['licksPerRewardTypeLP']= test['licksPerRewardTypeLP']

df['licksPerRewardTypeLP']= test['licksPerRewardTypeLP']

df.reset_index(inplace=True)



#-- Fix dtypes - explicitly assign categorical type to categorical vars
# note can use C() in statsmodels formula to treat as categorical tho good practice to change in df 

catVars= ['Subject', 'Projection', 'Session', 'Sex', 'trainPhase', 'trainPhaseLabel', 'trainDayThisPhase', 'typeLP']


df[catVars]= df[catVars].astype('category')




#%%-- Export to R.

# save to pickle
#- pandas version needs to match R environment version to load the pickle!
# # activate R environment for pickling (to make env management/consistency easier)
# conda activate r-env 

df= df.copy()

savePath= r'./_output/' #r'C:\Users\Dakota\Documents\GitHub\DS-Training\Python' 

print('saving fig5 df to file')

#Save as pickel
df.to_pickle(savePath+'fig5.pkl')




#%% ---------------------------FIG 6 ICSS ---------------



#%% ----- FIG 6 Stats -------

# OPTO ICSS

#%%--Load the data
datapath= r"C:\Users\Dakota\Documents\GitHub\DS-Training\Matlab\vp-vta-fp_stats_fig6Table.parquet"

dfFig6= pd.read_parquet(datapath)


df= dfFig6.copy()


#%%-- Isolate only data you want
#to save time/memory, pare down dataset to vars we are interested in

#multiply y vars in this table

# y= ['ResponseProb', 'RelLatency']

varsToInclude= ['Subject', 'Projection', 'Session', 'Sex','typeNP', 'trainPhase', 'logNP', 'countNP', 'npActiveProportion']

# varsToInclude.append(y)

df= df[varsToInclude]


#%%--Prepare data for stats

#% -Subset only Initial Phase
phaseToInclude= 'ICSS-OG-active-side'

df= df[df.trainPhase==phaseToInclude]

# #--remove missing/invalid observations

# #-can only do stat comparison for DS vs NS in stages/sessions where NS auc is present
# #so subset to stages >=5
# ind= []
# ind= df.stage>=5

# df= df.loc[ind,:]

#-- Fix dtypes - explicitly assign categorical type to categorical vars
# note can use C() in statsmodels formula to treat as categorical tho good practice to change in df 

catVars= ['Subject', 'Projection', 'Session', 'Sex','typeNP', 'trainPhase']

df[catVars]= df[catVars].astype('category')



#%%-- Export to R.

# save to pickle
#- pandas version needs to match R environment version to load the pickle!
# # activate R environment for pickling (to make env management/consistency easier)
# conda activate r-env 

df= df.copy()

savePath= r'./_output/' #r'C:\Users\Dakota\Documents\GitHub\DS-Training\Python' 

print('saving fig6 df to file')

#Save as pickel
df.to_pickle(savePath+'fig6.pkl')


# # Save an df with session-level observations (active proportion)
# df2= df[df.groupby(['Subject','Session']).cumcount()==0]


# print('saving fig6sessionLevel df to file')

# #Save as pickel
# df.to_pickle(savePath+'fig6sessionLevel.pkl')






#%% ---------------------------SUPPLEMENTAL FIG 5 Choice Task ---------------



#%%--Load the data
datapath= r"C:\Users\Dakota\Documents\GitHub\DS-Training\Matlab\vp-vta-fp_stats_fig5Table.parquet"

dfFig5= pd.read_parquet(datapath)


df= dfFig5.copy()


#%%-- Isolate only data you want
#to save time/memory, pare down dataset to vars we are interested in

#multiply y vars in this table

# y= ['ResponseProb', 'RelLatency']

varsToInclude= ['Subject', 'Projection', 'TotalStimulations', 'TotalPE', 'ActiveLicks', 'InactiveLicks', 'Session', 'Sex', 'Proportion', 'LicksPerReward', 'LicksPerRewardInactive', 'trainPhase', 'trainPhaseLabel', 'trainDayThisPhase', 'probActiveLP', 'probInactiveLP', 'leverPressTotal', 'typeLP', 'countLP']

# varsToInclude.append(y)

df= df[varsToInclude]


#%%--Prepare data for stats

#% -Don't Subset phase, retain all
# phaseToInclude= 1

# df= df[df.trainPhase==phaseToInclude]


# #--remove missing/invalid observations

# #-can only do stat comparison for DS vs NS in stages/sessions where NS auc is present
# #so subset to stages >=5
# ind= []
# ind= df.stage>=5

# df= df.loc[ind,:]

#- Stack licksPerReward and licksPerRewardInactive by typeLP
# test= df.melt(id_vars= 'typeLP', value_vars=['LicksPerReward','LicksPerRewardInactive'], value_name='rewardLicks')

#melt() and merge by setting index subject,session,typeLP

# df.reset_index(inplace=True)

test= df.melt(id_vars= ['Subject','Session'], value_vars=['LicksPerReward','LicksPerRewardInactive'], var_name= 'typeLP', value_name='licksPerRewardTypeLP')

# make typeLP labels identical
test.loc[(test.typeLP=='LicksPerReward'), 'typeLP']= 'ActiveLeverPress'
test.loc[(test.typeLP=='LicksPerRewardInactive'), 'typeLP']= 'InactiveLeverPress'



#already was melted/stacked by typeLP in matlab so redundant rows here added
test= test[test.groupby(['Subject','Session','typeLP']).cumcount()==0]


test.set_index(['Subject','Session','typeLP'], inplace=True)

df.set_index(['Subject','Session','typeLP'], inplace=True)


# test2= df.copy()
# test2['licksPerRewardTypeLP']= test['licksPerRewardTypeLP']

df['licksPerRewardTypeLP']= test['licksPerRewardTypeLP']

df.reset_index(inplace=True)



#-- Fix dtypes - explicitly assign categorical type to categorical vars
# note can use C() in statsmodels formula to treat as categorical tho good practice to change in df 

catVars= ['Subject', 'Projection', 'Session', 'Sex', 'trainPhase', 'trainPhaseLabel', 'trainDayThisPhase', 'typeLP']


df[catVars]= df[catVars].astype('category')




#%%-- Export to R.

# save to pickle
#- pandas version needs to match R environment version to load the pickle!
# # activate R environment for pickling (to make env management/consistency easier)
# conda activate r-env 

df= df.copy()

savePath= r'./_output/' #r'C:\Users\Dakota\Documents\GitHub\DS-Training\Python' 

print('saving Supplemental fig5 df to file')

#Save as pickel
df.to_pickle(savePath+'supplement_fig5.pkl')




#%% ---------------------------SUPPLEMENTAL FIG 6 ICSS ---------------



#%% ----- SUPPLEMENTAL FIG 6 Stats -------

# OPTO ICSS

#%%--Load the data
datapath= r"C:\Users\Dakota\Documents\GitHub\DS-Training\Matlab\vp-vta-fp_stats_fig6Table.parquet"

dfFig6= pd.read_parquet(datapath)


df= dfFig6.copy()


#%%-- Isolate only data you want
#to save time/memory, pare down dataset to vars we are interested in

#multiply y vars in this table

# y= ['ResponseProb', 'RelLatency']

varsToInclude= ['Subject', 'Projection', 'Session', 'Sex','typeNP', 'trainPhase', 'logNP', 'countNP', 'npActiveProportion']

# varsToInclude.append(y)

df= df[varsToInclude]


#%%--Prepare data for stats

# #% -DONT Subset by phase, keep all
# phaseToInclude= 'ICSS-OG-active-side'

# df= df[df.trainPhase==phaseToInclude]

# #--remove missing/invalid observations

# #-can only do stat comparison for DS vs NS in stages/sessions where NS auc is present
# #so subset to stages >=5
# ind= []
# ind= df.stage>=5

# df= df.loc[ind,:]

#-- Fix dtypes - explicitly assign categorical type to categorical vars
# note can use C() in statsmodels formula to treat as categorical tho good practice to change in df 

catVars= ['Subject', 'Projection', 'Session', 'Sex','typeNP', 'trainPhase']

df[catVars]= df[catVars].astype('category')



#%%-- Export to R.

# save to pickle
#- pandas version needs to match R environment version to load the pickle!
# # activate R environment for pickling (to make env management/consistency easier)
# conda activate r-env 

df= df.copy()

savePath= r'./_output/' #r'C:\Users\Dakota\Documents\GitHub\DS-Training\Python' 

print('saving Supplemental fig6 df to file')

#Save as pickel
df.to_pickle(savePath+'supplement_fig6.pkl')


# # Save an df with session-level observations (active proportion)
# df2= df[df.groupby(['Subject','Session']).cumcount()==0]


# print('saving fig6sessionLevel df to file')

# #Save as pickel
# df.to_pickle(savePath+'fig6sessionLevel.pkl')





#%% ------ OLD statsmodels code examples: ------
# #%% abandoned statsmodels because LME posthoc tests not working 
# #%%-- Run model

# # statsmodels simply doesn't seem to have the posthoc tests worked out for mixed effects models yet https://github.com/statsmodels/statsmodels/issues/4787 ; https://github.com/statsmodels/statsmodels/issues/4916

# # use C() to manually declare categorical & automatic dummy coding (should be inferred automatically)
# groups= 'subject'

# formula= 'periCueBlueAuc ~ C(trialType) * C(sesSpecialLabel)'

# model= smf.mixedlm(data=df, formula= formula, groups= df[groups])

# modelFit= model.fit()

# print(modelFit.summary())

# #TODO: print output to file?

# #significant trialType*sesSpecialLabel interaction. Follow-up below

# #%% -- Follow-up tests

# #pairwise failing here... because of dummy coding?
# pw= modelFit.t_test_pairwise('C(trialType)')

# pw= modelFit.t_test_pairwise('C(sesSpecialLabel)')

# pw= modelFit.t_test_pairwise('C(trialType)*C(sesSpecialLabel)')


# # ValueError: r_matrix for t-test should have 6 columns
# # what's the r_matrix..

#     # another f test documentation
#     # r_matrix{array_like, str, tuple}
#     # One of:
    
#     # array : An r x k array where r is the number of restrictions to test and k is the number of regressors. It is assumed that the linear combination is equal to zero.
    
#     # str : The full hypotheses to test can be given as a string. See the examples.
    
#     # tuple : A tuple of arrays in the form (R, q), q can be either a scalar or a length k row vector.

#     # t test documentation (not _t_test_paired)
#     # r_matrix{array_like, str, tuple}
#     # One of:
    
#     # array : If an array is given, a p x k 2d array or length k 1d array specifying the linear restrictions. It is assumed that the linear combination is equal to zero.
    
#     # str : The full hypotheses to test can be given as a string. See the examples.
    
#     # tuple : A tuple of arrays in the form (R, q). If q is given, can be either a scalar or a length p row vector.

# # pw= modelFit.t_test_pairwise('C(trialType)*C(sesSpecialLabel)')


# # #try simpler model then pairwise?
# # # groups= 'subject'

# # formula= 'periCueBlueAuc ~ C(trialType) + C(sesSpecialLabel)'

# # model= smf.mixedlm(data=df, formula= formula, groups=groups)

# # modelFit= model.fit()

# # print(modelFit.summary())

# # pw=modelFit.t_test_pairwise('C(trialType)')


# # #try simpler model then pairwise?
# # # groups= 'subject'

# # formula= 'periCueBlueAuc ~ trialType + sesSpecialLabel'

# # model= smf.mixedlm(data=df, formula= formula, groups=groups)

# # modelFit= model.fit()

# # print(modelFit.summary())

# # pw=modelFit.t_test_pairwise('trialType')


# # # maybe be more explicit with model call ?
# # model= smf.mixedlm(data=df, formula= 'periCueBlueAuc ~ trialType + sesSpecialLabel', groups='subject')

# # modelFit= model.fit()

# # print(modelFit.summary())

# # pw=modelFit.t_test_pairwise('trialType')


