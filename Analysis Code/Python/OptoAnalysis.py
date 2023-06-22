# On Windows all of your multiprocessing-using code must be guarded by if __name__ == "__main__":

# So to be safe, I would put all of your the code currently at the top-level of your script in a main() function, and then just do this at the top-level:

# if __name__ == "__main__":
#     main()

if __name__ == '__main__':

    # -*- coding: utf-8 -*-
    """
    Created on Thu Jun 17 10:03:30 2021

    @author: Dakota
    """

    import numpy as np
    import scipy.io as sio
    import pandas as pd
    import seaborn as sns
    import matplotlib.pyplot as plt
 
    import shelve
    
        
    # script ('module') containing custom fxns
    from customFunctions import saveFigCustom
    from customFunctions import subsetData
    from customFunctions import subsetLevelObs
    from customFunctions import percentPortEntryCalc
    from customFunctions import groupPercentCalc

    #%% Load previously saved dfTidyAnalyzed (and other vars) from pickle
    dataPath= r'./_output/' #'r'C:\Users\Dakota\Documents\GitHub\DS-Training\Python\\'
    
    dfTidyOpto= pd.read_pickle(dataPath+'dfTidyAnalyzed.pkl')
    
    #load any other variables saved during the import process ('dfTidymeta' shelf)
    my_shelf = shelve.open(dataPath+'dfTidymeta')
    for key in my_shelf:
        globals()[key]=my_shelf[key]
    my_shelf.close()
    
        
    #%% set opto specific plotting options
    sns.set_palette('Paired') #great for compairing laser on vs laser off trialTypes
    
    subjPalette= 'tab20'

    savePath= r'./_output/_optoAnalysis/'
    
    
   # #manually defining color order so that paired color scheme looks nice
   #and consistent between all plots
    trialOrder= (['DStime', 'DStime_laser', 'NStime', 'NStime_laser', 'Pre-Cue','ITI'])
 
    subjectOrder= dfTidyOpto.subject.unique()
    

    criteriaDS= 0.6
    
      
   #%% Declare hierarchical grouping variables for analysis
    # e.g. for aggregated measures, how should things be calculated and grouped?
    
    # examples of different measures @ different levels:
    # consider within-file (e.g. total PEs per session)
    # within-trialType (e.g. Probability of PEs during all DS vs. all NS)
    # within-trialID measures (e.g. Latency to enter port all individual trials)
    # within virus, cue identity, subject, stage, etc.
    
    if experimentType.__contains__('Opto'):
        groupHierarchySubject = ['virus', 'sex', 'stage',
                                'subject']
       
        groupHierarchyFileID = ['virus', 'sex', 'stage',
                                'subject', 'trainDayThisStage', 'fileID']
        
        groupHierarchyTrialType = ['virus', 'sex', 'stage',
                                   'subject', 'trainDayThisStage', 'fileID', 'trialType']
        
        groupHierarchyTrialID = ['virus', 'sex', 'stage',
                                 'subject', 'trainDayThisStage', 'trialType', 'fileID', 'trialID']
        
        groupHierarchyEventType = ['virus', 'sex', 'stage',
                                 'subject', 'trainDayThisStage', 'trialType', 'fileID', 'trialID', 'eventType']


   #%%- Add random 'laser' trial labels for pre-laser sessions (e.g. stage 5 technically didn't have laser trials)
   #TODO: diff() of PE probability won’t apply to subj. who are running below CM stage. There will be no Laser trials so no diff() can be represented in these plots. Either 1) add random laser trials (sync with other subjs) or 2) only include laser sessions in the diff() plots
      
    dfTidyOpto.trialType= dfTidyOpto.trialType.astype(str)
    dfTemp= dfTidyOpto.copy()
    
    #restrict to late sessions (stage 5) that already don't have laser labelled trials
    dfTemp= dfTemp.loc[dfTemp.stage.str.contains('5')]

    #restrict to DS and NS trialTypes
    dfTemp= dfTemp.loc[dfTemp.trialID>=0].copy()
    
    #subset to 1 obs per trial
    dfTemp= subsetLevelObs(dfTemp, groupHierarchyTrialID)
    
    #simply 'randomly' assign half as laser on
    trialCount= 30
    
    ids = dfTemp['trialID'].unique()
    ids = np.random.choice(ids, size=int(trialCount/2), replace=False)
    
    
    #2
    # test= dfTemp.groupby(groupHierarchyFileID)['trialID'].sample(n=int(trialCount/2), random_state=1)
    # test= dfTemp.groupby(groupHierarchyTrialID)['trialID'].sample(n=int(trialCount/2), random_state=1)

    #3

    #random sample half of the trials by trialType, label these as laser trials
    dfTemp= dfTemp.groupby(['fileID', 'trialType']).sample(n=int(trialCount/2), random_state=1)#.reset_index()
    
    # dfTemp['trialTypeNew']= dfTemp.trialType+'_laser'
    
    dfTemp['trialType']= dfTemp.trialType+'_laser'

    
    # #reassign to df!
    # dfTidyOpto.loc[dfTemp.index, 'trialType']= dfTemp.trialType.copy()
    
    # #ffill wont work unless filling na
    # dfTidyOpto.trialtype= dfTidyOpto.groupby(groupHierarchyTrialID).trialType.ffill()
    
    
    # dfTemp= dfTemp[groupHierarchyTrialID]
    # test= dfTidyOpto.copy()
    # test.trialType= test.merge(dfTemp, how='left', on=groupHierarchyTrialID).trialType


    # #Update- no bc want to merge on all fileID,trialID entries (not just single ind)
    # #since wanting to update same column, use update() instead of merge()?
    # test= dfTidyOpto.copy()
    # test2= test.update(dfTemp)

    # #Merge
    # #cant use trialtype as merger column bc it wont match
    
    # test= dfTidyOpto.copy()
    
    # # test= dfTidyOpto.merge(dfTemp[['fileID','trialID','trialTypeNew']], on=['fileID', 'trialID']).trialTypeNew.copy()
    
    # test= dfTidyOpto.merge(dfTemp[['fileID','trialID','trialType']], on=['fileID', 'trialID'])
    
    # #-try setting index before merge?
    # test= dfTidyOpto.copy()
    
    # test2= dfTemp.copy()
    # test2= test2.set_index(['fileID','trialID'])
    
    # # test= test.set_index(['fileID','trialID'])
    
    # test3= test.merge(test2, on=['fileID','trialID'], how='left')
    
    #try setting index, then assignment specifically using grouped ind- should work!?
    test= dfTidyOpto.copy()
    test2= dfTemp.copy()
    
    test= test.set_index(['fileID','trialID'])
    test2= test2.set_index(['fileID','trialID'])
    
    test4= test.copy()
    test4.loc[test2.index, 'trialType']= test2.trialType.copy()
    
    # #try set_index then update?
    # test= dfTidyOpto.copy()
    # test2= dfTemp.copy()
    
    # test= test.set_index(['fileID','trialID'])
    # test2= test2.set_index(['fileID','trialID'])

    # # test3= test.copy().trialType.update(test2.trialType)
    
    # test4= test.copy()
    
    # test4.trialType= test2.trialType
    
    
    # #-
    # dfTidyOpto.trialType= dfTidyOpto.merge(dfTemp[['fileID','trialID','trialType']], how='left', on=['fileID', 'trialID'])
    
     # Assign back to df by setting index, then assignment specifically using grouped ind
    dfTidyOpto.set_index(['fileID','trialID'], inplace=True)
    dfTemp.set_index(['fileID','trialID'], inplace=True)
    
    dfTidyOpto.loc[dfTemp.index, 'trialType']= dfTemp.trialType.copy()

    
    dfTidyOpto.trialType= dfTidyOpto.trialType.astype('category')
    
    dfTidyOpto.reset_index(inplace=True)

    #Viz trialTypes by stage now
    dfPlot= dfTidyOpto.copy()
    
    #subset
    stagesToPlot= dfPlot.loc[(dfPlot.stage.str.contains('CM') | dfPlot.stage.str.contains('5')), 'stage'].unique().astype(str)
    trialTypesToPlot= ['DStime','DStime_laser','NStime','NStime_laser']
    eventsToPlot= dfPlot.eventType.unique()

    dfPlot= subsetLevelObs(dfPlot, groupHierarchyTrialID)

    dfPlot= subsetData(dfPlot, stagesToPlot, trialTypesToPlot, eventsToPlot)


    dfPlot.loc[:,'trialCount']= dfPlot.groupby(groupHierarchyTrialType)['trialID'].transform('count').copy()
    
    
    
    sns.catplot(data= dfPlot, kind='bar', row='stage', col='trialType', x='trainDayThisStage', y='trialCount', hue='subject', palette=subjPalette, hue_order=subjectOrder)

    
    #%% - Add "Baseline" stage for comparison to test sessions
    #Don't have laser off cue manip sessions for some subjects...  should make new baseline 'stage' for simply day before laser began?
    #this will be baseline to compare against (instead of laser off day?)
    
    #briefly, will add column for laserState either ON or OFF, get first() trainDay ON for each subject, save this as new column, subtract nBaselineSessions from this trainDay, and update stages accordingly matching these trainDays
    
    dfTidyOpto.stage= dfTidyOpto.stage.astype(str)

    dfTemp= dfTidyOpto.copy()
    
    #number of sessions prior to laser ON which we should count as baseline (1+n bc of cumcount()), so 0 is 1 and 1 is 2
    nBaselineSessions= 1
    
    
    #go through and label sessions as laser off or on 
    #find first session for each subject with non-zero
    dfTemp['laserState']= dfTemp.laserDur.copy()
    
    dfTemp.loc[dfTemp.laserDur.isnull(),'laserState']= 'off'
    dfTemp.loc[dfTemp.laserDur.str.contains('0.0 @ 0'),'laserState']= 'off'
    dfTemp.loc[dfTemp.laserDur.str.contains('nan'), 'laserState']= 'off'
    
    dfTemp.loc[dfTemp.laserState!= 'off', 'laserState']= 'ON'

    
    #get trainDay corresponding to first laser ON day for each subj, subtract 1. This is the last laser off day.
    # dfTemp= dfTemp.loc[dfTemp.laserState!='off']
    # trainDay= dfTemp.groupby(['subject','laserState'], as_index=False)['trainDay'].first()
    
    
    # dfTemp['laserStartDay']= dfTemp.groupby(['subject','laserState'])['trainDay'].transform('first')-1

    dfTemp['laserStartDay']= dfTemp.loc[dfTemp.laserState!='off'].groupby(['subject','laserState'])['trainDay'].transform('first')-1
    
    dfTemp['laserStartDay'] = dfTemp.groupby(['subject'])['laserStartDay'].fillna(method='bfill')
      
    
     # test= (dfTemp.groupby(['subject','laserState'])['trainDay'].transform('first')-1).reset_index()
    
    # test= dfTemp.loc[dfTemp.laserState!='off'].groupby(['subject','laserState'])['trainDay'].transform('first')-1

    
    
    #use this to check matching trainDays and change stage accordingly
    ind= ((dfTemp.trainDay >= dfTemp.laserStartDay-nBaselineSessions) & (dfTemp.trainDay <= dfTemp.laserStartDay))
    dfTemp.loc[ind, 'stage']= '5.9-Pre-Laser'
    
    #save updated col back into df
    dfTidyOpto.stage= dfTemp.stage.copy()
    dfTidyOpto.stage= dfTidyOpto.stage.astype('category')

    
    #%%- exclude sessions without laser manipulations
    # dfTidyOpto= dfTidyOpto.loc[dfTidyOpto.laserDur!='nan @ nan']
    # dfTidyOpto= dfTidyOpto.loc[dfTidyOpto.laserDur.notnull()]
    
    # dfTidyOpto.laserDur= dfTidyOpto.laserDur.astype('category')
    
    
    #keep pre-laser 'stage'
    # stagesToInclude= ['CM', 'Pre-Laser']
    
    # dfTidyOpto= dfTidyOpto.stage.str.contains('CM')
    
    ind= (dfTidyOpto.stage.str.contains('CM') | dfTidyOpto.stage.str.contains('Pre-Laser'))
    
    dfTidyOpto= dfTidyOpto[ind]
    
    #-- Simply exclude remaining 0.0 @ 0 sessions (some subj had more than others, let's just grab the last nBaselineSessions and cut out all the rest)
    dfTidyOpto= dfTidyOpto.loc[~dfTidyOpto.stage.str.contains('0.0 @ 0')]

    
    #redefine categories
    dfTidyOpto.stage= dfTidyOpto.stage.cat.remove_unused_categories()
    
    
    #%%--- Recalculate trainDayThisStage now that we've altered stages ----
    
    dfGroup = dfTidyOpto.loc[dfTidyOpto.groupby('fileID').transform('cumcount') == 0, :].copy()  # one per session
    dfTidyOpto['trainDayThisStage'] = dfGroup.groupby(
        ['subject', 'stage']).transform('cumcount')
    dfTidyOpto.trainDayThisStage = dfTidyOpto.groupby(
        ['fileID'])['trainDayThisStage'].fillna(method='ffill').copy()
    
    #%%------ Recalculate trialOutcomes and probPE now that have new trialTypes! ------------------
    # TODO: consider adding trialTypes ealier in behaviorAnalysis instead of recalculating here
    
    # had trialTypeOutcomeBehProb10s but commented out bc memory error, so use 'try:' for now
    try:
        dfTidyOpto= dfTidyOpto.drop(['trialTypePEProb10s', 'trialTypeOutcomeBehProb10s'], axis=1)
    except:
        dfTidyOpto= dfTidyOpto.drop(['trialTypePEProb10s'], axis=1)

    # %%- Calculate Probability of behavioral outcome for each trial type.
    # This is normalized so is more informative than simple count of trials.
    
    # declare hierarchical level of analysis for the analysis we are doing (here there is one outcome per trial per file)
    levelOfAnalysis = ['fileID', 'trialID']
    
    # First we need to subset only one outcome per level of analysis (trial)
    dfGroup = dfTidyOpto.loc[dfTidyOpto.groupby(levelOfAnalysis).cumcount() == 0].copy()
    
    #alternatively, this is the same as:
    # dfGroup= dfTidyOpto[obsTrial]
    
    # declare hierarchical grouping variables (how should the observations be separated)
    groupHierarchy = groupHierarchyTrialType
    
    # here want percentage of each behavioral outcome per trialType per above groupers
    colToCalc = 'trialOutcomeBeh10s'
    
    dfTemp = groupPercentCalc(dfGroup, levelOfAnalysis, groupHierarchy, colToCalc)
    
    #instead of 1 col per probability, melt into single column that matches up to outcome
    dfTemp= dfTemp.reset_index().melt(
        id_vars=groupHierarchy, value_name='trialTypeOutcomeBehProb10s')
    
    #merge to save as new column in dfTidyOpto
    dfTidyOpto = dfTidyOpto.merge(dfTemp, how='left', on=groupHierarchy+[colToCalc])
    
    #%%- Calculate PE probability for each trialType
    #(combines all outcomes with PE vs all outcomes with no PE)
    
    dfTemp= dfTidyOpto.copy()
    
    
    # declare hierarchical grouping variables (how should the observations be separated)
    groupHierarchy = groupHierarchyTrialType
    
    
    # here want percentage of each behavioral outcome per trialType per above groupers
    colToCalc = 'trialOutcomeBeh10s'
    
    dfTemp= percentPortEntryCalc(dfTemp, groupHierarchy, colToCalc)
    
    dfTemp= dfTemp.reset_index()
    
    dfTemp= dfTemp.rename(columns= {'PE':'trialTypePEProb10s'})
    
    dfTidyOpto= dfTidyOpto.merge(dfTemp, how='left', on=groupHierarchy)

    
    

    
        #%% viz remaining sessions
    
    # #-stages
    # dfPlot= dfTidyOpto.copy()
    
    # dfPlot= subsetLevelObs(dfPlot, groupHierarchyFileID)
    
    
    # dfPlot['sesCount']= dfPlot.groupby(groupHierarchySubject).fileID.transform('count')

    
    # sns.catplot(data= dfPlot, kind='bar', x='stage', y='sesCount', hue='subject', hue_order=subjectOrder)
    
    # #-laserDur
    # dfPlot= dfTidyOpto.copy()
    
    # dfPlot= subsetLevelObs(dfPlot, groupHierarchyFileID)
    
    
    # dfPlot['sesCount']= dfPlot.groupby(['virus','sex','subject','laserDur']).fileID.transform('count')

    
    # sns.catplot(data= dfPlot, kind='bar', x='laserDur', y='sesCount', hue='subject', hue_order=subjectOrder)
  
    
      #%%- Remove Lick+Laser trials without PE+Lick
      
    #   #TODO: what is the best way to deal with this? 
    #   #could make a new column or trialType labels for just lick+laser sessions? 
    #   #or, could also just remove "laser off" trials without PE+lick- easier, doing this
      
    #   #However, instead of changing dfTidyOpto itself just do it locally later where necessary
      
    # #Correct comparison between laser ON and laser OFF trials for lick-paired should only include trials with PE+Lick
    
    # #noPE+lick laser trials exist, probably from first bad session without PE gate?
    # print(dfTidyOpto.loc[(dfTidyOpto.laserDur=='Lick') & (dfTidyOpto.trialType=='laserDStrial_1')].trialOutcomeBeh10s.unique())
    # print(dfTidyOpto.loc[(dfTidyOpto.laserDur=='Lick') & (dfTidyOpto.trialType=='laserNStrial_1')].trialOutcomeBeh10s.unique())
    
    
    # #for overall pe and lick probability, make a copy to keep all trials
    # dfTidyOpto2= dfTidyOpto.copy()

    
    # # #retain only trials with PE+lick for comparison
    # # #instead of making new df, just remove from dfTidyOpto
    # # dfTidyOpto.loc[dfTidyOpto.laserDur=='Lick',:]= dfTidyOpto.loc[(dfTidyOpto.laserDur=='Lick') & (dfTidyOpto.trialOutcomeBeh10s=='PE+lick')]
    


    #%%- redefine order of trialType for plotting; ITI trialtype from plotting
    trialOrder= (['DStime', 'DStime_laser', 'NStime', 'NStime_laser', 'Pre-Cue'])





   #%%---- Calculate difference score between laser off and laser on trialTypes ------
   
   #~~TODO: diff() of PE probability won’t apply to subj. who are running below CM stage. There will be no Laser trials so no diff() can be represented in these plots. Either 1) add random laser trials (sync with other subjs) or 2) only include laser sessions in the diff() plots
   
    dfTemp= dfTidyOpto.copy()
    
    #initialize empty col
    dfTidyOpto['trialTypePEProb10sdiff'] = pd.Series(dtype=float)

    #get rid of ITI & pre cue then just use diff() to get difference
    #basically, will groupby file, subset DS & NS separately, and diff() so get one value per file for DS and one per file per NS
    dfTemp= dfTemp.loc[((dfTemp.trialType!='Pre-Cue') & (dfTemp.trialType!='ITI') )].copy()

    #subset data at correct level of observation for variable    
    groupHierarchy= groupHierarchyTrialType
    dfTemp= subsetLevelObs(dfTemp, groupHierarchy)


    #sort to get consistent order of trialType for correct diff(), should not assume order of trialTypes 
    dfTemp= dfTemp.sort_values(['fileID','trialType']).copy()
    
    #diff then will be laser - non laser

    #take diff between DS trial types 
    ind= dfTidyOpto.trialType.str.contains('DS')
    
    # test2= dfTemp.loc[ind].groupby('fileID').trialTypePEProb10s.diff()

    test= dfTemp.copy()
    test.loc[ind,'trialTypePEProb10sdiff']= dfTemp.loc[ind].groupby('fileID').trialTypePEProb10s.diff()
    
    #examining some more extreme values
    test= test.loc[test.stage.str.contains('Pre-Laser')].copy()

    dfTidyOpto.loc[ind,'trialTypePEProb10sdiff']= dfTemp.loc[ind].groupby('fileID').trialTypePEProb10s.transform('diff')
    
    #take diff between NS trial types 
    ind= dfTidyOpto.trialType.str.contains('NS')

    dfTidyOpto.loc[ind,'trialTypePEProb10sdiff']= dfTemp.loc[ind].groupby('fileID').trialTypePEProb10s.transform('diff')
    
    
    #%% ------- Plots: -------------------
        #TODO: move to separate script?
    #%% -PE Prob Diff progression across days (all days separate per stage)
    
       #make plots
    dfPlot= dfTidyOpto.copy()

    stagesToPlot= dfPlot.stage.unique()
    trialTypesToPlot= ['DStime_laser','NStime_laser']
    eventsToPlot= dfPlot.eventType.unique()

    
    #running fxn still to remove unused categories
    dfPlot= subsetData(dfPlot, stagesToPlot, trialTypesToPlot, eventsToPlot)

    
   #individual subject facet
    g= sns.relplot(data= dfPlot, kind='line', estimator=None, col='subject', col_wrap=3, x='trainDayThisStage', y='trialTypePEProb10sdiff', hue='trialType', hue_order=trialOrder, style='stage', markers=True)
    # g.map(refline(y=0, linewidth=2, linestyle="-", color=None, clip_on=False))
    g.map(plt.axhline, y=0, color=".2", linewidth=3, dashes=(3,1), zorder=0)

    # g= sns.FacetGrid(data= dfPlot, row='stage', col='trialType')
    # g.map_dataframe(sns.lineplot, data= dfPlot, units='subject', estimator=None, x='trainDayThisStage', y='trialTypePEProb10sdiff', hue='trialType', hue_order=trialOrder, style='subject', markers=True)


    for virus in dfPlot.virus.unique():
        dfPlot2= dfPlot.loc[dfPlot.virus==virus]
        
        #get rid of extra categories
        dfPlot2= subsetData(dfPlot2, stagesToPlot, trialTypesToPlot, eventsToPlot)
    

        #--bar plot with point plot of individual subj overlaid
        g= sns.catplot(data=dfPlot2, col='stage', row='trialType', kind='bar', dodge=False, x='trainDayThisStage', y='trialTypePEProb10sdiff', hue='trialType', hue_order=trialOrder, palette='Paired')
        # g.map_dataframe(sns.pointplot, x='trainDayThisStage', y='trialTypePEProb10sdiff', hue= 'subject', palette= subjPalette, alpha=0.04)
     
        #using lineplot bc easy to adjust alpha
        
        #hue=subject
        # g.map_dataframe(sns.lineplot, estimator= None, x='trainDayThisStage', y='trialTypePEProb10sdiff', hue= 'subject', palette= subjPalette, alpha=0.6, style='subject', dashes=False, markers=True)
        
        #hue=trialType
        g.map_dataframe(sns.lineplot, units='subject', estimator= None, x='trainDayThisStage', y='trialTypePEProb10sdiff', hue= 'trialType', hue_order=trialOrder, palette= 'Paired', alpha=0.6, style='subject', dashes=False, markers=True)

        g.fig.suptitle(virus+'- Daily PE Probability difference score: laser - no laser')
        g.set_ylabels('delta PE prob (laser-no laser trials)')
        g.set_xlabels('trainDayThisStage')       
        
           #manually set axes limits
        g.set(xlim= (-0.5,dfPlot2.trainDayThisStage.max()+.5))   
        g.set(ylim= (-1,1))   

        # g.add_legend()
        
        saveFigCustom(g, virus+'- Daily PE Probability difference score (laser trial probPE - no laser trial probPE)', savePath)
        
       #%% --Plots: Combined PE Prob Diff (all days pooled per stage)
    
    #subset data
    dfPlot= dfTidyOpto.copy()

    stagesToPlot= dfPlot.stage.unique()
    trialTypesToPlot= ['DStime_laser','NStime_laser']
    eventsToPlot= dfPlot.eventType.unique()

    
    #running fxn still to remove unused categories
    dfPlot= subsetData(dfPlot, stagesToPlot, trialTypesToPlot, eventsToPlot)

    
   #individual subject facet
    g= sns.relplot(data= dfPlot, kind='line', estimator=None, col='subject', col_wrap=3, x='trainDayThisStage', y='trialTypePEProb10sdiff', hue='trialType', hue_order=trialOrder, style='stage', markers=True)
    # g.map(refline(y=0, linewidth=2, linestyle="-", color=None, clip_on=False))
    g.map(plt.axhline, y=0, color=".2", linewidth=3, dashes=(3,1), zorder=0)

    # g= sns.FacetGrid(data= dfPlot, row='stage', col='trialType')
    # g.map_dataframe(sns.lineplot, data= dfPlot, units='subject', estimator=None, x='trainDayThisStage', y='trialTypePEProb10sdiff', hue='trialType', hue_order=trialOrder, style='subject', markers=True)


    #get pooled mean() of diff for this subj score within-stages
    #definitely have multiple observations, why am i getting an error when i try to get mean() or plot?
    test= dfPlot.groupby(groupHierarchySubject).trialTypePEProb10sdiff.count().reset_index()

    #could be because of empty groups?
    test2= dfPlot.groupby(groupHierarchySubject, observed=True).trialTypePEProb10sdiff.count().reset_index()

    test3= dfPlot.groupby(groupHierarchySubject, observed=True).trialTypePEProb10sdiff.value_counts()




    for virus in dfPlot.virus.unique():
        dfPlot2= dfPlot.loc[dfPlot.virus==virus]
        
        #get rid of extra categories
        dfPlot2= subsetData(dfPlot2, stagesToPlot, trialTypesToPlot, eventsToPlot)
        

        #--bar plot with point plot of individual subj overlaid
        g= sns.catplot(data=dfPlot2, row='trialType', kind='bar', dodge=False, x='stage', y='trialTypePEProb10sdiff', hue='trialType', hue_order=trialOrder, palette='Paired')
        # g.map_dataframe(sns.pointplot, x='trainDayThisStage', y='trialTypePEProb10sdiff', hue= 'subject', palette= subjPalette, alpha=0.04)
     
        #using lineplot bc easy to adjust alpha
        
        #hue=subject
        # g.map_dataframe(sns.lineplot, estimator= None, x='stage', y='trialTypePEProb10sdiff', hue= 'subject', palette= subjPalette, alpha=0.6, style='subject', dashes=False, markers=True)
        g.map_dataframe(sns.stripplot, x= 'stage', y='trialTypePEProb10sdiff', hue= 'subject', hue_order= subjectOrder, palette= subjPalette, alpha=0.6)

        
        
        #hue=trialType
        
        #now observations aren't continuous so i think lineplot looks weird
        #still would be great to have lines connecting observations?
        #but maybe strip is more appropriate
        # g.map_dataframe(sns.lineplot,  x= 'stage', y='trialTypePEProb10sdiff', hue= 'trialType', hue_order=trialOrder, palette= 'Paired', alpha=0.6, style='subject', dashes=False, markers=True)
        # g.map_dataframe(sns.lineplot, units='subject', estimator=None, x= 'stage', y='trialTypePEProb10sdiff', hue= 'trialType', hue_order=trialOrder, palette= 'Paired', alpha=0.6, style='subject', dashes=False, markers=True)

        


        g.fig.suptitle(virus+'- Pooled PE Probability difference score (laser trial probPE - no laser trial probPE)')
        g.set_ylabels('delta PE prob (laser-no laser trials)')
        g.set_xlabels('trainDayThisStage')       
        
           #manually set axes limits
        # g.set(xlim= (-0.5,dfPlot2.trainDayThisStage.max()+.5))   
        # g.set(ylim= (-1,1))   

        # g.add_legend()
        
        saveFigCustom(g, virus+'-PE Probability difference score laser_pooled_days', savePath)
        
    
    #%% --plots: PE Prob overall plots similar to above (non-diff)
    
    
       #make plots
    dfPlot= dfTidyOpto.copy()

    stagesToPlot= dfPlot.stage.unique()
    trialTypesToPlot= ['DStime', 'DStime_laser', 'NStime', 'NStime_laser']
    eventsToPlot= ['PEtime']

    
    #running fxn still to remove unused categories
    dfPlot= subsetData(dfPlot, stagesToPlot, trialTypesToPlot, eventsToPlot)

    
   #individual subject facet
    g= sns.relplot(data= dfPlot, kind='line', estimator=None, col='subject', col_wrap=3, x='trainDayThisStage', y='trialTypePEProb10s', hue='trialType', hue_order=trialOrder, style='stage', markers=True)
    # g.map(refline(y=0, linewidth=2, linestyle="-", color=None, clip_on=False))
    g.map(plt.axhline, y=0, color=".2", linewidth=3, dashes=(3,1), zorder=0)

    # g= sns.FacetGrid(data= dfPlot, row='stage', col='trialType')
    # g.map_dataframe(sns.lineplot, data= dfPlot, units='subject', estimator=None, x='trainDayThisStage', y='trialTypePEProb10s', hue='trialType', hue_order=trialOrder, style='subject', markers=True)


    for virus in dfPlot.virus.unique():
        dfPlot2= dfPlot.loc[dfPlot.virus==virus]
        
        #get rid of extra categories
        dfPlot2= subsetData(dfPlot2, stagesToPlot, trialTypesToPlot, eventsToPlot)
    

        #--bar plot with point plot of individual subj overlaid
        g= sns.catplot(data=dfPlot2, col='stage', row='trialType', kind='bar', dodge=False, x='trainDayThisStage', y='trialTypePEProb10s', hue='trialType', hue_order=trialOrder, palette='Paired')
        # g.map_dataframe(sns.pointplot, x='trainDayThisStage', y='trialTypePEProb10s', hue= 'subject', palette= subjPalette, alpha=0.04)
     
        #using lineplot bc easy to adjust alpha
        
        #hue=subject
        # g.map_dataframe(sns.lineplot, estimator= None, x='trainDayThisStage', y='trialTypePEProb10s', hue= 'subject', palette= subjPalette, alpha=0.6, style='subject', dashes=False, markers=True)
        
        #hue=trialType
        g.map_dataframe(sns.lineplot, units='subject', estimator= None, x='trainDayThisStage', y='trialTypePEProb10s', hue= 'trialType', hue_order=trialOrder, palette= 'Paired', alpha=0.6, style='subject', dashes=False, markers=True)

        g.fig.suptitle(virus+'- Daily PE Probability')
        g.set_ylabels('PE prob')
        g.set_xlabels('trainDayThisStage')       
        
        #overlay criteria line (facilitates comparison btwn subplots) #todo: could be no-laser baseline
        g.map(plt.axhline, y=criteriaDS, color=".2",  linewidth=3, dashes=(3, 1), zorder=0) 
        
           #manually set axes limits
        g.set(xlim= (-0.5,dfPlot2.trainDayThisStage.max()+.5))   
        g.set(ylim= (0,1))   

        # g.add_legend()
        
        saveFigCustom(g, virus+'- Daily PE Probability', savePath)
        
     #%% --plots: virus ind subjects; pooled PE latency by stage
    #was considering viz of individal subj means just to see diff subj + group mean, requires intermediate calculation tho
    # #TODO: difference score for latency?
    #   #subset data
    # dfPlot= dfTidyOpto.copy()

    # stagesToPlot= dfPlot.stage.unique()
    # trialTypesToPlot= ['DStime', 'DStime_laser', 'NStime', 'NStime_laser']
    # eventsToPlot= ['PEtime']

    
    # #running fxn still to remove unused categories
    # dfPlot= subsetData(dfPlot, stagesToPlot, trialTypesToPlot, eventsToPlot)


    # #% -- barplot + point (let's see if ind subjects differ in their means)
    
    # g= sns.FacetGrid(data= dfPlot, col='stage', row='virus')
    

    # #--bar plot with point plot of individual subj means overlaid
    # g.map_dataframe(sns.barplot, data= dfPlot, dodge=False, x='trialType', y='eventLatency', hue='trialType', hue_order=trialOrder, palette='Paired')
    
    # #     #just calc & show means for each subj
    # # dfPlot2= dfPlot.copy()
    # # dfPlot2['eventLatency']= dfPlot2.groupby(groupHierarchyTrialType).eventLatency.mean()
    # g.map_dataframe(sns.lineplot, data=dfPlot2, units='subject', estimator= None, x='trialType', y='eventLatency', hue= 'trialType', hue_order=trialOrder, palette= 'Paired', alpha=0.6, style='subject', dashes=False, markers=True)
 
    
 
    
    
    #%% --plots: pooled between subj by virus; pooled first PE latency distribution by stage
       #subset data
    dfPlot= dfTidyOpto.copy()

    stagesToPlot= dfPlot.stage.unique()
    trialTypesToPlot= ['DStime', 'DStime_laser', 'NStime', 'NStime_laser']
    eventsToPlot= ['PEtime']

    
    #running fxn still to remove unused categories
    dfPlot= subsetData(dfPlot, stagesToPlot, trialTypesToPlot, eventsToPlot)


    for virus in dfPlot.virus.unique():
        
        dfPlot2= dfPlot.loc[dfPlot.virus==virus]
        
        dfPlot2= subsetData(dfPlot2, stagesToPlot, trialTypesToPlot, eventsToPlot)
        

    
        #--ecdf plot
        g= sns.displot(data=dfPlot2, kind='ecdf', col='stage',  x='eventLatency', hue='trialType', hue_order=trialOrder, palette='Paired')
    
        g.fig.suptitle(virus+'- Pooled PE latency')
        g.set_ylabels('PE latency')
        g.set_xlabels('trainDayThisStage')       
        
        #overlay laser line (facilitates comparison btwn subplots) 
        g.map(plt.axvline, x=1, color=".2",  linewidth=3, dashes=(3, 1), zorder=0) 
        
           #manually set axes limits
        # g.set(xlim= (-0.5,dfPlot2.trainDayThisStage.max()+.5))   
        # g.set(ylim= (0,1))   
    
        # g.add_legend()
        
        saveFigCustom(g, virus+'-betweenSubj- Pooled PE latency', savePath)
            
        
        g.fig.suptitle(virus+'- Pooled PE latency')
        g.set_ylabels('PE latency')
        g.set_xlabels('trainDayThisStage')       
        
        #overlay laser line (facilitates comparison btwn subplots) 
        g.map(plt.axvline, x=1, color=".2",  linewidth=3, dashes=(3, 1), zorder=0) 
        
        saveFigCustom(g, virus+'- Pooled PE Probability- Distribution', savePath)
        
        
        
        #--bar plot with individual subj lines overlaid
        g= sns.FacetGrid(dfPlot2, col= 'stage')
        g.map_dataframe(sns.barplot, data=dfPlot2, dodge=False, x='trialType', y='eventLatency', hue='trialType', hue_order=trialOrder, palette='Paired')
        g.map_dataframe(sns.lineplot, data=dfPlot2, x='trialType', y='eventLatency', hue= 'subject', hue_order= subjectOrder, alpha=0.6, style='subject', dashes=False, markers=True)
        
        
        g.fig.suptitle(virus+'- Pooled PE latency')
        g.set_ylabels('PE latency')
        g.set_xlabels('trainDayThisStage')  
        saveFigCustom(g, virus+'- Pooled PE Probability- Mean', savePath)

    
    #%%-- Plots: individual subjs; daily first PE latency distribution 
        
        
    dfPlot= dfTidyOpto.copy()
    
    #subset with customFunction
    stagesToPlot= dfTidyOpto.stage.unique()
    trialTypesToPlot= ['DStime','DStime_laser','NStime','NStime_laser','Pre-Cue']
    eventsToPlot= ['PEtime']
    dfPlot= subsetData(dfPlot, stagesToPlot, trialTypesToPlot, eventsToPlot)
    
    # #subset data at correct level of observation for variable    
    # subset to first event per trial
    groupHierarchy= groupHierarchyEventType
    dfPlot= subsetLevelObs(dfPlot, groupHierarchy)
    
    #--Plot evolution of PElatency- Individual subj
    for subject in dfPlot.subject.unique():
        
        dfPlot2= dfPlot.loc[dfPlot.subject==subject,:].copy()
        
        dfPlot2= subsetData(dfPlot2, stagesToPlot, trialTypesToPlot, eventsToPlot)
        

        g = sns.FacetGrid(dfPlot2, col= 'stage', row="trainDayThisStage")
        
        #       # kde + hist count
        # g.map_dataframe(sns.histplot, data=dfPlot2, bins=20, common_norm=False, element='step', alpha=0.4, x="eventLatency", hue='trialType', hue_order=trialOrder)
        # g.map_dataframe(sns.kdeplot, data=dfPlot2, common_norm=False,  linewidth=2, x="eventLatency", hue='trialType', hue_order=trialOrder)
        

        #ecdf
        g.map_dataframe(sns.ecdfplot, data=dfPlot2, x="eventLatency", hue='trialType', hue_order=trialOrder)


        g.map(plt.axvline, x=1, color=".2",  linewidth=3, dashes=(3, 1), zorder=0)         

        
        
    
        
        g.fig.suptitle(str(subject)+'- Daily PE latency distribution')
        g.set_xlabels('First PE latency')       
        
      
           #manually set axes limits
        g.set(xlim= (0,10))   
            
        saveFigCustom(g, str(subject)+'- Daily distribution PE latency', savePath)

    

      #%% #For lick+laser, plot trialType counts
      #since laser delivery is contingent on animal's licking, should check to see how many trials they are actually getting laser
    try:
        #subset data and save as intermediate variable dfGroup
        dfGroup= dfTidyOpto.copy()
        #retain only trials with PE+lick for comparison
        dfGroup.loc[dfGroup.laserDur=='Lick',:]= dfGroup.loc[(dfGroup.laserDur=='Lick') & (dfGroup.trialOutcomeBeh10s=='PE+lick')].copy()
    
        #get count of each trialType by subject and trainDayThisStage
        dfPlot= dfGroup.loc[(dfGroup.laserDur=='Lick') & ((dfGroup.eventType=='NStime') | (dfGroup.eventType=='DStime'))].groupby(['subject','trainDayThisStage','trialType'])['eventTime'].count().reset_index()
        
        
        #Plot count of trial types for each session
        g= sns.relplot(data=dfPlot, col='subject', col_wrap=4, x='trainDayThisStage', y='eventTime', hue='trialType', hue_order=trialOrder, kind='line')
                        # facet_kws={'sharey': False, 'sharex': True})
        g.fig.subplots_adjust(top=0.9)  # adjust the figure for title
        g.fig.suptitle('Total trial type count across LICK+laser sessions')
        g.set_ylabels('# of events')
        g.set_ylabels('session')
        
        #total count of each trial type across all sessions for each subject
        sns.set_palette('Paired')  # good for comparing two groups (laser on vs off)
        
        g= sns.catplot(data=dfPlot, x='subject', y='eventTime', hue='trialType', hue_order=trialOrder, kind='bar')
                        # facet_kws={'sharey': False, 'sharex': True})
        g.fig.subplots_adjust(top=0.9)  # adjust the figure for title
        g.fig.suptitle('Total trial type count across LICK+laser sessions')
        g.set_ylabels('Total trial count (lick+laser sessions)')
        g.set_xlabels('Subject')
        
        #Use trialLick10ss to get # of licks per trial by type, then plot distribution by trial type
        
        dfPlot = dfGroup[(dfGroup.laserDur=='Lick')].copy()
            #transform keeps original index?
        lickCount=dfPlot.groupby(['fileID','trialID','trialType'])['trialLick10s'].transform('count')
    
        #aggregated measure, but trialIDs repeat, so just restrict to first one   
        trialAgg= dfPlot.groupby(['fileID','trialID','trialType'])['trialID'].cumcount()==0
        dfPlot= dfPlot.loc[trialAgg]
        
        g= sns.displot(data=dfPlot, x=lickCount, hue='trialType', hue_order=trialOrder, kind='hist', stat="density", common_norm=False, kde=True, multiple='dodge')
        g.fig.subplots_adjust(top=0.9)  # adjust the figure for title
        g.fig.suptitle('Lick count by trial type: LICK+laser sessions')
        g.set_ylabels('Lick count (lick+laser sessions)')
        
    
        #check inter-lick interval
        #All subj distribution of ILI (inter-lick interval)
        #only include trialLick10s~=nan
        dfPlot = dfGroup[dfGroup.trialLick10s.notnull()].copy()
        #calculate ILI by taking diff() of latencies
        ili= dfPlot.groupby(['fileID','trialID','trialType'])['eventLatency'].diff()
    
        #bar- all subj
        g= sns.catplot(data=dfPlot, y=ili, x='trialType',  kind='bar', row='virus', order=trialOrder)
        g.fig.subplots_adjust(top=0.9)  # adjust the figure for title
        g.fig.suptitle('ILI by trial type; LICK+Laser; all subj')
        g.set_ylabels('ILI (s)')
        g.set(ylim=(0,0.5))
        
    except:
        print('lick+laser exception')
    
    
    
    #%% Evolution across days/stages: PE prob & latency
        
    sns.set_palette('Paired')

    
    #--Training: DS PE Prob+latency in 1 fig
    
    dfPlot= dfTidyOpto.copy()
    
    #subset with customFunction
    stagesToPlot= dfPlot.stage.unique()
    trialTypesToPlot= dfPlot.trialType.unique()
    eventsToPlot= ['PEtime']
    dfPlot= subsetData(dfPlot, stagesToPlot, trialTypesToPlot, eventsToPlot)
    
    
    #subset data at correct level of observation for variable    
    groupHierarchy= groupHierarchyTrialType
    dfPlot= subsetLevelObs(dfPlot, groupHierarchy)
    
    
    #subset data further to correct level of observation for variable
    dfPlot2= subsetLevelObs(dfPlot, groupHierarchyEventType)
    
    #subset with customFunction
    stagesToPlot= dfPlot2.stage.unique()
    trialTypesToPlot= ['DStime']
    eventsToPlot= ['PEtime']
    dfPlot2= subsetData(dfPlot2, stagesToPlot, trialTypesToPlot, eventsToPlot)
    
    #subset data further to correct level of observation
    groupHierarchy= groupHierarchyEventType
    dfPlot2= subsetLevelObs(dfPlot2, groupHierarchy)
    
    # #make figure
    # f, ax= plt.subplots(2,1)
    
    # g= sns.lineplot(ax=ax[0], data=dfPlot, x='trainDayThisStage', y='trialTypeOutcomeBehProb10s', hue='subject', style='stage')
    # ax[0].axhline(y=criteriaDS, color=".2", linewidth=3, dashes=(3, 1), zorder=0)
    # g.set(title=('Training: 10s PE probability, DS trials'))
    # g.set( ylabel='PE probability (10s)')
    
    # g= sns.lineplot(ax=ax[1], data=dfPlot2, x='trainDayThisStage', y='eventLatency', hue='subject', style='trialType')
    # g.set(title=('Training: PE latency, DS trials'))
    # g.set( ylabel='latency to first PE (s)')
        

    sns.set_palette('Paired')
    
    # #TODO: was trying to
    # #make darker variant of this for mean?
    # paletteOriginal= sns.color_palette()
    
    # paletteMean= []
    
    # for r,g,b in paletteOriginal: 
    #     color= (r*.05,g,b)
        


    #plot prob by trialType by stage
    for virus in dfPlot.virus.unique():
        dfPlot2= dfPlot.loc[dfPlot.virus==virus].copy()
        
        #remove unused stages (diff opto groups should have diff laser params) to keep sns from making empty facets
        dfPlot2.stage= dfPlot2.stage.cat.remove_unused_categories().copy()
        
        #mean lines w individual subj
        g= sns.FacetGrid(data=dfPlot2, col='stage')
        
        g.map_dataframe(sns.lineplot, data=dfPlot2, x='trainDayThisStage', y='trialTypeOutcomeBehProb10s', hue='trialType', hue_order=trialOrder)
        g.map_dataframe(sns.lineplot, data=dfPlot2, units='subject', estimator=None, alpha=0.6, x='trainDayThisStage', y='trialTypeOutcomeBehProb10s', hue='trialType', hue_order=trialOrder, style='subject', dashes=False, markers=True)

        g.map(plt.axhline, y=criteriaDS, color=".2",  linewidth=3, dashes=(3, 1), zorder=0) 


        # g= sns.relplot(data=dfPlot2, kind='line', row='stage', x='trainDayThisStage', y='trialTypeOutcomeBehProb10s', hue='trialType', hue_order=trialOrder)
       
        # g.map_dataframe(sns.lineplot, data=dfPlot2, units='subject', estimator=None, alpha=0.6, x='trainDayThisStage', y='trialTypeOutcomeBehProb10s', hue='trialType', hue_order=trialOrder, style='subject', dashes=False, markers=True)
        
        # g= sns.catplot(data=dfPlot2, col='subject', row='stage', kind='point', alpha=0.6, x='trainDayThisStage', y='trialTypeOutcomeBehProb10s', hue='trialType', hue_order=trialOrder)

        # g.map_dataframe(sns.scatterplot, data=dfPlot2, alpha=0.6, x='trainDayThisStage', y='trialTypeOutcomeBehProb10s', hue='trialType', hue_order=trialOrder, style='subject', markers=True)
        
        g.fig.suptitle(virus+'-Opto-PE prob across laser days')

        saveFigCustom(g, virus+'- Daily PEprob by stage', savePath)




    #%% Plot individual subject First lick latencies (time from cue or trialEnd if ITI events)
    # # should represent "baseline" behavior  without laser
          
    # #trial-based, ignoring ITI
    # # dfPlot = dfTidyOpto[(dfTidyOpto.trialID >= 0) & (dfTidyOpto.laserDur=="Off")].copy()
    # #trial-based, including ITI
    # dfPlot = dfTidyOpto[(dfTidyOpto.laserDur=="off")].copy()

    # #All subj distribution of ILI (inter-lick interval)
    # #only include first trialLick10s ==0
    # dfPlot = dfPlot[dfPlot.trialLick10s==0].copy()


    # #bar- all subj
    # #median here takes awhile
    # g= sns.catplot(data=dfPlot, y='eventLatency', x='trialType', row='virus', col='laserDur', kind='bar', order=trialOrder)
    # g.fig.subplots_adjust(top=0.9)  # adjust the figure for title
    # g.fig.suptitle('first lick latencies by trial type; laser OFF; all subj')
    # g.set_ylabels('lick latency from epoch start (s)')

    
    # # #hist- all subj
    # # ili= ili.astype('float') #allows KDE, but kde here takes awhile
    # # g= sns.displot(data=dfPlot, x=ili, hue='trialType',  kind='hist', stat="density", common_norm=False, kde=True, multiple='layer', hue_order=np.sort(dfPlot.trialType.unique()))
    # # g.fig.subplots_adjust(top=0.9)  # adjust the figure for title
    # # g.fig.suptitle('ILI by trial type; laser OFF; all subj')
    # # g.set_xlabels('ILI (s)')
    # # g.set(xlim=(0,1))
    
    # #box- all subj
    # g= sns.catplot(data=dfPlot, y='eventLatency', x='trialType',  kind='box', order=trialOrder)
    # g.fig.subplots_adjust(top=0.9)  # adjust the figure for title
    # g.fig.suptitle('First Lick latencies by trial type; laser OFF; all subj')
    # g.set_ylabels('lick latency from epoch start (s)')

    
    # #ecdf- all subj'[]
    # g= sns.displot(data=dfPlot, x='eventLatency', hue='trialType',  kind='ecdf', hue_order=trialOrder)
    # g.fig.subplots_adjust(top=0.9)  # adjust the figure for title
    # g.fig.suptitle('First Lick latencies by trial type; laser OFF; all subj')
    # g.set_xlabels('lick latency from epoch start (s)')

    
    # #Individual distribution of ILI (inter-lick interval)
    # #only include trialLick10s~=nan 
    # #bar- individual subj
    # g= sns.catplot(data=dfPlot, y='eventLatency', x='subject', hue='trialType',  kind='bar', hue_order=trialOrder)
    # g.fig.subplots_adjust(top=0.9)  # adjust the figure for title
    # g.fig.suptitle('First Lick latencies by trial type; laser OFF; individual subj')
    # g.set_ylabels('lick latency from epoch start (s)')

        
   # %% Effect of cue+laser on current trial PE latency- laserDur included in stage
        
   #select data corresponding to first PE from valid trials
    # dfPlot = dfTidyOpto[(dfTidyOpto.trialType!='ITI') & (dfTidyOpto.trialPE10s == 0)].copy()
    
    
    dfPlot= dfTidyOpto.copy()
    
    #subset with customFunction
    stagesToPlot= dfPlot.stage.unique() #['5']
    trialTypesToPlot= dfPlot.trialType.unique()[ dfPlot.trialType.unique()!='ITI']
    eventsToPlot= ['PEtime']
    dfPlot= subsetData(dfPlot, stagesToPlot, trialTypesToPlot, eventsToPlot)
    
    # #subset data at correct level of observation for variable    
    # subset to first event per trial
    groupHierarchy= groupHierarchyEventType
    dfPlot= subsetLevelObs(dfPlot, groupHierarchy)

    # # PE latency: virus x laserDur
    # g = sns.displot(data=dfPlot, x='eventLatency', hue='trialType',
    #                 col='laserDur', row='virus', kind='ecdf', hue_order= trialOrder)
    # g.fig.suptitle('First PE latency by trial type')
    # g.set_ylabels('First PE latency from epoch start (s)')
    
    # #PE latency: virus individual subj
    # g=sns.catplot(data=dfPlot,y='eventLatency',hue='trialType', x='subject', kind='bar', hue_order=trialOrder)
    # g.fig.suptitle('First PE latency by trial type')
    # g.set_ylabels('First PE latency from epoch start (s)')
    
    #   #PE latency:  individual subj CUE+laser
    # g=sns.displot(data=dfPlot.loc[dfPlot.laserDur=='10'], col='subject', col_wrap=4, x='eventLatency',hue='trialType', kind='ecdf', hue_order=trialOrder)
    # g.fig.suptitle('First PE latency by trial type; laser + CUE')
    # g.set_ylabels('First PE latency from epoch start (s)')
    
    # #PE latency: virus x laser dur box
    # g=sns.catplot(data=dfPlot,y='eventLatency', row='virus', col='laserDur', hue='subject', x='trialType', style='sex', kind='point')
    # g.fig.suptitle('First PE latency by trial type')
    # g.set_ylabels('First PE latency from epoch start (s)')
    
    # boxplots for each trial type with individual data points
    #individual subj facet
    # g = sns.FacetGrid(data=dfPlot, col='subject',col_wrap=3)
    # g.fig.suptitle('PE latency by trialType; laser + CUE')
    # g.map_dataframe(sns.boxplot, x='stage', y='eventLatency', hue='trialType', hue_order=trialOrder, palette='Paired')
    # g.map_dataframe(sns.stripplot, x='stage', y='eventLatency', hue='trialType', hue_order=trialOrder, palette='Paired', dodge='True', size=4, alpha=0.2, edgecolor='gray', linewidth=1)
    # g.set_axis_labels( 'stage', 'latency to first PE (10s)')
    # saveFigCustom(g, 'opto_individual_peLatency_10s_box', savePath)
    
    # g = sns.FacetGrid(data=dfPlot, col='subject',col_wrap=3)
    # g.fig.suptitle('PE latency by trialType; laser + CUE')
    # g.map_dataframe(sns.barplot, ci=68, x='stage', y='eventLatency', hue='trialType', hue_order=trialOrder, palette='Paired')
    # g.map_dataframe(sns.stripplot, x='stage', y='eventLatency', hue='trialType', hue_order=trialOrder, palette='Paired', dodge='True', size=4, alpha=0.2, edgecolor='gray', linewidth=1)
    # g.set_axis_labels( 'laser duration', 'latency to first PE (10s)')
    # saveFigCustom(g, 'opto_individual_peLatency_10s_bar', savePath)
    
    #virus facet
    # g = sns.FacetGrid(data=dfPlot, row='virus')
    # g.fig.suptitle('PE latency by trialType; laser + CUE')
    # g.map_dataframe(sns.boxplot, x='stage', y='eventLatency', hue='trialType', hue_order=trialOrder, palette='Paired')
    # g.map_dataframe(sns.stripplot, x='stage', y='eventLatency', hue='trialType', hue_order=trialOrder, palette='Paired', dodge='True', size=4, alpha=0.2, edgecolor='gray', linewidth=1)
    # g.set_axis_labels( 'laser duration', 'latency to first PE (10s)')
    # saveFigCustom(g, 'opto_virus_peLatency_10s_box', savePath)
    
    # barplots for each trial type with individual data points 
    #individual subj facet
    g = sns.FacetGrid(data=dfPlot, col='subject',col_wrap=3)
    g.fig.suptitle('PE latency by trialType; laser + CUE')
    g.map_dataframe(sns.barplot, ci=68, x='stage', y='eventLatency', hue='trialType', hue_order=trialOrder, palette='Paired')
    g.map_dataframe(sns.stripplot, x='stage', y='eventLatency', hue='trialType', hue_order=trialOrder, palette='Paired', dodge='True', size=4, alpha=0.2, edgecolor='gray', linewidth=1)
    g.set_axis_labels( 'laser duration', 'latency to first PE (10s)')
    saveFigCustom(g, 'opto_individual_peLatency_10s_bar', savePath)
    
    #virus facet
    g = sns.FacetGrid(data=dfPlot, row='virus')
    g.fig.suptitle('PE latency by trialType; laser + CUE')
    g.map_dataframe(sns.barplot, ci=68, x='stage', y='eventLatency', hue='trialType', hue_order=trialOrder, palette='Paired')
    g.map_dataframe(sns.stripplot, x='stage', y='eventLatency', hue='trialType', hue_order=trialOrder, palette='Paired', dodge='True', size=4, alpha=0.2, edgecolor='gray', linewidth=1)
    g.set_axis_labels( 'laser duration', 'latency to first PE (10s)')
    saveFigCustom(g, 'opto_virus_peLatency_10s_bar', savePath)
    
    #virus + sex facet
    g = sns.FacetGrid(data=dfPlot, row='virus', col='sex')
    g.fig.suptitle('PE latency by trialType; laser + CUE')
    g.map_dataframe(sns.barplot, ci=68, x='stage', y='eventLatency', hue='trialType', hue_order=trialOrder, palette='Paired')
    g.map_dataframe(sns.stripplot, x='stage', y='eventLatency', hue='trialType', hue_order=trialOrder, palette='Paired', dodge='True', size=4, alpha=0.2, edgecolor='gray', linewidth=1)
    g.set_axis_labels( 'laser duration', 'latency to first PE (10s)')
    saveFigCustom(g, 'opto_virus+sex_peLatency_10s_bar', savePath)
    
    # ECDFs
    #vius facet
    g = sns.displot(data=dfPlot, row='virus', col='stage', x='eventLatency', hue='trialType', hue_order=trialOrder, palette='Paired', kind='ecdf')
    g.fig.suptitle('PE latency by trialType; laser + CUE')
    g.set_xlabels('latency to first PE (10s)')
    saveFigCustom(g, 'opto_virus_peLatency_10s_ecdf', savePath)    
    
    # # %% Old Effect of cue+laser on current trial PE latency
        
    # #select data corresponding to first PE from valid trials
    # dfPlot = dfTidyOpto[(dfTidyOpto.trialType!='ITI') & (dfTidyOpto.trialPE10s == 0)].copy()
    
    # # # PE latency: virus x laserDur
    # # g = sns.displot(data=dfPlot, x='eventLatency', hue='trialType',
    # #                 col='laserDur', row='virus', kind='ecdf', hue_order= trialOrder)
    # # g.fig.suptitle('First PE latency by trial type')
    # # g.set_ylabels('First PE latency from epoch start (s)')
    
    # # #PE latency: virus individual subj
    # # g=sns.catplot(data=dfPlot,y='eventLatency',hue='trialType', x='subject', kind='bar', hue_order=trialOrder)
    # # g.fig.suptitle('First PE latency by trial type')
    # # g.set_ylabels('First PE latency from epoch start (s)')
    
    # #   #PE latency:  individual subj CUE+laser
    # # g=sns.displot(data=dfPlot.loc[dfPlot.laserDur=='10'], col='subject', col_wrap=4, x='eventLatency',hue='trialType', kind='ecdf', hue_order=trialOrder)
    # # g.fig.suptitle('First PE latency by trial type; laser + CUE')
    # # g.set_ylabels('First PE latency from epoch start (s)')
    
    # # #PE latency: virus x laser dur box
    # # g=sns.catplot(data=dfPlot,y='eventLatency', row='virus', col='laserDur', hue='subject', x='trialType', style='sex', kind='point')
    # # g.fig.suptitle('First PE latency by trial type')
    # # g.set_ylabels('First PE latency from epoch start (s)')
    
    # # boxplots for each trial type with individual data points
    # #individual subj facet
    # g = sns.FacetGrid(data=dfPlot, col='subject',col_wrap=3)
    # g.fig.suptitle('PE latency by trialType; laser + CUE')
    # g.map_dataframe(sns.boxplot, x='laserDur', y='eventLatency', hue='trialType', hue_order=trialOrder, palette='Paired')
    # g.map_dataframe(sns.stripplot, x='laserDur', y='eventLatency', hue='trialType', hue_order=trialOrder, palette='Paired', dodge='True', size=4, alpha=0.2, edgecolor='gray', linewidth=1)
    # g.set_axis_labels( 'laser duration', 'latency to first PE (10s)')
    # saveFigCustom(g, 'opto_individual_peLatency_10s_box')
    
    # g = sns.FacetGrid(data=dfPlot, col='subject',col_wrap=3)
    # g.fig.suptitle('PE latency by trialType; laser + CUE')
    # g.map_dataframe(sns.barplot, ci=68, x='laserDur', y='eventLatency', hue='trialType', hue_order=trialOrder, palette='Paired')
    # g.map_dataframe(sns.stripplot, x='laserDur', y='eventLatency', hue='trialType', hue_order=trialOrder, palette='Paired', dodge='True', size=4, alpha=0.2, edgecolor='gray', linewidth=1)
    # g.set_axis_labels( 'laser duration', 'latency to first PE (10s)')
    # saveFigCustom(g, 'opto_individual_peLatency_10s_bar')
    
    # #virus facet
    # g = sns.FacetGrid(data=dfPlot, row='virus')
    # g.fig.suptitle('PE latency by trialType; laser + CUE')
    # g.map_dataframe(sns.boxplot, x='laserDur', y='eventLatency', hue='trialType', hue_order=trialOrder, palette='Paired')
    # g.map_dataframe(sns.stripplot, x='laserDur', y='eventLatency', hue='trialType', hue_order=trialOrder, palette='Paired', dodge='True', size=4, alpha=0.2, edgecolor='gray', linewidth=1)
    # g.set_axis_labels( 'laser duration', 'latency to first PE (10s)')
    # saveFigCustom(g, 'opto_virus_peLatency_10s_box')
    
    # # barplots for each trial type with individual data points 
    # #individual subj facet
    # g = sns.FacetGrid(data=dfPlot, col='subject',col_wrap=3)
    # g.fig.suptitle('PE latency by trialType; laser + CUE')
    # g.map_dataframe(sns.barplot, ci=68, x='laserDur', y='eventLatency', hue='trialType', hue_order=trialOrder, palette='Paired')
    # g.map_dataframe(sns.stripplot, x='laserDur', y='eventLatency', hue='trialType', hue_order=trialOrder, palette='Paired', dodge='True', size=4, alpha=0.2, edgecolor='gray', linewidth=1)
    # g.set_axis_labels( 'laser duration', 'latency to first PE (10s)')
    # saveFigCustom(g, 'opto_individual_peLatency_10s_bar')
    
    # #virus facet
    # g = sns.FacetGrid(data=dfPlot, row='virus')
    # g.fig.suptitle('PE latency by trialType; laser + CUE')
    # g.map_dataframe(sns.barplot, ci=68, x='laserDur', y='eventLatency', hue='trialType', hue_order=trialOrder, palette='Paired')
    # g.map_dataframe(sns.stripplot, x='laserDur', y='eventLatency', hue='trialType', hue_order=trialOrder, palette='Paired', dodge='True', size=4, alpha=0.2, edgecolor='gray', linewidth=1)
    # g.set_axis_labels( 'laser duration', 'latency to first PE (10s)')
    # saveFigCustom(g, 'opto_virus_peLatency_10s_bar')
    
    # #virus + sex facet
    # g = sns.FacetGrid(data=dfPlot, row='virus', col='sex')
    # g.fig.suptitle('PE latency by trialType; laser + CUE')
    # g.map_dataframe(sns.barplot, ci=68, x='laserDur', y='eventLatency', hue='trialType', hue_order=trialOrder, palette='Paired')
    # g.map_dataframe(sns.stripplot, x='laserDur', y='eventLatency', hue='trialType', hue_order=trialOrder, palette='Paired', dodge='True', size=4, alpha=0.2, edgecolor='gray', linewidth=1)
    # g.set_axis_labels( 'laser duration', 'latency to first PE (10s)')
    # saveFigCustom(g, 'opto_virus+sex_peLatency_10s_bar')
    
    # # ECDFs
    # #vius facet
    # g = sns.displot(data=dfPlot, row='virus', col='laserDur', x='eventLatency', hue='trialType', hue_order=trialOrder, palette='Paired', kind='ecdf')
    # g.fig.suptitle('PE latency by trialType; laser + CUE')
    # g.set_xlabels('latency to first PE (10s)')
    # saveFigCustom(g, 'opto_virus_peLatency_10s_ecdf')    
    

    #%% Calculate PE probability of each trial type. This is normalized so is more informative than count of trials. 
    
   # #  # #TODO: clean up and move higher to prelim analysis section
    
   # #  # # outcomeProb= dfPlot[dfPlot.trialOutcomeBeh10s=='PE'].groupby(['fileID','trialID'])['trialOutcomeBeh10s'].count().index

    
   # #  # #calculate Probortion of trials with PE out of all trials for each trial type
   # #  # #can use nunique() to get count of unique trialIDs with specific PE outcome per file
   # #  # #given this, can calculate Probortion as #PE/#PE+#noPE
   
   # #  # #subset data and save as intermediate variable dfGroup
   # #  # dfGroup= dfTidyOpto.copy()
   # #  # #for Lick+laser sessions, retain only trials with PE+lick for comparison
   # #  # dfGroup.loc[dfGroup.laserDur=='Lick',:]= dfGroup.loc[(dfGroup.laserDur=='Lick') & (dfGroup.trialOutcomeBeh10s=='PE+lick')].copy()
   
   # #  # dfPlot= dfGroup.copy() 
    
   # #  # #excluded trials from lick+laser sessions are all nan. don't include
   # #  # outcomes= dfTidyOpto.loc[dfTidyOpto.trialOutcomeBeh10s.notnull()].trialOutcomeBeh10s.unique()
    
   # #  # #TODO: optimize this- combine outcomes here into one variable
   # #  # #using apply() might help? or pivot?
    
   # #  # # tester[outcomes]= dfPlot[(dfPlot.trialOutcomeBeh10s==outcomes)].reset_index().groupby(
   # #  # #     ['fileID','trialType','trialOutcomeBeh10s'])['trialID'].nunique()
    
   # #  # test1= dfPlot[(dfPlot.trialOutcomeBeh10s=='PE')].reset_index().groupby(['fileID','trialType','trialOutcomeBeh10s'])['trialID'].nunique()
   # #  # test1.name= 'PE'
   # #  # test2= dfPlot[dfPlot.trialOutcomeBeh10s=='noPE'].reset_index().groupby(['fileID','trialType','trialOutcomeBeh10s'])['trialID'].nunique()
   # #  # test2.name= 'noPE'    
    
   # #  # test5= dfPlot[(dfPlot.trialOutcomeBeh10s=='PE+lick')].reset_index().groupby(['fileID','trialType','trialOutcomeBeh10s'])['trialID'].nunique()
   # #  # test5.name= 'PE+lick'
   # #  # test8= dfPlot[(dfPlot.trialOutcomeBeh10s=='noPE+lick')].reset_index().groupby(['fileID','trialType','trialOutcomeBeh10s'])['trialID'].nunique()
   # #  # test8.name= 'noPE+lick'
 
           
   # #  # ##num of unique trials per trial type per session, but still cant sum
   # #  # test6= pd.concat((test1,test2,test5,test8),ignore_index=False,axis=1)
    
   # #  # ##reset index and groupby trialType so we can sum across columns
   # #  # test7= test6.reset_index().groupby(['fileID','trialType'])[outcomes].sum()
 
   # #  # ##calculate probability for each trial type: num trials/total num trials
   # #  # outcomeProb= test7.divide(test7.sum(axis=1),axis=0)
    
   # #  # #melt() into single column w label
   # #  # test8= outcomeProb.reset_index().melt(id_vars=['fileID','trialType'],var_name='trialOutcomeBeh10s',value_name='outcomeProbFile')
    
   # #  # #assign back to df by merging
   # #  # #TODO: can probably be optimized. if this section is run more than once will get errors due to assignment back to dfTidyOpto
   # #  # # dfTidyOpto.reset_index(inplace=True) #reset index so eventID index is kept
    
   # #  # dfTidyOpto= dfTidyOpto.reset_index().merge(test8,'left', on=['fileID','trialType','trialOutcomeBeh10s']).copy()
    
   # #  # dfTidyOpto.loc[:,'outcomeProbFile']= test8.outcomeProbFile
    
         
   # #  #subset data and save as intermediate variable dfGroup
   # #  dfGroup= dfTidyOpto.copy()
     
   # #  #select data
   # #  #all trialTypes excluding ITI     
   # #  dfPlot = dfGroup[(dfGroup.trialType != 'ITI')].copy()
     
   # #  #get only PE outcomes
   # #  # dfPlot.reset_index(inplace=True)
   # #  dfPlot= dfPlot.loc[(dfPlot.trialOutcomeBeh10s=='PE') | (dfPlot.trialOutcomeBeh10s=='PE+lick')].copy()
     
   # #  #since we calculated aggregated proportion across all trials in session,
   # #  #take only first index. Otherwise repeated observations are redundant
   # #  dfPlot= dfPlot.groupby(['fileID','trialType','trialOutcomeBeh10s']).first().copy()
     
     
   # #  #sum together both PE and PE+lick for total overall PE prob
   # #  # dfPlot['outcomeProbFile']= dfPlot.groupby(['fileID'])['outcomeProbFile'].sum().copy()
     
   # #  dfPlot['trialTypePEProb10s']= dfPlot.groupby(['fileID','trialType'])['outcomeProbFile10s'].sum().copy()
    
   # #  #get an aggregated x axis for files per subject
   # #  fileAgg= dfPlot.reset_index().groupby(['subject','fileID','trialType']).cumcount().copy()==0
     
   # #  #since grouping PE and PE+lick, we still have redundant observations
   # #  #retain only 1 per trial type per file
   # #  dfPlot= dfPlot.reset_index().loc[fileAgg]
    
   # #  #% visualize peProb
    
    
   # #  # #subset data and save as intermediate variable dfGroup
   # #  # dfGroup= dfTidyOpto.copy()
   # #  # #for Lick+laser sessions, retain only trials with PE+lick for comparison
   # #  # dfGroup.loc[dfGroup.laserDur=='Lick',:]= dfGroup.loc[(dfGroup.laserDur=='Lick') & (dfGroup.trialOutcomeBeh10s=='PE+lick')].copy()
   
    
   # #  # #select data     
   # #  # dfPlot = dfTidyOpto[(dfGroup.trialType !='ITI')].copy()
   # #  #Plot probability of PE by trialType 
    
   # #  # #get only PE outcomes
   # #  # # dfPlot.reset_index(inplace=True)
   # #  # dfPlot= dfPlot.loc[(dfPlot.trialOutcomeBeh10s=='PE') | (dfPlot.trialOutcomeBeh10s=='PE+lick')].copy()
    
   # #  # #since we calculated aggregated probability across all trials in session,
   # #  # #take only first index. Otherwise repeated observations are redundant
   # #  # dfPlot= dfPlot.groupby(['fileID','trialType','trialOutcomeBeh10s']).first().copy()
    
    
   # #  # #sum together both PE and PE+lick for total PE prob
   # #  # # dfPlot['outcomeProbFile']= dfPlot.groupby(['fileID'])['outcomeProbFile'].sum().copy()
    
   # #  # dfPlot['trialTypePEProb10s']= dfPlot.groupby(['fileID','trialType'])['outcomeProbFile'].sum().copy()

   # #  # #get an aggregated x axis for files per subject
   # #  # fileAgg= dfPlot.reset_index().groupby(['subject','fileID','trialType']).cumcount().copy()==0
    
   # #  # #since grouping PE and PE+lick, we still have redundant observations
   # #  # #retain only 1 per trial type per file
   # #  # dfPlot= dfPlot.reset_index().loc[fileAgg]

   # # # #Plot
   # # #  #one line per per trialType per subj would be ideal. In subplots
   # # #  #manual control here of facetgrid and titles (i). 
   # # #  #Manual:
   # # #  sns.set_palette('tab20')
   # # #  g = sns.FacetGrid(dfPlot, col='subject', hue='trialType', hue_order=trialOrder, col_wrap=4)

   # # #  # Add the line over the area with the plot function
   # # #  g = g.map(plt.plot, 'fileID', 'trialTypePEProb10s')
    
   # # #  # Control the title of each facet
   # # #  g = g.set_titles("{col_name}")
     
   # # #  # Add a title for the whole plot
   # # #  plt.subplots_adjust(top=0.9)
   # # #  g = g.fig.suptitle('Evolution of the trialTypePEProb10s in subjects by trialType')
    
     
   # # #  #same with relplot:
   # # #  g= sns.relplot(data=dfPlot, x='fileID', y='trialTypePEProb10s', col='subject', col_wrap=4, hue='trialType', hue_order=trialOrder, kind='line')
   # # #  # g.map(plt.axhline, y=0.6, color=".7", dashes=(2, 1), zorder=0)
   # # #  g.set_titles('{col_name}')
   # # #  g.fig.suptitle('Evolution of the trialTypePEProb10s in subjects by trialType')
   # # #  g.tight_layout(w_pad=0)
    
   # #  # #plot by laserDur
   # #  # g= sns.relplot(data=dfPlot, x='trainDayThisStage', y='trialTypePEProb10s', col='subject', col_wrap=4, hue='trialType', hue_order=trialOrder, style='laserDur', kind='line')
   # #  # # g.map(plt.axhline, y=0.6, color=".7", dashes=(2, 1), zorder=0)
   # #  # g.set_titles('{col_name}')
   # #  # g.fig.suptitle('Evolution of the trialTypePEProb10s in subjects by trialType')
   # #  # g.tight_layout(w_pad=0)
    
   # #  # #group by virus
   # #  # g= sns.relplot(data=dfPlot, x='trainDayThisStage', y='trialTypePEProb10s', row='virus', hue='trialType', hue_order=trialOrder, style='laserDur', kind='line')
   # #  # # g.map(plt.axhline, y=0.6, color=".7", dashes=(2, 1), zorder=0)
   # #  # g.set_titles('{row_name}')
   # #  # g.fig.suptitle('Evolution of the trialTypePEProb10s in subjects by trialType')
   # #  # g.tight_layout(w_pad=0)
    
   # #  # #show individual subj
   # #  # # g= sns.relplot(data=dfPlot, x='trainDayThisStage', y='trialTypePEProb10s', row='virus', units='subject', estimator=None, hue='trialType', hue_order=trialOrder, style='laserDur', kind='line')

   # #  # #subjects run different session types on same day, so can't plot by day across subjects
   # #  # sns.set_palette('Paired')

   # #  # g= sns.relplot(data=dfPlot, x='trainDayThisStage', y='trialTypePEProb10s', col='subject', col_wrap=4, hue='trialType', hue_order=trialOrder, style='laserDur', kind='line')
   # #  # # g.map(plt.axhline, y=0.6, color=".7", dashes=(2, 1), zorder=0)
   # #  # g.set_titles('{col_name}')
   # #  # g.fig.suptitle('Evolution of the trialTypePEProb10s in subjects by trialType')
   # #  # g.tight_layout(w_pad=0)
    
   # #  #individual subj
   # #  # for subj in dfPlot.subject.unique():
   # #  #     g= sns.catplot(data=dfPlot.loc(dfPlot.subject==subj), x='laserDur', y='trialTypePEProb10s',hue='trialType')
   
   # #  # g=sns.catplot(data= dfPlot, x='laserDur', y='trialTypePEProb10s', hue='trialType', hue_order=trialOrder, col='subject', col_wrap=4, kind='point')
   # #  # g=sns.relplot(data= dfPlot, estimator=None, x='trialType', y='trialTypePEProb10s', hue='laserDur', col='subject', col_wrap=4, kind='line')

   # #  # boxplots for each trial type with individual data points

   #  #individual subj facet
   #  g = sns.FacetGrid(data=dfPlot, col='subject',col_wrap=3)
   #  g.fig.suptitle('PE probability by trialType; laser + CUE')
   #  g.map_dataframe(sns.barplot, x='stage', y='trialTypePEProb10s', hue='trialType', hue_order=trialOrder, palette='Paired', ci=68)
   #  g.map_dataframe(sns.stripplot, x='stage', y='trialTypePEProb10s', hue='trialType', hue_order=trialOrder, palette='Paired', dodge='True', size=4, alpha=0.8, edgecolor='gray', linewidth=1)
   #  # g.map_dataframe(sns.lineplot, estimator=None, x='stage', y='trialTypePEProb10s', hue='trialType', hue_order=trialOrder,palette='Paired', size=4, alpha=0.8, linewidth=1)
   #  g.set_axis_labels( 'laser duration', 'probability of PE (10s)')
   #  # g.add_legend()
   #  # g.tight_layout()
   #  saveFigCustom(g, 'opto_individual_peProb_10s_bar')
    

   #  #virus facet
   #  g = sns.FacetGrid(data=dfPlot, row='virus')
   #  g.fig.suptitle('PE probability by trialType; laser + CUE')
   #  g.map_dataframe(sns.boxplot, x='stage', y='trialTypePEProb10s', hue='trialType', hue_order=trialOrder, palette='Paired')
   #  g.map_dataframe(sns.stripplot, x='stage', y='trialTypePEProb10s', hue='trialType', hue_order=trialOrder, palette='Paired', dodge='True', size=4, alpha=0.8, edgecolor='gray', linewidth=1)
   #  g.set_axis_labels( 'laser duration', 'probability of PE (10s)')
   #  # g.add_legend()
   #  # g.tight_layout()
   #  saveFigCustom(g, 'opto_virus_peProb_10s_box')
    
   #  g = sns.FacetGrid(data=dfPlot, row='virus')
   #  g.fig.suptitle('PE probability by trialType; laser + CUE')
   #  g.map_dataframe(sns.barplot, ci=68, x='stage', y='trialTypePEProb10s', hue='trialType', hue_order=trialOrder, palette='Paired')
   #  g.map_dataframe(sns.stripplot, x='stage', y='trialTypePEProb10s', hue='trialType', hue_order=trialOrder, palette='Paired', dodge='True', size=4, alpha=0.8, edgecolor='gray', linewidth=1)
   #  g.set_axis_labels( 'laser duration', 'probability of PE (10s)')
   #  # g.add_legend()
   #  # g.tight_layout()
   #  saveFigCustom(g, 'opto_virus_peProb_10s_bar')
    
   #  #virus and sex facet
   #  g = sns.FacetGrid(data=dfPlot, row='virus', col='sex')
   #  g.fig.suptitle('PE probability by trialType; laser + CUE')
   #  g.map_dataframe(sns.boxplot, x='stage', y='trialTypePEProb10s', hue='trialType', hue_order=trialOrder, palette='Paired')
   #  g.map_dataframe(sns.stripplot, x='stage', y='trialTypePEProb10s', hue='trialType', hue_order=trialOrder, palette='Paired', dodge='True', size=4, alpha=0.8, edgecolor='gray', linewidth=1)
   #  g.set_axis_labels( 'laser duration', 'probability of PE (10s)')
   #  # g.add_legend()
   #  # g.tight_layout()
   #  saveFigCustom(g, 'opto_virus+sex_peProb_10s_box')
    
   #  g = sns.FacetGrid(data=dfPlot, row='virus', col='sex')
   #  g.fig.suptitle('PE probability by trialType; laser + CUE')
   #  g.map_dataframe(sns.barplot, ci=68, x='stage', y='trialTypePEProb10s', hue='trialType', hue_order=trialOrder, palette='Paired')
   #  g.map_dataframe(sns.stripplot, x='stage', y='trialTypePEProb10s', hue='trialType', hue_order=trialOrder, palette='Paired', dodge='True', size=4, alpha=0.8, edgecolor='gray', linewidth=1)
   #  g.set_axis_labels( 'laser duration', 'probability of PE (10s)')
   #  saveFigCustom(g, 'opto_virus+sex_peProb_10s_bar')
   
   # #trying to connect individual subj points
   #  #pointplot with units=subject #seems to work well for each subj
   #  g= sns.catplot(data=dfPlot, y='trialTypePEProb10s', x='trialType',  kind='point', row='virus', col='stage', units='subject', hue='subject', order=trialOrder, palette=('deep'))
   #  g.fig.suptitle('PE probability by trialType; laser + CUE')
   #  g.set_axis_labels( 'trialType', 'probability of PE (10s)')
   #  g.map_dataframe(sns.barplot, y='trialTypePEProb10s', x='trialType', hue='trialType', hue_order=trialOrder, order=trialOrder, palette='Paired')

   #  saveFigCustom(g, 'opto_virus+sex_peProb_10s_point')

   
   #  # #trying to connect individual subject points...
   #  # g = sns.FacetGrid(data=dfPlot, row='virus') 
   #  # g.fig.suptitle('Probability of PE by trialType')
   #  # g.map_dataframe(sns.boxplot, x='stage', y='trialTypePEProb10s', hue='trialType', hue_order=trialOrder, palette='Paired')
   #  # #doens't line up properly
   #  # # g.map_dataframe(sns.stripplot, x='stage', y='trialTypePEProb10s', hue='subject', palette='tab20', dodge='True', size=4, alpha=0.8, edgecolor='gray', linewidth=1)
   #  # # g.map_dataframe(sns.lineplot, x='stage', y='trialTypePEProb10s', hue='subject', palette='tab20', size=4, alpha=0.8, linewidth=1)
   #  # g.set_axis_labels( 'laser duration', 'probability of PE')
   #  # g.add_legend()
    
   #  #  #trying to connect individual subject points...
   #  # g = sns.FacetGrid(data=dfPlot, row='virus', col='stage') 
   #  # g.fig.suptitle('Probability of PE by trialType')
   #  # g.map_dataframe(sns.boxplot, x='trialType', order= trialOrder, y='trialTypePEProb10s', hue='trialType', hue_order=trialOrder, palette='Paired')
   #  # #doens't line up properly
   #  # # g.map_dataframe(sns.stripplot, x='stage', y='trialTypePEProb10s', hue='subject', palette='tab20', dodge='True', size=4, alpha=0.8, edgecolor='gray', linewidth=1)
   #  # g.map_dataframe(sns.pointplot, x='trialType', order= trialOrder, y='trialTypePEProb10s', hue='subject', palette='tab20', size=0.2, alpha=0.2, linewidth=0.2)
   #  # g.set_axis_labels( 'trialType', 'probability of PE')
   #  # g.add_legend()
    
   #  #%Plot evolution of PE probability across laser test days
    
   #  #individual subject facet
   #  g= sns.relplot(data= dfPlot, kind='line', estimator=None, col='subject', col_wrap=3, x='trainDayThisStage', y='trialTypePEProb10s', hue='trialType', hue_order=trialOrder, style='stage', markers=True)
  
   #  # g= sns.relplot(data= dfPlot, kind='line', estimator=None, row='trialType', x='trainDayThisStage', y='trialTypePEProb10s', hue='virus', style='stage', markers=True)


   #  #virus facet
   #  g= sns.relplot(data= dfPlot, kind='line', row='virus', x='trainDayThisStage', y='trialTypePEProb10s', hue='trialType', hue_order=trialOrder)
   #  # g= sns.relplot(data= dfPlot, estimator=None, kind='line', row='virus', x='trainDayThisStage', y='trialTypePEProb10s', units='subject', hue='trialType', hue_order=trialOrder)


 

    #%% aggregate DS and NS trial types
    # # like above but recalculating peProb for combined laser off&on
    #  #select data  
    # dfPlot = dfTidyOpto[(dfTidyOpto.trialType != 'ITI')].copy()   
    
    # #make a dict to swap values
    # trialTypes= {'laserDStrial_0':'DS', 'laserDStrial_1':'DS', 'laserNStrial_0':'NS',
    #    'laserNStrial_1':'NS'}
    # dfPlot.loc[:,'trialType']= dfPlot.trialType.replace(trialTypes).copy()
    
    # #get only PE outcomes
    # # dfPlot.reset_index(inplace=True)
    # dfPlot= dfPlot.loc[(dfPlot.trialOutcomeBeh10s=='PE') | (dfPlot.trialOutcomeBeh10s=='PE+lick')].copy()
    
    # #since we calculated aggregated probability across all trials in session,
    # #take only first index. Otherwise repeated observations are redundant
    # dfPlot= dfPlot.groupby(['fileID','trialType','trialOutcomeBeh10s']).first().copy()
    
    
    # #sum together both PE and PE+lick for total PE prob
    # # dfPlot['outcomeProbFile']= dfPlot.groupby(['fileID'])['outcomeProbFile'].sum().copy()
    
    # dfPlot['trialTypePEProb10s']= dfPlot.groupby(['fileID','trialType'])['outcomeProbFile'].sum().copy()

    # #get an aggregated x axis for files per subject
    # fileAgg= dfPlot.reset_index().groupby(['subject','fileID','trialType']).cumcount().copy()==0
    
    # #since grouping PE and PE+lick, we still have redundant observations
    # #retain only 1 per trial type per file
    # dfPlot= dfPlot.reset_index().loc[fileAgg]
 
    # #now get just first value
    # # dfPlot= dfPlot.loc[dfPlot.groupby(['fileID','trialType']).cumcount()==0]    
    
    # #visualize
    # sns.set_palette('tab10')

    # # g= sns.relplot(data=dfPlot, x='trainDayThisStage', y='trialTypePEProb10s', row='virus', hue='trialType', style='stage', kind='line')
    # # g.map(plt.axhline, y=0.6, color=".2", dashes=(2, 1), zorder=0, linewidth=4)

