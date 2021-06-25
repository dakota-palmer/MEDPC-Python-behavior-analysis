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
    
    #%% kaggle 
    #https://www.kaggle.com/avilesmarcel/open-mat-in-python-pandas-dataframe
    mdata= matContents['trainData'] #struct variable from .mat 
    # mdata= matContents['trainData'][0]
    #looks like we have 109 np arrays, one for each struct element (session)
    
    mtype= mdata.dtype 
    #looks like there are 17 'types' of data here, corresponding to each column
    
    #now it looks like we are creating a dict matching up data from mdata with column names
    # ndata= {n: mdata[n][0,0]for n in mtype.names} #seems to be dict matching column titles with nparray of data
    #i think above works for 1 element struct, but I think need below to get all sessions
    ndata= {n: mdata[n] for n in mtype.names} #seems to be dict matching column titles with nparray of data
    

    data_headline= [] #will hold list of var labels for columns
    data_raw=[]
    # data_raw= np.empty([mdata.shape[1],len(mtype.names)],dtype=object) #not squeezed
    data_raw= np.empty([mdata.shape[0],len(mtype.names)],dtype=object) # squeezed

    #since our struct contains multiple data types, make this np array of object type
    # data_raw[:]=np.NaN
    
    for var in range(len(mtype.names)):   
    
    
        data_headline.append([mtype.names[var]][0])
    
        # data_raw.append(mdata[data_headline[var]]) #grab data matching this var name header
        for ses in range(data_raw.shape[0]): #probably inefficient looping through each row but couldn't get assignment to work without it
                data_raw[ses,var]= ndata[mtype.names[var]].flatten()[ses]

                #try converting to single data type for comparison
                # data_raw[ses,var]= np.asarray(data_raw[ses,var]).astype(float)
                #Remove string type data
                # if type(data_raw[ses,var][0])==numpy.str_
                # data_raw[ses,var]

    #save the data as a pandas dataframe 
    df= pd.DataFrame(data_raw, columns=data_headline)
    
    #Something is keeping us from running ProfileReport()
    #TypeError: Cannot compare types 'ndarray(dtype=object)' and 'float'
    
    #I'm thinking it's just that I have multiple data points as arrays in each element of the dataframe
    #instead of running on the raw data would be good to try with some calculated variables of interest e.g. PE ratio
    
    #might be shape of ndarrays?
    # df[data_headline[5]][0].shape
    # type(df[data_headline[5]][0])
    # df[data_headline[5]][0].flatten().shape
    # type(df[data_headline[5]][0].flatten()) #still ndarray after flattening
    
    #seems that ProfileReport doesn't like the ndarrays within df
    #so try converting to numerical
    # for var in range(df.shape[1]):
    #     if (type(df[data_headline[var]][0])).__name__=='string':
    #         print(var)
    #         # df[data_headline[var]].apply(pd.to_numeric)
    #         df[data_headline[var]]= df[data_headline[var]].astype('object')
    #         df[data_headline[var]]= pd.to_numeric(df[data_headline[var]], errors='coerce')
    
    
    #%% May need to do some reaarranging of data for easiest plotting
    #https://stackoverflow.com/questions/38372016/split-nested-array-values-from-pandas-dataframe-cell-over-multiple-rows?newreg=1c04242af3c7428faaecc1daf25d783a
   #https://stackoverflow.com/questions/52200710/pandasseaborn-faceting-with-multidimensional-dataframes
    #e.g. could have one row for each date and 60 columns for trial series?
    
    #let's just get a few variables
df2= df[['RatID','x_M_DSPElatency','x_E_DSLaser','x_N_NSPElatency','x_F_NSLaser']].copy()


#really interesting potential solution looks like here we get 2 indices, one for subject and one for file (date)
unnested_lst = []
for col in df2.columns:
    unnested_lst.append(df2[col].apply(pd.Series).stack())
result = pd.concat(unnested_lst, axis=1, keys=df2.columns).fillna(method='ffill')

