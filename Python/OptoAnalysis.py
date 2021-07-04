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
    
    # import matlab struct from .mat
    #setting squeeze_me argument=true, otherwise each element seems to get nested in individual arrays
    # matContents= sio.loadmat(r'Z:\Dakota\MEDPC\Downstairs\vp-vta-stgtacr_DStrain\Opto DS Task Test- CUE Laser Manipulation\trainData.mat',squeeze_me=True)
    matContents= sio.loadmat(r'C:\Users\Dakota\Desktop\Opto DS Task Test- CUE Laser Manipulation\trainData.mat',squeeze_me=True)

    #%% Extract the relevant data and get the data into pandas.dataframe format
    #adapted from https://www.kaggle.com/avilesmarcel/open-mat-in-python-pandas-dataframe
    
    mdata= matContents['trainData'] #extract the struct contents from the loaded .mat 
    
    mtype= mdata.dtype  #1 'type' of data corresponding to each column
    
    #now it looks like we are creating a dict matching up data (in np.arrays) from mdata with column names
    ndata= {n: mdata[n] for n in mtype.names} 
    

    data_headline= [] #will hold list of var labels for columns
    data_raw=[]   #will hold the raw data for each column
    #since our struct contains multiple data types/classes, make this np array of object type
    data_raw= np.empty([mdata.shape[0],len(mtype.names)],dtype=object) 
    
    
    #now simply loop through each variable type and get the corresponding data. Probably a better way to do this
    for var in range(len(mtype.names)):   
    
        data_headline.append([mtype.names[var]][0])
    
        for ses in range(data_raw.shape[0]): 
                data_raw[ses,var]= ndata[mtype.names[var]].flatten()[ses]
                
    #save the data as a pandas dataframe 
    df= pd.DataFrame(data_raw, columns=data_headline)
    
    #%% Do some preliminary behavioral analysis
    #TODO: Reshape the table first
    
    #for now, just grab MPC calculated DS PE ratios
    #to do so make an empty array, cat() together values and then assign as column in df
    var= np.empty(df.shape[0])
    for ses in range(df.shape[0]):
        # B(23)=DS PE ratio ; B(24= NS PE ratio)
        # df[ses].DSPEratio.assign=df.x_B_workingVars[ses][23].copy()
        var[ses]=df.x_B_workingVars[ses][23]
        
    df= df.assign(DSPEratio=var)
    
    var= np.empty(df.shape[0])
    for ses in range(df.shape[0]):
        # B(23)=DS PE ratio ; B(24= NS PE ratio)
        # df[ses].DSPEratio.assign=df.x_B_workingVars[ses][23].copy()
        var[ses]=df.x_B_workingVars[ses][24]
    df= df.assign(NSPEratio=var)
    
    #calculate a 'discrimination index' as DSratio/NSratio
    df= df.assign(discrimPEratio= df.DSPEratio/df.NSPEratio)

    #calculate port exit time estimate using PEtime and peDur, save this as a new variable
    df= df.assign(PExEst= df.x_K_PEtime + df.x_L_PEdur)     
    
    #somehow different amount of cues and laser states...
    #possibly due to error in code from 20210604 session
    #26 missing NSlaser entries x 11 subjects =286. = size mismatch
     
    #~~EXCLUDE this date~~~~~~~~~~~~~~~~~~~!!!
    df= df[df.date!=20210604]
    
    #%% May need to do some reaarranging of data for easiest plotting
    #https://stackoverflow.com/questions/38372016/split-nested-array-values-from-pandas-dataframe-cell-over-multiple-rows?newreg=1c04242af3c7428faaecc1daf25d783a
   #https://stackoverflow.com/questions/52200710/pandasseaborn-faceting-with-multidimensional-dataframes
    #e.g. could have one row for each date and 60 columns for trial series?
    
    #temp copy of missing N & F
    # df['x_N_NSPElat']=df['x_M_DSPElat']
    # df['x_F_laserNStrial']=df['x_E_laserDStrial']
    
    #let's just get a few variables
    df2= df[['RatID','Sex','laserDur','Virus','date','x_M_DSPElat','x_E_laserDStrial','x_N_NSPElat','x_F_laserNStrial','DSPEratio','NSPEratio','discrimPEratio']].copy()
    
    
    #really interesting potential solution looks like here we get 2 indices, one for subject and one for file (date)
    #but, I think different sized variables within session complicates this factor and causes many repeating values that aren't accurate?
    unnested_lst = []
    for col in df2.columns:
        #pd.series combines into single long array
        #then, stack() this into one long column. Each value has hierarchical index
        unnested_lst.append(df2[col].apply(pd.Series).stack())
    result = pd.concat(unnested_lst, axis=1, keys=df2.columns).fillna(method='ffill')
    
    #Now let's perform some preliminary analysis, make a new variable for DS PE outcome per trial
    result['DSPEoutcome']= result['x_M_DSPElat']
    result['DSPEoutcome']=result['DSPEoutcome'].replace(10,0) #10s= no PE
    result.loc[result['DSPEoutcome'] > 0, 'DSPEoutcome'] = 1
    #also replace 10s or 0s latencies with nan (since there was no PE)
    #not sure where the 0s latencies are coming from, but are there for every trial 30 & 31?
    result.x_M_DSPElat[result.x_M_DSPElat==10] = np.nan
    result.x_M_DSPElat[result.x_M_DSPElat==0]= np.nan
    
    #same for NS
    result['NSPEoutcome']= result['x_N_NSPElat']
    result['NSPEoutcome']=result['NSPEoutcome'].replace(10,0) #10s= no PE
    result.loc[result['NSPEoutcome'] > 0, 'NSPEoutcome'] = 1
    #also replace 10s latencies with nan (since there was no PE)
    result.x_N_NSPElat[result.x_N_NSPElat==10] = np.nan
    result.x_N_NSPElat[result.x_N_NSPElat==0]= np.nan


    #convert ratID to categorical data type so seaborn uses divergent color hues
    result.RatID= result.RatID.astype('category')
    

    #change date axis to day count just for nice look
    #use np.argwhere to convert date to day count (assuming dates in order?) then replace
    for date in result.date.unique():
        result.date= result.date.replace(date,np.argwhere(date==result.date.unique())[0][0])
    
        #visualize
    import seaborn as sns
    import matplotlib.pyplot as plt
    
    #paired seems nice for comparing laser on vs off
    # sns.set_palette('Paired')
    sns.set_palette('tab10') #tab10 is default

    
    
    plt.figure()
    # plt.subplot(1,2,1) #DS #violin too dense by subj
    # sns.violinplot(x='RatID',y='x_M_DSPElat',hue='x_E_laserDStrial',data=result, split=True, inner='stick')
    sns.violinplot(x='RatID',y='x_M_DSPElat',hue='x_E_laserDStrial',data=result, cut=0, split=True, inner='quartile') #, scale='count')

    plt.figure() 
    # plt.subplot(1,2,2) #NS #violin too dense by subj
    sns.violinplot(x='RatID',y='x_N_NSPElat',hue='x_F_laserNStrial',data=result, cut=0, split=True, inner='quartile') #, scale='count')
    
    
    #~~note that seaborn documentation says that ci=68 can be used to plot SEM but this is actually different from sem. Default is 95% CI i think
    #ci 68 assumes normal distro and then it's still only 68% probability that mean lies here?
    plt.figure()
    plt.subplot(1,2,1) #DS 
    sns.barplot(x='RatID',y='x_M_DSPElat',hue='x_E_laserDStrial',data=result,capsize=.2) 
    plt.subplot(1,2,2) #NS
    sns.barplot(x='RatID',y='x_N_NSPElat',hue='x_F_laserNStrial',data=result, capsize=.2)
    
    
    plt.figure()
    plt.subplot(1,2,1) #DS
    sns.boxplot(x='RatID',y='x_M_DSPElat',hue='x_E_laserDStrial',data=result)
    # sns.swarmplot(x='RatID',y='x_M_DSPElat',hue='x_E_laserDStrial',data=result, dodge=True,size=1.5,color='.2')
    plt.subplot(1,2,2) #NS
    sns.boxplot(x='RatID',y='x_N_NSPElat',hue='x_F_laserNStrial',data=result)
    # sns.swarmplot(x='RatID',y='x_N_NSPElat',hue='x_F_laserNStrial',data=result, dodge=True,size=1.5,color='.2')


    # #try multiple hist()
    #initially, hist() by count makes it seem that NS + laser has higher latency, but after normalization here looks same
    plt.figure()
    plt.subplot(1,2,1) #DS
    sns.histplot(data=result, x='x_M_DSPElat', hue='x_E_laserDStrial',  stat="density", common_norm=False, kde=True, multiple='layer',bins=20)
    plt.subplot(1,2,2) #NS
    sns.histplot(data=result, x='x_N_NSPElat', hue='x_F_laserNStrial',  stat="density", common_norm=False, kde=True, multiple='layer',bins=20)
    
    #ecdf plot
    plt.figure()
    plt.subplot(1,2,1) #DS
    sns.ecdfplot(data=result, x='x_M_DSPElat', hue='x_E_laserDStrial')
    plt.subplot(1,2,2) #NS
    sns.ecdfplot(data=result, x='x_N_NSPElat', hue='x_F_laserNStrial')

    
    #Figure level functions (e.g. catplot) may be better
    
    g=sns.catplot(x='RatID',y='x_M_DSPElat',hue='x_E_laserDStrial', row='laserDur', col='Virus',data=result,kind="box")

    g=sns.catplot(x='RatID',y='x_M_DSPElat',hue='x_E_laserDStrial', row='laserDur', col='Virus',data=result,kind="bar")

    #individual trial PE outcome vs individual trial laser state?
    
    #todo- normalize count of pe outcome or convert to % for countplot()
    # g=sns.catplot(x='DSPEoutcome',hue='x_E_laserDStrial', row='laserDur', col='Virus',data=result,kind="count")
   
    g=sns.displot(data= result, x='DSPEoutcome', hue='x_E_laserDStrial', col='laserDur', row='Virus', kind='hist', stat='probability', common_norm=False, multiple='layer')
    g.fig.subplots_adjust(top=0.9) # adjust the figure for title 
    g.fig.suptitle('DS PE outcome: Laser x virus')

    g=sns.displot(data= result, x='NSPEoutcome', hue='x_F_laserNStrial', col='laserDur', row='Virus', kind='hist', stat='probability', common_norm=False, multiple='layer')
    g.fig.subplots_adjust(top=0.9) # adjust the figure for title 
    g.fig.suptitle('NS PE outcome: Laser x virus')

    #To get trial # on X axis, use the index from our dataframe corresponding to trial (0:31)
    result=result.assign(trial=result.index.get_level_values(1))
    
    
    with sns.axes_style("whitegrid"), sns.color_palette('tab20',n_colors=np.unique(result.RatID).size): 
        g=sns.relplot(x= result.trial, y='DSPEoutcome', hue='RatID', row='laserDur', col='x_E_laserDStrial', data=result, kind='line')

    # g=sns.displot(data= result, x='trial', y='DSPEoutcome', hue='x_E_laserDStrial', row='laserDur', col='Virus', kind='hist', stat='probability', common_norm=False)

    # g=sns.displot(data= result, y='DSPEoutcome', x='trial', hue='x_E_laserDStrial', row='laserDur', col='Virus', kind='hist', stat='probability', common_norm=False)


    # g=sns.catplot(x='RatID',y='DSPEratio',hue='x_E_laserDStrial', row='laserDur', col='Virus',data=result,kind="bar")
    
    #session wide ratio data vs. session laserDur
    # g=sns.catplot(x='RatID',y='discrimPEratio', hue='laserDur',col='Virus',data=result,kind="bar")
    # g=sns.catplot(x='RatID',y='discrimPEratio', hue='laserDur',col='Virus',data=result,kind="box")


    # g=sns.displot(x='DSPEratio',hue='RatID', row='laserDur', col='Virus', data= result,kind="ecdf")
        
    
    #Aggregate effect of laser
    g=sns.displot(x='x_M_DSPElat',hue='x_E_laserDStrial', col='laserDur', row='Virus', data= result,kind="ecdf")
    g.fig.subplots_adjust(top=0.9) # adjust the figure for title 
    g.fig.suptitle('DS PE latency: Laser x virus')
    
    g=sns.displot(x='x_N_NSPElat',hue='x_F_laserNStrial', col='laserDur', row='Virus', data= result,kind="ecdf")
    g.fig.subplots_adjust(top=0.9) # adjust the figure for title 
    g.fig.suptitle('NS PE latency: Laser x virus')
    
    # g=sns.catplot(x='Virus',y= 'x_M_DSPElat',hue='x_E_laserDStrial', row='laserDur', data= result,kind="bar")
    # g=sns.catplot(x='Virus',y= 'DSPEratio',hue='laserDur', data= result,kind="bar")

    #Individual effect of laser
    with sns.axes_style("whitegrid"), sns.color_palette('tab20',n_colors=np.unique(result.RatID).size): 
        g=sns.displot(x='x_M_DSPElat',hue='x_E_laserDStrial', col='laserDur', row='RatID', data= result,kind="ecdf")
        g.fig.subplots_adjust(top=0.9) # adjust the figure for title 
        g.fig.suptitle('Individual DS PE latency: Laser x virus')    


    #Individual training data
    #for plot across sessions of individual rats, change color to tab20 and make background white to help colors pop...default color palettes have blues that I can't distinguish
    with sns.axes_style("whitegrid"), sns.color_palette('tab20',n_colors=np.unique(result.RatID).size): 
          g=sns.relplot(x='date',y='DSPEratio',hue='RatID', col='Virus', row='Sex', data= result,kind="line",linewidth=3)
          g.fig.subplots_adjust(top=0.9) # adjust the figure for title 
          g.fig.suptitle('Individual DS PE ratio')

          g=sns.relplot(x='date',y='NSPEratio',hue='RatID', col='Virus', row='Sex', data= result,kind="line",linewidth=3)
          g.fig.subplots_adjust(top=0.9) # adjust the figure for title 
          g.fig.suptitle('Individual NS PE ratio')
          
          g=sns.relplot(x='date',y='discrimPEratio',hue='RatID', col='Virus', row='Sex', data= result,kind="line",linewidth=3)
          g.fig.subplots_adjust(top=0.9) # adjust the figure for title 
          g.fig.suptitle('Individual PE discrimination (DS/NS ratio)')
        
          g=sns.relplot(x='date',y='discrimPEratio',hue='laserDur', row='RatID', data= result,kind="scatter",linewidth=3)
          g.fig.subplots_adjust(top=0.9) # adjust the figure for title 
          g.fig.suptitle('Individual PE discrimination (DS/NS ratio): Laser ON vs Laser OFF days')
                  
          
    #Aggregated training data
    sns.set_palette('tab10')
    
    # g=sns.relplot(x='date',y='DSPEratio',hue='laserDur', col='Virus', row='Sex', data= result,kind="line",linewidth=2)
    # g=sns.relplot(x='date',y='NSPEratio',hue='laserDur', col='Virus', row='Sex', data= result,kind="line",linewidth=2)
    g=sns.relplot(x='date',y='DSPEratio',hue='laserDur', col='Virus', data= result,kind="line",linewidth=2)
    g=sns.relplot(x='date',y='discrimPEratio',hue='laserDur', col='Virus', data= result,kind="line",linewidth=2)
    g=sns.relplot(x='date',y='DSPEratio',hue='Virus', data= result,kind="line",linewidth=2)


