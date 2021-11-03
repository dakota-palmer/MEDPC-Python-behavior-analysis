# -*- coding: utf-8 -*-
"""
Created on Wed Nov  3 11:49:15 2021

@author: Dakota
"""

#use statsmodels package for factorial ANOVA
import statsmodels.api as sm
import statsmodels.formula.api as smf
import pandas as pd

def optoStats (df, y, fixedEffects, mixedEffects):
    
    df_lm = smf.ols('probPE ~ C(sex, Sum)*C(virus, Sum)', data=df).fit()    
    
    df_lm_table= sm.stats.anova_lm(df_lm, typ=2) #Type 2 ANOVA DataFrame

# Y = C + M1*X1 + M2*X2
# Y = Dependent variable (output/outcome/prediction/estimation)
# C = Constant (Y-Intercept)
# M = Slope of the regression line (the effect that X has on Y)
# X = Independent variable (input variable used in the prediction of 


#%% testing regression functions - should be pretty good baseline example for regression modeling time series data
#remove empty placeholders, ensure dtypes ok
# all categorical variables should be converted into dummy variables before modeling!!! 
# https://www.statology.org/pandas-get-dummies/
# df.subject= df.subject.astype('category')
# df.virus= df.virus.astype('category')
# df.sex= df.sex.astype('category')
df= dfPlot.copy()

#subset as needed
# df= df.loc[df.subject.notnull()]

#datetime needs to be converted as well?
# df.date= pd.datetime(df.date)


# catVars= ['virus', 'sex', 'subject','stage', 'laserDur', 'trialType']
# df= pd.get_dummies(df, columns=catVars , drop_first=True)


#if columns= None, will automatically make dummies of Object and Categorical type columns
df= pd.get_dummies(df, columns=None , drop_first=True)


# search auto-generated dummy columns for variable names we want to include in model. Iterate through and collect into new series
fixedEffects= ['virus','sex', 'stage', 'trialType', 'laserDur']
fixedEffectsDum= pd.Series()

for var in fixedEffects:
    fixedEffectsDum= fixedEffectsDum.append(df.columns[df.columns.str.contains(pat = var)].to_series())
    

y= ['probPE']


#FIXED EFFECTS LM

testModel= sm.OLS(df.loc[:,y], df.loc[:,fixedEffectsDum]).fit()

testPredict= testModel.predict(df.loc[:,fixedEffectsDum])

print_testModel= testModel.summary()

print(print_testModel)


#MIXED EFFECTS LM
df= dfPlot.copy()
#removing empty placeholders
df= df.loc[df.subject.notnull()]

#convert categorical var strings to int codes?
df['subjCode'] = df.subject.cat.codes.copy()
df['trialTypeCode'] = df.trialType.cat.codes.copy()
df['laserDurCode'] = df.laserDur.cat.codes.copy()


mixedEffects= ['subjCode']

#random intercept for subject

# Since the random effects structure is not specified, the default random effects structure (a random intercept for each group) is automatically used.

testMixed = smf.mixedlm(data=df, formula= 'probPE ~virus + sex + laserDurCode + trialTypeCode', groups= df['subjCode'])
#why would i get error for trialType but not laserDur?

testMixedFit= testMixed.fit() #(method=['lbfgs'])

print(testMixedFit.summary())

# Next we fit a model with two random effects for each animal: a random intercept, and a random slope (with respect to time). This means that each pig may have a different baseline weight, as well as growing at a different rate. 
# 
#%% ANOVA testing
