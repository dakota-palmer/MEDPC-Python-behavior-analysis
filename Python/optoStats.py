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


#%% FIXED EFFECTS LM

testModel= sm.OLS(df.loc[:,y], df.loc[:,fixedEffectsDum]).fit()

testPredict= testModel.predict(df.loc[:,fixedEffectsDum])

print_testModel= testModel.summary()

print(print_testModel)


#%% MIXED EFFECTS LM
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
# 
testMixed = smf.mixedlm(data=df, formula= 'probPE ~virus + sex + laserDurCode + trialTypeCode', groups= df['subjCode'])
# testMixed = smf.mixedlm(data=df, formula= 'probPE ~virus + sex + laserDur + trialType', groups= df['subjCode'])

#why would i get error for fitting trialType but not laserDur?

testMixedFit= testMixed.fit() #(method=['lbfgs'])

print(testMixedFit.summary())

# Next we fit a model with two random effects for each animal: a random intercept, and a random slope (with respect to time). This means that each pig may have a different baseline weight, as well as growing at a different rate. 
# 
#%% ANOVA testing

# https://www.theanalysisfactor.com/why-anova-and-linear-regression-are-the-same-analysis/
# https://www.statsimprove.com/en/what-is-the-difference-between-anova-and-regression-and-which-one-to-choose/

df= dfPlot.copy()


df_lm = smf.ols('probPE ~ C(sex, Sum)*C(virus, Sum)', data=df).fit()    

df_lm = smf.ols('probPE ~ sex * trialType', data=df).fit()    
 

df_lm_table= sm.stats.anova_lm(df_lm, typ=2) #Type 2 ANOVA DataFrame

print(df_lm.summary())

#%% statsmodels getting started notes
import statsmodels.api as sm
import statsmodels.formula.api as smf
import formulaic


df= dfPlot.copy()

#subset data
df= df.loc[dfPlot.stage=='Cue Manipulation'].copy()
df= df.loc[dfPlot.trialType.str.contains('DS') | dfPlot.trialType.str.contains('NS')].copy()

#subset by virus
df= df.loc[dfPlot.virus=='stgtacr'].copy()


#For stats, split trialType column into cueType and laserType
df[['cueType','laserType']]= df.trialType.copy().str.split('_', expand=True)
df.loc[df.laserType.isnull(),'laserType']= 'noLaser'


# To fit most of the models covered by statsmodels, you will need to create two design matrices. The first is a matrix of endogenous variable(s) (i.e. dependent, response, regressand, etc.). The second is a matrix of exogenous variable(s) (i.e. independent, predictor, regressor, etc.). The OLS coefficient estimates are calculated as usual

 # Typically, the raw input data for a model is stored in a dataframe, but the actual implementations of various statistical methodologies (e.g. linear regression solvers) act on two-dimensional numerical matrices that go by several names depending on the prevailing nomenclature of your field, including "model matrices", "design matrices" and "regressor matrices" (within Formulaic, we refer to them as "model matrices"). A formula provides the necessary information required to automate much of the translation of a dataframe into a model matrix suitable for ingestion into a statistical model.
# set()                                                       
# We use patsy’s dmatrices function to create design matrices:
# y, X = dmatrices('Lottery ~ Literacy + Wealth + Region', data=df, return_type='dataframe')

# y, X= dmatrices('probPE ~ virus + sex + stage + laserDur + subject +  trialType', data=df, return_type='dataframe')

# Formulaic module is successor to Patsy which is no longer in development
# y, X = model_matrix("y ~ a + b + a:b", df)
# This is short-hand for:
# y, X = formulaic.Formula('y ~ a + b + a:b').get_model_matrix(df)
# y, X = formulaic.Formula('probPE ~ virus + sex + virus:sex').get_model_matrix(df)

# a * b is equivalent to a + b + a:b
y, X = formulaic.Formula('probPE ~ sex * cueType * laserType * laserDur').get_model_matrix(df)


# Fitting a model in statsmodels typically involves 3 easy steps:

#1) Use the model class to describe the model
#e.g. mod = sm.OLS(y, X)    # Describe model


#2) Fit the model using a class method
# e.g. res = mod.fit()       # Fit model


#3) Inspect the results using a summary method
# e.g. print(res.summary())   # Summarize model


# statsmodels also provides graphics functions. For example, we can draw a plot of partial regression for a set of regressors by:
# : sm.graphics.plot_partregress('Lottery', 'Wealth', ['Region', 'Literacy'],
#    ....:                              data=df, obs_labels=False)
mod= sm.OLS(y,X) # Describe model
res = mod.fit()       # Fit model

print(res.summary())   # Summarize model



# # regression visualizations
# fig = sm.graphics.influence_plot(res, criterion="cooks")
# fig.tight_layout(pad=1.0)
# fig.tight_layout(pad=1.0)


