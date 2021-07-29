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
    
#%% Set seaborn style up front
    sns.set_style("darkgrid")


#%% define a function to open file with gui
    def openFile():
        global matContents #global var so we can access later
        filepath = filedialog.askopenfilename(initialdir=r'C:\Users\Dakota\Desktop\Opto DS Task Test- CUE Laser Manipulation',
                                           title="open trainData.mat",
                                           filetypes= (("mat files","*.mat"),
                                           ("all files","*.*")))
        print(filepath)
        #load the mat file contents
        # setting squeeze_me argument=true, otherwise each element seems to get nested in individual arrays
        # matContents= sio.loadmat(r'Z:\Dakota\MEDPC\Downstairs\vp-vta-stgtacr_DStrain\Opto DS Task Test- CUE Laser Manipulation\trainData.mat',squeeze_me=True)
        matContents= sio.loadmat(filepath,squeeze_me=True)
        window.destroy()
     
 
#%% import matlab struct from .mat
    from tkinter import *
    from tkinter import filedialog
    
# #use GUI
    window = Tk()
    button = Button(text="Open",command=openFile) #openFile() function
    button.pack()
    window.mainloop()
# %% Extract the relevant data and get the data into pandas.dataframe format
    # adapted from https://www.kaggle.com/avilesmarcel/open-mat-in-python-pandas-dataframe

    # extract the struct contents from the loaded .mat
    mdata = matContents['trainData']

    mtype = mdata.dtype  # 1 'type' of data corresponding to each column

    # now it looks like we are creating a dict matching up data (in np.arrays) from mdata with column names
    ndata = {n: mdata[n] for n in mtype.names}

    data_headline = []  # will hold list of var labels for columns
    data_raw = []  # will hold the raw data for each column
    # since our struct contains multiple data types/classes, make this np array of object type
    data_raw = np.empty([mdata.shape[0], len(mtype.names)], dtype=object)

    # now simply loop through each variable type and get the corresponding data. Probably a better way to do this
    for var in range(len(mtype.names)):

        data_headline.append([mtype.names[var]][0])

        for ses in range(data_raw.shape[0]):
            data_raw[ses, var] = ndata[mtype.names[var]].flatten()[ses]

    # save the data as a pandas dataframe
    df = pd.DataFrame(data_raw, columns=data_headline)

    # %% Exclude data
    # %% Add other events if necessary before tidying
    
    # calculate port exit time estimate using PEtime and peDur, save this as a new variable
    df = df.assign(PExEst=df.x_K_PEtime + df.x_L_PEdur)
    # Exclude specific date
    df = df[df.date != 20210604]

    # %% melt() each event variable into eventType and eventTime
    # use explode() to reduce arrays of event timestamps into many rows with single element
    # retain hierarchical indexing (1 per file)

    # here am melting columns of behavioral events into single column of event label and column of individual timestamps (value_vars= want to melt)
    # ignore_index=False: to keep the original index (1 per file)
    dfEvent = df.melt(id_vars=['subject', 'Virus', 'Sex', 'date', 'laserDur', 'note'], value_vars=[
                      'x_K_PEtime', 'PExEst', 'x_S_lickTime', 'x_D_laserTime'], var_name='eventType', value_name='eventTime', ignore_index=False)

    # now explode event timestamp array
    dfEvent = dfEvent.explode('eventTime')

    # #visualize
    # eventCount= dfEvent.groupby(['subject','date'])['eventType'].value_counts()

    # g=sns.relplot(x='date',y=eventCount.values,hue='eventType',
    #               data=eventCount,kind="line",
    #               facet_kws={'sharey': False, 'sharex': True})
    # g.fig.subplots_adjust(top=0.9) # adjust the figure for title
    # g.fig.suptitle('Event counts over time pre deletion')

    # remove invalid/placeholder 0s
    # TODO: seem to be removing legitimate port exits with peDur==0, not sure how to deal with this so just excluding
    dfEvent = dfEvent[dfEvent.eventTime != 0]

    ## for visualizing- get the counts for each unique eventType for each file (group by subj & date)
    ## eventCount here is a  pandas.Series, which is a labelled set (multiindex= subject, date, eventType) of 1D values (each value here is a count of the unique event types for a given subject & date
    # eventCount = dfEvent.groupby(['subject', 'date'])[
    #     'eventType'].value_counts()


    # g = sns.relplot(x='date', y=eventCount.values, hue='eventType',
    #                 data=eventCount, kind="line",
    #                 facet_kws={'sharey': False, 'sharex': True})
    # g.fig.subplots_adjust(top=0.9)  # adjust the figure for title
    # g.fig.suptitle('Event counts over time by subject post deletion')

    # %% Tidy df org: All events in single column, sort by time by file, with fileID column and trialID column that matches trial 1-60 through each session.
    dfEventAll = df.melt(id_vars=['subject', 'RatID', 'Virus', 'Sex', 'date', 'laserDur', 'note'], value_vars=[

                         'x_K_PEtime', 'PExEst', 'x_S_lickTime', 'x_D_laserTime', 'x_H_DStime', 'x_I_NStime',
                         'x_G_laserOffTime'], var_name='eventType', value_name='eventTime', ignore_index=False)

    # now explode event timestamp array
    dfEventAll = dfEventAll.explode('eventTime')
    
    #checking type, for some reason laser session retaining matlab.opaque somewhere- trialState
    # for ev in dfEventAll.eventType.unique():
    #     print(ev,'times = type ',df[ev][0].dtype) #coming from most recent sessions with array w for some reason

    # remove invalid/placeholder 0s
    # TODO: seem to be removing legitimate port exits with peDur==0, not sure how to deal with this so just excluding
    dfEventAll = dfEventAll[dfEventAll.eventTime != 0]

    # before any removal/sorting is done, next issue is to match up laser state with cues.
    dfLaser = df.melt(id_vars=['subject', 'RatID', 'Virus', 'Sex', 'date', 'laserDur', 'note'], value_vars=[
                      'x_E_laserDStrial', 'x_F_laserNStrial'], var_name='laserType', value_name='laserState', ignore_index=False)
    # explode arrays into their own cells
    dfLaser = dfLaser.explode('laserState')

    # use cumcount() of DS & NS to match up laser status with cue time (redundant since we have a timestamp of laser on, but good verification still and easy grouping by trial)
    dfEventAll.index.name = 'fileID'
    dfEventAll.reset_index(inplace=True)
    dfEventAll.index.name= 'eventID'
    dfEventAll['g'] = dfEventAll[(dfEventAll.eventType == 'x_H_DStime') | (
        dfEventAll.eventType == 'x_I_NStime')].groupby('fileID').cumcount()  # .index

    dfLaser.index.name = 'fileID'
    dfLaser.reset_index(inplace=True)
    dfLaser['g'] = dfLaser[(dfLaser.laserType == 'x_E_laserDStrial') | (
        dfLaser.laserType == 'x_F_laserNStrial')].groupby('fileID').cumcount()

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
    dfEventAll['trialID'] = dfEventAll[(dfEventAll.eventType == 'x_H_DStime') | (
        dfEventAll.eventType == 'x_I_NStime')].groupby('fileID').cumcount()

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


    dfTidy = dfEventAll
    
    #TODO: round decimals to point of precision. 
    # #important because floats are imprecise and can lead to compounding errors
    # #first convert columns to string
    # dfTidy= dfTidy.astype(str)
    # #now loop through columns and convert to decimal (if we can, otherwise skip column)
    # import decimal
    # #set precision of decimal places to 2
    # decimal.DefaultContext.prec = 2 

    # for col in dfTidy.columns:
    #     try:
    #         dfTidy[col]=dfTidy[col].values.apply(decimal.Decimal)
    #     except:
    #         continue
                    
    # dfTidy.values= dfTidy.values.round(2)
    # visualize all events per fileq
    # sns.relplot(x='eventTime',y='fileID',hue='eventType', data= dfTidy, kind='scatter')
    
    # %% Identify events during each trial, assign them trialID matching the cue

    # TODO: for now assume cue duration = 10, but should get programmatically from A() array

    cueDur = 10

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
    dfTidy.loc[dfTidy.trialID.isnull(),'trialID']= -0.5


    # Can get a trial end time based on cue onset, then just check
    # event times against this
    dfTidy = dfTidy.sort_values(by=['fileID', 'eventTime']).copy()

    dfTidy.loc[:, 'trialEnd'] = dfTidy.eventTime[dfTidy.trialID >= 0].copy() + \
        cueDur

    dfTidy.loc[:, 'trialEnd'] = dfTidy.fillna(method='ffill').copy()
    
    ##TODO: for first ILI, make trial end the first cue onset
    # dfTidy.loc[dfTidy.trialID== -0.5,'trialEnd']= dfTidy.loc[dfTidy.loc[dfTidy.trialID==1].groupby(['fileID','trialID'])['eventTime'].cumcount()==0]

    # find events that occur after cue start but before cue duration end.
    # multiply those trialIDs by -1 so that they match the corresponding cue.
    # remaining events with negative trialIDs must have occurred somewhere in that ITI (or 'pre/post cue')

    dfTidy.loc[(dfTidy.trialEnd-dfTidy.eventTime >= 0) & ((dfTidy.trialEnd -
                                                          dfTidy.eventTime).apply(np.round) < 10.0), 'trialID'] = dfTidy.trialID.copy()*-1

    # remove trialType labels from events outside of cueDur (- trial ID or nan trialID)
    # for now labelling with "ITI", but could be nan
    dfTidy.loc[(dfTidy.trialID < 0) | (dfTidy.trialID.isnull()), 'trialType'] = 'ITI'

    

    #%% for lick-paired laser sessions, classify trials as laser on vs. laser off
    #since laser delivery in these sessions is contingent on lick behavior
    #use actual laser on & off times to define trials where laser delivered
        
    #cumcount each laser onsets per trial
    dfTidy['trialLaser'] = dfTidy[(dfTidy.laserDur=='Lick') & (dfTidy.eventType == 'x_D_laserTime')].groupby([
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
    dfLaser= dfTidy[((dfTidy.laserDur=='Lick') & ((dfTidy.eventType=='x_H_DStime') | (dfTidy.eventType=='x_I_NStime')))].reset_index().set_index(['fileID','trialID'])
    
    # combine laserState and laserType into one variable for labelling each trial: trialType
    # #only include the laser sessions
    dfLaser.trialType= dfLaser.laserType + '_' + laserCount.astype(str).copy()
    
    #set index to eventID before assignment
    dfLaser= dfLaser.reset_index().set_index('eventID')
    
    #insert trialTypes using eventID as index
    dfTidy.loc[dfLaser.index.get_level_values(0),'trialType']= dfLaser.trialType
    
    #ffill trialType for each trial
    dfTidy.loc[dfTidy.trialID>=0,'trialType']= dfTidy[dfTidy.trialID>=0].groupby('fileID')['trialType'].fillna(method='ffill').copy()

    # drop redundant columns
    dfTidy = dfTidy.drop(columns=['laserType', 'laserState']).copy()

# %% Preliminary data analyses
# Event latency, count, and behavioral outcome for each trial

#TODO: Lick 'cleaning' to eliminate invalid licks (are they in port, is ILI within reasonable range)


#Calculate latency to each event in trial (from cue onset). based on trialEnd to keep it simple
  # trialEnd is = cue onset + cueDur. So just subtract cueDur for cue onset time  
    dfTidy.loc[dfTidy.trialID>=0, 'eventLatency'] = (
        (dfTidy.eventTime)-(dfTidy.trialEnd-cueDur)).copy()

    #for 'ITI' events, calculate latency based on last trial end (not cue onset)
    dfTidy.loc[dfTidy.trialID<0, 'eventLatency'] = (
        (dfTidy.eventTime)-(dfTidy.trialEnd)).copy()
    
    #TODO: exception needs to be made for first ITI
    #for now fill w nan
    dfTidy.loc[dfTidy.trialID== -0.5, 'eventLatency']= np.nan
    
#Count events in each trial 
    #use cumcount() of event times within file & trial 
    dfTidy['trialPE'] = dfTidy.loc[(dfTidy.eventType == 'x_K_PEtime')].groupby([
    'fileID', 'trialID'])['eventTime'].cumcount().copy()
    
    dfTidy['trialLick'] = dfTidy.loc[(dfTidy.eventType == 'x_S_lickTime')].groupby([
        'fileID', 'trialID']).cumcount().copy()
    
#Define behavioral (pe,lick) outcome for each trial. For my lick+laser sessions I need 
#to isolate trials with both a PE+lick to measure effect of laser

    #For each trial (trialID >=0),
    #count the number of PEs per trial. if >0, they entered the port and earned sucrose. If=0, they did not.
    #since groupby counting methods don't work well with nans, using nunique() 
    # peOutcome= dfTidy.loc[dfTidy.trialID>=0].groupby(['fileID','trialID'],dropna=False)['trialPE'].nunique()
    #do for all trials
    outcome= dfTidy.groupby(['fileID','trialID'],dropna=False)['trialPE'].nunique()

    #naming "trialOutcomeBeh" for now to distinguish between behavioral outcome and reward outcome if needed later
    trialOutcomeBeh= outcome.copy()
    
    trialOutcomeBeh.loc[outcome>0]='PE'
    trialOutcomeBeh.loc[outcome==0]='noPE'
    
    #now do the same for licks
    outcome= dfTidy.groupby(['fileID','trialID'],dropna=False)['trialLick'].nunique()
    
    #add lick outcome + PE outcome for clarity #if it doesn't say '+lick', then none was counted
    trialOutcomeBeh.loc[outcome>0]=trialOutcomeBeh.loc[outcome>0]+ '+' + 'lick'
    
    #set index to file,trial and
    #fill in matching file,trial with trialOutcomeBeh
    #TODO: I think there is a more efficient way to do this assignment, doens't take too long tho

    dfTidy= dfTidy.reset_index().set_index(['fileID','trialID'])
    
    dfTidy.loc[trialOutcomeBeh.index,'trialOutcomeBeh']= trialOutcomeBeh

    #reset index to eventID
    dfTidy= dfTidy.reset_index().set_index(['eventID'])
    
      #%% Remove Lick+Laser trials without PE+Lick
      #TODO: what is the best way to deal with this? 
      #could make a new column or trialType labels for just lick+laser sessions? 
      #or, could also just remove "laser off" trials without PE+lick- easier, doing this
      
      #However, instead of changing dfTidy itself just do it locally later where necessary
      
    #Correct comparison between laser ON and laser OFF trials for lick-paired should only include trials with PE+Lick
    
    #noPE+lick laser trials exist, probably from first bad session without PE gate?
    print(dfTidy.loc[(dfTidy.laserDur=='Lick') & (dfTidy.trialType=='x_E_laserDStrial_1')].trialOutcomeBeh.unique())
    print(dfTidy.loc[(dfTidy.laserDur=='Lick') & (dfTidy.trialType=='x_F_laserNStrial_1')].trialOutcomeBeh.unique())
    
    
    #for overall pe and lick probability, make a copy to keep all trials
    dfTidy2= dfTidy.copy()

    
    # #retain only trials with PE+lick for comparison
    # #instead of making new df, just remove from dfTidy
    # dfTidy.loc[dfTidy.laserDur=='Lick',:]= dfTidy.loc[(dfTidy.laserDur=='Lick') & (dfTidy.trialOutcomeBeh=='PE+lick')]
    
    
    # %% Analysis & visualization

    # visualize using seaborn
    import seaborn as sns
    import matplotlib.pyplot as plt

    # paired seems nice for comparing conditions (laser on vs off)
    sns.set_palette('Paired')
    
   #manually defining color order so that paired color scheme looks nice
    trialOrder =['x_E_laserDStrial_0', 'x_E_laserDStrial_1',
       'x_F_laserNStrial_0', 'x_F_laserNStrial_1','ITI']


  #%% Exploratory data vis & profiling
   #visualize the raw data, identify patterns and outliers
    dfTidy.date= dfTidy.date.astype('string')
   #%% Check for outlier sessions/event counts
    # convert ratID to categorical data type so seaborn uses divergent color hues
    dfTidy.RatID = dfTidy.RatID.astype('category')
    sns.set_palette('tab20')  #good for plotting by many subj

    
    #I know that lick count was absurdly high (>9000) due to liquid shorting lickometer on at least 1 session
    #visualize event counts by session to ID outliers
    #not interested in some events (e.g. # cues is fixed), remove those
    dfPlot= dfTidy.loc[(dfTidy.eventType!='x_I_NStime') & (dfTidy.eventType!='x_H_DStime') & (dfTidy.eventType!='PExEst') & (dfTidy.eventType!='x_G_laserOffTime')] 
    
    #count of each event type by date and subj
    dfPlot= dfPlot.groupby(['RatID','date', 'eventType'])['eventTime'].count().reset_index()
    
    
    g= sns.relplot(data=dfPlot, col='eventType', x='date', y='eventTime', hue='RatID', kind='line',
                    facet_kws={'sharey': False, 'sharex': True})
    g.fig.subplots_adjust(top=0.9)  # adjust the figure for title
    g.fig.suptitle('Total event count across sessions by type- check for outliers')
    g.set_ylabels('# of events')
    g.set_ylabels('session')
    
      #%% #For lick+laser, plot trialType counts
      #since laser delivery is contingent on animal's licking, should check to see how many trials they are actually getting laser

    #subset data and save as intermediate variable dfGroup
    dfGroup= dfTidy.copy()
    #retain only trials with PE+lick for comparison
    dfGroup.loc[dfGroup.laserDur=='Lick',:]= dfGroup.loc[(dfGroup.laserDur=='Lick') & (dfGroup.trialOutcomeBeh=='PE+lick')].copy()

    #get count of each trialType by subject and date
    dfPlot= dfGroup.loc[(dfGroup.laserDur=='Lick') & ((dfGroup.eventType=='x_I_NStime') | (dfGroup.eventType=='x_H_DStime'))].groupby(['RatID','date','trialType'])['eventTime'].count().reset_index()
    
    
    #Plot count of trial types for each session
    g= sns.relplot(data=dfPlot, col='RatID', col_wrap=4, x='date', y='eventTime', hue='trialType', hue_order=trialOrder, kind='line')
                    # facet_kws={'sharey': False, 'sharex': True})
    g.fig.subplots_adjust(top=0.9)  # adjust the figure for title
    g.fig.suptitle('Total trial type count across LICK+laser sessions')
    g.set_ylabels('# of events')
    g.set_ylabels('session')
    
    #total count of each trial type across all sessions for each subject
    sns.set_palette('Paired')  # good for comparing two groups (laser on vs off)
    
    g= sns.catplot(data=dfPlot, x='RatID', y='eventTime', hue='trialType', hue_order=trialOrder, kind='bar')
                    # facet_kws={'sharey': False, 'sharex': True})
    g.fig.subplots_adjust(top=0.9)  # adjust the figure for title
    g.fig.suptitle('Total trial type count across LICK+laser sessions')
    g.set_ylabels('Total trial count (lick+laser sessions)')
    g.set_xlabels('Subject')
    
    #Use trialLicks to get # of licks per trial by type, then plot distribution by trial type
    
    dfPlot = dfGroup[(dfGroup.laserDur=='Lick')].copy()
        #transform keeps original index?
    lickCount=dfPlot.groupby(['fileID','trialID','trialType'])['trialLick'].transform('count')

    #aggregated measure, but trialIDs repeat, so just restrict to first one   
    trialAgg= dfPlot.groupby(['fileID','trialID','trialType'])['trialID'].cumcount()==0
    dfPlot= dfPlot.loc[trialAgg]
    
    g= sns.displot(data=dfPlot, x=lickCount, hue='trialType', hue_order=trialOrder, kind='hist', stat="density", common_norm=False, kde=True, multiple='dodge')
    g.fig.subplots_adjust(top=0.9)  # adjust the figure for title
    g.fig.suptitle('Lick count by trial type: LICK+laser sessions')
    g.set_ylabels('Lick count (lick+laser sessions)')
    

    #check inter-lick interval
    #All subj distribution of ILI (inter-lick interval)
    #only include trialLick~=nan
    dfPlot = dfGroup[dfGroup.trialLick.notnull()].copy()
    #calculate ILI by taking diff() of latencies
    ili= dfPlot.groupby(['fileID','trialID','trialType'])['eventLatency'].diff()

    #bar- all subj
    g= sns.catplot(data=dfPlot, y=ili, x='trialType',  kind='bar', row='Virus', order=trialOrder)
    g.fig.subplots_adjust(top=0.9)  # adjust the figure for title
    g.fig.suptitle('ILI by trial type; LICK+Laser; all subj')
    g.set_ylabels('ILI (s)')
    g.set(ylim=(0,0.5))
    

    # %% Plot individual subject ILIs: laser OFF sessions (laserDur=="Off").
    # for plot across sessions of individual rats, change color to tab20 and make background white to help colors pop...default color palettes have blues that I can't distinguish
    
    #trial-based, ignoring ITI
    # dfPlot = dfTidy[(dfTidy.trialID >= 0) & (dfTidy.laserDur=="Off")].copy()
    #trial-based, including ITI
    dfPlot = dfTidy[(dfTidy.laserDur=='Off')].copy()

    #All subj distribution of ILI (inter-lick interval)
    #only include trialLick~=nan
    dfPlot = dfPlot[dfPlot.trialLick.notnull()].copy()
    #calculate ILI by taking diff() of latencies
    ili= dfPlot.groupby(['fileID','trialID','trialType'])['eventLatency'].diff()

    #bar- all subj
    g= sns.catplot(data=dfPlot, y=ili, x='trialType',  kind='bar', order=trialOrder)
    g.fig.subplots_adjust(top=0.9)  # adjust the figure for title
    g.fig.suptitle('ILI by trial type; laser OFF; all subj')
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
    g.fig.suptitle('ILI by trial type; laser OFF; all subj')
    g.set_ylabels('ILI (s)')
    g.set(ylim=(0,0.5))

    
    #ecdf- all subj
    g= sns.displot(data=dfPlot, x=ili, hue='trialType',  kind='ecdf', hue_order=trialOrder)
    g.fig.subplots_adjust(top=0.9)  # adjust the figure for title
    g.fig.suptitle('ILI by trial type; laser OFF; all subj')
    g.set_xlabels('ILI (s)')
    g.set(xlim=(0,1))

    
    #Individual distribution of ILI (inter-lick interval)
    #only include trialLick~=nan
    dfPlot = dfPlot[dfPlot.trialLick.notnull()].copy()
    #calculate ILI by taking diff() of latencies
    ili= dfPlot.groupby(['fileID','trialID','trialType'])['eventLatency'].diff()
    #bar- individual subj
    g= sns.catplot(data=dfPlot, y=ili, x='RatID', hue='trialType',  kind='bar', hue_order=trialOrder)
    g.fig.subplots_adjust(top=0.9)  # adjust the figure for title
    g.fig.suptitle('ILI by trial type; laser OFF; individual subj')
    g.set_ylabels('ILI (s)')
    g.set(ylim=(0,1))

    #%% Plot individual subject First lick latencies (time from cue or trialEnd if ITI events)
    # should represent "baseline" behavior  without laser
          
    #trial-based, ignoring ITI
    # dfPlot = dfTidy[(dfTidy.trialID >= 0) & (dfTidy.laserDur=="Off")].copy()
    #trial-based, including ITI
    dfPlot = dfTidy[(dfTidy.laserDur=="Off")].copy()

    #All subj distribution of ILI (inter-lick interval)
    #only include first trialLick ==0
    dfPlot = dfPlot[dfPlot.trialLick==0].copy()


    #bar- all subj
    #median here takes awhile
    g= sns.catplot(data=dfPlot, y='eventLatency', x='trialType', kind='bar', order=trialOrder)
    g.fig.subplots_adjust(top=0.9)  # adjust the figure for title
    g.fig.suptitle('first lick latencies by trial type; laser OFF; all subj')
    g.set_ylabels('lick latency from epoch start (s)')

    
    # #hist- all subj
    # ili= ili.astype('float') #allows KDE, but kde here takes awhile
    # g= sns.displot(data=dfPlot, x=ili, hue='trialType',  kind='hist', stat="density", common_norm=False, kde=True, multiple='layer', hue_order=np.sort(dfPlot.trialType.unique()))
    # g.fig.subplots_adjust(top=0.9)  # adjust the figure for title
    # g.fig.suptitle('ILI by trial type; laser OFF; all subj')
    # g.set_xlabels('ILI (s)')
    # g.set(xlim=(0,1))
    
    #box- all subj
    g= sns.catplot(data=dfPlot, y='eventLatency', x='trialType',  kind='box', order=trialOrder)
    g.fig.subplots_adjust(top=0.9)  # adjust the figure for title
    g.fig.suptitle('First Lick latencies by trial type; laser OFF; all subj')
    g.set_ylabels('lick latency from epoch start (s)')

    
    #ecdf- all subj'[]
    g= sns.displot(data=dfPlot, x='eventLatency', hue='trialType',  kind='ecdf', hue_order=trialOrder)
    g.fig.subplots_adjust(top=0.9)  # adjust the figure for title
    g.fig.suptitle('First Lick latencies by trial type; laser OFF; all subj')
    g.set_xlabels('lick latency from epoch start (s)')

    
    #Individual distribution of ILI (inter-lick interval)
    #only include trialLick~=nan 
    #bar- individual subj
    g= sns.catplot(data=dfPlot, y='eventLatency', x='RatID', hue='trialType',  kind='bar', hue_order=trialOrder)
    g.fig.subplots_adjust(top=0.9)  # adjust the figure for title
    g.fig.suptitle('First Lick latencies by trial type; laser OFF; individual subj')
    g.set_ylabels('lick latency from epoch start (s)')

        

        # %% Effect of cue+laser on current trial PE behavior
        
    ##TODO: PE prob for lick+laser trials will always be 1, should look at next trial
        
    #select data corresponding to first PE from valid trials
    dfPlot = dfTidy[(dfTidy.trialID >= 0) & (dfTidy.trialPE == 0)].copy()
    
    # PE latency: virus x laserDur
    g = sns.displot(data=dfPlot, x='eventLatency', hue='trialType',
                    col='laserDur', row='Virus', kind='ecdf', hue_order= trialOrder)
    g.fig.suptitle('First PE latency by trial type')
    g.set_ylabels('First PE latency from epoch start (s)')
    
    #PE latency: virus individual subj
    g=sns.catplot(data=dfPlot,y='eventLatency',hue='trialType', x='RatID', kind='bar', hue_order=trialOrder)
    g.fig.suptitle('First PE latency by trial type')
    g.set_ylabels('First PE latency from epoch start (s)')
    
      #PE latency:  individual subj CUE+laser
    g=sns.displot(data=dfPlot.loc[dfPlot.laserDur=='10'], col='subject', col_wrap=4, x='eventLatency',hue='trialType', kind='ecdf', hue_order=trialOrder)
    g.fig.suptitle('First PE latency by trial type; laser + CUE')
    g.set_ylabels('First PE latency from epoch start (s)')
    
    #%% Calculate PE probability of each trial type. This is normalized so is more informative than count of trials. 
    
    #TODO: clean up and move higher to prelim analysis section
    
    # outcomeProp= dfPlot[dfPlot.trialOutcomeBeh=='PE'].groupby(['fileID','trialID'])['trialOutcomeBeh'].count().index

    
    #calculate Proportion of trials with PE out of all trials for each trial type
    #can use nunique() to get count of unique trialIDs with specific PE outcome per file
    #given this, can calculate Probortion as #PE/#PE+#noPE
   
    #subset data and save as intermediate variable dfGroup
    dfGroup= dfTidy.copy()
    #for Lick+laser sessions, retain only trials with PE+lick for comparison
    dfGroup.loc[dfGroup.laserDur=='Lick',:]= dfGroup.loc[(dfGroup.laserDur=='Lick') & (dfGroup.trialOutcomeBeh=='PE+lick')].copy()
   
    dfPlot= dfGroup.copy() 
    
    #excluded trials from lick+laser sessions are all nan. don't include
    outcomes= dfTidy.loc[dfTidy.trialOutcomeBeh.notnull()].trialOutcomeBeh.unique()
    
    #TODO: optimize this- combine outcomes here into one variable
    #using apply() might help? or pivot?
    
    # tester[outcomes]= dfPlot[(dfPlot.trialOutcomeBeh==outcomes)].reset_index().groupby(
    #     ['fileID','trialType','trialOutcomeBeh'])['trialID'].nunique()
    
    test1= dfPlot[(dfPlot.trialOutcomeBeh=='PE')].reset_index().groupby(['fileID','trialType','trialOutcomeBeh'])['trialID'].nunique()
    test1.name= 'PE'
    test2= dfPlot[dfPlot.trialOutcomeBeh=='noPE'].reset_index().groupby(['fileID','trialType','trialOutcomeBeh'])['trialID'].nunique()
    test2.name= 'noPE'    
    
    test5= dfPlot[(dfPlot.trialOutcomeBeh=='PE+lick')].reset_index().groupby(['fileID','trialType','trialOutcomeBeh'])['trialID'].nunique()
    test5.name= 'PE+lick'
    test8= dfPlot[(dfPlot.trialOutcomeBeh=='noPE+lick')].reset_index().groupby(['fileID','trialType','trialOutcomeBeh'])['trialID'].nunique()
    test8.name= 'noPE+lick'
 
           
    ##num of unique trials per trial type per session, but still cant sum
    test6= pd.concat((test1,test2,test5,test8),ignore_index=False,axis=1)
    
    ##reset index and groupby trialType so we can sum across columns
    test7= test6.reset_index().groupby(['fileID','trialType'])[outcomes].sum()
 
    ##calculate proportion for each trial type: num trials/total num trials
    outcomeProp= test7.divide(test7.sum(axis=1),axis=0)
    
    #melt() into single column w label
    test8= outcomeProp.reset_index().melt(id_vars=['fileID','trialType'],var_name='trialOutcomeBeh',value_name='outcomePropFile')
    
    #assign back to df by merging
    #TODO: can probably be optimized
    dfTidy= dfTidy.merge(test8,'right', on=['fileID','trialType','trialOutcomeBeh'])
    
    #%% visualize peProp
    
    
    #subset data and save as intermediate variable dfGroup
    dfGroup= dfTidy.copy()
    #for Lick+laser sessions, retain only trials with PE+lick for comparison
    dfGroup.loc[dfGroup.laserDur=='Lick',:]= dfGroup.loc[(dfGroup.laserDur=='Lick') & (dfGroup.trialOutcomeBeh=='PE+lick')].copy()
   
    
    #select data     
    dfPlot = dfTidy[(dfGroup.trialID >= 0)].copy()
    #Plot probability of PE by trialType 
    
    #get only PE outcomes
    # dfPlot.reset_index(inplace=True)
    dfPlot= dfPlot.loc[(dfPlot.trialOutcomeBeh=='PE') | (dfPlot.trialOutcomeBeh=='PE+lick')].copy()
    
    #since we calculated aggregated proportion across all trials in session,
    #take only first index. Otherwise repeated observations are redundant
    dfPlot= dfPlot.groupby(['fileID','trialType','trialOutcomeBeh']).first().copy()
    
    
    #sum together both PE and PE+lick for total PE prop
    # dfPlot['outcomePropFile']= dfPlot.groupby(['fileID'])['outcomePropFile'].sum().copy()
    
    dfPlot['propPE']= dfPlot.groupby(['fileID','trialType'])['outcomePropFile'].sum().copy()

    #get an aggregated x axis for files per subject
    fileAgg= dfPlot.reset_index().groupby(['subject','fileID','trialType']).cumcount().copy()==0
    
    #since grouping PE and PE+lick, we still have redundant observations
    #retain only 1 per trial type per file
    dfPlot= dfPlot.reset_index().loc[fileAgg]

   #Plot
    #one line per per trialType per subj would be ideal. In subplots
    #manual control here of facetgrid and titles (i). 
    #Manual:
    sns.set_palette('tab20')
    g = sns.FacetGrid(dfPlot, col='subject', hue='trialType', hue_order=trialOrder, col_wrap=4)

    # Add the line over the area with the plot function
    g = g.map(plt.plot, 'fileID', 'propPE')
    
    # Control the title of each facet
    g = g.set_titles("{col_name}")
     
    # Add a title for the whole plot
    plt.subplots_adjust(top=0.9)
    g = g.fig.suptitle('Evolution of the propPE in subjects by trialType')
    
     
    #same with relplot:
    g= sns.relplot(data=dfPlot, x='fileID', y='propPE', col='subject', col_wrap=4, hue='trialType', hue_order=trialOrder, kind='line')
    # g.map(plt.axhline, y=0.6, color=".7", dashes=(2, 1), zorder=0)
    g.set_titles('{col_name}')
    g.fig.suptitle('Evolution of the propPE in subjects by trialType')
    g.tight_layout(w_pad=0)
    
    # #plot by laserDur
    # g= sns.relplot(data=dfPlot, x='date', y='propPE', col='subject', col_wrap=4, hue='trialType', hue_order=trialOrder, style='laserDur', kind='line')
    # # g.map(plt.axhline, y=0.6, color=".7", dashes=(2, 1), zorder=0)
    # g.set_titles('{col_name}')
    # g.fig.suptitle('Evolution of the propPE in subjects by trialType')
    # g.tight_layout(w_pad=0)
    
    # #group by virus
    # g= sns.relplot(data=dfPlot, x='date', y='propPE', row='Virus', hue='trialType', hue_order=trialOrder, style='laserDur', kind='line')
    # # g.map(plt.axhline, y=0.6, color=".7", dashes=(2, 1), zorder=0)
    # g.set_titles('{row_name}')
    # g.fig.suptitle('Evolution of the propPE in subjects by trialType')
    # g.tight_layout(w_pad=0)
    
    # #show individual subj
    # # g= sns.relplot(data=dfPlot, x='date', y='propPE', row='Virus', units='subject', estimator=None, hue='trialType', hue_order=trialOrder, style='laserDur', kind='line')

    #subjects run different session types on same day, so can't plot by day across subjects
    g= sns.relplot(data=dfPlot, x='date', y='propPE', col='subject', col_wrap=4, hue='trialType', hue_order=trialOrder, style='laserDur', kind='line')
    # g.map(plt.axhline, y=0.6, color=".7", dashes=(2, 1), zorder=0)
    g.set_titles('{col_name}')
    g.fig.suptitle('Evolution of the propPE in subjects by trialType')
    g.tight_layout(w_pad=0)
    
    g=sns.catplot(data= dfPlot, x='laserDur', y='propPE', hue='trialType', hue_order=trialOrder, col='subject', col_wrap=4, kind='bar')
    

    #%% aggregate DS and NS trial types
    # like above but recalculating peProp for combined laser off&on
     #select data  
    dfPlot = dfTidy[(dfTidy.trialID >= 0)].copy()   
    
    #make a dict to swap values
    trialTypes= {'x_E_laserDStrial_0':'DS', 'x_E_laserDStrial_1':'DS', 'x_F_laserNStrial_0':'NS',
       'x_F_laserNStrial_1':'NS'}
    dfPlot.loc[:,'trialType']= dfPlot.trialType.replace(trialTypes).copy()
    
    #get only PE outcomes
    # dfPlot.reset_index(inplace=True)
    dfPlot= dfPlot.loc[(dfPlot.trialOutcomeBeh=='PE') | (dfPlot.trialOutcomeBeh=='PE+lick')].copy()
    
    #since we calculated aggregated proportion across all trials in session,
    #take only first index. Otherwise repeated observations are redundant
    dfPlot= dfPlot.groupby(['fileID','trialType','trialOutcomeBeh']).first().copy()
    
    
    #sum together both PE and PE+lick for total PE prop
    # dfPlot['outcomePropFile']= dfPlot.groupby(['fileID'])['outcomePropFile'].sum().copy()
    
    dfPlot['propPE']= dfPlot.groupby(['fileID','trialType'])['outcomePropFile'].sum().copy()

    #get an aggregated x axis for files per subject
    fileAgg= dfPlot.reset_index().groupby(['subject','fileID','trialType']).cumcount().copy()==0
    
    #since grouping PE and PE+lick, we still have redundant observations
    #retain only 1 per trial type per file
    dfPlot= dfPlot.reset_index().loc[fileAgg]
 

    #now get just first value
    # dfPlot= dfPlot.loc[dfPlot.groupby(['fileID','trialType']).cumcount()==0]    
    
    #visualize
    sns.set_palette('tab10')

    g= sns.relplot(data=dfPlot, x='date', y='propPE', row='Virus', hue='trialType', style='laserDur', kind='line')
    g.map(plt.axhline, y=0.6, color=".2", dashes=(2, 1), zorder=0, linewidth=4)



    
    #%% Above gives us one value per session of PE probability
    # #would be good to have individual trials for variance?
    
    # #count is same as proportion so not really helpful?
    
    # dfPlot= dfTidy.copy()
    
    # #aggregated measure, but trialIDs repeat, so just restrict to first one
    # trialAgg= dfPlot.groupby(['fileID','trialID'])['trialID'].cumcount()==0

    # dfPlot= dfPlot.loc[trialAgg].copy() 
    
    # #count of trials for each trialType
    # dfPlot= dfPlot.groupby(['fileID','trialType'])['trialOutcomeBeh'].value_counts()
    
    # #for some reason value_counts() isn't giving 0 count for all categories. Fill these with 0 so we have a count for each possibility
    # dfPlot= dfPlot.unstack(fill_value=0).stack().reset_index(name='count')
    
    # #merge w other data
    # dfPlot= dfTidy.merge(dfPlot,'right', on=['fileID','trialType','trialOutcomeBeh'])


    #%% TODO: evolution within session (typical trial progression)
    
    
      #get data, only trials (not ITI)
    dfPlot= dfTidy.loc[dfTidy.trialID>=0].copy()
    
    sns.set_palette('Paired')
    
    #aggregated measure, but trialIDs repeat, so just restrict to first one
    trialAgg= dfPlot.groupby(['fileID','trialID'])['trialID'].cumcount()==0

    dfPlot= dfPlot.loc[trialAgg].copy()   
       
   #counts of each trial type by trialID
   #trial count seems biased? many more DS?
    # dfPlot= dfPlot.groupby(['subject','trialID','trialType'])['laserDur'].value_counts()#.reset_index(name='count')
    
    dfPlot= dfPlot.groupby(['subject','trialID','laserDur'])['trialType'].value_counts()
    
    #for some reason value_counts() isn't giving 0 count for all categories. Fill these with 0 so we have a count for each possibility
    dfPlot= dfPlot.unstack(fill_value=0).stack().reset_index(name='count')

    sns.relplot(data=dfPlot, row='laserDur', x='trialID', y='count', hue='trialType',  hue_order= trialOrder, kind='line')
    
    #####repeat for behavior outcome
      #get data, only trials (not ITI)
    dfPlot= dfTidy.loc[dfTidy.trialID>=0].copy()
    
    sns.set_palette('Paired')
    
    #aggregated measure, but trialIDs repeat, so just restrict to first one
    trialAgg= dfPlot.groupby(['fileID','trialID'])['trialID'].cumcount()==0

    dfPlot= dfPlot.loc[trialAgg].copy()   
       
   #counts of each trial type by trialID
   #trial count seems biased? many more DS?
    # dfPlot= dfPlot.groupby(['subject','trialID','trialType'])['laserDur'].value_counts()#.reset_index(name='count')
    
    dfPlot= dfPlot.groupby(['subject','trialID','laserDur','trialType'])['trialOutcomeBeh'].value_counts()
    
    #for some reason value_counts() isn't giving 0 count for all categories. Fill these with 0 so we have a count for each possibility
    dfPlot= dfPlot.unstack(fill_value=0).stack().reset_index(name='count')

    sns.relplot(data=dfPlot, row='laserDur', x='trialID', y='count', hue='trialOutcomeBeh', style='trialType', kind='line')
    
    
    ###
   #  #get data, only trials (not ITI)
   #  dfPlot= dfTidy.loc[dfTidy.trialID>=0].copy()
       
   #  #aggregated measure, but trialIDs repeat, so just restrict to first one
   #  trialAgg= dfPlot.groupby(['fileID','trialID']).cumcount()==0    
    
   #  dfPlot= dfPlot.loc[trialAgg]
    
   #  #estimate response profile by subject and laserDur (session type), and trialType
   #  dfPlot= dfPlot.groupby(['subject','laserDur','trialType','trialID'])['trialOutcomeBeh'].value_counts().reset_index(name='count')


   #  sns.set_palette('tab20')
    
   #  g=sns.relplot(data=dfPlot, col='subject', col_wrap=4, x='trialID', y='count', hue='trialOutcomeBeh', kind='line')
    
   #  #TODO: UNITS should be fileID
   #  dfPlot= dfTidy.merge(dfPlot, how='right', on=['subject','laserDur','trialType','trialID']).copy()
    
   #  g=sns.relplot(data=dfPlot, units='fileID', estimator=None, x='trialID', y='count', hue='trialOutcomeBeh', kind='line')
        
   #  for sesType in dfPlot.laserDur.unique():
   #      g=sns.displot(data=dfPlot.loc[dfPlot.laserDur==sesType], col='subject', col_wrap=4, 
   #                    x='trialID', hue='trialOutcomeBeh', kind='hist', 
   #                    stat='count', multiple='dodge')
   #      # g=sns.relplot(data=dfPlot.loc[dfPlot.laserDur==sesType], col='subject', col_wrap=4, x='trialID', y='count', hue='trialOutcomeBeh', kind='line')
        
   #      g.set_titles('{col_name}')
   #      g.fig.suptitle('Evolution of behavior within sessions by trialID; laser='+sesType)
   #      g.tight_layout(w_pad=0)
    
   #  sns.catplot(data=dfPlot, x='trialID', y='count', hue='trialOutcomeBeh', kind='bar')
    
 
    
   #  #
   #  sns.relplot(data=dfPlot,x='trialID',y='trialOutcomeBeh')
    
   # #count # of each outcomes?
   #  count= dfPlot.groupby(['fileID','trialType'])['trialOutcomeBeh'].value_counts().unstack()
    
    
   #  #merge 
   #  test = dfPlot.merge(count,
   #             left_on=['fileID','trialType'], 
   #             right_index=True)
    
    
   #  #set index for plotting
   #  dfPlot=dfPlot.set_index(['fileID','trialType'])
    
   #  sns.catplot(data=dfPlot, x='fileID', y=count,hue='trialOutcomeBeh', kind='bar')
    
    # %% Effect of laser on current trial lick behavior
       #select data corresponding to first lick from valid trials
    dfPlot = dfTidy[(dfTidy.trialID >= 0) & (dfTidy.trialLick == 0)].copy()
    
    # lick latency: virus x laserDur
    g = sns.displot(data=dfPlot, x='eventLatency', hue='trialType',
                    col='laserDur', row='Virus', kind='ecdf', hue_order= trialOrder)
    g.fig.suptitle('First lick latency by trial type; laser + CUE')
    g.set_ylabels('First lick latency from epoch start (s)')
    
    #lick latency: virus individual subj
    g=sns.catplot(data=dfPlot,y='eventLatency',hue='trialType', x='RatID', kind='bar', hue_order=trialOrder)
    g.fig.suptitle('First lick latency by trial type; laser + CUE')
    g.set_ylabels('First lick latency from epoch start (s)')
    
    # %% examine lick+laser on licks
    
     #subset data and save as intermediate variable dfGroup
    dfGroup= dfTidy.copy()
    #for Lick+laser sessions, retain only trials with PE+lick for comparison
    dfGroup.loc[dfGroup.laserDur=='Lick',:]= dfGroup.loc[(dfGroup.laserDur=='Lick') & (dfGroup.trialOutcomeBeh=='PE+lick')].copy()
   
    dfPlot = dfGroup[(dfGroup.laserDur=='Lick')].copy()
    
    #All subj distribution of ILI (inter-lick interval)
    #only include trialLick~=nan
    dfPlot = dfPlot[dfPlot.trialLick.notnull()].copy()
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
    #only include trialLick~=nan
    dfPlot = dfPlot[dfPlot.trialLick.notnull()].copy()
    #calculate ILI by taking diff() of latencies
    ili= dfPlot.groupby(['fileID','trialID','trialType'])['eventLatency'].diff()
    #bar- individual subj
    g= sns.catplot(data=dfPlot, y=ili, x='RatID', hue='trialType',  kind='bar', hue_order=trialOrder)
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
    lickCount= dfPlot.groupby(['fileID','trialID','trialType'])['trialLick'].transform('count').copy()
    
    #get only one aggregated value per trial
    lickCount= lickCount.loc[trialAgg].copy()
    dfPlot= dfPlot.loc[trialAgg].copy()
        
    g= sns.catplot(data=dfPlot, y=lickCount,x='RatID',hue='trialType',kind='bar',hue_order=trialOrder)
    g.fig.subplots_adjust(top=0.9)  # adjust the figure for title
    g.fig.suptitle('Lick count by trial type; laser+LICK; individual subj')
    g.set_ylabels('count of licks per trial')
    g.set_xlabels('subject')
    
    #bar with overlay individual trial overlay
    plt.figure()
    plt.subplot(1, 1, 1)
    sns.barplot(data=dfPlot, y=lickCount,x='RatID',hue='trialType',hue_order=trialOrder)
    sns.stripplot(data=dfPlot, y=lickCount,x='RatID',hue='trialType',hue_order=trialOrder, dodge=True,size=2)
    
    ##Compare to CUE and laser OFF
    ##TODO: error here
    # dfPlot = dfTidy.copy() #all data
    
    # #need an index for aggregated trial variables- since trialID repeats we need to restrict observations to first otherwise we'll plot redundant data and stats will be off
    # trialAgg= (dfPlot.groupby(['fileID','trialID','trialType'])['trialID'].cumcount()==0).copy()
    # #transform keeps original index
    # lickCount= dfPlot.groupby(['fileID','trialID','trialType'])['trialLick'].transform('count').copy()
    
    # #get only one aggregated value per trial
    # lickCount= lickCount.loc[trialAgg].copy()
    # dfPlot= dfPlot.loc[trialAgg].copy()
    
    # g= sns.catplot(data=dfPlot, row='laserDur', y=lickCount,x='RatID',hue='trialType',kind='bar',hue_order=trialOrder)
    
  
    
    #%% Use pandas profiling on event counts
    ##This might be a decent way to quickly view behavior session results if automated
    
    ##Unstack() the groupby output for a dataframe we can profile
    # dfPlot= dfTidy
    # dfPlot= dfPlot.groupby(['RatID','date','eventType'])['eventTime'].count().unstack()
    # #add trialType counts
    # dfPlot= dfPlot.merge(dfTidy.loc[(dfTidy.eventType=='x_I_NStime') | (dfTidy.eventType=='x_H_DStime')].groupby(['RatID','date','trialType'])['eventTime'].count().unstack(),left_index=True,right_index=True)

    # from pandas_profiling import ProfileReport

    # profile = ProfileReport(dfPlot, title='Event Count by Session Pandas Profiling Report', explorative = True)

    # # save profile report as html
    # profile.to_file('pandasProfileEventCounts.html')
    
  # %% Try Pandas_profiling report
    # note- if you are getting errors with ProfileReport() and you installed using conda, remove and reinstall using pip install

    # from pandas_profiling import ProfileReport

    # profile = ProfileReport(dfTidy, title='Pandas Profiling Report', explorative = True)

    # # save profile report as html
    # profile.to_file('pandasProfile.html')
