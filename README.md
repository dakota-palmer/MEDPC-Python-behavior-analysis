# Python code for analysis of MED-PC behavioral data

Python code used to import, tidy, and analyze MEDPC data in Python.

## Overview

* Import, tidy, & analyze your behavioral time-series data from MEDPC in Python. 

    * Combine behavioral data with manually-defined subject & session metadata.

    * Combine behavioral data from multiple sessions & subjects into single tidy dataframe (with 1 row per event timestamp).

        * Break sessions into trials (with trialTypes) and other custom behavioral epochs.

        * Perform session-based, epoch-based, & trial-based analyses.

* Designed to work with medpc2excel Python package.

* Designed to be generalizable and modular- Currently focused on DS task analyses but should support many custom .MPC protocols & behavioral paradigms.  


## Workflow

### Raw data extraction using medpc2excel

0. Make sure you have Raw input data described in detail below workflow.


### Import and Tidy behavioral time-series  


1. Run importMPCdata.py
    * ***User defines variables depending on their *experimentType* (their .MPC protocol/behavioral paradigm)*** - this supports modularity.
        * *eventVars*= Variable names corresponding to recorded event timestamps (Matching variable name labels in .MPC file / .xlsx columns)

        * *trialVars*= Variable names of event timestamps which should break session into trials 
            * (as of 2023-09-20 analyses largely focused on DS Task .MPC protocols so trialIDs are defined by DS and NS onset times)

        * *idVars*=  Subject & Session metadata variables corresponding to recorded event timestamps

    * Script imports MPC data, combines with relevant subject and session metadata (recorded in separate excel spreadsheets). Saves output tidy dataframe as .pkl file.
        *  Resulting dataframe has 1 row per event timestamp with columns for eventType and metadata
        *  Adds columns for fileIDs (session identifier), trialIDs (within-session), trialTypes (corresponding to trialVars), and other epoch labels (e.g. pre-trial, ITI, and post-trial)
            * This approach enables efficient analyses and subsetting of data based on session-, file-, trial-, and epoch-


### Example analyses & vizualizations

Some examples of analyses & vizualizations using the seaborn package. Again, mostly focused on DS task use-cases as of 2023-09-20:


2. Run behaviorAnalysis.py- Performs additional analyses and saves as .pkl
    
    * Trial-based analyses
        * Event count & event latency per trial
        * Probability of behavioral outcome by trialType

3. Run optoAnalysis.m (for optogenetics experimentType)-  Performs additional optogenetics-focused analyses and saves as .pkl
    * Additional comparisons between trialType (e.g. laser vs no laser) & viral group (e.g. opsin vs control)

* customFunctions.py has additional custom functions including:
    * Subsetting / aggregation of data according to hierarchical organization (e.g. by virus, subject, fileID, trialType, trialID)
    * Automatic figure saving

## Additional info: Raw input data 

1. MedPC data .xslx sheets (generated using medpc2excel Python package)

2. Manually-managed subject metadata .xlsx sheet (containing relevant metadata for each subject e.g. viral group, experimental condition, sex)

3. Manually-managed session metadata .xlsx sheet (containing relevant metadata for each session e.g. training stage, other session parameters)


## Related Projects

### MEDPC Preprocessing: https://github.com/dakota-palmer/medpc_preprocessing


### medpc2excel: https://github.com/dakota-palmer/medpc2excel

### Similar code for use in conjunction with continuously-sampled time-series signals (fiber photometry): TBD repo (fp-analysis)