#%% Testing groupby()- accessing values & index of grouped data

    # grouped= dfTidyOpto.groupby(['fileID','trialType'])
    
    # groupedInd= grouped.indices
    
    # groupedExtracted=  grouped.apply(lambda x: x) 
    # # grouped.reset_index()#dfTidyOpto.loc[groupedInd.keys()]
    
    # #this gb.groups() seems to give index of all values for each group
    # groups= grouped.groups
    
    
    # #this too probably slower
    # groups = dict(list(grouped))
    
    # #which returns a dictionary whose keys are your group labels and whose values are DataFrames, i.e.
    
    # groupedHead= grouped.head()
    
    # # #iterating through like this takes way too long
    # # groupedRows= pd.DataFrame()
    # # for row in grouped:
    # #     groupedRows= groupedRows.append(row[1])
        
    #%% Above gives us one value per session of PE probability
    # #would be good to have individual trials for variance?
    
    # #count is same as probability so not really helpful?
    
    # dfPlot= dfTidyOpto.copy()
    
    # #aggregated measure, but trialIDs repeat, so just restrict to first one
    # trialAgg= dfPlot.groupby(['fileID','trialID'])['trialID'].cumcount()==0

    # dfPlot= dfPlot.loc[trialAgg].copy() 
    
    # #count of trials for each trialType
    # dfPlot= dfPlot.groupby(['fileID','trialType'])['trialOutcomeBeh10s'].value_counts()
    
    # #for some reason value_counts() isn't giving 0 count for all categories. Fill these with 0 so we have a count for each possibility
    # dfPlot= dfPlot.unstack(fill_value=0).stack().reset_index(name='count')
    
    # #merge w other data
    # dfPlot= dfTidyOpto.merge(dfPlot,'right', on=['fileID','trialType','trialOutcomeBeh10s'])


    #%% TODO: evolution within session (typical trial progression)
    
    # #commenting out bc hitting memory error 2023-01-24
  
    # #New- rewriting
    
    # # declare hierarchical level of analysis for the analysis we are doing (here there is one outcome per trial per file)
    # levelOfAnalysis = ['fileID', 'trialID']
    
    # # First we need to subset only one outcome per level of analysis (trial)
    # dfGroup = dfTidyOpto.loc[dfTidyOpto.groupby(levelOfAnalysis).cumcount() == 0].copy()
    
    # # declare hierarchical grouping variables (how should the observations be separated)
    # groupHierarchy = groupHierarchyTrialID
    
    # # here want percentage of each behavioral outcome per trialID per above groupers
    # colToCalc = 'trialOutcomeBeh10s'
    
    # # 2023-01-24 hitting memory error 

    # #-- hitting memory error here
    # dfTemp = groupPercentCalc(dfGroup, levelOfAnalysis, groupHierarchy, colToCalc)
    
    # #instead of 1 col per probability, melt into single column that matches up to outcome
    # dfTemp= dfTemp.reset_index().melt(
    #     id_vars=groupHierarchy, value_name='trialIDoutcomeBehProb10s')
    
    # #merge to save as new column in dfTidyOpto
    # dfTidyOpto = dfTidyOpto.merge(dfTemp, how='left', on=groupHierarchy+[colToCalc])
    
    # #calculate PE probability by trialID
    # dfGroup= percentPortEntryCalc(dfGroup, groupHierarchy, colToCalc)
    
    
    # #OLD
    
    # #get data, only trials (not ITI)
    # dfGroup= dfTidyOpto.loc[dfTidyOpto.trialType!='ITI'].copy()
    # #only trials
    # dfGroup= dfTidyOpto.copy().loc[dfTidyOpto.trialID>=0].copy()

    
    # sns.set_palette('Paired')
    
    # #aggregated measure, but trialIDs repeat, so just restrict to first one
    # trialAgg= dfGroup.groupby(['fileID','trialID'])['trialID'].cumcount()==0

    # dfGroup= dfGroup.loc[trialAgg].copy()   
    
    # #simple plot of binary PE or noPE outcome count by trialID across stages
    # #not great since # of trials will vary by stage & subject, proportion is better...
    # dfPlot= dfGroup.copy()
    # #combine outcomeBeh into PE or noPE
    # dfPlot.loc[(dfPlot.trialOutcomeBeh10s=='PE')|(dfGroup.trialOutcomeBeh10s=='PE+lick'),'trialOutcomeBeh10s']= 'PE'
    # dfPlot.loc[(dfPlot.trialOutcomeBeh10s=='noPE')|(dfGroup.trialOutcomeBeh10s=='noPE+lick'),'trialOutcomeBeh10s']= 'noPE'

    # g= sns.catplot(data=dfPlot, col='stage', col_wrap=3, x='trialID', hue='trialOutcomeBeh10s', palette='tab10', kind='count')
    # g.set_xlabels('trialID')
    
    # #for each unique behavioral outcome, loop through and get count for each trialID within each level of session vars (e.g. stage, stage)
    # dfTemp=dfGroup.groupby(
    #         ['subject','trialID','stage','trialType','trialOutcomeBeh10s'],dropna=False)['trialOutcomeBeh10s'].nunique(dropna=False).unstack(fill_value=0)
    
    
    # ##calculate proportion for each trial type: num trials with outcome/total num trials of this type

    # trialCount= dfTemp.sum(axis=1)
    
    
    # outcomeProb= dfTemp.divide(dfTemp.sum(axis=1),axis=0)
    
    # #melt() outcomeProb into single column w label
    # dfTemp= outcomeProb.reset_index().melt(id_vars=['subject','trialID','stage','trialType'],var_name='trialOutcomeBeh10s',value_name='outcomeProbSubjTrialID')
    
    
    # dfPlot = dfTemp.copy()
    # #viz
    # g= sns.catplot(data=dfPlot, col='stage', row='trialType', x='trialID', y='outcomeProbSubjTrialID', hue= 'subject', palette=subjPalette)
    # g= sns.relplot(data=dfPlot, col='stage', col_wrap=3, x='trialID', hue= 'subject', palette=subjPalette, kind='line')

    # g.set_xlabels('trialID')
    
    # #assign back to df by merging
    # #TODO: can probably be optimized. if this section is run more than once will get errors due to assignment back to dfTidyOpto
    # # dfTidyOpto.reset_index(inplace=True) #reset index so eventID index is kept
    
    # dfTidyOpto= dfTidyOpto.merge(dfTemp,'left', on=['subject','trialID','stage','trialType','trialOutcomeBeh10s']).copy()
    # #%% Plot probability of PE outcome by trialID (evolution within sessions from above)
     
    # #subset data and save as intermediate variable dfGroup
    # dfGroup= dfTidyOpto.copy()
     
    # #select data
    # #all trialTypes excluding ITI     
    # dfPlot = dfGroup[(dfGroup.trialType != 'ITI')].copy()
    # dfPlot = dfGroup[(dfGroup.trialID >= 0)].copy()
    
    # #combine all PE outcomes 
    # dfPlot.loc[dfPlot.trialOutcomeBeh10s=='PE+lick','trialOutcomeBeh10s']= 'PE'
    
    
    # #get only PE outcomes
    # # dfPlot.reset_index(inplace=True)
    # dfPlot= dfPlot.loc[(dfPlot.trialOutcomeBeh10s=='PE')].copy()# | (dfPlot.trialOutcomeBeh10s=='PE+lick')].copy()
     
    # #since we calculated aggregated proportion by session vars within subj
    # #take only first index using the same groupers. Otherwise repeated observations are redundant
    # dfPlot= dfPlot.groupby(['subject','trialID','stage','trialType']).first().copy()
    # #['outcomeProbSubjTrialID'].first().copy()
     
     
    # #sum together both PE and PE+lick for total overall PE prob
    # # dfPlot['outcomeProbFile']= dfPlot.groupby(['fileID'])['outcomeProbFile'].sum().copy()
    
    # # dfPlot['trialTypePEProb10s']= dfPlot.groupby(['subject','trialID','stage','laserDur','trialType'])['outcomeProbFile10s'].sum().copy()
    # # dfPlot['trialTypePEProb10s']= dfPlot.reset_index().groupby(['subject','trialID','stage','laserDur','trialType'])['outcomeProbFile10s'].sum().copy()
    
    # dfPlot['trialTypePEProb10s']= dfPlot.groupby(['subject','trialID','stage','trialType'])['outcomeProbSubjTrialID'].sum().copy()
    
    # #get an aggregated x axis for files per subject
    # # fileAgg= dfPlot.groupby(['subject','fileID','trialType']).cumcount().copy()==0
     
    # #since grouping PE and PE+lick, we still have redundant observations
    # #retain only 1 per trial type per file
    # # dfPlot= dfPlot.reset_index().loc[fileAgg]
    
    
    # dfPlot.reset_index(inplace=True)
    
    # g= sns.relplot(data= dfPlot, x='trialID', y='trialTypePEProb10s', hue='trialType', row='stage', kind='line')
    
  #   #%%
  #%% old code:
       
  #     #get data, only trials (not ITI)
  #   dfGroup= dfTidyOpto.loc[dfTidyOpto.trialType!='ITI'].copy()
    
  #   sns.set_palette('Paired')
    
  #   #aggregated measure, but trialIDs repeat, so just restrict to first one
  #   trialAgg= dfGroup.groupby(['fileID','trialID'])['trialID'].cumcount()==0

  #   dfGroup= dfGroup.loc[trialAgg].copy()   
  #  #counts of each trial type by trialID
  #  #trial count seems biased? many more DS?
  #   # dfPlot= dfPlot.groupby(['subject','trialID','trialType'])['laserDur'].value_counts()#.reset_index(name='count')
    
  #   #take count of each trialType for each trialID within each level of session vars (e.g. stage or laserDur) 
  #   #this is the total count which will act as divisor for probability calc
  #   dfPlot= dfGroup.groupby(['subject','trialID','stage'])['trialType'].value_counts()
    
  #   #for some reason value_counts() isn't giving 0 count for all categories. Fill these with 0 so we have a count for each possibility
  #   dfPlot= dfPlot.unstack(fill_value=0).stack().reset_index(name='count')

  #   #temporary df to store all
  #   dfTemp= dfPlot.copy()

  #   # sns.relplot(data=dfPlot, row='laserDur', x='trialID', y='count', hue='trialType',  hue_order= trialOrder, kind='line')
    
  #   #####repeat for behavior outcome
  #     #get data, only trials (not ITI)
  #   dfGroup= dfTidyOpto.loc[dfTidyOpto.trialType!='ITI'].copy()
    
  #   sns.set_palette('Paired')
    
  #   #aggregated measure, but trialIDs repeat, so just restrict to first one
  #   trialAgg= dfGroup.groupby(['fileID','trialID'])['trialID'].cumcount()==0

  #   dfPlot= dfGroup.loc[trialAgg].copy()   
       
  #  #counts of each trial type by trialID
  #  #trial count seems biased? many more DS?
  #   # dfPlot= dfPlot.groupby(['subject','trialID','trialType'])['laserDur'].value_counts()#.reset_index(name='count')
    
  #   dfPlot= dfPlot.groupby(['subject','trialID','stage','trialType'])['trialOutcomeBeh10s'].value_counts()
    
  #   #for some reason value_counts() isn't giving 0 count for all categories. Fill these with 0 so we have a count for each possibility
  #   dfPlot= dfPlot.unstack(fill_value=0).stack().reset_index(name='count')
    
  #   # sns.relplot(data=dfPlot, row='laserDur', x='trialID', y='count', hue='trialOutcomeBeh10s', style='trialType', kind='line')
  #   # sns.catplot(data=dfPlot, row='stage', x='trialID', hue='trialOutcomeBeh10s', kind='count')

    
  #   ###
  #  #  #get data, only trials (not ITI)
  #  #  dfPlot= dfTidyOpto.loc[dfTidyOpto.trialType!='ITI'].copy()
       
  #  #  #aggregated measure, but trialIDs repeat, so just restrict to first one
  #  #  trialAgg= dfPlot.groupby(['fileID','trialID']).cumcount()==0    
    
  #  #  dfPlot= dfPlot.loc[trialAgg]
    
  #  #  #estimate response profile by subject and laserDur (session type), and trialType
  #  #  dfPlot= dfPlot.groupby(['subject','laserDur','trialType','trialID'])['trialOutcomeBeh10s'].value_counts().reset_index(name='count')


  #  #  sns.set_palette('tab20')
    
  #  #  g=sns.relplot(data=dfPlot, col='subject', col_wrap=4, x='trialID', y='count', hue='trialOutcomeBeh10s', kind='line')
    
  #  #  #TODO: UNITS should be fileID
  #  #  dfPlot= dfTidyOpto.merge(dfPlot, how='right', on=['subject','laserDur','trialType','trialID']).copy()
    
  #  #  g=sns.relplot(data=dfPlot, units='fileID', estimator=None, x='trialID', y='count', hue='trialOutcomeBeh10s', kind='line')
        
  #  #  for sesType in dfPlot.laserDur.unique():
  #  #      g=sns.displot(data=dfPlot.loc[dfPlot.laserDur==sesType], col='subject', col_wrap=4, 
  #  #                    x='trialID', hue='trialOutcomeBeh10s', kind='hist', 
  #  #                    stat='count', multiple='dodge')
  #  #      # g=sns.relplot(data=dfPlot.loc[dfPlot.laserDur==sesType], col='subject', col_wrap=4, x='trialID', y='count', hue='trialOutcomeBeh10s', kind='line')
        
  #  #      g.set_titles('{col_name}')
  #  #      g.fig.suptitle('Evolution of behavior within sessions by trialID; laser='+sesType)
  #  #      g.tight_layout(w_pad=0)
    
  #  #  sns.catplot(data=dfPlot, x='trialID', y='count', hue='trialOutcomeBeh10s', kind='bar')
    
 
    
  #  #  #
  #  #  sns.relplot(data=dfPlot,x='trialID',y='trialOutcomeBeh10s')
    
  #  # #count # of each outcomes?
  #  #  count= dfPlot.groupby(['fileID','trialType'])['trialOutcomeBeh10s'].value_counts().unstack()
    
    
  #  #  #merge 
  #  #  test = dfPlot.merge(count,
  #  #             left_on=['fileID','trialType'], 
  #  #             right_index=True)
    
    
  #  #  #set index for plotting
  #  #  dfPlot=dfPlot.set_index(['fileID','trialType'])
    
  #  #  sns.catplot(data=dfPlot, x='fileID', y=count,hue='trialOutcomeBeh10s', kind='bar')
    
  #   # %% Effect of laser on current trial lick behavior
  #      #select data corresponding to first lick from valid trials
  #   dfPlot = dfTidyOpto[(dfTidyOpto.trialType!= 'ITI') & (dfTidyOpto.trialLick10s == 0)].copy()
    
  #   # lick latency: virus x laserDur
  #   g = sns.displot(data=dfPlot, x='eventLatency', hue='trialType',
  #                   col='stage', row='virus', kind='ecdf', hue_order= trialOrder)
  #   g.fig.suptitle('First lick latency by trial type; laser + CUE')
  #   g.set_ylabels('First lick latency from epoch start (s)')
    
  #   #lick latency: virus individual subj
  #   # g=sns.catplot(data=dfPlot,y='eventLatency',hue='trialType', x='subject', kind='bar', hue_order=trialOrder)
  #   # g.fig.suptitle('First lick latency by trial type; laser + CUE')
  #   # g.set_ylabels('First lick latency from epoch start (s)')
    
  #   #TODO:
  #   #     #bar with overlay individual trial overlay
  #   # plt.figure()
  #   # plt.subplot(1, 1, 1)
  #   # sns.barplot(data=dfPlot, y='eventLatency', x='trialType',hue='trialType',hue_order=trialOrder)
  #   # sns.lineplot(data=dfPlot, estimator=None, y='eventLatency', x='trialType',hue='subject', alpha=0.5, size=2)
    
  #       #bar for group with individual connected subj lines
  #   # g = sns.FacetGrid(data=dfPlot, row='virus', col='stage') 
  #   # g.map_dataframe(sns.barplot, x='trialType', y='eventLatency', hue='trialType', hue_order=trialOrder, palette='Paired', ci=68)
  #   # g.map_dataframe(sns.lineplot, estimator=None, x='trialType', y='eventLatency', hue='subject', palette='tab20', alpha=0.5)
  #   # # g.map_dataframe(sns.scatterplot, x='trialType', y='eventLatency', hue='subject', palette='tab20', alpha=0.5)

  # # box for group with individual data points
  #   g = sns.FacetGrid(data=dfPlot, row='virus')
  #   g.fig.suptitle('First lick latency by trial type; laser + CUE')
  #   g.map_dataframe(sns.boxplot, x='stage', y='eventLatency', hue='trialType', hue_order=trialOrder, palette='Paired')
  #   g.map_dataframe(sns.stripplot, x='stage', y='eventLatency', hue='trialType', hue_order=trialOrder, palette='Paired', dodge='True', size=4, alpha=0.8, edgecolor='gray', linewidth=1)
  #   g.set_axis_labels( 'laser duration', 'First lick latency from epoch start (s)')
  #   g.add_legend()
    
  #   saveFigCustom(g, 'opto_virus_lickLatency_10s_box')
    
  #   # bar for group with individual data points
  #   g = sns.FacetGrid(data=dfPlot, row='virus')
  #   g.fig.suptitle('First lick latency by trial type; laser + CUE')
  #   g.map_dataframe(sns.barplot, ci=68, x='stage', y='eventLatency', hue='trialType', hue_order=trialOrder, palette='Paired')
  #   g.map_dataframe(sns.stripplot, x='stage', y='eventLatency', hue='trialType', hue_order=trialOrder, palette='Paired', dodge='True', size=4, alpha=0.8, edgecolor='gray', linewidth=1)
  #   g.set_axis_labels( 'laser duration', 'First lick latency from epoch start (s)')
  #   g.add_legend()
    
  #   saveFigCustom(g, 'opto_virus_lickLatency_10s_bar')
    
    
    # %% Laser effect on subsequent trial(s)
    #TODO: currently this approach is blind to the next trial type. Data is only grouped by the preceding trialType.
    #Depending on how trial types are drawn in the code, it may be that certain trial types are selected in biased order which could 
    #be reflected in response probability (e.g. maybe DS trials are more likely to be followed by an NS trial)
    
    
    shiftNum= -1 #number of trials backward (-) to shift data. Expect hig`hest effect at most recent preceding trial -1
        
    dfGroup= dfTidyOpto.copy()
    
    
    #include only valid trials (remove ITIs)
    dfGroup= dfGroup.loc[dfGroup.trialType!='ITI'].copy()
    
    #if dtype is 'category',value_counts() should count all
    dfGroup.trialType= dfGroup.trialType.astype('category')
    dfGroup.trialOutcomeBeh10s=dfGroup.trialOutcomeBeh10s.astype('category')
    
   #aggregated measures, but trialIDs repeat, so just restrict to first one
    trialAgg= dfGroup.groupby(['fileID','trialID'])['trialID'].cumcount()==0
    
    dfGroup= dfGroup.loc[trialAgg]
    
    # trials= dfGroup.trialID.unique()
    
    #index by file, trial
    dfGroup.set_index(['fileID','trialID'], inplace=True)
    
    #use df.shift() on measures of interest
    # dfPlot= dfGroup.copy()

    #shift data within file (level=0)
    dfGroup.loc[:,'trialOutcomeBeh10sShift']= dfGroup.groupby(level=0)['trialOutcomeBeh10s'].shift(shiftNum).copy()
    dfGroup.loc[:,'trialTypeShift']= dfGroup.groupby(level=0)['trialType'].shift(shiftNum).copy()

    
    #will need to recalculate prob & latency (or other measures) based on shifted df
    

    #transform keeps original index
    # dfPlot['outcomeCount']= dfPlot.groupby(['fileID','trialType','trialOutcomeBeh10sShift']).
    
    #count of each trial type, followed by count of each behavioral outcome for each trial type
    # trialCount= dfPlot.groupby(['fileID','trialType'])['trialOutcomeBeh10sShift'].value_counts()
    
    
    # #count of each outcome for each trialType
    
    # trialCount= dfGroup.groupby(['fileID','trialType'])['trialOutcomeBeh10sShift'].count() #returns 4 values per session
    
    # # trialCount= dfGroup.groupby(['fileID','trialType'])['trialOutcomeBeh10sShift'].value_counts().reindex(dfGroup.trialOutcomeBeh10sShift.unique(),fill_value=0)
    
    # trialCount = dfGroup.groupby(['fileID','trialType'])['trialOutcomeBeh10sShift'].value_counts().unstack(fill_value=0).stack() #still gives 12 for ses 258
    
    # trialCount = dfGroup.groupby(['fileID'])['trialOutcomeBeh10sShift'].value_counts().unstack(fill_value=0).stack() #still gives 12 for ses 258

    #Size instead of value_counts(): size() gives a count for each category, where value_counts() has issues with/skips unobserved groups
    trialCount = dfGroup.groupby(['fileID','trialType','trialOutcomeBeh10sShift']).size()#.unstack(fill_value=0).stack() #still gives 12 for ses 258


    #grouping fileID alone and getting value_counts is cool, but combinging with trialType seems to be wrong.
    #try fillna?
    # trialCount = dfGroup.groupby(['fileID','trialType'])['trialOutcomeBeh10sShift'].value_counts().unstack(fill_value=0).stack() #still gives 12 for ses 258

    
    # test= dfGroup.loc[258,:]
    # test2= test.groupby(['trialType'])['trialOutcomeBeh10sShift'].count()
    # # test3= test.groupby(['trialType'])['trialOutcomeBeh10sShift'].value_counts().unstack(fill_value=0)
   
    # test4= test.groupby(['trialType','trialOutcomeBeh10sShift']).size()
    
    #only have6 endtries for ses 258...should have 16 per file (4 trial types x 4 outcomes)? 

    
    #still missing data in trialCount as of this point? e.g. check ses 258
   
    #for some reason value_counts() isn't giving 0 count for all categories. Fill these with 0 so we have a count for each possibility
    # trialCount= trialCount.unstack(fill_value=0).stack().reset_index(name='count')
    
    #divide count of each outcome by total count for this trial type
    #calculate probability for each trial type: num trials/total num trials
    trialCount= trialCount.unstack(fill_value=0)
    # trialCount2= trialCount.unstack(fill_value=0)

