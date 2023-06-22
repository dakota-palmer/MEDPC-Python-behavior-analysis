clear all
close all
clc

%% Figure options
figPath= strcat(pwd,'\_output\_DS_task_stimDay\');

figFormats= {'.fig','.svg'} %list of formats to save figures as (for saveFig.m)


%% Data import
% CurrentDir ='/Volumes/nsci_richard/Christelle/Codes/Matlab';
% SavingDir = '/Volumes/nsci_richard/Christelle/Codes/Matlab';
% cd(CurrentDir)



% %--christelle opto data
CurrentDir = 'C:\Users\Dakota\Desktop\_christelle_opto_copy';
cd(CurrentDir)

[~,~,raw] = xlsread('OptoStimDayAnalysis051121.xlsx');
[~,~,ratinfo] = xlsread('Christelle Opto Summary Record.xlsx');

% [~,~,ratinfo] = xlsread('Christelle Opto Summary Record_dp.xlsx');

VarNames = raw(1,:);
Data = raw(2: end,:);

 
DSStimulation = struct();

for i = 1 : 41
    if strcmp(VarNames{i},'Subject') %strcmp=compares string. If the string is 'Subject' then.. 
        DSStimulation.(VarNames{i}) = Data(1:end,(i));
    else
        DSStimulation.(VarNames{i}) = cell2mat(Data(1:end,(i)));
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
PEColIndexFirst = find(strcmp(strip(VarNames),'PETimestamps'))+1;% the column after this is the column that has data for the timestamps in Christelle data
PEColIndexFinal = find(strcmp(strip(VarNames),'PEDurations')) - 1;
DSStimulation.PETimestamps = Data(1:end,PEColIndexFirst:PEColIndexFinal); % for first 3 groups the largest number of port entry is 674, which is 908 column
LaserColIndex = find(strcmp(strip(VarNames),'LaserTimestamps'));
DSStimulation.LaserTimestamps = Data(1:end,LaserColIndex+1 : LaserColIndex + 30);


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
DSStimulation.DSCueOnset = cell2mat(DSStimulation.DSCueOnset);% turn the cell arrays into matricies
DSStimulation.NSCueOnset = cell2mat(DSStimulation.NSCueOnset);



for y=1:size(DSStimulation.PETimestamps,1)
    for x=1:size(DSStimulation.PETimestamps,2)
        if ischar(DSStimulation.PETimestamps{y,x})
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
DSStimulation.DSNoLaserArray=NaN(size(DSStimulation.DSCueOnset,1),size(DSStimulation.DSCueOnset,2))
DSStimulation.DSLaserArray=NaN(size(DSStimulation.DSCueOnset,1),size(DSStimulation.DSCueOnset,2))
DSStimulation.NSNoLaserArray=NaN(size(DSStimulation.DSCueOnset,1),size(DSStimulation.DSCueOnset,2))
DSStimulation.NSLaserArray=NaN(size(DSStimulation.DSCueOnset,1),size(DSStimulation.DSCueOnset,2))
%for i = 1 : 2
for j = 1:size(DSStimulation.DSCueOnset,1)
    % DS
    DSNoLaserIndex = 1;
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

DSStimulation.DSNoLaserRelLatMean = nanmean(DSStimulation.DSNoLaserRelLatency,2);
DSStimulation.DSNoLaserAbsLatMean = nanmean(DSStimulation.DSNoLaserAbsLatency,2);
DSStimulation.DSNoLaser10sResponseProb = nanmean(DSStimulation.DSNoLaser10sResponse,2);
DSStimulation.NSNoLaser10sResponseProb = nanmean(DSStimulation.NSNoLaser10sResponse,2);
DSStimulation.NSNoLaserRelLatMean = nanmean(DSStimulation.NSNoLaserRelLatency,2);% removing nan values and calculating the NSRelLatMean across columns
DSStimulation.NSNoLaserAbsLatMean = nanmean(DSStimulation.NSNoLaserAbsLatency,2);% removing nan values and calculating the DSRelLatMean across columns

%%Calculate DS/NS Ratio
DSStimulation.DSNSRatio=DSStimulation.DSPERatio./DSStimulation.NSPERatio

%% Reformat data for plots


CueType=vertcat(ones([length(DSStimulation.Subject) 1]),2.*ones([length(DSStimulation.Subject) 1]),3.*ones([length(DSStimulation.Subject) 1]),4.*ones([length(DSStimulation.Subject) 1])) 
RelLatency=vertcat(DSStimulation.DSNoLaserRelLatMean,DSStimulation.DSLaserRelLatMean,DSStimulation.NSNoLaserRelLatMean,DSStimulation.NSLaserRelLatMean)
ResponseProb=vertcat(DSStimulation.DSNoLaser10sResponseProb,DSStimulation.DSLaser10sResponseProb,DSStimulation.NSNoLaser10sResponseProb,DSStimulation.NSLaser10sResponseProb)
StimLength=vertcat(DSStimulation.StimLength,DSStimulation.StimLength,DSStimulation.StimLength,DSStimulation.StimLength)
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
selection= Mode==1 & Expression==1 & StimLength==0 & DSRatio > 0.4 & DSNSRatio >1.5 
g=gramm('x',Group(selection),'y',RelLatency(selection),'color',CueType(selection))
g.stat_summary('type','sem', 'geom',{'bar' 'black_errorbar'}) 
g.set_names('x','Projections','y','Latency')
g.set_title('Pre Stim Day Latency')
g.draw()


title= 'pre_stimulation_day_peLatency';

saveFig(gcf, figPath,title,figFormats);


%Probability 
figure 
selection= Mode==1 & Expression==1 & StimLength==0 & DSRatio > 0.4 & DSNSRatio >1.5
g=gramm('x',Group(selection),'y',ResponseProb(selection),'color',CueType(selection))
g.stat_summary('type','sem', 'geom',{'bar' 'black_errorbar'})
g.set_names('x','Projections','y','Probability')
g.set_title('Pre Stim Day Probability')
g.draw()

SubjMetCriteria=unique(Subject(selection))


title= 'pre_stimulation_day_peProb';

saveFig(gcf, figPath,title,figFormats);


%% Plot Stim Days - OG Christelle
%%Stimulation Latency

figure 
selection= Mode==1 & Expression==1 & Learner==1 
g(1,1)=gramm('x',Group(selection),'y',RelLatency(selection),'color',CueType(selection))
g(1,1).stat_summary('type','sem', 'geom',{'bar' 'black_errorbar'}) 

g(1,1).facet_grid([],StimLength(selection))
g(1,1).set_names('x','Projections','y','Latency')
g(1,1).set_title('Stim Laser Day Latency')
g.draw()

%%Stimulation Probability

selection= Mode==1 & Expression==1 & Learner==1 
g(2,1)=gramm('x',Group(selection),'y',ResponseProb(selection),'color',CueType(selection))
g(2,1).stat_summary('type','sem', 'geom',{'bar' 'black_errorbar'})
g(2,1).facet_grid([],StimLength(selection))
g(2,1).set_names('x','Projections','y','Probability')
g(2,1).set_title('Stim Laser Day Probability')
g(2,1).no_legend()
g.draw()
% g.export('file_name','Stimulation Day Data','export_path','/Volumes/nsci_richard/Christelle/Data/Opto Project/Figures','file_type','pdf') 

title= 'stimulation_day_data_ogPlot'

saveFig(gcf, figPath,title,figFormats);



%% Plot Stim Days - dp new

%TODO: facet grid not aggreeing with subplots here it seems for some reason

%plot settings 
 %if only 2 groupings, brewer2 and brewer_dark work well 
paletteGroup= 'brewer_dark';
paletteSubj= 'brewer2';

dodge= 0.6; %if dodge constant between point and bar, will align correctly

%%Stimulation Latency
clear g;
figure; 

%adding point of individual observations, but i think requires update()
%call with different grouping for proper alignment

selection= Mode==1 & Expression==1 & Learner==1

% -- 1 = subplot of stimulation PE latency
%- Bar of btwn subj means (group = [] or Group)
group= []; %var by which to group

g(1,1)=gramm('x',Group(selection),'y',RelLatency(selection),'color',CueType(selection), 'group', group);
g(1,1).facet_grid([],StimLength(selection))

g(1,1).stat_summary('type','sem', 'geom',{'bar' 'black_errorbar'}, 'dodge', dodge) 
g(1,1).set_color_options('map',paletteGroup); 

g(1,1).set_names('x','Projections','y','Latency')
g(1,1).set_title('Stim Laser Day Latency')
g.draw()

%- Update with point of individual subj points (group= subject)
group= Subject(selection);
g(1,1).update('x',Group(selection),'y',RelLatency(selection),'color',CueType(selection), 'group', group);
g(1,1).stat_summary('type','sem','geom',{'point'}, 'dodge', dodge)%,'bar' 'black_errorbar'});