#regression
    g=sns.lmplot(x= 'x_E_laserDStrial', y='x_M_DSPElat',hue='Virus',col='laserDur',data=result)

     #%% Playing with grouping and shape
    groupBySex= df.groupby('Sex')
    groupBySex.count()
    groupBySex.get_group('F')
    
    groupBySexVirus= df.groupby(['Sex','Virus'])
    groupBySexVirus.count()
    groupBySexVirus.groups #groups
    groupBySexVirus.get_group(('F', 1)) #get this specific group
    # groupBySexVirus['x_M_DSPElat'].mean()

     
    #%% melt() each event variable into eventType and eventTime 
    #use explode() to reduce arrays of event timestamps into many rows with single element
    #retain hierarchical indexing (1 per file) 

    #here am melting columns of behavioral events into single column of event label and column of individual timestamps (value_vars= want to melt) 
    #ignore_index=False: to keep the original index (1 per file)
    dfEvent= df.melt(id_vars=['subject','Virus','Sex','date','laserDur','note'],value_vars=['x_K_PEtime','PExEst','x_S_lickTime','x_D_laserTime'],var_name='eventType',value_name='eventTime', ignore_index=False)

  

    #now explode event timestamp array
    dfEvent= dfEvent.explode('eventTime')


    # eventCount= dfEvent.groupby(['subject','date'])['eventType'].value_counts()

    # g=sns.relplot(x='date',y=eventCount.values,hue='eventType',
    #               data=eventCount,kind="line", 
    #               facet_kws={'sharey': False, 'sharex': True})
    # g.fig.subplots_adjust(top=0.9) # adjust the figure for title 
    # g.fig.suptitle('Event counts over time pre deletion')

    #remove invalid/placeholder 0s
    #TODO: seem to be removing legitimate port exits with peDur==0, not sure how to deal with this so just excluding
    dfEvent= dfEvent[dfEvent.eventTime!=0]
        
    #for visualizing- get the counts for each unique eventType for each file (group by subj & date)
    #eventCount here is a  pandas.Series, which is a labelled set (multiindex= subject, date, eventType) of 1D values (each value here is a count of the unique event types for a given subject & date
    eventCount= dfEvent.groupby(['subject','date'])['eventType'].value_counts()
    
    #tried grouping by level=0 here is grouping by the index of dfEvent, effectively doing the same as grouping by subject & date
    #catplot still wouldn't work
    #dfEvent.eventCount= dfEvent.groupby(level=0)['eventType'].value_counts()
    
    #visualize- for some reason catplot()s specifically won't work with this series
    #sharey= false: don't share y axis since event counts vary widely by typ
    # g=sns.relplot(x='date',y=eventCount.values,hue='subject',
    #               col='eventType', data=eventCount,kind="line", 
    #               facet_kws={'sharey': False, 'sharex': True})
    # g.fig.subplots_adjust(top=0.9) # adjust the figure for title 
    # g.fig.suptitle('Event counts over time by subject')
    g=sns.relplot(x='date',y=eventCount.values,hue='eventType',
                  data=eventCount,kind="line", 
                  facet_kws={'sharey': False, 'sharex': True})
    g.fig.subplots_adjust(top=0.9) # adjust the figure for title 
    g.fig.suptitle('Event counts over time by subject post deletion')
 
    #%% Do same for trial-based events (DS,NS,laser state for both trial types )

    # dfCue= df.melt(id_vars=['subject','Virus','Sex','date','laserDur','note'],value_vars=['x_H_DStime','x_I_NStime'],var_name='cueType',value_name='cueTime');
    
    #retain original index (1 per file) by setting ignore_index=False
    dfCue= df.melt(id_vars=['subject','Virus','Sex','date','laserDur','note'],value_vars=['x_H_DStime','x_I_NStime'],var_name='cueType',value_name='cueTime', ignore_index=False);
    #so can use dfCue.loc[ses] to get values from specific session

    #explode arrays of timestamps into their own cells
    dfCue= dfCue.explode('cueTime')
        
    #now remove entires where cueTime==0 (these are invalid or fillers just due to how MPC code was written)
    #may have to remove these at end so they match up with laser?
    dfCue= dfCue[dfCue.cueTime!=0]
    
    #let's check the shape of dfCue to see how many cue timestamps we have per session now
    # print('num cue timestamps per file= ',dfCue.loc[1].shape[0])
    # g= sns.catplot(x='date', y='cueTime', hue='cueType', kind='box', data=dfCue)
    # g.fig.subplots_adjust(top=0.9) # adjust the figure for title 
    # g.fig.suptitle('cue onset time by date')
  
    
    #Now melt() laser state for each cue, keep original index
    dfLaser= df.melt(id_vars=['subject','Virus','Sex','date','laserDur','note'],value_vars=['x_E_laserDStrial','x_F_laserNStrial'],var_name='laserType',value_name='laserState',ignore_index=False);
    #explode arrays into their own cells
    dfLaser= dfLaser.explode('laserState')
     
    #somehow different amount of cues and laser states...
    #possibly due to error in code from 20210604 session
    #~26 missing NSlaser entries x 11 subjects ~286. = size mismatch
    dfCue.shape[0]-dfLaser.shape[0]
 
    #Merge two together
    dfCue= pd.concat([dfCue,dfLaser[['laserType','laserState']]],axis=1)
    # test=pd.merge(dfCue,dfLaser,how= 'left')
    
    #Finally, merge the event and cue dfs into one df
    #concat() taking long time?
    # dfTidy= pd.concat([dfCue,dfEvent[['eventType','eventTime']]],axis=1)
    # dfTidy= pd.concat([dfCue,dfEvent],axis=1, keys= ['trial','event'])

    # dfTidy= dfCue.join(dfEvent, dfEvent)
    
    # # dfTidy= pd.merge(dfCue,dfEvent,how='left')
    # dfTidy= pd.merge(dfCue,dfEvent['eventType','eventTime'],on=['subject','date'])
    # dfTidy = pd.merge(dfCue, dfEvent[['eventType','eventTime']], left_index=True, right_index=True, how='outer').drop_duplicates()
   
    #related https://stackoverflow.com/questions/51669232/pandas-merge-with-duplicated-key-removing-duplicated-rows-or-preventing-its-c 
    dfEvent['g'] = dfEvent.groupby(level=0).cumcount()
    
    #save a named index for fileID 
    dfCue.index.name= 'fileID'
    dfEvent.index.name= 'fileID'
    
    #save an index for trialID, first sort by cueTime within file so trials are in order
    dfCue= dfCue.sort_values(by=['fileID','cueTime'])
    dfCue['g'] = dfCue.groupby(level=0).cumcount()
    
    dfCue['trialID']= dfCue['g']
    
    # dfCue= dfCue.set_index([dfCue.index,'trialID'])

    # dfEvent.reset_index().merge(dfCue, how="right").set_index('fileID')
        #works but doesn't retain ind
    # dfTidy = pd.merge(dfCue,dfEvent[['subject','date','g','eventType','eventTime']],on=['subject','date', 'g'],how='right').drop('g',axis=1)
    dfTidy = pd.merge(dfCue,dfEvent[['g','eventType','eventTime']],on=['fileID', 'g'],how='right').drop('g',axis=1)

    # is there a wayto set the index below such that events don't havea a trialID unless I assign them?  (e.g. nan in these spots but could assign later on?)   
    # dfTidy.eventType= dfTidy.eventType.reset_index()
    #summing together should cause offset so events don't match with trialID?
    #but just causes everything to be nan (probs bc 'g' has no matches):
     
        #resolved in next 
        
    # dfEvent['g']= dfEvent['g']+dfCue['g'].max()+1 
    # dfTidy = pd.merge(dfCue,dfEvent[['g','eventType','eventTime']],on=['fileID', 'g'],how='right').drop('g',axis=1)

    #now it seems we have everything together, set multiindex to help readability
    #this gives us a df with a hierarchical index of fileID,trialID. While not all events match
    #up at this point, should be good fordoing trial-by-trial analyses. And now, since we sorted all the trials
    #we don't have to treat DS & NS separately at all anymore! we can just go by cueType and laserType
    dfTidy= dfTidy.set_index([dfTidy.index,'trialID'])
    
  
    #%% Better df org: All events in single column, sort by time by file, with fileID column and trialID column that matches trial 1-60 through each session.

    dfEventAll= df.melt(id_vars=['subject','Virus','Sex','date','laserDur','note'],value_vars=['x_K_PEtime','PExEst','x_S_lickTime','x_D_laserTime','x_H_DStime','x_I_NStime'],var_name='eventType',value_name='eventTime', ignore_index=False)
     
    #now explode event timestamp array
    dfEventAll= dfEventAll.explode('eventTime')

    #remove invalid/placeholder 0s
    #TODO: seem to be removing legitimate port exits with peDur==0, not sure how to deal with this so just excluding
    dfEventAll= dfEventAll[dfEventAll.eventTime!=0]


    #before any removal/sorting is done, next issue is to match up laser state with cues. 
    dfLaser= df.melt(id_vars=['subject','Virus','Sex','date','laserDur','note'],value_vars=['x_E_laserDStrial','x_F_laserNStrial'],var_name='laserType',value_name='laserState',ignore_index=False);
    #explode arrays into their own cells
    dfLaser= dfLaser.explode('laserState')
     
    #use cumcount() of DS & NS to match up laser status with cue time (redundant since we have a timestamp of laser on, but good verification still)
    dfEventAll.index.name= 'fileID'
    dfEventAll= dfEventAll.reset_index()
    dfEventAll['g']= dfEventAll[(dfEventAll.eventType=='x_H_DStime') | (dfEventAll.eventType=='x_I_NStime')].groupby('fileID').cumcount()#.index
    
    
    dfLaser.index.name= 'fileID'
    dfLaser= dfLaser.reset_index()
    dfLaser['g']= dfLaser[(dfLaser.laserType== 'x_E_laserDStrial') | (dfLaser.laserType== 'x_F_laserNStrial')].groupby('fileID').cumcount()
    
    # print(dfLaser['g'].shape, dfLaser['g'].max(), dfEventAll['g'].shape, dfEventAll['g'].max())

    
    
    dfEventAll= pd.merge(dfEventAll,dfLaser[['g', 'fileID', 'laserType','laserState']],on=['fileID', 'g'],how='left').drop('g',axis=1)
    
    #sort all event times by file and timestamp
    #set index name so we can sort by it easily
    # dfEventAll.index.name= 'fileID'
    dfEventAll= dfEventAll.sort_values(by=['fileID','eventTime'])
    
    #need to reset_index before assigning values back to dfEventAll (this is because the fileID index repeats so assignment is ambiguous)
    dfEventAll= dfEventAll.reset_index()
    
    #add trialID column by cumulative counting each DS or NS within each file
    #now we have ID for trials 0-59 matching DS or NS within each session, nan for other events
    dfEventAll['trialID']= dfEventAll[(dfEventAll.eventType=='x_H_DStime') | (dfEventAll.eventType=='x_I_NStime')].groupby('fileID').cumcount()
    
    dfTidy= dfEventAll
    #visualize all events per file
    # sns.relplot(x='eventTime',y='fileID',hue='eventType', data= dfTidy, kind='scatter')
    
      #%% Identify events during each trial
      
     #TODO: for now assume cue duration = 10, but should get programmatically from A() array
    
    cueDur= 10
    
    #fill in intermediate trialID values... We have absolute trialIDs now for each Cue but other events have trialID=nan
    #we can't tell for certain if events happened during a trial or ITI at this point but we do have all of the timestamps
    #and we know the cue duration, so we can calculate and assign events to a trial using this.
    
    #To start, fill in these values between each trialID as -trialID (could also use decimal like trial 1.5) between each actual Cue
    #Get the values and index of nan trialIDs
    #this returns a series of each nan trialID along with its index. 
    indNan= dfTidy.trialID[dfTidy.trialID.isnull()]
    
    #pandas has a function for this- groupby().ffill or .backfill or .fillna
    #this fills nan trialID
    dfTidy.trialID= dfTidy.trialID.fillna(method='ffill')
    
    # #try groupbytrial before -1
    # test=dfTidy.groupby(['fileID','trialID']).eventTime
 
    # #group by event type within same file and trial, then we can just subtract 
    # test2= dfTidy.groupby(['fileID','trialID'])
    # #groupby returns each combination of the values
    # #this still takes awhile.
    # for file, trial in test2.groups:
    #     if trial>=0: #ignore the - trialIDs
    #         # atestSubj= group['eventType']
    #         print(file, trial)
    #         test= dfTidy.eventTime[(dfTidy.fileID==file) & dfTidy.trialID==trial]
        
    # # dfTidy[trialID] eventType~= DS | NS - eventType= DS | NS?
    
    # # #get time difference between non-cue event types and cue per trial
    # # for trial in dfTidy.trialID.unique():
    # #     dfTrial= dfTidy.trialID==trial
    # #     dfTrial.dfTidy.eventType!='x_I_NStime' | dfTidy.eventType!='x_H_DStime'
    # #     trialDiff= dfTidy.eventTime[dfTidy.eventType!='x_I_NStime' | dfTidy.eventType!='x_H_DStime' & dfTidy.eventTime[dfTidy.trialTyp==trial]]
        

    
    #now multiply previously nan trialIDs by -1 so we can set them apart from the valid trialIDs
    #using .at[] replaces value without SettingWithCopyWarning
    dfTidy.trialID.at[indNan.index]= dfTidy.trialID[indNan.index]*-1
     
    # #should be easy right?
    # #if dfTidy.eventTime[fileID][-trial] <= eventTime[fileID][trial]
    #     # dfTidy.eventTime[fileID]
    
    # #pandas cross-section method df.xs() might be good
    # # test= dfTidy.xs['trialID'==1,'fileID=='1]
    # #get time difference between non-cue event types and cue per trial
    
    # #this method is taking too long... 
    
    
    # testSub=np.empty([60,dfTidy.shape[0]])
    # for file in dfTidy.fileID:
    #     for trial in dfTidy.trialID[dfTidy.trialID>=0].unique():
    #         # dfTrial= dfTidy[(dfTidy.fileID==file) & (dfTidy.trialID==trial)]
    #         # dfTrial= dfTrial.assign(trialDiff= dfTidy.eventTime[dfTidy.trialID==trial] - dfTidy.eventTime[dfTidy.trialID==-trial])
    #         print(file)
    # #maybe it would be faster if we set the df index to file and trial first? then we avoid two loops?
    # #reindex by file, trial and then use pandas cross section method df.xs() to select data
    # #TODO: this may be more efficient https://pandas.pydata.org/pandas-docs/stable/whatsnew/v0.14.0.html#multi-indexing-using-slicers
    
    # # trials= dfTidy.trialID[dfTidy.trialID>=0].unique()
    
    # dfTidy= dfTidy.reset_index()
    # dfTidy= dfTidy.set_index(['fileID','trialID'])
    
    # #sort ind before, faster
    # dfTidy= dfTidy.sort_index()
    # #~!~~~~~HERE~~~~~
    # #still takes way too long
    # for file in dfTidy.index.get_level_values(0):
    #     for trial in dfTidy.index.get_level_values(1)[dfTidy.index.get_level_values(1)>=0].unique():#dfTidy.trialID[dfTidy.trialID.unique()[dfTidy.trialID>=0]].unique():
    #         # test= dfTidy.xs((trial),level='trialID')
        
    #         # test2= dfTidy.xs((file,trial),level=['fileID','trialID'])

    #         print(dfTidy.loc[file,trial])
            
    # trials= dfTidy.trialID[dfTidy.trialID>=0].unique()

    # dfTidy= dfTidy.reset_index()

    # for date, new_df in dfTidy.groupby(['fileID',dfTidy.trialID==trials]):
    #     print(new_df)

    # #now use groupby() trialID and take difference of event times in -trialID with the cue time in +trialID
    # test=dfTidy.groupby(['fileID','trialID']).eventTime.groups
    
    #Did a lot of experimenting with different methods to subtract each event
    #from each cue on a trial-by-trial basis...didn't find a good way to do it quickly
    #without nested loops.
    #Instead, can just get a trial end time based on cue onset, then just check
    #event times against this
    dfTidy= dfTidy.sort_values(by=['fileID','eventTime'])

    dfTidy['trialEnd']= dfTidy.eventTime[dfTidy.trialID>=0]+cueDur
    
    dfTidy.trialEnd= dfTidy.trialEnd.fillna(method='ffill')
    
    #find events that occur after cue start but before cue duration end
    dfTidy.trialID.loc[(dfTidy.eventTime-dfTidy.trialEnd<=0) & (dfTidy.eventTime-dfTidy.trialEnd>-10)]= dfTidy.trialID*-1
    
    



    #groupby trialID to get all of the trials. will just loop through
    #and find events occurring within cueDur for this trial
    # dfTidy.groupby(level=1).cueType-cueTime

    
#    #%% Try Pandas_profiling report
    #note- if you are getting errors with ProfileReport() and you installed using conda, remove and reinstall using pip install  
    from pandas_profiling import ProfileReport
    
    # profile = ProfileReport(result, title='Pandas Profiling Report', explorative = True)
        
    ## save profile report as html
    # profile.to_file('pandasProfile.html')

    
        