#good up til here, now outcomeProb is missing a group?
    
        #from prior code
      ##calculate probability for each trial type: num trials/total num trials
    outcomeProb= trialCount.divide(trialCount.sum(axis=1),axis=0)
    
    #This calculation will result in nans where trialTypes or outcomes are missing. Replace nan values with 0
    outcomeProb.fillna(0, inplace=True)    


    #now we need to reindex before adding columns (problem with categorical dtypes)
    outcomeProb.columns = pd.Index(list(outcomeProb.columns))
    
    #melt() into single column w label
    
    dfPlot= outcomeProb.reset_index().melt(id_vars=['fileID','trialType'],var_name='trialOutcomeBeh10sShift',value_name='outcomeProbShift')
    
    
    #assign back to df by merging
    #TODO: can probably be optimized
    dfGroup.reset_index(inplace=True) #reset index so eventID index is kept
    # dfPlot= dfGroup.merge(dfPlot,'right', on=['fileID','trialType','trialOutcomeBeh10sShift']).copy()
    
    #Expect this ^ will not work now since we have calculated values for unobserved trialTypes and outcomes
    # test= dfPlot.merge(dfGroup,'left', on=['fileID','trialType','trialOutcomeBeh10sShift']).copy()


    #aggregated measures, but trialTypes repeat, so just restrict to first one
    trialAgg= dfPlot.groupby(['fileID','trialType','trialOutcomeBeh10sShift']).cumcount()==0
     
    dfPlot= dfPlot.loc[trialAgg]
    
    #merge after this restriction
    #first, merge on specific outcomes
    dfPlot= dfPlot.merge(dfGroup,'left', on=['fileID','trialType','trialOutcomeBeh10sShift']).copy()
     
    #then, fill matching session data?
    # dfPlot= dfPlot.merge(dfGroup,'left', on=['fileID']).copy()
    dfPlot.set_index('fileID', inplace=True)
    dfPlot.fillna(method= 'ffill', inplace=True)
    dfPlot.reset_index(inplace=True)
    
    dfPlot.set_index(['fileID','trialType'], inplace=True)     
    
    
    #best to combine PE outcomes and restrict plotting to just peProb since 4 outcomes gets very busy, so calculate peProb by combining PE and PE+lick outcome prob
    #retain  only PE and PE+lick outcomes
    dfPlot= dfPlot.loc[(dfPlot.trialOutcomeBeh10sShift=='PE') | (dfPlot.trialOutcomeBeh10sShift=='PE+lick')].copy()

    #since grouping PE and PE+lick, we still have redundant observations
    #retain only 1 per trial type per file
    fileAgg= dfPlot.reset_index().groupby(['subject','fileID','trialType']).cumcount().copy()==0
    dfPlot= dfPlot.reset_index().loc[fileAgg]


    #sum together both PE and PE+lick for total PE prob. Do this for each trial type
    dfPlot['trialTypePEProb10sshift']= dfPlot.groupby(['fileID','trialType'])['outcomeProbShift'].transform('sum').copy()
    
    #Plots
    g=sns.catplot(data= dfPlot, x='stage', y='trialTypePEProb10sshift', hue='trialType', hue_order=trialOrder, col='subject', col_wrap=4, ci=68, kind='bar')
    g.fig.suptitle('Effect of laser on subsequent PE probability (shifted'+ str(shiftNum)+'trials)')

    #bar with overlay of individual sessions
    g = sns.FacetGrid(data=dfPlot, col='subject', col_wrap=4) 
    g.map_dataframe(sns.barplot, x='stage', y='trialTypePEProb10sshift', hue='trialType', hue_order=trialOrder, palette='Paired', alpha=0.5, ci=None)
    g.map_dataframe(sns.stripplot, x='stage', y='trialTypePEProb10sshift', hue='trialType', hue_order=trialOrder, palette='Paired', dodge=True)

    g.set_axis_labels( 'laser duration', 'probability of trials with PE')

    g.add_legend()
    
      # bar for group with individual data points
    g = sns.FacetGrid(data=dfPlot, row='virus')
    g.fig.suptitle('Effect of laser on subsequent PE probability (shifted'+ str(shiftNum)+'trials)')
    g.map_dataframe(sns.boxplot, x='stage', y='trialTypePEProb10sshift', hue='trialType', hue_order=trialOrder, palette='Paired')
    g.map_dataframe(sns.stripplot, x='stage', y='trialTypePEProb10sshift', hue='trialType', hue_order=trialOrder, palette='Paired', dodge='True', size=4, alpha=0.8, edgecolor='gray', linewidth=1)
    g.set_axis_labels( 'laser duration', 'probability of PE on subsequent trial')
    g.add_legend()
    
    saveFigCustom(g, 'opto_virus_trialTypePEProb10s_shifted_10s_box')

