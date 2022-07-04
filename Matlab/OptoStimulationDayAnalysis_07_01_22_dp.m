clear all
close all
clc

%% Figure options
figPath= strcat(pwd,'\_output\');

figFormats= {'.fig','.svg'} %list of formats to save figures as (for saveFig.m)



%% Import data

% % % --dp vp-vta-stgtacr data
% CurrentDir ='Z:\Dakota\MEDPC\Downstairs\vp-vta-stgtacr_DStrain';
% SavingDir = 'Z:\Dakota\MEDPC\Downstairs\stgtacr_behavior\laser';
% cd(CurrentDir)
% 
% [~,~,raw] = xlsread('Z:\Dakota\MEDPC\Downstairs\vp-vta-stgtacr_DStrain\vp-vta-stgtacr_mpc2excel _laser.xlsx'); %import the mpc excel data generated by row profile
% [~,~,ratinfo] = xlsread('vp-vta-fp stgtacr metadata.xlsx'); %import rat metadata from excel sheet generated manually


% %--christelle opto data
CurrentDir = 'C:\Users\Dakota\Desktop\_christelle_opto_copy';
SavingDir = 'C:\Users\Dakota\Desktop\_christelle_opto_copy\_output'; %'/Volumes/nsci_richard/Christelle/Codes/Matlab';
cd(CurrentDir)

% [~,~,raw] = xlsread("OptoStimDayAnalysis051121.xlsx");

%slow to read entire allses xlsx
[~,~,raw] = xlsread("christelle_opto_data_allSessions_withMSN_stripped_dp.xlsx"); %dp new all ses xlsx

% [~,~,ratinfo] =  xlsread('Christelle Opto Summary Record.xlsx');
[~,~,ratinfo] = xlsread('Christelle Opto Summary Record_dp.xlsx');


VarNames = raw(1,:);
Data = raw(2: end,:);

% first convert to table(nice to work with)
% cell2table kinda slow here? profiling... 247s
Data= cell2table(raw);

%assign first row as column names
Data.Properties.VariableNames = Data{1,:};

%% --SUBSET data from only opto manipulation stages

%-'Experiment' field should have notes for laser stim days? - imperfect,
%relies on user imput and I saw some that I think were left blank
%search for files with stimulation day .mpc specifically

%  unique(Data.Experiment(:))
% experimentStringToFind= {'STIM DAY', 'STIMULATION DAY', 'STIMULATION TEST'};


% - just use StimLength later on to exclude
% % Better to use MSN if possible
% %-' MSN ' field has the MSN used for each session.
% % unique(Data.MSN);
% %- seems that 'PulsePal Gated Stimulation' = 10s laser
% % -seems that 'PulsePal Opto Laser DS Code' = 1s laser
% msnToInclude= {'PulsePal Opto Laser DS Code', 'PulsePal Gated Stimulation'}
% 
% % find index of data rows matching msnToInclude
% ind= [];
% ind= ismember(Data.MSN, msnToInclude);
% 
% %subset data
% Data= Data(ind, :);

% Remove empty data entries (missing Subject)  ? %TODO: Validate, make sure these are
% actually empty sessions
ind= [];

ind= cellfun(@isnan,Data.Subject,'UniformOutput',false);

ind= ~cellfun(@any,ind);

Data= Data(ind,:);

%Remove ses where NumDSCues blank 
ind= [];

ind= cellfun(@ischar,Data.NumDSCues,'UniformOutput',false);

ind= ~cellfun(@any,ind);

Data= Data(ind,:);

 
% Noting another weird empty data entry (82) 
% DS Cue onsets are all blank...
% Probably due to macro or something autofilling subject? Search for these
% and remove also.
ind= [];
% ind= Data.NumDSCues>0 %non-zero
ind= [Data.NumDSCues{:}] >0;

Data= Data(ind,:);

%% -- Use Christelle's spreadsheet to find StimLength for sessions
%- StimLength seems manually added by Christelle per session in .xlsx

%initialize StimLength field
Data{:,"StimLength"}= {nan};%cell(size(Data,1));

%load the original sheet used by Christelle
[~,~,DataOG] = xlsread("OptoStimDayAnalysis051121.xlsx");

DataOG= cell2table(DataOG);

DataOG.Properties.VariableNames = DataOG{1,:};

DataOG= DataOG(2:end,:);

%get unique subjects & sessions from my sheet for matching
subjects= unique(Data.Subject);

% dates= unique([Data.StartDate{:}]);

%loop thru unique subj & dates to match up StimLengths between .xlsx sheets
for subj= 1:numel(subjects)
    ind= [];
    ind= strcmp(Data.Subject,subjects{subj});
    
    %find dates for this subject
    datesThisSubj= [];
    datesThisSubj= unique([Data.StartDate{ind}]); 

    %search original spreadsheet for matches
    for date = 1:numel(datesThisSubj)
        %get data matching this session from OG xlsx
        indOG= [];
        
        indOG= strcmp(DataOG.Subject,subjects{subj});
        
        indOG= indOG &  ismember([DataOG.StartDate{:}], datesThisSubj(date))';
     
        StimLength= [];
        StimLength= DataOG.StimLength(indOG);
        
        if isempty(StimLength) %if not found, make nan
            StimLength= {nan};
        end
        
        %insert into updated Data on matching session
        ind=[];
        ind= strcmp(Data.Subject,subjects{subj});
        ind= ind &  ismember([Data.StartDate{:}], datesThisSubj(date))';

        
        Data{ind, "StimLength"}= StimLength;
        

    end
    
    
end

 %Update VsrNames!
 VarNames= Data.Properties.VariableNames;

 %% Exclude data without StimLength
 
 % find index of data rows matching msnToInclude
ind= [];
ind= ~isnan([Data.StimLength{:}]);

%subset data
Data= Data(ind, :);
 
%% searching for missing files

%185 sessions in original sheet
%only 142 in mine...

% - diffs
% + OM1
% - multiple subjs test 200121 , 200123
% 
datesOG= unique([DataOG.StartDate{:}]);
datesNew= unique([Data.StartDate{:}]);

datesMissing= datesOG(~ismember(datesOG,datesNew))

 
 
 %% Save this Data set as .xlsx (to compare against orginial)
filename = '_new_Data.xlsx';
% writetable(Data,filename);

%% convert table back to original format (so works with old code)
Data=table2cell(Data);




%% Initialize DSStimulation struct to hold data
DSStimulation = struct();

%remove spaces in VarName
VarNames= strrep(VarNames, ' ','');

%dp- seems christelle looped thru 41 simply bc first 41 variables were ones
% she wanted saved into the struct. I left others in.

%for her col 41= 'TotalLaserTrials'

%old- I could get rid of the extra data or just include it all (will do this, shouldn't hurt)
% for me this is col 69

%dp getting rid of extra data cols in spreadsheet.
%now TotalLaserTrials is col 45

for i = 1 :45 %41
    if strcmp(VarNames{i},'Subject') %strcmp=compares string. If the string is 'Subject' then.. 
        DSStimulation.(VarNames{i}) = Data(1:end,(i));
    else
        %dp- seems cell2mat here is used for math computations later on..
        %make exception for strings
        if any(cellfun(@ischar, Data(:,i)))%any(ischar(Data{:,i}))
            DSStimulation.(VarNames{i}) = (Data(1:end,(i)));%cell2mat(Data(1:end,(i)));
        else
            DSStimulation.(VarNames{i}) = cell2mat(Data(1:end,(i)));
        end
    end
end

for i = 1 : size(DSStimulation.Subject,1)
    DSStimulation.Group{i,1} = DSStimulation.Subject{i,1}(1:2);
    DSStimulation.SubjectNum(i,1) = str2double(DSStimulation.Subject{i,1}(3:end));
end

DSColIndex = find(strcmp(strip(VarNames),'DSCueOnset'));
DSStimulation.DSCueOnset = Data(1:end,DSColIndex+1 : DSColIndex + 29); % 30 trials of DS, not sure this is the same as Runbo's?
NSColIndex = find(strcmp(strip(VarNames),'NSCueOnset'));
DSStimulation.NSCueOnset = Data(1:end,NSColIndex : NSColIndex + 29); % Christelle's has 29 trials of NS??

%dp add StimLength field (at end of my data  so search)
ind=[];
ind = find(strcmp(strip(VarNames),'StimLength'));
DSStimulation.StimLength = Data(1:end,ind);
DSStimulation.StimLength= cell2mat(DSStimulation.StimLength);

%DP clearly missing port entries, only getting like 160 PEtimestamps
%this dependence on the row profile is a problem? 
PEColIndexFirst = find(strcmp(strip(VarNames),'PETimestamps'))+1;% the column after this is the column that has data for the timestamps in Christelle data
PEColIndexFinal = find(strcmp(strip(VarNames),'PEDurations')) - 1;
DSStimulation.PETimestamps = Data(1:end,PEColIndexFirst:PEColIndexFinal); % for first 3 groups the largest number of port entry is 674, which is 908 column
LaserColIndex = find(strcmp(strip(VarNames),'LaserTimestamps'));
DSStimulation.LaserTimestamps = Data(1:end,LaserColIndex+1 : LaserColIndex + 30);

%dp add laser status for each trial
DSColIndex = find(strcmp(strip(VarNames),'DSLaserTrialArray'));
DSStimulation.DSLaserTrialArray = Data(1:end,DSColIndex+1 : DSColIndex + 29);
NSColIndex = find(strcmp(strip(VarNames),'NSLaserTrialArray'));
DSStimulation.NSLaserTrialArray = Data(1:end,NSColIndex : NSColIndex + 29); % Christelle's has 29 trials of NS??


medPCDSlatIndex = find(strcmp(strip(VarNames),'medPCDSLat'));
DSStimulation.medPCDSLat = Data(1:end,medPCDSlatIndex : medPCDSlatIndex + 29); % 30 trials of DS
medPCNSlatIndex = find(strcmp(strip(VarNames),'medPCNSLat'));
DSStimulation.medPCNSLat = Data(1:end,medPCNSlatIndex : medPCNSlatIndex + 29); % 30 trials of NS

for i = 1 : length(DSStimulation.Subject)
    ind = strcmp(DSStimulation.Subject{i},ratinfo(:,1));
    DSStimulation.Sex{i,1} = ratinfo{ind,3};
    DSStimulation.Expression{i,1}=ratinfo{ind,6};
    DSStimulation.ExpType{i,1}=ratinfo{ind,5};
    DSStimulation.Projection{i,1}=ratinfo{ind,4};
    DSStimulation.RatID{i,1}=ratinfo{ind,10};    
    DSStimulation.Learner{i,1}=ratinfo{ind,11};  
end
%% Sort into DS vs NS Laser vs No Laser Arrays
DSStimulation.DSCueOnset =  cell2mat(DSStimulation.DSCueOnset);% turn the cell arrays into matricies
DSStimulation.NSCueOnset = cell2mat(DSStimulation.NSCueOnset);

%each row is a session, each column is a cue (DS and NS are separated)

% dp- 'PETimestamps controlling the loop here can't be right? It's capped
% off at 126 despite many more total PEs in sessions...

% here simply overwriting empty spots in array with nan
for y=1:size(DSStimulation.PETimestamps,1)
    for x=1:size(DSStimulation.PETimestamps,2)
        if ischar(DSStimulation.PETimestamps{y,x}) %dp- this is true if placeholder variable is present? e.g. if no PE logged in this slot?
           DSStimulation.PETimestamps{y,x} = NaN;
        end
    end
end

for y=1:size(DSStimulation.LaserTimestamps,1)
    for x=1:size(DSStimulation.LaserTimestamps,2)
        if ischar(DSStimulation.LaserTimestamps{y,x})
           DSStimulation.LaserTimestamps{y,x} = NaN;
        end
    end
end

DSStimulation.PETimestamps = cell2mat(DSStimulation.PETimestamps);
DSStimulation.LaserTimestamps = cell2mat(DSStimulation.LaserTimestamps);
%%
GroupIndex = 1;

%initialize trial type arrays with nan
DSStimulation.DSNoLaserArray=NaN(size(DSStimulation.DSCueOnset,1),size(DSStimulation.DSCueOnset,2))
DSStimulation.DSLaserArray=NaN(size(DSStimulation.DSCueOnset,1),size(DSStimulation.DSCueOnset,2))
DSStimulation.NSNoLaserArray=NaN(size(DSStimulation.DSCueOnset,1),size(DSStimulation.DSCueOnset,2))
DSStimulation.NSLaserArray=NaN(size(DSStimulation.DSCueOnset,1),size(DSStimulation.DSCueOnset,2))


%for i = 1 : 2
for j = 1:size(DSStimulation.DSCueOnset,1)
    % DS
    DSNoLaserIndex = 1; %counter for each trial type (Laser on vs Laser off)
    DSLaserIndex = 1;
    for k = 1 : size(DSStimulation.DSCueOnset,2)
        if isempty(find(DSStimulation.LaserTimestamps(j,:) == DSStimulation.DSCueOnset(j,k), 1))
            DSStimulation.DSNoLaserArray(j,DSNoLaserIndex) = DSStimulation.DSCueOnset(j,k);
            DSNoLaserIndex = DSNoLaserIndex + 1;
        else
            DSStimulation.DSLaserArray(j,DSLaserIndex) = DSStimulation.DSCueOnset(j,k);
            DSLaserIndex = DSLaserIndex + 1;
        end
    end
    % NS
    NSNoLaserIndex = 1;
    NSLaserIndex = 1;
    for k = 1 : size(DSStimulation.NSCueOnset,2)
        
        if isempty(find(DSStimulation.LaserTimestamps(j,:) == DSStimulation.NSCueOnset(j,k), 1))
            DSStimulation.NSNoLaserArray(j,NSNoLaserIndex) = DSStimulation.NSCueOnset(j,k);
            NSNoLaserIndex = NSNoLaserIndex + 1;
        else
            DSStimulation.NSLaserArray(j,NSLaserIndex) = DSStimulation.NSCueOnset(j,k);
            NSLaserIndex = NSLaserIndex + 1;
        end
    end
end
%end

%% Calculate trial-by-trial PE latencies for DS and NS


for i =  1 : size(DSStimulation.DSLaserArray,1)
    for j = 1 : size(DSStimulation.DSLaserArray,2)
        if ~isnan(DSStimulation.DSLaserArray(i,j)) && DSStimulation.DSLaserArray(i,j) > 0  %&& DSStimulation.medpcDSLat{i,j} > 0.01 % anything that is not a NaN and greater than zero and the latency is greater than 0.01 continues on in the loop
            curDS = DSStimulation.DSLaserArray(i,j); % if all that was true then current DS= the (i,j) cell
            nextDS = DSStimulation.DSCueOnset(i,find(DSStimulation.DSCueOnset(i,:) > curDS,1)); % next DS will be in the same row and the first element that is greater than the curDS in the i row of every column
            nextNS = DSStimulation.NSCueOnset(i,find(DSStimulation.NSCueOnset(i,:) > curDS,1)); % next NS will be in the same row and the first element that is greater than the curDS in variable NSCueOnset
            if ~isempty(nextDS) && ~isempty(nextNS)%if next DS is not empty and next NS is not empty nextcue is the smallest value of the two elements it is comparing
            nextCue = min(nextDS,nextNS);
            elseif isempty(nextDS) && ~isempty(nextNS) % no DS left
                nextCue = nextNS;
            elseif isempty(nextNS) && ~isempty(nextDS) % no NS left
                nextCue = nextDS;
            else % no cue left
                nextCue = inf;%inf is infinity, don't know why?
            end
            curDSDuration = 10; %match up the tone duration location for the current DS with the i location
            firstEnter = DSStimulation.PETimestamps(i,find(DSStimulation.PETimestamps(i,:) > curDS & DSStimulation.PETimestamps(i,:) < nextCue,1 ));% identify when animal first entered by finding the 
            %first element of PETimestamps that is greater than the curDS
            %and less than the next cue
            if isempty(firstEnter)% if the first enter variable is an empry vector than the latencies are NaN
                DSStimulation.DSLaserRelLatency(i,j) = NaN;
                DSStimulation.DSLaserAbsLatency(i,j) = NaN;
                DSStimulation.DSLaser10sResponse(i,j) = 0;
            elseif firstEnter - curDS > curDSDuration % otherwise if the time of first entering-curDS cue time is greater than the DS duration the absolute latencey is the difference between the DScue and the PEtime
                DSStimulation.DSLaserRelLatency(i,j) = NaN;
                DSStimulation.DSLaser10sResponse(i,j) = 0;
                DSStimulation.DSLaserAbsLatency(i,j) = firstEnter - curDS;              
            elseif firstEnter - curDS < curDSDuration % otherwise if the difference between the DS and PE times is less than the duration of the cue (entered during the cue), both the relative and absolute latency is equal to that difference
                DSStimulation.DSLaserRelLatency(i,j) = firstEnter - curDS;
                DSStimulation.DSLaserAbsLatency(i,j) = firstEnter - curDS;
                if firstEnter - curDS <= 10
                    DSStimulation.DSLaser10sResponse(i,j) = 1;
                else
                    DSStimulation.DSLaser10sResponse(i,j) = 0;
                end
            end
        else
            DSStimulation.DSLaserRelLatency(i,j) = NaN; % if the DS cue onset is Nan, equal to zero or the medPC reads the latency as 0.01 then assign these cells a NaN value
            DSStimulation.DSLaserAbsLatency(i,j) = NaN;%  WANT TO CHANGE THIS EVENTUALLY TO HAVE RESPONSE VARIABLES!!
            DSStimulation.DSLaser10sResponse(i,j) = NaN;
        end        
    end
end


% NS Laser latency calcualtion
for i = 1 : size(DSStimulation.NSLaserArray,1)
    for j = 1 : size(DSStimulation.NSLaserArray,2)
        if ~isnan(DSStimulation.NSLaserArray(i,j)) && DSStimulation.NSLaserArray(i,j) > 0 %&& TrainingData.medpcNSLat{i,j} > 0.01
            curNS = DSStimulation.NSLaserArray(i,j);
            nextNS = DSStimulation.NSCueOnset(i,find(DSStimulation.NSCueOnset(i,:) > curNS,1));
            nextDS = DSStimulation.DSCueOnset(i,find(DSStimulation.DSCueOnset(i,:) > curNS,1));
            if ~isempty(nextDS) && ~isempty(nextNS) 
                nextCue = min(nextDS,nextNS);
            elseif isempty(nextDS) && ~isempty(nextNS) % no DS left
                nextCue = nextNS;
            elseif isempty(nextNS) && ~isempty(nextDS) % no NS left
                nextCue = nextDS;
            else % no cue left
                nextCue = inf;
            end
            curNSDuration = 10; % NS always last 10 s
            firstEnter = DSStimulation.PETimestamps(i,find(DSStimulation.PETimestamps(i,:) > curNS & DSStimulation.PETimestamps(i,:) < nextCue,1 ));
            if isempty(firstEnter)
                DSStimulation.NSLaserRelLatency(i,j) = NaN;
                DSStimulation.NSLaserAbsLatency(i,j) = NaN;  
                DSStimulation.NSLaser10sResponse(i,j) = 0;
            elseif firstEnter - curNS > curNSDuration
                DSStimulation.NSLaserRelLatency(i,j) = NaN;
                DSStimulation.NSLaserAbsLatency(i,j) = firstEnter - curNS; 
                DSStimulation.NSLaser10sResponse(i,j) = 0;
            elseif firstEnter - curNS < curNSDuration
                DSStimulation.NSLaserRelLatency(i,j) = firstEnter - curNS;
                DSStimulation.NSLaserAbsLatency(i,j) = firstEnter - curNS;
                DSStimulation.NSLaser10sResponse(i,j) = 1;
            end
        else
            DSStimulation.NSLaserRelLatency(i,j) = NaN;
            DSStimulation.NSLaserAbsLatency(i,j) = NaN;
            DSStimulation.NSLaser10sResponse(i,j) = NaN;
        end
    end
end

DSStimulation.DSLaserRelLatMean = nanmean(DSStimulation.DSLaserRelLatency,2);
DSStimulation.DSLaserAbsLatMean = nanmean(DSStimulation.DSLaserAbsLatency,2);
DSStimulation.DSLaser10sResponseProb = nanmean(DSStimulation.DSLaser10sResponse,2);
DSStimulation.NSLaser10sResponseProb = nanmean(DSStimulation.NSLaser10sResponse,2);
DSStimulation.NSLaserRelLatMean = nanmean(DSStimulation.NSLaserRelLatency,2);% removing nan values and calculating the NSRelLatMean across columns
DSStimulation.NSLaserAbsLatMean = nanmean(DSStimulation.NSLaserAbsLatency,2);% removing nan values and calculating the DSRelLatMean across columns
%% No laser DS latency calculation

for i =  1 : size(DSStimulation.DSNoLaserArray,1)
    for j = 1 : size(DSStimulation.DSNoLaserArray,2)
        if ~isnan(DSStimulation.DSNoLaserArray(i,j)) && DSStimulation.DSNoLaserArray(i,j) > 0  %&& DSStimulation.medpcDSLat{i,j} > 0.01 % anything that is not a NaN and greater than zero and the latency is greater than 0.01 continues on in the loop
            curDS = DSStimulation.DSNoLaserArray(i,j); % if all that was true then current DS= the (i,j) cell
            nextDS = DSStimulation.DSCueOnset(i,find(DSStimulation.DSCueOnset(i,:) > curDS,1)); % next DS will be in the same row and the first element that is greater than the curDS in the i row of every column
            nextNS = DSStimulation.NSCueOnset(i,find(DSStimulation.NSCueOnset(i,:) > curDS,1)); % next NS will be in the same row and the first element that is greater than the curDS in variable NSCueOnset
            if ~isempty(nextDS) && ~isempty(nextNS)%if next DS is not empty and next NS is not empty nextcue is the smallest value of the two elements it is comparing
            nextCue = min(nextDS,nextNS);
            elseif isempty(nextDS) && ~isempty(nextNS) % no DS left
                nextCue = nextNS;
            elseif isempty(nextNS) && ~isempty(nextDS) % no NS left
                nextCue = nextDS;
            else % no cue left
                nextCue = inf;%inf is infinity, don't know why?
            end
            curDSDuration = 10; %match up the tone duration location for the current DS with the i location
            firstEnter = DSStimulation.PETimestamps(i,find(DSStimulation.PETimestamps(i,:) > curDS & DSStimulation.PETimestamps(i,:) < nextCue,1 ));% identify when animal first entered by finding the 
            %first element of PETimestamps that is greater than the curDS
            %and less than the next cue
            if isempty(firstEnter)% if the first enter variable is an empry vector than the latencies are NaN
                DSStimulation.DSNoLaserRelLatency(i,j) = NaN;
                DSStimulation.DSNoLaserAbsLatency(i,j) = NaN;
                DSStimulation.DSNoLaser10sResponse(i,j) = 0;
            elseif firstEnter - curDS > curDSDuration % otherwise if the time of first entering-curDS cue time is greater than the DS duration the absolute latencey is the difference between the DScue and the PEtime
                DSStimulation.DSNoLaserRelLatency(i,j) = NaN;
                DSStimulation.DSNoLaser10sResponse(i,j) = 0;
                DSStimulation.DSNoLaserAbsLatency(i,j) = firstEnter - curDS;              
            elseif firstEnter - curDS < curDSDuration % otherwise if the difference between the DS and PE times is less than the duration of the cue (entered during the cue), both the relative and absolute latency is equal to that difference
                DSStimulation.DSNoLaserRelLatency(i,j) = firstEnter - curDS;
                DSStimulation.DSNoLaserAbsLatency(i,j) = firstEnter - curDS;
                if firstEnter - curDS <= 10
                    DSStimulation.DSNoLaser10sResponse(i,j) = 1;
                else
                    DSStimulation.DSNoLaser10sResponse(i,j) = 0;
                end
            end
        else
            DSStimulation.DSNoLaserRelLatency(i,j) = NaN; % if the DS cue onset is Nan, equal to zero or the medPC reads the latency as 0.01 then assign these cells a NaN value
            DSStimulation.DSNoLaserAbsLatency(i,j) = NaN;%  WANT TO CHANGE THIS EVENTUALLY TO HAVE RESPONSE VARIABLES!!
            DSStimulation.DSNoLaser10sResponse(i,j) = NaN;
        end        
    end
end

% No laser NS latency calcualtion
for i = 1 : size(DSStimulation.NSNoLaserArray,1)
    for j = 1 : size(DSStimulation.NSNoLaserArray,2)
        if ~isnan(DSStimulation.NSNoLaserArray(i,j)) && DSStimulation.NSNoLaserArray(i,j) > 0 %&& TrainingData.medpcNSLat{i,j} > 0.01
            curNS = DSStimulation.NSNoLaserArray(i,j);
            nextNS = DSStimulation.NSCueOnset(i,find(DSStimulation.NSCueOnset(i,:) > curNS,1));
            nextDS = DSStimulation.DSCueOnset(i,find(DSStimulation.DSCueOnset(i,:) > curNS,1));
            if ~isempty(nextDS) && ~isempty(nextNS) 
                nextCue = min(nextDS,nextNS);
            elseif isempty(nextDS) && ~isempty(nextNS) % no DS left
                nextCue = nextNS;
            elseif isempty(nextNS) && ~isempty(nextDS) % no NS left
                nextCue = nextDS;
            else % no cue left
                nextCue = inf;
            end
            curNSDuration = 10; % NS always last 10 s
            firstEnter = DSStimulation.PETimestamps(i,find(DSStimulation.PETimestamps(i,:) > curNS & DSStimulation.PETimestamps(i,:) < nextCue,1 ));
            if isempty(firstEnter)
                DSStimulation.NSNoLaserRelLatency(i,j) = NaN;
                DSStimulation.NSNoLaserAbsLatency(i,j) = NaN;  
                DSStimulation.NSNoLaser10sResponse(i,j) = 0;
            elseif firstEnter - curNS > curNSDuration
                DSStimulation.NSNoLaserRelLatency(i,j) = NaN;
                DSStimulation.NSNoLaserAbsLatency(i,j) = firstEnter - curNS; 
                DSStimulation.NSNoLaser10sResponse(i,j) = 0;
            elseif firstEnter - curNS < curNSDuration
                DSStimulation.NSNoLaserRelLatency(i,j) = firstEnter - curNS;
                DSStimulation.NSNoLaserAbsLatency(i,j) = firstEnter - curNS;
                DSStimulation.NSNoLaser10sResponse(i,j) = 1;
            end
        else
            DSStimulation.NSNoLaserRelLatency(i,j) = NaN;
            DSStimulation.NSNoLaserAbsLatency(i,j) = NaN;
            DSStimulation.NSNoLaser10sResponse(i,j) = NaN;
        end
    end
end

%get the mean values of all trials for each session
%RESPONSE PROB. Taking mean of binary array, not the actual
%probabilities? nope, since nanmean is used it works out the same.

%but the math just doesn't add up to match the MPC calculated ratio

%can calculate probability based on binary array though, just divide the
%number of 1's by the total number of trials of this type (~isnan)
for session= 1:size(DSStimulation.Subject,1)%loop through each session
%     DSStimulation.DSNoLaser10sResponse(session,:)= (numel(DSStimulation.DSNoLaser10sResponse(session,:)==1)/numel(~isnan(DSStimulation.DSNoLaser10sResponse(session,:))));
       test1(session,:)= (sum(DSStimulation.DSNoLaser10sResponse(session,:)==1))/sum(~isnan(DSStimulation.DSNoLaser10sResponse(session,:)));
       test2(session,:)= (sum(DSStimulation.DSLaser10sResponse(session,:)==1))/sum(~isnan(DSStimulation.DSLaser10sResponse(session,:)));

end

DSStimulation.DSNoLaserRelLatMean = nanmean(DSStimulation.DSNoLaserRelLatency,2);
DSStimulation.DSNoLaserAbsLatMean = nanmean(DSStimulation.DSNoLaserAbsLatency,2);
DSStimulation.DSNoLaser10sResponseProb = nanmean(DSStimulation.DSNoLaser10sResponse,2);
DSStimulation.NSNoLaser10sResponseProb = nanmean(DSStimulation.NSNoLaser10sResponse,2);
DSStimulation.NSNoLaserRelLatMean = nanmean(DSStimulation.NSNoLaserRelLatency,2);% removing nan values and calculating the NSRelLatMean across columns
DSStimulation.NSNoLaserAbsLatMean = nanmean(DSStimulation.NSNoLaserAbsLatency,2);% removing nan values and calculating the DSRelLatMean across columns

%%Calculate DS/NS Ratio
DSStimulation.DSNSRatio=DSStimulation.DSPERatio./DSStimulation.NSPERatio

%% Reformat data for plots - result is one value per session per rat so individual trial data lost?

%dp not using CueType. Previously relied on specific cat() sequence of trial types below..
%It actually doesn't seem to work with what's been done below anyway. Info
%is being collapsed within sessions using the vertcat() method below so
%instead of 29 trials with either laser on or off a single session's worth
%of data is represented by one or the other. I suppose it does work since
%those calculations are based originally on those trial types but hard to
%visualize the raw data in this format.

%This trial type info is actually saved in MPC output as
%"DSLaserTrialArray" and "NSLaserTrialArray". Will use these instead (1=
%laser on trial, 0= laser off trial)

CueType=vertcat(ones([length(DSStimulation.Subject) 1]),2.*ones([length(DSStimulation.Subject) 1]),3.*ones([length(DSStimulation.Subject) 1]),4.*ones([length(DSStimulation.Subject) 1])) 
RelLatency=vertcat(DSStimulation.DSNoLaserRelLatMean,DSStimulation.DSLaserRelLatMean,DSStimulation.NSNoLaserRelLatMean,DSStimulation.NSLaserRelLatMean)
ResponseProb=vertcat(DSStimulation.DSNoLaser10sResponseProb,DSStimulation.DSLaser10sResponseProb,DSStimulation.NSNoLaser10sResponseProb,DSStimulation.NSLaser10sResponseProb)

%---- StimLength seems manually added by Christelle per session in .xlsx
StimLength=vertcat(DSStimulation.StimLength,DSStimulation.StimLength,DSStimulation.StimLength,DSStimulation.StimLength)
%----

Group=vertcat(DSStimulation.Group,DSStimulation.Group,DSStimulation.Group,DSStimulation.Group)
Subject=vertcat(DSStimulation.RatID,DSStimulation.RatID,DSStimulation.RatID,DSStimulation.RatID)
Expression=vertcat(DSStimulation.Expression,DSStimulation.Expression,DSStimulation.Expression,DSStimulation.Expression)
Mode=vertcat(DSStimulation.ExpType,DSStimulation.ExpType,DSStimulation.ExpType,DSStimulation.ExpType)
Subject=vertcat(DSStimulation.RatID,DSStimulation.RatID,DSStimulation.RatID,DSStimulation.RatID);
DSRatio=vertcat(DSStimulation.DSPERatio,DSStimulation.DSPERatio,DSStimulation.DSPERatio,DSStimulation.DSPERatio);
DSNSRatio=vertcat(DSStimulation.DSNSRatio,DSStimulation.DSNSRatio,DSStimulation.DSNSRatio,DSStimulation.DSNSRatio);
Learner=vertcat(DSStimulation.Learner,DSStimulation.Learner,DSStimulation.Learner,DSStimulation.Learner);

Learner=cell2mat(Learner);
Expression=cell2mat(Expression);
Mode=cell2mat(Mode);
Subject=cell2mat(Subject);

%% DP reorganizing: All data from all trials instead of data collapsed
% % across session
% CueType= [1,2,3,4]; CueTypeLabel= ['DS','DS+Laser','NS','NS+Laser'];
% 
% %get entire counts of sessions and trials. Will be used for making and
% %indexing arrays
% trialCount= size(DSStimulation.DSLaserTrialArray,2)*2; %*2 because DS & NS
% sessionCount= size(DSStimulation.DSLaserTrialArray,1); %number of files

% Subject= nan(sessionCount,trialCount); % Subject;
% Subject= repmat(Subject,2)

%% plots
%histogram to determine which animals learned

% selection= DSStimulation.StimLength==0
% learn= DSStimulation.NSPERatio(selection)
% animal= DSStimulation.Subject (selection)
% BinNums = [0:.1:1]
% histogram (learn, BinNums)

% 
% selection2 = DSStimulation.DSPERatio(selection) >= 0.6 & DSStimulation.NSPERatio(selection) <= 0.5
% learned= DSStimulation.Subject (selection2)

%% Plot Stim Day 0

%Latency
figure 
selection= Mode==0 & Expression==1 & StimLength==0 %& DSRatio > 0.4 & DSNSRatio >1.5 
g=gramm('x',Group(selection),'y',RelLatency(selection),'color',CueType(selection))
g.stat_summary('type','sem', 'geom',{'bar' 'black_errorbar'}) 
g.set_names('x','Projections','y','Latency')
g.set_title('Pre Stim Day Latency')
g.draw()


%Probability 
figure 
selection= Mode==0 & Expression==1 & StimLength==0 %& DSRatio > 0.4 & DSNSRatio >1.5
g=gramm('x',Group(selection),'y',ResponseProb(selection),'color',CueType(selection))
g.stat_summary('type','sem', 'geom',{'bar' 'black_errorbar'})
g.set_names('x','Projections','y','Probability')
g.set_title('Pre Stim Day Probability')
g.draw()

SubjMetCriteria=unique(Subject(selection))


%% Plot Stim Days 
%%Stimulation Latency

figure 
selection= Mode==0 & Expression==1 & Learner==1 
g(1,1)=gramm('x',Group(selection),'y',RelLatency(selection),'color',CueType(selection))
g(1,1).stat_summary('type','sem', 'geom',{'bar' 'black_errorbar'}) 
g(1,1).facet_grid([],StimLength(selection))
g(1,1).set_names('x','Projections','y','Latency')
g(1,1).set_title('Stim Laser Day Latency')
g.draw()

%%Stimulation Probability

selection= Mode==0 & Expression==1 & Learner==1 
g(2,1)=gramm('x',Group(selection),'y',ResponseProb(selection),'color',CueType(selection))
g(2,1).stat_summary('type','sem', 'geom',{'bar' 'black_errorbar'})
g(2,1).facet_grid([],StimLength(selection))
g(2,1).set_names('x','Projections','y','Probability')
g(2,1).set_title('Stim Laser Day Probability')
g(2,1).no_legend()
g.draw()
g.export('file_name','Stimulation Day Data','export_path',SavingDir,'file_type','pdf') 

%% Plot Post-Stim Session

%Latency
figure 
selection= Mode==0 & Expression==1 & Learner==1 & StimLength==20
g=gramm('x',Group(selection),'y',RelLatency(selection),'color',CueType(selection))
g.stat_summary('type','sem', 'geom',{'bar' 'black_errorbar'}) 
g.set_names('x','Projections','y','Latency')
g.set_title('Post Stim Day Latency')


%Probability 

selection= Mode==0 & Expression==1 & Learner==1 & StimLength==20
g=gramm('x',Group(selection),'y',ResponseProb(selection),'color',CueType(selection))
g.stat_summary('type','sem', 'geom',{'bar' 'black_errorbar'})
g.set_names('x','Projections','y','Probability')
g.set_title('Post Stim Day Probability')
g.draw()


%% Histogram
% %% histogram 
% NSselection= CueType==3 & StimLength==0
% BinNums = [0:.1:1]
% histogram (ResponseProb(NSselection), BinNums)
% 
% figure
% DSselection= CueType==1 & StimLength==0
% BinNums = [0:.1:1]
% histogram (ResponseProb(DSselection), BinNums)

%% -- dp vp-vta-stgtacr specific below
% 
% %% dp plots
% 
% % % Make labels for cueType- not accurate
% CueTypeLabel= cell(size(CueType));
% CueTypeLabel(find(CueType==1))= {'DS'};
% CueTypeLabel(find(CueType==2))= {'DS+Laser'};
% CueTypeLabel(find(CueType==3))= {'NS'};
% CueTypeLabel(find(CueType==4))= {'NS+Laser'};
% 
% %selecting specific subj to plot
% % 
% % subjIncluded= [6, 9]
% 
% % for subj= subjIncluded
%     figure 
%     selection= Subject== 7 | Subject== 10; %strcmp(Subject, 'VP-VTA-STGTACR-07') | strcmp(Subject, 'VP-VTA-STGTACR-10'); %Mode==0 & Expression==1 & Learner==1 
%     g(1,1)=gramm('x',CueTypeLabel(selection),'y',RelLatency(selection),'color',Subject(selection))
%     g(1,1).stat_summary('type','sem', 'geom',{'bar' 'black_errorbar'}) 
% %     g(1,1).facet_grid([],StimLength(selection))
%     g(1,1).geom_point(); %plot raw data
%     g(1,1).set_names('x','Cue Type','y','Latency')
%     g(1,1).set_title('StGtACR Laser Day Latency')
% %     g.draw()
% % end 
% %%Stimulation Probability
% 
% % selection= Mode==0 & Expression==1 & Learner==1 
% g(2,1)=gramm('x',CueTypeLabel(selection),'y',ResponseProb(selection),'color',Subject(selection))
% g(2,1).stat_summary('type','sem', 'geom',{'bar' 'black_errorbar'})
% % g(2,1).facet_grid([],StimLength(selection))
% g(2,1).geom_point(); %plot raw data
% g(2,1).set_names('x','Cue Type','y','Probability')
% g(2,1).set_title('StGtACR Laser Day Probability')
% g(2,1).no_legend()
% g.draw()
% g.export('file_name','Stimulation Day Data','export_path',SavingDir,'file_type','pdf') 
% 
% %% Plot all data
% % I think what I want is to plot
% % probability & latency of the noLaser and Laser trial types 
% 
% %plot progression within session over all trials 
% figure;
% 
% 
% 
% %create trialArray for x axis: sequential count of each trial in session
% %TODO: This should probably be 1:60 for all cues instead of 1:30 for DS and
% %NS separately, could cat() together and have a label for NS & DS?
% trialArray= [1:size(DSStimulation.DSLaserRelLatency,2)]
% trialArray= repmat(trialArray, size(DSStimulation.DSLaserRelLatency,1),1)
% 
% selection= Subject==7 | Subject==10;
% g(1,1)= gramm('x', trialArray(selection,:), 'y', DSStimulation.DSLaserRelLatency(selection,:), 'color', Subject(selection))
% g(1,1).geom_point(); %plot raw data
% 
% g(1,1).draw();