g(1,1).set_color_options('map',paletteSubj); 
g.draw()


title= 'stimulation_day_peLatency';

saveFig(gcf, figPath,title,figFormats);


% % -- 2 = subplot of stimulation PE probability

%- Bar of btwn subj means (group = [] or Group)
group= []; %var by which to group

clear g; figure; %TODO: subplot not agreeing with facet so sep figs now

selection= Mode==1 & Expression==1 & Learner==1 

g(1,1)= gramm('x',Group(selection),'y',ResponseProb(selection),'color',CueType(selection), 'group', group);
g(1,1).facet_grid([],StimLength(selection))

g(1,1).stat_summary('type','sem', 'geom',{'bar' 'black_errorbar'}, 'dodge', dodge)
g(1,1).set_color_options('map',paletteGroup); 

g(1,1).set_names('x','Projections','y','Probability')
g(1,1).set_title('Stim Laser Day Probability')
g(1,1).no_legend()
g.draw()

%- Update with point of individual subj points (group= subject)
group= Subject(selection);
g(1,1).update('x',Group(selection),'y',ResponseProb(selection),'color',CueType(selection), 'group', group);

    %todo: tried lines connecting subj but doesn't seem to work-- probs bc
    %color facet wont allow
% g(1,1).geom_line('dodge',dodge) %lines connecting subj
g(1,1).stat_summary('type','sem','geom',{'line'}, 'dodge', dodge)%,'bar' 'black_errorbar'});

