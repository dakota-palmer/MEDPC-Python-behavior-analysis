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
    dfEvent= df.melt(id_vars=['subject','Virus','Sex','date','laserDur','note'],value_vars=['x_K_PEtime','x_L_PEdur','PExEst','x_S_lickTime','x_D_laserTime'],var_name='eventType',value_name='eventTime', ignore_index=False)

  

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
    dfCue= pd.concat([dfCue,dfLaser])

    #here am melting all except id_vars 
    # df3= df.melt(id_vars= ['file','subject','Sex','Virus','laserDur','note'], var_name='eventType', value_name='eventTime') 
    #related?https://stackoverflow.com/questions/53218931/how-to-unnest-explode-a-column-in-a-pandas-dataframe 
    def unnesting(df, explode):
        idx = df.index.repeat(df[explode[0]].str.len())
        df1 = pd.concat([
            pd.DataFrame({x: np.concatenate(df[x].values)}) for x in explode], axis=1)
        df1.index = idx
        return df1.join(df.drop(explode, 1), how='left')

    
    df4= unnesting(df,['x_E_laserDStrial'])
    
    #     Option 2
    
    # If the sublists have different length, you need an additional step:
    
    # vals = df.B.values.tolist()
    # rs = [len(r) for r in vals]    
    # a = np.repeat(df.A, rs)
    
    # pd.DataFrame(np.column_stack((a, np.concatenate(vals))), columns=df.columns)
        
    #%% Doing some more basic visualizations
    import seaborn as sns
    import matplotlib.pyplot as plt
    # Apply the default theme
    sns.set_theme()    
    
    #plot relationships between some variables
    # for ses in range(len(df)):
    # sns.relplot(x=df['file'][0],y=df['x_O_DSPE'][0].flatten(), hue=df['RatID'][0])
    
    # for ses in range(len(df)):
        # df['file'][ses]= df['file'][ses][0]
        # df['subject'][ses]= df['subject'][ses][0]
        # df['Virus'][ses]= df['Virus'][ses][0][0]
    
        
    df['file']= df['file'].astype('category')
    df['subject']= df['subject'].astype('category')
    df['Mode_0_stgtacr_1_mCherry_']= df['Virus'].astype('category')
    
    # #don't fully understand what is being done here... but it is plotting without reorganizing data
    # #plot DS PE latency based on Laser state
    # grid = sns.FacetGrid(df,row='Virus',col='Sex')
    # grid.map(lambda _x,_y,**kwargs : plt.scatter(_x.values[0],_y.values[0]),'x_E_laserDStrial','x_M_DSPElat')
    
    # #plot DS PE latency based on Laser state
    # grid = sns.FacetGrid(df,row='Virus',col='Sex')
    # #this works but I think am only getting one session?
    # grid.map(lambda _x,_y,**kwargs : sns.histplot(x=_x.values[0],hue=_y.values[0]),'x_M_DSPElat','x_E_laserDStrial')
    
    # #try visualizing DS PE and latency based on Laser state
    # grid = sns.FacetGrid(df,row='x_E_laserDStrial',col='Group_0_Stgtacr_1_Mcherry') 
    # grid.map(lambda _x,_y,**kwargs : plt.scatter(_x.values[0],_y.values[0]),'x_O_DSPE','x_M_DSPElat')
        
        
    #%% Try Pandas_profiling report
    #note- if you are getting errors with ProfileReport() and you installed using conda, remove and reinstall using pip install  
    from pandas_profiling import ProfileReport
    
    # profile = ProfileReport(result, title='Pandas Profiling Report', explorative = True)
        
    ## save profile report as html
    # profile.to_file('pandasProfile.html')

    
        
    
     #%% result is a numpy structured array, let's convert it to pandas dataframe
    # # df= pd.DataFrame(matContents['trainData'], index=[0]) #.set_index('f0')
    
    # mdata = matContents['trainData']  # variable in mat file
    # mdtype = mdata.dtype  # dtypes of structures are "unsized objects"
    # # * SciPy reads in structures as structured NumPy arrays of dtype object
    # # * The size of the array is the size of the structure array, not the number
    # #   elements in any particular field. The shape defaults to 2-dimensional.
    # # * For convenience make a dictionary of the data using the names from dtypes
    # # * Since the structure has only one element, but is 2-D, index it at [0, 0]
    # ndata = {n: mdata[n][0, 0] for n in mdtype.names}
    # # Reconstruct the columns of the data table from just the time series
    # # Use the number of intervals to test if a field is a column or metadata
    # # columns = [n for n, v in ndata.items() if v.size == ndata['numIntervals']]
    # columns = [n for n in ndata.items()]
    
    # # now make a data frame, setting the time stamps as the index
    # # df = pd.DataFrame(np.concatenate([ndata[c] for c in columns], axis=1),
    # #                   index=[datetime(*ts) for ts in ndata['timestamps']],
    # #                   columns=columns)
    
    
    # for c in columns:
    #     varName= [c][0][0] #getting the first element which is a string label
    #     test=(np.concatenate([ndata[varName]]))#, axis=1))#,
    #                   # index= [datetime(*ts) for ts in ndata['timestamps']],
    #                   # columns=columns)
    
    # df = pd.DataFrame(test,index=0)#,columns=varName)