#Now let's perform some preliminary analysis, make a new variable for DS PE outcome per trial
result['DSPEoutcome']= result['x_M_DSPElatency']
result['DSPEoutcome']=result['DSPEoutcome'].replace(10,0) #10s= no PE
result.loc[result['DSPEoutcome'] > 0, 'DSPEoutcome'] = 1
#also replace 10s latencies with nan (since there was no PE)
result.x_M_DSPElatency[result.x_M_DSPElatency==10] = np.nan

#same for NS
result['NSPEoutcome']= result['x_N_NSPElatency']
result['NSPEoutcome']=result['NSPEoutcome'].replace(10,0) #10s= no PE
result.loc[result['NSPEoutcome'] > 0, 'NSPEoutcome'] = 1
#also replace 10s latencies with nan (since there was no PE)
result.x_N_NSPElatency[result.x_N_NSPElatency==10] = np.nan
    #visualize
import seaborn as sns
import matplotlib.pyplot as plt

#This works!!
# sns.relplot(x=result['file'], y=result['x_K_PEtimestamps'],hue=result['RatID'], data= result)

# sns.histplot(x='x_E_DSLaser',y='x_M_DSPElatency',hue='RatID', data=result)

sns.relplot(x='RatID',y='x_M_DSPElatency',hue='x_E_DSLaser',data=result)

plt.figure()
plt.subplot(1,2,1) #DS
sns.violinplot(x='RatID',y='x_M_DSPElatency',hue='x_E_DSLaser',data=result)
plt.subplot(1,2,2) #NS
sns.violinplot(x='RatID',y='x_N_NSPElatency',hue='x_F_NSLaser',data=result)

plt.figure()
plt.subplot(1,2,1) #DS
sns.barplot(x='RatID',y='x_M_DSPElatency',hue='x_E_DSLaser',data=result)



plt.figure()
sns.boxplot(x='RatID',y='x_M_DSPElatency',hue='x_E_DSLaser',data=result)

# #try multiple hist()
plt.figure()
sns.histplot(data=result, x='x_M_DSPElatency', hue='x_E_DSLaser', multiple='layer')

# g = sns.FacetGrid(result, hue='x_E_DSLaser', size=7.5)
 
# g.map(sns.distplot, 'x_M_DSPELatency', bins=10,
#       kde=False, rug=True).add_legend()
 
# g.set(xlabel='DSPELatency',
#       ylabel='Frequency',
#       title='Distribution of DS PElat by laser state')

# plt.figure()
# #plot DS PE latency based on Laser state?
# grid = sns.FacetGrid(result,row='Group_0_Stgtacr_1_Mcherry_',col='Sex')
# #this works but I think am only getting one session?
# grid.map(lambda _x,_y,**kwargs : sns.histplot(x=_x.values,hue=_y.values),'x_M_DSPElatency','x_E_DSLaser')


#%% Extract Date from filenames
# #just converting filename to date
# import re, datetime

# for ses in range(len(df['file'])):
#     match = re.search('\d{4}\d{2}\d{2}', df['file'][ses][0])
#     df['file'][ses] = datetime.datetime.strptime(match.group(), '%Y%m%d').date()

    

#%% Help from stackexchange
#import plotting resources
import seaborn as sns
import matplotlib.pyplot as plt

# Apply the default theme
sns.set_theme() 

#create dataframe df2 using example data
df2= df[['RatID','file','x_K_PEtimestamps']].copy()

#%% try relplot, fails- unhashable type: 'numpy.ndarray'
# sns.relplot(x=df2['file'],y=df2['x_K_PEtimestamps'],hue=df2['RatID'], data=df2)
   
#%% try scatter plot
# sns.scatterplot(x=df2['file'],y=df2['x_K_PEtimestamps'])

#%% try collect datat in loop, then scatter?
# x= np.empty(len(df2),dtype= 'object')
# y= np.empty(len(df2),dtype= 'object')
# for ses in range(len(df2)):
#     x[ses]= df2['file'][ses]
#     y[ses]= df2['x_K_PEtimestamps'][ses]
#     yStack[ses]= y[ses].column_stack()
    
# # yStack= y.column_stack()
    
# sns.scatterplot(x=x[ses],y=y)

#%% Doing some basic visualizations
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
from pandas_profiling import ProfileReport

#infinite error?
# profile = ProfileReport(df, title='Pandas Profiling Report') #, explorative = True)
    
    
    
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