% g(1,1).stat_summary('type','sem','geom',{'point'}, 'dodge', dodge)%,'bar' 'black_errorbar'});

g(1,1).set_color_options('map',paletteSubj); 
g.draw()


title= 'stimulation_day_peProbability';

saveFig(gcf, figPath,title,figFormats);

%TODO: 3- lines for each subj (no color facet?)
%still doesn't work below:
% group= Subject(selection);
% 
% g(1,1).update('x',Group(selection),'y',ResponseProb(selection), 'group', group);
% g(1,1).stat_summary('type','sem','geom',{'line'}, 'dodge', dodge)%,'bar' 'black_errorbar'});
% g.draw()


% g.export('file_name','Stimulation Day Data','export_path','/Volumes/nsci_richard/Christelle/Data/Opto Project/Figures','file_type','pdf') 


%% Plot Post-Stim Session

%Latency
figure 
selection= Mode==1 & Expression==1 & Learner==1 & StimLength==20
g=gramm('x',Group(selection),'y',RelLatency(selection),'color',CueType(selection))
g.stat_summary('type','sem', 'geom',{'bar' 'black_errorbar'}) 
g.set_names('x','Projections','y','Latency')
g.set_title('Post Stim Day Latency')
g.draw();

title= 'post_stimulation_day_peLatency';
saveFig(gcf, figPath,title,figFormats);

%Probability 
figure();
selection= Mode==1 & Expression==1 & Learner==1 & StimLength==20
g=gramm('x',Group(selection),'y',ResponseProb(selection),'color',CueType(selection))
g.stat_summary('type','sem', 'geom',{'bar' 'black_errorbar'})
g.set_names('x','Projections','y','Probability')
g.set_title('Post Stim Day Probability')
g.draw()

title= 'post_stimulation_day_peProbability';
saveFig(gcf, figPath,title,figFormats);

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




