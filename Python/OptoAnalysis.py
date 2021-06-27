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
    matContents= sio.loadmat(r'Z:\Dakota\MEDPC\Downstairs\vp-vta-stgtacr_DStrain\Opto DS Task Test- CUE Laser Manipulation\trainData.mat',squeeze_me=True)
    
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
    
    #%% May need to do some reaarranging of data for easiest plotting
    #https://stackoverflow.com/questions/38372016/split-nested-array-values-from-pandas-dataframe-cell-over-multiple-rows?newreg=1c04242af3c7428faaecc1daf25d783a
   #https://stackoverflow.com/questions/52200710/pandasseaborn-faceting-with-multidimensional-dataframes
    #e.g. could have one row for each date and 60 columns for trial series?
    
    #let's just get a few variables
    df2= df[['RatID','x_M_DSPElatency','x_E_DSLaser','x_N_NSPElatency','x_F_NSLaser']].copy()
    
    
    #really interesting potential solution looks like here we get 2 indices, one for subject and one for file (date)
    #but, I think different sized variables within session complicates this factor and causes many repeating values that aren't accurate?
    unnested_lst = []
    for col in df2.columns:
        unnested_lst.append(df2[col].apply(pd.Series).stack())
    result = pd.concat(unnested_lst, axis=1, keys=df2.columns).fillna(method='ffill')
    
    #Now let's perform some preliminary analysis, make a new variable for DS PE outcome per trial
    result['DSPEoutcome']= result['x_M_DSPElatency']
    result['DSPEoutcome']=result['DSPEoutcome'].replace(10,0) #10s= no PE
    result.loc[result['DSPEoutcome'] > 0, 'DSPEoutcome'] = 1
    #also replace 10s or 0s latencies with nan (since there was no PE)
    #not sure where the 0s latencies are coming from, but are there for every trial 30 & 31?
    result.x_M_DSPElatency[result.x_M_DSPElatency==10] = np.nan
    result.x_M_DSPElatency[result.x_M_DSPElatency==0]= np.nan
    
    #same for NS
    result['NSPEoutcome']= result['x_N_NSPElatency']
    result['NSPEoutcome']=result['NSPEoutcome'].replace(10,0) #10s= no PE
    result.loc[result['NSPEoutcome'] > 0, 'NSPEoutcome'] = 1
    #also replace 10s latencies with nan (since there was no PE)
    result.x_N_NSPElatency[result.x_N_NSPElatency==10] = np.nan
    result.x_N_NSPElatency[result.x_N_NSPElatency==0]= np.nan

        #visualize
    import seaborn as sns
    import matplotlib.pyplot as plt
    
    #This works!!
    # sns.relplot(x=result['file'], y=result['x_K_PEtimestamps'],hue=result['RatID'], data= result)
    
    # sns.histplot(x='x_E_DSLaser',y='x_M_DSPElatency',hue='RatID', data=result)
    
    sns.relplot(x='RatID',y='x_M_DSPElatency',hue='x_E_DSLaser',data=result)
    
    
    
    plt.figure()
    # plt.subplot(1,2,1) #DS #violin too dense by subj
    # sns.violinplot(x='RatID',y='x_M_DSPElatency',hue='x_E_DSLaser',data=result, split=True, inner='stick')
    sns.violinplot(x='RatID',y='x_M_DSPElatency',hue='x_E_DSLaser',data=result, cut=0, split=True, inner='quartile') #, scale='count')

    plt.figure() 
    # plt.subplot(1,2,2) #NS #violin too dense by subj
    sns.violinplot(x='RatID',y='x_N_NSPElatency',hue='x_F_NSLaser',data=result, cut=0, split=True, inner='quartile') #, scale='count')
    
    
    #~~note that seaborn documentation says that ci=68 can be used to plot SEM but this is actually different from sem. Default is 95% CI i think
    #ci 68 assumes normal distro and then it's still only 68% probability that mean lies here?
    plt.figure()
    plt.subplot(1,2,1) #DS 
    sns.barplot(x='RatID',y='x_M_DSPElatency',hue='x_E_DSLaser',data=result,capsize=.2) 
    plt.subplot(1,2,2) #NS
    sns.barplot(x='RatID',y='x_N_NSPElatency',hue='x_F_NSLaser',data=result, capsize=.2)
    
    
    plt.figure()
    plt.subplot(1,2,1) #DS
    sns.boxplot(x='RatID',y='x_M_DSPElatency',hue='x_E_DSLaser',data=result)
    # sns.swarmplot(x='RatID',y='x_M_DSPElatency',hue='x_E_DSLaser',data=result, dodge=True,size=1.5,color='.2')
    plt.subplot(1,2,2) #NS
    sns.boxplot(x='RatID',y='x_N_NSPElatency',hue='x_F_NSLaser',data=result)
    # sns.swarmplot(x='RatID',y='x_N_NSPElatency',hue='x_F_NSLaser',data=result, dodge=True,size=1.5,color='.2')


    # #try multiple hist()
    #initially, hist() by count makes it seem that NS + laser has higher latency, but after normalization here looks same
    plt.figure()
    plt.subplot(1,2,1) #DS
    sns.histplot(data=result, x='x_M_DSPElatency', hue='x_E_DSLaser',  stat="density", common_norm=False, kde=True, multiple='layer',bins=20)
    plt.subplot(1,2,2) #NS
    sns.histplot(data=result, x='x_N_NSPElatency', hue='x_F_NSLaser',  stat="density", common_norm=False, kde=True, multiple='layer',bins=20)
    
    #ecdf plot
    plt.figure()
    plt.subplot(1,2,1) #DS
    sns.ecdfplot(data=result, x='x_M_DSPElatency', hue='x_E_DSLaser')
    plt.subplot(1,2,2) #NS
    sns.ecdfplot(data=result, x='x_N_NSPElatency', hue='x_F_NSLaser')

    #%% Trying to melt() each event variable into eventType and eventTime 
    #goal here is to reduce arrays of event timestamps into single element
    #could have hierarchical indexing for date & subject
    
    # df3= df.melt(id_vars='x_C_DSlaserState')

    #related?https://stackoverflow.com/questions/53218931/how-to-unnest-explode-a-column-in-a-pandas-dataframe 
    def unnesting(df, explode):
        idx = df.index.repeat(df[explode[0]].str.len())
        df1 = pd.concat([
            pd.DataFrame({x: np.concatenate(df[x].values)}) for x in explode], axis=1)
        df1.index = idx
        return df1.join(df.drop(explode, 1), how='left')

    
    df3= unnesting(df,['x_E_DSLaser'])
    
    #     Option 2
    
    # If the sublists have different length, you need an additional step:
    
    vals = df.B.values.tolist()
    rs = [len(r) for r in vals]    
    a = np.repeat(df.A, rs)
    
    pd.DataFrame(np.column_stack((a, np.concatenate(vals))), columns=df.columns)
        
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
        # df['Group_0_Stgtacr_1_Mcherry_'][ses]= df['Group_0_Stgtacr_1_Mcherry_'][ses][0][0]
    
        
    df['file']= df['file'].astype('category')
    df['subject']= df['subject'].astype('category')
    df['Mode_0_stgtacr_1_mCherry_']= df['Group_0_Stgtacr_1_Mcherry_'].astype('category')
    
    #don't fully understand what is being done here... but it is plotting without reorganizing data
    #plot DS PE latency based on Laser state
    grid = sns.FacetGrid(df,row='Group_0_Stgtacr_1_Mcherry_',col='Sex')
    grid.map(lambda _x,_y,**kwargs : plt.scatter(_x.values[0],_y.values[0]),'x_E_DSLaser','x_M_DSPElatency')
    
    #plot DS PE latency based on Laser state
    grid = sns.FacetGrid(df,row='Group_0_Stgtacr_1_Mcherry_',col='Sex')
    #this works but I think am only getting one session?
    grid.map(lambda _x,_y,**kwargs : sns.histplot(x=_x.values[0],hue=_y.values[0]),'x_M_DSPElatency','x_E_DSLaser')
    
    # #try visualizing DS PE and latency based on Laser state
    # grid = sns.FacetGrid(df,row='x_E_DSLaser',col='Group_0_Stgtacr_1_Mcherry') 
    # grid.map(lambda _x,_y,**kwargs : plt.scatter(_x.values[0],_y.values[0]),'x_O_DSPE','x_M_DSPElatency')
        
        
    #%% Try Pandas_profiling report
    #note- if you are getting errors with ProfileReport() and you installed using conda, remove and reinstall using pip install  
    from pandas_profiling import ProfileReport
    
    profile = ProfileReport(result, title='Pandas Profiling Report', explorative = True)
        
    #%% save profile report as html
    profile.to_file('pandasProfile.html')

    
        
    
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