#%% TODO: shifted count & latency 

#for each event type, calculate latency from trial start to event
    
    # %% examine lick+laser on licks
    try:
         #subset data and save as intermediate variable dfGroup
        dfGroup= dfTidyOpto.copy()
        #for Lick+laser sessions, retain only trials with PE+lick for comparison
        dfGroup.loc[dfGroup.laserDur=='Lick',:]= dfGroup.loc[(dfGroup.laserDur=='Lick') & (dfGroup.trialOutcomeBeh10s=='PE+lick')].copy()
       
        dfPlot = dfGroup[(dfGroup.laserDur=='Lick')].copy()
        
        #All subj distribution of ILI (inter-lick interval)
        #only include trialLick10s~=nan
        dfPlot = dfPlot[dfPlot.trialLick10s.notnull()].copy()
        #calculate ILI by taking diff() of latencies
        ili= dfPlot.groupby(['fileID','trialID','trialType'])['eventLatency'].diff()
    
        #bar- all subj
        g= sns.catplot(data=dfPlot, y=ili, x='trialType',  kind='bar', order=trialOrder)
        g.fig.subplots_adjust(top=0.9)  # adjust the figure for title
        g.fig.suptitle('ILI by trial type; laser+LICK; all subj')
        g.set_ylabels('ILI (s)')
        g.set(ylim=(0,0.5))
    
        
        # #hist- all subj
        # ili= ili.astype('float') #allows KDE, but kde here takes awhile
        # g= sns.displot(data=dfPlot, x=ili, hue='trialType',  kind='hist', stat="density", common_norm=False, kde=True, multiple='layer', hue_order=np.sort(dfPlot.trialType.unique()))
        # g.fig.subplots_adjust(top=0.9)  # adjust the figure for title
        # g.fig.suptitle('ILI by trial type; laser OFF; all subj')
        # g.set_xlabels('ILI (s)')
        # g.set(xlim=(0,1))
        
        #box- all subj
        g= sns.catplot(data=dfPlot, y=ili, x='trialType',  kind='box', order=trialOrder)
        g.fig.subplots_adjust(top=0.9)  # adjust the figure for title
        g.fig.suptitle('ILI by trial type; laser+LICK; all subj')
        g.set_ylabels('ILI (s)')
        g.set(ylim=(0,0.5))
    
        
        #ecdf- all subj
        g= sns.displot(data=dfPlot, x=ili, hue='trialType',  kind='ecdf', hue_order=trialOrder)
        g.fig.subplots_adjust(top=0.9)  # adjust the figure for title
        g.fig.suptitle('ILI by trial type; laser+LICK; all subj')
        g.set_xlabels('ILI (s)')
        g.set(xlim=(0,1))
    
        
        #Individual distribution of ILI (inter-lick interval)
        dfPlot = dfGroup[(dfGroup.laserDur=='Lick')].copy()
        #only include trialLick10s~=nan
        dfPlot = dfPlot[dfPlot.trialLick10s.notnull()].copy()
        #calculate ILI by taking diff() of latencies
        ili= dfPlot.groupby(['fileID','trialID','trialType'])['eventLatency'].diff()
        #bar- individual subj
        g= sns.catplot(data=dfPlot, y=ili, x='subject', hue='trialType',  kind='bar', hue_order=trialOrder)
        g.fig.subplots_adjust(top=0.9)  # adjust the figure for title
        g.fig.suptitle('ILI by trial type; laser+LICK; individual subj')
        g.set_ylabels('ILI (s)')
        g.set(ylim=(0,1))
        
        #lick count by trial
        dfPlot = dfGroup[(dfGroup.laserDur=='Lick')].copy()
        #TODO: consider alternate reshaping df for plotting different aggregations. Not sure what is most convenient
        
        #need an index for aggregated trial variables- since trialID repeats we need to restrict observations to first otherwise we'll plot redundant data and stats will be off
        trialAgg= (dfPlot.groupby(['fileID','trialID'])['trialID'].cumcount()==0).copy()
        #transform keeps original index
        lickCount= dfPlot.groupby(['fileID','trialID','trialType'])['trialLick10s'].transform('count').copy()
        
        #get only one aggregated value per trial
        lickCount= lickCount.loc[trialAgg].copy()
        dfPlot= dfPlot.loc[trialAgg].copy()
            
        g= sns.catplot(data=dfPlot, y=lickCount,x='subject',hue='trialType',kind='bar',hue_order=trialOrder)
        g.fig.subplots_adjust(top=0.9)  # adjust the figure for title
        g.fig.suptitle('Lick count by trial type; laser+LICK; individual subj')
        g.set_ylabels('count of licks per trial')
        g.set_xlabels('subject')
        
        #bar with overlay individual trial overlay
        plt.figure()
        plt.subplot(1, 1, 1)
        sns.barplot(data=dfPlot, y=lickCount,x='subject',hue='trialType',hue_order=trialOrder)
        sns.stripplot(data=dfPlot, y=lickCount,x='subject',hue='trialType',hue_order=trialOrder, dodge=True,size=2)
        
        ##Compare to CUE and laser OFF
        ##TODO: error here
        # dfPlot = dfTidyOpto.copy() #all data
        
        # #need an index for aggregated trial variables- since trialID repeats we need to restrict observations to first otherwise we'll plot redundant data and stats will be off
        # trialAgg= (dfPlot.groupby(['fileID','trialID','trialType'])['trialID'].cumcount()==0).copy()
        # #transform keeps original index
        # lickCount= dfPlot.groupby(['fileID','trialID','trialType'])['trialLick10s'].transform('count').copy()
        
        # #get only one aggregated value per trial
        # lickCount= lickCount.loc[trialAgg].copy()
        # dfPlot= dfPlot.loc[trialAgg].copy()
        
        # g= sns.catplot(data=dfPlot, row='laserDur', y=lickCount,x='subject',hue='trialType',kind='bar',hue_order=trialOrder)
        
    except:
        print('lick+laser exception')
    
    #%% Save dfTidyOpto so it can be loaded quickly for subesequent analysis

