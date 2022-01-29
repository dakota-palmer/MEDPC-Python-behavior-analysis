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

    # #%% Load previously saved dfTidyAnalyzed (and other vars) from pickle
    dataPath= r'./_output/' #'r'C:\Users\Dakota\Documents\GitHub\DS-Training\Python\\'
    
    dfTidyOpto= pd.read_pickle(dataPath+'dfTidyAnalyzed.pkl')
    
    #load any other variables saved during the import process ('dfTidymeta' shelf)
    my_shelf = shelve.open(dataPath+'dfTidymeta')
    for key in my_shelf:
        globals()[key]=my_shelf[key]
    my_shelf.close()
    
     #%% define a function to save and close figures
    def saveFigCustom(figure, figName):
        plt.gcf().set_size_inches((20,10), forward=False) # ~monitor size
        plt.legend(bbox_to_anchor=(1.01, 1), borderaxespad=0) #creates legend ~right of the last subplot
        
        plt.gcf().tight_layout()
        plt.savefig(r'./_output/_behaviorAnalysis/'+figName+'.png', bbox_inches='tight')
        plt.close()
        
    #%% set opto specific plotting options
    sns.set_palette('Paired') #great for compairing laser on vs laser off trialTypes

    #%% exclude sessions without laser manipulations
    dfTidyOpto= dfTidyOpto.loc[dfTidyOpto.laserDur!='nan @ nan']
    dfTidyOpto= dfTidyOpto.loc[dfTidyOpto.laserDur.notnull()]
    
    dfTidyOpto.laserDur= dfTidyOpto.laserDur.astype('category')
    
    #redefine categories
    dfTidyOpto.laserDur= dfTidyOpto.laserDur.cat.remove_unused_categories()
      #%% Remove Lick+Laser trials without PE+Lick
      
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
    

    # %% Analysis & visualization

   #  # visualize using seaborn
   #  import seaborn as sns
   #  import matplotlib.pyplot as plt

   #  # paired seems nice for comparing conditions (laser on vs off)
    sns.set_palette('Paired')
    
   # #manually defining color order so that paired color scheme looks nice
   #  trialOrder =['laserDStrial_0', 'laserDStrial_1',
   #     'laserNStrial_0', 'laserNStrial_1','ITI']
    trialOrder= (['DStime', 'DStime_laser', 'NStime', 'NStime_laser', 'Pre-Cue','ITI'])
 
    #%% remove ITI trialtype
    trialOrder= (['DStime', 'DStime_laser', 'NStime', 'NStime_laser', 'Pre-Cue'])


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
    dfPlot = dfTidyOpto[(dfTidyOpto.trialType!='ITI') & (dfTidyOpto.trialPE10s == 0)].copy()
    
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
    g = sns.FacetGrid(data=dfPlot, col='subject',col_wrap=3)
    g.fig.suptitle('PE latency by trialType; laser + CUE')
    g.map_dataframe(sns.boxplot, x='stage', y='eventLatency', hue='trialType', hue_order=trialOrder, palette='Paired')
    g.map_dataframe(sns.stripplot, x='stage', y='eventLatency', hue='trialType', hue_order=trialOrder, palette='Paired', dodge='True', size=4, alpha=0.2, edgecolor='gray', linewidth=1)
    g.set_axis_labels( 'stage', 'latency to first PE (10s)')
    saveFigCustom(g, 'opto_individual_peLatency_10s_box')
    
    g = sns.FacetGrid(data=dfPlot, col='subject',col_wrap=3)
    g.fig.suptitle('PE latency by trialType; laser + CUE')
    g.map_dataframe(sns.barplot, ci=68, x='stage', y='eventLatency', hue='trialType', hue_order=trialOrder, palette='Paired')
    g.map_dataframe(sns.stripplot, x='stage', y='eventLatency', hue='trialType', hue_order=trialOrder, palette='Paired', dodge='True', size=4, alpha=0.2, edgecolor='gray', linewidth=1)
    g.set_axis_labels( 'laser duration', 'latency to first PE (10s)')
    saveFigCustom(g, 'opto_individual_peLatency_10s_bar')
    
    #virus facet
    g = sns.FacetGrid(data=dfPlot, row='virus')
    g.fig.suptitle('PE latency by trialType; laser + CUE')
    g.map_dataframe(sns.boxplot, x='stage', y='eventLatency', hue='trialType', hue_order=trialOrder, palette='Paired')
    g.map_dataframe(sns.stripplot, x='stage', y='eventLatency', hue='trialType', hue_order=trialOrder, palette='Paired', dodge='True', size=4, alpha=0.2, edgecolor='gray', linewidth=1)
    g.set_axis_labels( 'laser duration', 'latency to first PE (10s)')
    saveFigCustom(g, 'opto_virus_peLatency_10s_box')
    
    # barplots for each trial type with individual data points 
    #individual subj facet
    g = sns.FacetGrid(data=dfPlot, col='subject',col_wrap=3)
    g.fig.suptitle('PE latency by trialType; laser + CUE')
    g.map_dataframe(sns.barplot, ci=68, x='stage', y='eventLatency', hue='trialType', hue_order=trialOrder, palette='Paired')
    g.map_dataframe(sns.stripplot, x='stage', y='eventLatency', hue='trialType', hue_order=trialOrder, palette='Paired', dodge='True', size=4, alpha=0.2, edgecolor='gray', linewidth=1)
    g.set_axis_labels( 'laser duration', 'latency to first PE (10s)')
    saveFigCustom(g, 'opto_individual_peLatency_10s_bar')
    
    #virus facet
    g = sns.FacetGrid(data=dfPlot, row='virus')
    g.fig.suptitle('PE latency by trialType; laser + CUE')
    g.map_dataframe(sns.barplot, ci=68, x='stage', y='eventLatency', hue='trialType', hue_order=trialOrder, palette='Paired')
    g.map_dataframe(sns.stripplot, x='stage', y='eventLatency', hue='trialType', hue_order=trialOrder, palette='Paired', dodge='True', size=4, alpha=0.2, edgecolor='gray', linewidth=1)
    g.set_axis_labels( 'laser duration', 'latency to first PE (10s)')
    saveFigCustom(g, 'opto_virus_peLatency_10s_bar')
    
    #virus + sex facet
    g = sns.FacetGrid(data=dfPlot, row='virus', col='sex')
    g.fig.suptitle('PE latency by trialType; laser + CUE')
    g.map_dataframe(sns.barplot, ci=68, x='stage', y='eventLatency', hue='trialType', hue_order=trialOrder, palette='Paired')
    g.map_dataframe(sns.stripplot, x='stage', y='eventLatency', hue='trialType', hue_order=trialOrder, palette='Paired', dodge='True', size=4, alpha=0.2, edgecolor='gray', linewidth=1)
    g.set_axis_labels( 'laser duration', 'latency to first PE (10s)')
    saveFigCustom(g, 'opto_virus+sex_peLatency_10s_bar')
    
    # ECDFs
    #vius facet
    g = sns.displot(data=dfPlot, row='virus', col='stage', x='eventLatency', hue='trialType', hue_order=trialOrder, palette='Paired', kind='ecdf')
    g.fig.suptitle('PE latency by trialType; laser + CUE')
    g.set_xlabels('latency to first PE (10s)')
    saveFigCustom(g, 'opto_virus_peLatency_10s_ecdf')    
    
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
    
    # #TODO: clean up and move higher to prelim analysis section
    
    # # outcomeProb= dfPlot[dfPlot.trialOutcomeBeh10s=='PE'].groupby(['fileID','trialID'])['trialOutcomeBeh10s'].count().index

    
    # #calculate Probortion of trials with PE out of all trials for each trial type
    # #can use nunique() to get count of unique trialIDs with specific PE outcome per file
    # #given this, can calculate Probortion as #PE/#PE+#noPE
   
    # #subset data and save as intermediate variable dfGroup
    # dfGroup= dfTidyOpto.copy()
    # #for Lick+laser sessions, retain only trials with PE+lick for comparison
    # dfGroup.loc[dfGroup.laserDur=='Lick',:]= dfGroup.loc[(dfGroup.laserDur=='Lick') & (dfGroup.trialOutcomeBeh10s=='PE+lick')].copy()
   
    # dfPlot= dfGroup.copy() 
    
    # #excluded trials from lick+laser sessions are all nan. don't include
    # outcomes= dfTidyOpto.loc[dfTidyOpto.trialOutcomeBeh10s.notnull()].trialOutcomeBeh10s.unique()
    
    # #TODO: optimize this- combine outcomes here into one variable
    # #using apply() might help? or pivot?
    
    # # tester[outcomes]= dfPlot[(dfPlot.trialOutcomeBeh10s==outcomes)].reset_index().groupby(
    # #     ['fileID','trialType','trialOutcomeBeh10s'])['trialID'].nunique()
    
    # test1= dfPlot[(dfPlot.trialOutcomeBeh10s=='PE')].reset_index().groupby(['fileID','trialType','trialOutcomeBeh10s'])['trialID'].nunique()
    # test1.name= 'PE'
    # test2= dfPlot[dfPlot.trialOutcomeBeh10s=='noPE'].reset_index().groupby(['fileID','trialType','trialOutcomeBeh10s'])['trialID'].nunique()
    # test2.name= 'noPE'    
    
    # test5= dfPlot[(dfPlot.trialOutcomeBeh10s=='PE+lick')].reset_index().groupby(['fileID','trialType','trialOutcomeBeh10s'])['trialID'].nunique()
    # test5.name= 'PE+lick'
    # test8= dfPlot[(dfPlot.trialOutcomeBeh10s=='noPE+lick')].reset_index().groupby(['fileID','trialType','trialOutcomeBeh10s'])['trialID'].nunique()
    # test8.name= 'noPE+lick'
 
           
    # ##num of unique trials per trial type per session, but still cant sum
    # test6= pd.concat((test1,test2,test5,test8),ignore_index=False,axis=1)
    
    # ##reset index and groupby trialType so we can sum across columns
    # test7= test6.reset_index().groupby(['fileID','trialType'])[outcomes].sum()
 
    # ##calculate probability for each trial type: num trials/total num trials
    # outcomeProb= test7.divide(test7.sum(axis=1),axis=0)
    
    # #melt() into single column w label
    # test8= outcomeProb.reset_index().melt(id_vars=['fileID','trialType'],var_name='trialOutcomeBeh10s',value_name='outcomeProbFile')
    
    # #assign back to df by merging
    # #TODO: can probably be optimized. if this section is run more than once will get errors due to assignment back to dfTidyOpto
    # # dfTidyOpto.reset_index(inplace=True) #reset index so eventID index is kept
    
    # dfTidyOpto= dfTidyOpto.reset_index().merge(test8,'left', on=['fileID','trialType','trialOutcomeBeh10s']).copy()
    
    # dfTidyOpto.loc[:,'outcomeProbFile']= test8.outcomeProbFile
    
         
    #subset data and save as intermediate variable dfGroup
    dfGroup= dfTidyOpto.copy()
     
    #select data
    #all trialTypes excluding ITI     
    dfPlot = dfGroup[(dfGroup.trialType != 'ITI')].copy()
     
    #get only PE outcomes
    # dfPlot.reset_index(inplace=True)
    dfPlot= dfPlot.loc[(dfPlot.trialOutcomeBeh10s=='PE') | (dfPlot.trialOutcomeBeh10s=='PE+lick')].copy()
     
    #since we calculated aggregated proportion across all trials in session,
    #take only first index. Otherwise repeated observations are redundant
    dfPlot= dfPlot.groupby(['fileID','trialType','trialOutcomeBeh10s']).first().copy()
     
     
    #sum together both PE and PE+lick for total overall PE prob
    # dfPlot['outcomeProbFile']= dfPlot.groupby(['fileID'])['outcomeProbFile'].sum().copy()
     
    dfPlot['probPE']= dfPlot.groupby(['fileID','trialType'])['outcomeProbFile10s'].sum().copy()
    
    #get an aggregated x axis for files per subject
    fileAgg= dfPlot.reset_index().groupby(['subject','fileID','trialType']).cumcount().copy()==0
     
    #since grouping PE and PE+lick, we still have redundant observations
    #retain only 1 per trial type per file
    dfPlot= dfPlot.reset_index().loc[fileAgg]
    
    #% visualize peProb
    
    
    # #subset data and save as intermediate variable dfGroup
    # dfGroup= dfTidyOpto.copy()
    # #for Lick+laser sessions, retain only trials with PE+lick for comparison
    # dfGroup.loc[dfGroup.laserDur=='Lick',:]= dfGroup.loc[(dfGroup.laserDur=='Lick') & (dfGroup.trialOutcomeBeh10s=='PE+lick')].copy()
   
    
    # #select data     
    # dfPlot = dfTidyOpto[(dfGroup.trialType !='ITI')].copy()
    #Plot probability of PE by trialType 
    
    # #get only PE outcomes
    # # dfPlot.reset_index(inplace=True)
    # dfPlot= dfPlot.loc[(dfPlot.trialOutcomeBeh10s=='PE') | (dfPlot.trialOutcomeBeh10s=='PE+lick')].copy()
    
    # #since we calculated aggregated probability across all trials in session,
    # #take only first index. Otherwise repeated observations are redundant
    # dfPlot= dfPlot.groupby(['fileID','trialType','trialOutcomeBeh10s']).first().copy()
    
    
    # #sum together both PE and PE+lick for total PE prob
    # # dfPlot['outcomeProbFile']= dfPlot.groupby(['fileID'])['outcomeProbFile'].sum().copy()
    
    # dfPlot['probPE']= dfPlot.groupby(['fileID','trialType'])['outcomeProbFile'].sum().copy()

    # #get an aggregated x axis for files per subject
    # fileAgg= dfPlot.reset_index().groupby(['subject','fileID','trialType']).cumcount().copy()==0
    
    # #since grouping PE and PE+lick, we still have redundant observations
    # #retain only 1 per trial type per file
    # dfPlot= dfPlot.reset_index().loc[fileAgg]

   # #Plot
   #  #one line per per trialType per subj would be ideal. In subplots
   #  #manual control here of facetgrid and titles (i). 
   #  #Manual:
   #  sns.set_palette('tab20')
   #  g = sns.FacetGrid(dfPlot, col='subject', hue='trialType', hue_order=trialOrder, col_wrap=4)

   #  # Add the line over the area with the plot function
   #  g = g.map(plt.plot, 'fileID', 'probPE')
    
   #  # Control the title of each facet
   #  g = g.set_titles("{col_name}")
     
   #  # Add a title for the whole plot
   #  plt.subplots_adjust(top=0.9)
   #  g = g.fig.suptitle('Evolution of the probPE in subjects by trialType')
    
     
   #  #same with relplot:
   #  g= sns.relplot(data=dfPlot, x='fileID', y='probPE', col='subject', col_wrap=4, hue='trialType', hue_order=trialOrder, kind='line')
   #  # g.map(plt.axhline, y=0.6, color=".7", dashes=(2, 1), zorder=0)
   #  g.set_titles('{col_name}')
   #  g.fig.suptitle('Evolution of the probPE in subjects by trialType')
   #  g.tight_layout(w_pad=0)
    
    # #plot by laserDur
    # g= sns.relplot(data=dfPlot, x='trainDayThisStage', y='probPE', col='subject', col_wrap=4, hue='trialType', hue_order=trialOrder, style='laserDur', kind='line')
    # # g.map(plt.axhline, y=0.6, color=".7", dashes=(2, 1), zorder=0)
    # g.set_titles('{col_name}')
    # g.fig.suptitle('Evolution of the probPE in subjects by trialType')
    # g.tight_layout(w_pad=0)
    
    # #group by virus
    # g= sns.relplot(data=dfPlot, x='trainDayThisStage', y='probPE', row='virus', hue='trialType', hue_order=trialOrder, style='laserDur', kind='line')
    # # g.map(plt.axhline, y=0.6, color=".7", dashes=(2, 1), zorder=0)
    # g.set_titles('{row_name}')
    # g.fig.suptitle('Evolution of the probPE in subjects by trialType')
    # g.tight_layout(w_pad=0)
    
    # #show individual subj
    # # g= sns.relplot(data=dfPlot, x='trainDayThisStage', y='probPE', row='virus', units='subject', estimator=None, hue='trialType', hue_order=trialOrder, style='laserDur', kind='line')

    # #subjects run different session types on same day, so can't plot by day across subjects
    # sns.set_palette('Paired')

    # g= sns.relplot(data=dfPlot, x='trainDayThisStage', y='probPE', col='subject', col_wrap=4, hue='trialType', hue_order=trialOrder, style='laserDur', kind='line')
    # # g.map(plt.axhline, y=0.6, color=".7", dashes=(2, 1), zorder=0)
    # g.set_titles('{col_name}')
    # g.fig.suptitle('Evolution of the probPE in subjects by trialType')
    # g.tight_layout(w_pad=0)
    
    #individual subj
    # for subj in dfPlot.subject.unique():
    #     g= sns.catplot(data=dfPlot.loc(dfPlot.subject==subj), x='laserDur', y='probPE',hue='trialType')
   
    # g=sns.catplot(data= dfPlot, x='laserDur', y='probPE', hue='trialType', hue_order=trialOrder, col='subject', col_wrap=4, kind='point')
    # g=sns.relplot(data= dfPlot, estimator=None, x='trialType', y='probPE', hue='laserDur', col='subject', col_wrap=4, kind='line')

    # boxplots for each trial type with individual data points

    #individual subj facet
    g = sns.FacetGrid(data=dfPlot, col='subject',col_wrap=3)
    g.fig.suptitle('PE probability by trialType; laser + CUE')
    g.map_dataframe(sns.barplot, x='stage', y='probPE', hue='trialType', hue_order=trialOrder, palette='Paired', ci=68)
    g.map_dataframe(sns.stripplot, x='stage', y='probPE', hue='trialType', hue_order=trialOrder, palette='Paired', dodge='True', size=4, alpha=0.8, edgecolor='gray', linewidth=1)
    # g.map_dataframe(sns.lineplot, estimator=None, x='stage', y='probPE', hue='trialType', hue_order=trialOrder,palette='Paired', size=4, alpha=0.8, linewidth=1)
    g.set_axis_labels( 'laser duration', 'probability of PE (10s)')
    # g.add_legend()
    # g.tight_layout()
    saveFigCustom(g, 'opto_individual_peProb_10s_bar')
    

    #virus facet
    g = sns.FacetGrid(data=dfPlot, row='virus')
    g.fig.suptitle('PE probability by trialType; laser + CUE')
    g.map_dataframe(sns.boxplot, x='stage', y='probPE', hue='trialType', hue_order=trialOrder, palette='Paired')
    g.map_dataframe(sns.stripplot, x='stage', y='probPE', hue='trialType', hue_order=trialOrder, palette='Paired', dodge='True', size=4, alpha=0.8, edgecolor='gray', linewidth=1)
    g.set_axis_labels( 'laser duration', 'probability of PE (10s)')
    # g.add_legend()
    # g.tight_layout()
    saveFigCustom(g, 'opto_virus_peProb_10s_box')
    
    g = sns.FacetGrid(data=dfPlot, row='virus')
    g.fig.suptitle('PE probability by trialType; laser + CUE')
    g.map_dataframe(sns.barplot, ci=68, x='stage', y='probPE', hue='trialType', hue_order=trialOrder, palette='Paired')
    g.map_dataframe(sns.stripplot, x='stage', y='probPE', hue='trialType', hue_order=trialOrder, palette='Paired', dodge='True', size=4, alpha=0.8, edgecolor='gray', linewidth=1)
    g.set_axis_labels( 'laser duration', 'probability of PE (10s)')
    # g.add_legend()
    # g.tight_layout()
    saveFigCustom(g, 'opto_virus_peProb_10s_bar')
    
    #virus and sex facet
    g = sns.FacetGrid(data=dfPlot, row='virus', col='sex')
    g.fig.suptitle('PE probability by trialType; laser + CUE')
    g.map_dataframe(sns.boxplot, x='stage', y='probPE', hue='trialType', hue_order=trialOrder, palette='Paired')
    g.map_dataframe(sns.stripplot, x='stage', y='probPE', hue='trialType', hue_order=trialOrder, palette='Paired', dodge='True', size=4, alpha=0.8, edgecolor='gray', linewidth=1)
    g.set_axis_labels( 'laser duration', 'probability of PE (10s)')
    # g.add_legend()
    # g.tight_layout()
    saveFigCustom(g, 'opto_virus+sex_peProb_10s_box')
    
    g = sns.FacetGrid(data=dfPlot, row='virus', col='sex')
    g.fig.suptitle('PE probability by trialType; laser + CUE')
    g.map_dataframe(sns.barplot, ci=68, x='stage', y='probPE', hue='trialType', hue_order=trialOrder, palette='Paired')
    g.map_dataframe(sns.stripplot, x='stage', y='probPE', hue='trialType', hue_order=trialOrder, palette='Paired', dodge='True', size=4, alpha=0.8, edgecolor='gray', linewidth=1)
    g.set_axis_labels( 'laser duration', 'probability of PE (10s)')
    saveFigCustom(g, 'opto_virus+sex_peProb_10s_bar')
   
   #trying to connect individual subj points
    #pointplot with units=subject #seems to work well for each subj
    g= sns.catplot(data=dfPlot, y='probPE', x='trialType',  kind='point', row='virus', col='stage', units='subject', hue='subject',order=trialOrder, palette=('deep'))
    g.fig.suptitle('PE probability by trialType; laser + CUE')
    g.set_axis_labels( 'trialType', 'probability of PE (10s)')
    g.map_dataframe(sns.barplot, y='probPE', x='trialType', hue='trialType', hue_order=trialOrder, order=trialOrder, palette='Paired')

    saveFigCustom(g, 'opto_virus+sex_peProb_10s_point')

   
    # #trying to connect individual subject points...
    # g = sns.FacetGrid(data=dfPlot, row='virus') 
    # g.fig.suptitle('Probability of PE by trialType')
    # g.map_dataframe(sns.boxplot, x='stage', y='probPE', hue='trialType', hue_order=trialOrder, palette='Paired')
    # #doens't line up properly
    # # g.map_dataframe(sns.stripplot, x='stage', y='probPE', hue='subject', palette='tab20', dodge='True', size=4, alpha=0.8, edgecolor='gray', linewidth=1)
    # # g.map_dataframe(sns.lineplot, x='stage', y='probPE', hue='subject', palette='tab20', size=4, alpha=0.8, linewidth=1)
    # g.set_axis_labels( 'laser duration', 'probability of PE')
    # g.add_legend()
    
    #  #trying to connect individual subject points...
    # g = sns.FacetGrid(data=dfPlot, row='virus', col='stage') 
    # g.fig.suptitle('Probability of PE by trialType')
    # g.map_dataframe(sns.boxplot, x='trialType', order= trialOrder, y='probPE', hue='trialType', hue_order=trialOrder, palette='Paired')
    # #doens't line up properly
    # # g.map_dataframe(sns.stripplot, x='stage', y='probPE', hue='subject', palette='tab20', dodge='True', size=4, alpha=0.8, edgecolor='gray', linewidth=1)
    # g.map_dataframe(sns.pointplot, x='trialType', order= trialOrder, y='probPE', hue='subject', palette='tab20', size=0.2, alpha=0.2, linewidth=0.2)
    # g.set_axis_labels( 'trialType', 'probability of PE')
    # g.add_legend()
    
    #%Plot evolution of PE probability across laser test days
    
    #individual subject facet
    g= sns.relplot(data= dfPlot, kind='line', estimator=None, col='subject', col_wrap=3, x='trainDayThisStage', y='probPE', hue='trialType', hue_order=trialOrder, style='stage', markers=True)
  
    # g= sns.relplot(data= dfPlot, kind='line', estimator=None, row='trialType', x='trainDayThisStage', y='probPE', hue='virus', style='stage', markers=True)


    #virus facet
    g= sns.relplot(data= dfPlot, kind='line', row='virus', x='trainDayThisStage', y='probPE', hue='trialType', hue_order=trialOrder)
    # g= sns.relplot(data= dfPlot, estimator=None, kind='line', row='virus', x='trainDayThisStage', y='probPE', units='subject', hue='trialType', hue_order=trialOrder)


    #%% Calculate difference score between laser off and laser on trialTypes
    
    #get rid of ITI & pre cue then just use diff() to get difference
    dfGroup= dfPlot.loc[((dfPlot.trialType!='Pre-Cue') & (dfPlot.trialType!='ITI') )].copy()


    #take diff between DS trial types 
    test= dfGroup.trialType.str.contains('DS')

    dfGroup.loc[test,'probPEdiff']= dfGroup.loc[test].groupby('fileID').probPE.diff()
    
    #take diff between NS trial types 
    test= dfGroup.trialType.str.contains('NS')

    dfGroup.loc[test,'probPEdiff']= dfGroup.loc[test].groupby('fileID').probPE.diff()
    
    #make plots
    dfPlot= dfGroup.copy()
    
   #individual subject facet
    g= sns.relplot(data= dfPlot, kind='line', estimator=None, col='subject', col_wrap=3, x='trainDayThisStage', y='probPEdiff', hue='trialType', hue_order=trialOrder, style='stage', markers=True)
    # g.map(refline(y=0, linewidth=2, linestyle="-", color=None, clip_on=False))
    g.map(plt.axhline, y=0, color=".2", linewidth=3, dashes=(3,1), zorder=0)

    

    #%% aggregate DS and NS trial types
    # like above but recalculating peProb for combined laser off&on
     #select data  
    dfPlot = dfTidyOpto[(dfTidyOpto.trialType != 'ITI')].copy()   
    
    #make a dict to swap values
    trialTypes= {'laserDStrial_0':'DS', 'laserDStrial_1':'DS', 'laserNStrial_0':'NS',
       'laserNStrial_1':'NS'}
    dfPlot.loc[:,'trialType']= dfPlot.trialType.replace(trialTypes).copy()
    
    #get only PE outcomes
    # dfPlot.reset_index(inplace=True)
    dfPlot= dfPlot.loc[(dfPlot.trialOutcomeBeh10s=='PE') | (dfPlot.trialOutcomeBeh10s=='PE+lick')].copy()
    
    #since we calculated aggregated probability across all trials in session,
    #take only first index. Otherwise repeated observations are redundant
    dfPlot= dfPlot.groupby(['fileID','trialType','trialOutcomeBeh10s']).first().copy()
    
    
    #sum together both PE and PE+lick for total PE prob
    # dfPlot['outcomeProbFile']= dfPlot.groupby(['fileID'])['outcomeProbFile'].sum().copy()
    
    dfPlot['probPE']= dfPlot.groupby(['fileID','trialType'])['outcomeProbFile'].sum().copy()

    #get an aggregated x axis for files per subject
    fileAgg= dfPlot.reset_index().groupby(['subject','fileID','trialType']).cumcount().copy()==0
    
    #since grouping PE and PE+lick, we still have redundant observations
    #retain only 1 per trial type per file
    dfPlot= dfPlot.reset_index().loc[fileAgg]
 
    #now get just first value
    # dfPlot= dfPlot.loc[dfPlot.groupby(['fileID','trialType']).cumcount()==0]    
    
    #visualize
    sns.set_palette('tab10')

    # g= sns.relplot(data=dfPlot, x='trainDayThisStage', y='probPE', row='virus', hue='trialType', style='stage', kind='line')
    # g.map(plt.axhline, y=0.6, color=".2", dashes=(2, 1), zorder=0, linewidth=4)

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
        
    #get data, only trials (not ITI)
    dfGroup= dfTidyOpto.loc[dfTidyOpto.trialType!='ITI'].copy()
    #only trials
    dfGroup= dfTidyOpto.copy().loc[dfTidyOpto.trialID>=0].copy()

    
    sns.set_palette('Paired')
    
    #aggregated measure, but trialIDs repeat, so just restrict to first one
    trialAgg= dfGroup.groupby(['fileID','trialID'])['trialID'].cumcount()==0

    dfGroup= dfGroup.loc[trialAgg].copy()   
    
    #simple plot of binary PE or noPE outcome count by trialID across stages
    #not great since # of trials will vary by stage & subject, proportion is better...
    dfPlot= dfGroup.copy()
    #combine outcomeBeh into PE or noPE
    dfPlot.loc[(dfPlot.trialOutcomeBeh10s=='PE')|(dfGroup.trialOutcomeBeh10s=='PE+lick'),'trialOutcomeBeh10s']= 'PE'
    dfPlot.loc[(dfPlot.trialOutcomeBeh10s=='noPE')|(dfGroup.trialOutcomeBeh10s=='noPE+lick'),'trialOutcomeBeh10s']= 'noPE'

    g= sns.catplot(data=dfPlot, col='stage', col_wrap=3, x='trialID', hue='trialOutcomeBeh10s', palette='tab10', kind='count')
    g.set_xlabels('trialID')
    
    #for each unique behavioral outcome, loop through and get count for each trialID within each level of session vars (e.g. stage, stage)
    dfTemp=dfGroup.groupby(
            ['subject','trialID','stage','trialType','trialOutcomeBeh10s'],dropna=False)['trialOutcomeBeh10s'].nunique(dropna=False).unstack(fill_value=0)
    
    
    ##calculate proportion for each trial type: num trials with outcome/total num trials of this type

    trialCount= dfTemp.sum(axis=1)
    
    
    outcomeProb= dfTemp.divide(dfTemp.sum(axis=1),axis=0)
    
    #melt() outcomeProb into single column w label
    dfTemp= outcomeProb.reset_index().melt(id_vars=['subject','trialID','stage','trialType'],var_name='trialOutcomeBeh10s',value_name='outcomeProbSubjTrialID')
    
    #assign back to df by merging
    #TODO: can probably be optimized. if this section is run more than once will get errors due to assignment back to dfTidyOpto
    # dfTidyOpto.reset_index(inplace=True) #reset index so eventID index is kept
    
    dfTidyOpto= dfTidyOpto.merge(dfTemp,'left', on=['subject','trialID','stage','trialType','trialOutcomeBeh10s']).copy()
    #%% Plot probability of PE outcome by trialID (evolution within sessions from above)
     
    #subset data and save as intermediate variable dfGroup
    dfGroup= dfTidyOpto.copy()
     
    #select data
    #all trialTypes excluding ITI     
    dfPlot = dfGroup[(dfGroup.trialType != 'ITI')].copy()
    dfPlot = dfGroup[(dfGroup.trialID >= 0)].copy()
    
    #combine all PE outcomes 
    dfPlot.loc[dfPlot.trialOutcomeBeh10s=='PE+lick','trialOutcomeBeh10s']= 'PE'
    
    
    #get only PE outcomes
    # dfPlot.reset_index(inplace=True)
    dfPlot= dfPlot.loc[(dfPlot.trialOutcomeBeh10s=='PE')].copy()# | (dfPlot.trialOutcomeBeh10s=='PE+lick')].copy()
     
    #since we calculated aggregated proportion by session vars within subj
    #take only first index using the same groupers. Otherwise repeated observations are redundant
    dfPlot= dfPlot.groupby(['subject','trialID','stage','trialType']).first().copy()
    #['outcomeProbSubjTrialID'].first().copy()
     
     
    #sum together both PE and PE+lick for total overall PE prob
    # dfPlot['outcomeProbFile']= dfPlot.groupby(['fileID'])['outcomeProbFile'].sum().copy()
    
    # dfPlot['probPE']= dfPlot.groupby(['subject','trialID','stage','laserDur','trialType'])['outcomeProbFile10s'].sum().copy()
    # dfPlot['probPE']= dfPlot.reset_index().groupby(['subject','trialID','stage','laserDur','trialType'])['outcomeProbFile10s'].sum().copy()
    
    dfPlot['probPE']= dfPlot.groupby(['subject','trialID','stage','trialType'])['outcomeProbSubjTrialID'].sum().copy()
    
    #get an aggregated x axis for files per subject
    # fileAgg= dfPlot.groupby(['subject','fileID','trialType']).cumcount().copy()==0
     
    #since grouping PE and PE+lick, we still have redundant observations
    #retain only 1 per trial type per file
    # dfPlot= dfPlot.reset_index().loc[fileAgg]
    
    
    dfPlot.reset_index(inplace=True)
    
    g= sns.relplot(data= dfPlot, x='trialID', y='probPE', hue='trialType', row='stage', kind='line')
    
    #%%
    #old code:
       
      #get data, only trials (not ITI)
    dfGroup= dfTidyOpto.loc[dfTidyOpto.trialType!='ITI'].copy()
    
    sns.set_palette('Paired')
    
    #aggregated measure, but trialIDs repeat, so just restrict to first one
    trialAgg= dfGroup.groupby(['fileID','trialID'])['trialID'].cumcount()==0

    dfGroup= dfGroup.loc[trialAgg].copy()   
   #counts of each trial type by trialID
   #trial count seems biased? many more DS?
    # dfPlot= dfPlot.groupby(['subject','trialID','trialType'])['laserDur'].value_counts()#.reset_index(name='count')
    
    #take count of each trialType for each trialID within each level of session vars (e.g. stage or laserDur) 
    #this is the total count which will act as divisor for probability calc
    dfPlot= dfGroup.groupby(['subject','trialID','stage'])['trialType'].value_counts()
    
    #for some reason value_counts() isn't giving 0 count for all categories. Fill these with 0 so we have a count for each possibility
    dfPlot= dfPlot.unstack(fill_value=0).stack().reset_index(name='count')

    #temporary df to store all
    dfTemp= dfPlot.copy()

    # sns.relplot(data=dfPlot, row='laserDur', x='trialID', y='count', hue='trialType',  hue_order= trialOrder, kind='line')
    
    #####repeat for behavior outcome
      #get data, only trials (not ITI)
    dfGroup= dfTidyOpto.loc[dfTidyOpto.trialType!='ITI'].copy()
    
    sns.set_palette('Paired')
    
    #aggregated measure, but trialIDs repeat, so just restrict to first one
    trialAgg= dfGroup.groupby(['fileID','trialID'])['trialID'].cumcount()==0

    dfPlot= dfGroup.loc[trialAgg].copy()   
       
   #counts of each trial type by trialID
   #trial count seems biased? many more DS?
    # dfPlot= dfPlot.groupby(['subject','trialID','trialType'])['laserDur'].value_counts()#.reset_index(name='count')
    
    dfPlot= dfPlot.groupby(['subject','trialID','stage','trialType'])['trialOutcomeBeh10s'].value_counts()
    
    #for some reason value_counts() isn't giving 0 count for all categories. Fill these with 0 so we have a count for each possibility
    dfPlot= dfPlot.unstack(fill_value=0).stack().reset_index(name='count')
    
    # sns.relplot(data=dfPlot, row='laserDur', x='trialID', y='count', hue='trialOutcomeBeh10s', style='trialType', kind='line')
    # sns.catplot(data=dfPlot, row='stage', x='trialID', hue='trialOutcomeBeh10s', kind='count')

    
    ###
   #  #get data, only trials (not ITI)
   #  dfPlot= dfTidyOpto.loc[dfTidyOpto.trialType!='ITI'].copy()
       
   #  #aggregated measure, but trialIDs repeat, so just restrict to first one
   #  trialAgg= dfPlot.groupby(['fileID','trialID']).cumcount()==0    
    
   #  dfPlot= dfPlot.loc[trialAgg]
    
   #  #estimate response profile by subject and laserDur (session type), and trialType
   #  dfPlot= dfPlot.groupby(['subject','laserDur','trialType','trialID'])['trialOutcomeBeh10s'].value_counts().reset_index(name='count')


   #  sns.set_palette('tab20')
    
   #  g=sns.relplot(data=dfPlot, col='subject', col_wrap=4, x='trialID', y='count', hue='trialOutcomeBeh10s', kind='line')
    
   #  #TODO: UNITS should be fileID
   #  dfPlot= dfTidyOpto.merge(dfPlot, how='right', on=['subject','laserDur','trialType','trialID']).copy()
    
   #  g=sns.relplot(data=dfPlot, units='fileID', estimator=None, x='trialID', y='count', hue='trialOutcomeBeh10s', kind='line')
        
   #  for sesType in dfPlot.laserDur.unique():
   #      g=sns.displot(data=dfPlot.loc[dfPlot.laserDur==sesType], col='subject', col_wrap=4, 
   #                    x='trialID', hue='trialOutcomeBeh10s', kind='hist', 
   #                    stat='count', multiple='dodge')
   #      # g=sns.relplot(data=dfPlot.loc[dfPlot.laserDur==sesType], col='subject', col_wrap=4, x='trialID', y='count', hue='trialOutcomeBeh10s', kind='line')
        
   #      g.set_titles('{col_name}')
   #      g.fig.suptitle('Evolution of behavior within sessions by trialID; laser='+sesType)
   #      g.tight_layout(w_pad=0)
    
   #  sns.catplot(data=dfPlot, x='trialID', y='count', hue='trialOutcomeBeh10s', kind='bar')
    
 
    
   #  #
   #  sns.relplot(data=dfPlot,x='trialID',y='trialOutcomeBeh10s')
    
   # #count # of each outcomes?
   #  count= dfPlot.groupby(['fileID','trialType'])['trialOutcomeBeh10s'].value_counts().unstack()
    
    
   #  #merge 
   #  test = dfPlot.merge(count,
   #             left_on=['fileID','trialType'], 
   #             right_index=True)
    
    
   #  #set index for plotting
   #  dfPlot=dfPlot.set_index(['fileID','trialType'])
    
   #  sns.catplot(data=dfPlot, x='fileID', y=count,hue='trialOutcomeBeh10s', kind='bar')
    
    # %% Effect of laser on current trial lick behavior
       #select data corresponding to first lick from valid trials
    dfPlot = dfTidyOpto[(dfTidyOpto.trialType!= 'ITI') & (dfTidyOpto.trialLick10s == 0)].copy()
    
    # lick latency: virus x laserDur
    g = sns.displot(data=dfPlot, x='eventLatency', hue='trialType',
                    col='stage', row='virus', kind='ecdf', hue_order= trialOrder)
    g.fig.suptitle('First lick latency by trial type; laser + CUE')
    g.set_ylabels('First lick latency from epoch start (s)')
    
    #lick latency: virus individual subj
    # g=sns.catplot(data=dfPlot,y='eventLatency',hue='trialType', x='subject', kind='bar', hue_order=trialOrder)
    # g.fig.suptitle('First lick latency by trial type; laser + CUE')
    # g.set_ylabels('First lick latency from epoch start (s)')
    
    #TODO:
    #     #bar with overlay individual trial overlay
    # plt.figure()
    # plt.subplot(1, 1, 1)
    # sns.barplot(data=dfPlot, y='eventLatency', x='trialType',hue='trialType',hue_order=trialOrder)
    # sns.lineplot(data=dfPlot, estimator=None, y='eventLatency', x='trialType',hue='subject', alpha=0.5, size=2)
    
        #bar for group with individual connected subj lines
    # g = sns.FacetGrid(data=dfPlot, row='virus', col='stage') 
    # g.map_dataframe(sns.barplot, x='trialType', y='eventLatency', hue='trialType', hue_order=trialOrder, palette='Paired', ci=68)
    # g.map_dataframe(sns.lineplot, estimator=None, x='trialType', y='eventLatency', hue='subject', palette='tab20', alpha=0.5)
    # # g.map_dataframe(sns.scatterplot, x='trialType', y='eventLatency', hue='subject', palette='tab20', alpha=0.5)

  # box for group with individual data points
    g = sns.FacetGrid(data=dfPlot, row='virus')
    g.fig.suptitle('First lick latency by trial type; laser + CUE')
    g.map_dataframe(sns.boxplot, x='stage', y='eventLatency', hue='trialType', hue_order=trialOrder, palette='Paired')
    g.map_dataframe(sns.stripplot, x='stage', y='eventLatency', hue='trialType', hue_order=trialOrder, palette='Paired', dodge='True', size=4, alpha=0.8, edgecolor='gray', linewidth=1)
    g.set_axis_labels( 'laser duration', 'First lick latency from epoch start (s)')
    g.add_legend()
    
    saveFigCustom(g, 'opto_virus_lickLatency_10s_box')
    
    # bar for group with individual data points
    g = sns.FacetGrid(data=dfPlot, row='virus')
    g.fig.suptitle('First lick latency by trial type; laser + CUE')
    g.map_dataframe(sns.barplot, ci=68, x='stage', y='eventLatency', hue='trialType', hue_order=trialOrder, palette='Paired')
    g.map_dataframe(sns.stripplot, x='stage', y='eventLatency', hue='trialType', hue_order=trialOrder, palette='Paired', dodge='True', size=4, alpha=0.8, edgecolor='gray', linewidth=1)
    g.set_axis_labels( 'laser duration', 'First lick latency from epoch start (s)')
    g.add_legend()
    
    saveFigCustom(g, 'opto_virus_lickLatency_10s_bar')
    
    
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
    dfPlot['probPEshift']= dfPlot.groupby(['fileID','trialType'])['outcomeProbShift'].transform('sum').copy()
    
    #Plots
    g=sns.catplot(data= dfPlot, x='stage', y='probPEshift', hue='trialType', hue_order=trialOrder, col='subject', col_wrap=4, ci=68, kind='bar')
    g.fig.suptitle('Effect of laser on subsequent PE probability (shifted'+ str(shiftNum)+'trials)')

    #bar with overlay of individual sessions
    g = sns.FacetGrid(data=dfPlot, col='subject', col_wrap=4) 
    g.map_dataframe(sns.barplot, x='stage', y='probPEshift', hue='trialType', hue_order=trialOrder, palette='Paired', alpha=0.5, ci=None)
    g.map_dataframe(sns.stripplot, x='stage', y='probPEshift', hue='trialType', hue_order=trialOrder, palette='Paired', dodge=True)

    g.set_axis_labels( 'laser duration', 'probability of trials with PE')

    g.add_legend()
    
      # bar for group with individual data points
    g = sns.FacetGrid(data=dfPlot, row='virus')
    g.fig.suptitle('Effect of laser on subsequent PE probability (shifted'+ str(shiftNum)+'trials)')
    g.map_dataframe(sns.boxplot, x='stage', y='probPEshift', hue='trialType', hue_order=trialOrder, palette='Paired')
    g.map_dataframe(sns.stripplot, x='stage', y='probPEshift', hue='trialType', hue_order=trialOrder, palette='Paired', dodge='True', size=4, alpha=0.8, edgecolor='gray', linewidth=1)
    g.set_axis_labels( 'laser duration', 'probability of PE on subsequent trial')
    g.add_legend()
    
    saveFigCustom(g, 'opto_virus_probPE_shifted_10s_box')

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
    
    #%% Save dfTidy so it can be loaded quickly for subesequent analysis

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
