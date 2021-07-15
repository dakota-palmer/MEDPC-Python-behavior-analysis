%for use with python module https://github.com/dakota-palmer/medpc2excel/tree/RichardLab_config
clear; close all; clc

% profile on; %trying to optimize
%% load .xlsx generated by medpctoexcel python module
%cd to folder containing your .xlsx
cd 'C:\Users\Dakota\Desktop\Opto DS Task Test- Laser Manipulation'%\lickLaserDay'

%default is 1 file per date, containing sheet for each subject (plus one extra)
fileList= dir('*.xlsx');

sessionCount= 1; %for indexing into struct. Multiple 'sessions' per .xlsx file
%here we'll have a struct with fields that have one row for every session.
%mirroring christelle's organization
for file= 1:numel(fileList)
    %load the raw MPC data from .xlsx generated by python medpc2excel module
    [~,sheet_name]=xlsfinfo(fileList(file).name); %one sheet per subject + first sheet 'MSNs'
    %remove the first sheet 'MSNs' (only concerned about raw data)
    sheet_name=sheet_name(2:end);
    
    %just putting into trainData struct, one row per session
    for subj= 1:numel(sheet_name)
        
        %dp manually defining import options to exclude variable W
        %(accidentally saved this as a huge array of 0s so if its included
        %other columns are autofilled to match huge dims)
        %this is an earlier place where we can exclude variables
        %~~opts SPECIFIC TO VP-VTA-STGTACR cue manipulation test~~~~~~~~~~~~~!!
        %opts here will let us retain variable names even if we import as cell array
        opts = detectImportOptions(fileList(file).name,'Sheet',cell2mat(sheet_name(subj)),'Range','A1:X10000');  %still have to specify the full range
%         opts.SelectedVariableNames = opts.SelectedVariableNames([1:end]~=19);  %ignore column 19 (array W)
        
        %read the excel sheet and extract variables using opts defined
        %above
        %Start as a cell array so we can remove empty cells without things
        %being filled as nan. Then convert to table.
%         MPCraw= readtable(fileList(file).name, opts);% 'Sheet', cell2mat(sheet_name(subj)));
        
        %trying readcell instead of table so that variables can have
        %different sizes
        MPCraw= readcell(fileList(file).name, opts, 'Sheet', cell2mat(sheet_name(subj)));

        
        %remove rows containing only NaN (remnants from data import)
%         MPCraw(all(ismissing(MPCraw),2),:)=[]; % for nan - rows
            %slow, ~2min  for one file
        MPCraw= cellfun(@rmmissing,MPCraw,'UniformOutput',false); %only do this for cell array
   
            %slow, another ~2min for one file
        MPCraw= cell2table(MPCraw);

        
        varNames= opts.VariableNames;%MPCraw.Properties.VariableNames; %get var labels
        %label the new table with the variable names
        MPCraw.Properties.VariableNames= varNames;
        
        %!!!~~~Pick only variables you care about~~~~~~~~~~~~~~~!!!
%         varNames= varNames([7,8,9,10,11,12,13,14,17,20,21,22,23,24]); %just pulling vars i want
        varNames([1,2,3,4,5,20]) = []; %delete
        MPCraw= MPCraw(:,varNames); 
        
%         %preallocate struct if first file
%         if file==1
%             trainData=struct;
%             for var=1:numel(varNames)
%                 %estimate each field should have an entry for num files*num subjects
%                 for ses=1:(numel(fileList)*numel(sheet_name))
%                     trainData(ses).(varNames{var})= nan;
%                 end
%             end
%         end
        trainData(sessionCount).subject= sheet_name(subj); 
        trainData(sessionCount).file= fileList(file).name;
        for var = 1:numel(varNames)
                        
            trainData(sessionCount).(varNames{var})= MPCraw(:,var);
            
            %can't import table class into python, so convert to array
            if class(trainData(sessionCount).(varNames{var}))=='table'
                trainData(sessionCount).(varNames{var})=table2array(trainData(sessionCount).(varNames{var}));
            end
        end
        
        sessionCount= sessionCount+1; %iterate sessionCount 
    end