savePath= r'./_output/' #r'C:\Users\Dakota\Documents\GitHub\DS-Training\Python' 

print('saving dfTidyOpto to file')

#Save as pickel
dfTidyOpto.to_pickle(savePath+'dfTidyOpto.pkl')
    
    
  
    
    #%% Use pandas profiling on event counts
    ##This might be a decent way to quickly view behavior session results if automated
    
    ##Unstack() the groupby output for a dataframe we can profile
    # dfPlot= dfTidyOpto
    # dfPlot= dfPlot.groupby(['subject','trainDayThisStage','eventType'])['eventTime'].count().unstack()
    # #add trialType counts
    # dfPlot= dfPlot.merge(dfTidyOpto.loc[(dfTidyOpto.eventType=='x_I_NStime') | (dfTidyOpto.eventType=='x_H_DStime')].groupby(['subject','trainDayThisStage','trialType'])['eventTime'].count().unstack(),left_index=True,right_index=True)

    # from pandas_profiling import ProfileReport

    # profile = ProfileReport(dfPlot, title='Event Count by Session Pandas Profiling Report', explorative = True)

    # # save profile report as html
    # profile.to_file('pandasProfileEventCounts.html')
    
  # %% Try Pandas_profiling report
    # note- if you are getting errors with ProfileReport() and you installed using conda, remove and reinstall using pip install

    # from pandas_profiling import ProfileReport

    # profile = ProfileReport(dfTidyOpto, title='Pandas Profiling Report', explorative = True)

    # # save profile report as html
    # profile.to_file('pandasProfile.html')