end

%% now associate relevant metadata to each subject (e.g. sex, condition)
%just using a separate spreadsheet for this
ratInfo= readtable('C:\Users\Dakota\Desktop\Opto DS Task Test- Laser Manipulation\vp-vta-stgtacr_subj_metadata.xlsx'); %import rat metadata from excel sheet generated manually
subjects= unique([trainData.subject]);
for subj= 1:numel(subjects)
    varNames= ratInfo.Properties.VariableNames; %get var labels
    
    sessions= find(strcmp([trainData.subject],subjects{subj})); %find sessions matching this subject so we can insert metadata
    
    for ses= sessions
    %Assumes that first column of metadata sheet is subject!
        for var= 2:numel(varNames)
            if strcmp(ratInfo{subj,1}{1},subjects{subj}) %find data matching this subject in xlsx... todo: probably better way to do this
                trainData(ses).(varNames{var})= table2array(ratInfo(subj,var));
            end
%             trainData(ses).(varNames{var})= table2array(ratInfo(strcmp(ratInfo{subj,1}{1},subjects{subj}),var));
        end
    end
end

%% now associate relevant metadata to each Session (e.g. laser parameters, notes, exclusion flag)
%just using a separate spreadsheet for this

%should contain column 'date' in YYYYMMDD format
sesInfo= readtable('C:\Users\Dakota\Desktop\Opto DS Task Test- Laser Manipulation\vp-vta-stgtacr_session_metadata.xlsx'); %import session metadata from excel sheet generated manually

%since metadata will vary based on both subject and session, retain loop
%through unique subjects but get metadata from each unique date
subjects= unique([trainData.subject]);

for subj= 1:numel(subjects)
    varNames= sesInfo.Properties.VariableNames; %get var labels    
    
    sessions= find(strcmp([trainData.subject],subjects{subj})); %find sessions matching this subject so we can insert metadata

    
    for ses= 1:numel(sessions) %for each unique session this subject ran in trainData 
        for var= 2:numel(varNames) %assume column 1 is subject
                                
                %each .xlsx file name in trainData contains date before the '.xlsx', so extract date using strfind
                date= str2num(trainData(sessions(ses)).file(1:strfind(trainData(sessions(ses)).file,'.x')-1));

                %find sessions that match this date and this subject then assign to
                %proper position in trainData
                trainData(sessions(ses)).(varNames{var})= table2array(sesInfo(sesInfo.date==date & strcmp(sesInfo.subject,subjects{subj}),var));
        end
    end
end

%% convert data types for convenience in python
%tables can't be read into python, so convert to array (done earlier)
%cell arrays result in complicated nesting, so convert to char vectors if
%possible

for subj= 1:numel(subjects)
    varNames= fieldnames(trainData); %get var labels
        
    for var= 1:numel(varNames)
%             if iscell(trainData(end).(varNames{var})) %if this is a cell array with string, make char
            for ses= 1:numel(trainData)
                if iscell(trainData(ses).(varNames{var}))
%                     trainData(ses).(varNames{var})= char(trainData(ses).(varNames{var}));
                    %remove empty cells
                    trainData(ses).(varNames{var})= cellfun(@rmmissing,trainData(ses).(varNames{var}),'UniformOutput',false); %only do this for cell array
                    validInd= ~cellfun('isempty',trainData(ses).(varNames{var}));
                    trainData(ses).(varNames{var})=trainData(ses).(varNames{var})(validInd);
                    
                    trainData(ses).(varNames{var})= cell2mat(trainData(ses).(varNames{var}));

                end
            end
    end
end


%% save reorganized trainData
save(strcat(datestr(now,'yyyy-mm-dd-HH-MM-SS'),'trainData.mat'),'trainData');

% profile viewer;
% 
