clear all
close all
clc
%% Figure options
figPath= strcat(pwd,'\_output\_choiceTask\');

% figFormats= {'.png'} %list of formats to save figures as (for saveFig.m)
figFormats= {'.svg'} %list of formats to save figures as (for saveFig.m)


set_gramm_plot_defaults;


%% load data
%CurrentDir ='/Volumes/nsci_richard/Christelle/Codes/Matlab';
%SavingDir = '/Volumes/nsci_richard/Christelle/Codes/Matlab';
%cd(CurrentDir)


% %--christelle opto data
% CurrentDir = 'C:\Users\Dakota\Desktop\_christelle_opto_copy';
CurrentDir = 'C:\Users\Dakota\Desktop\_dp_christelle_opto_workingDir';
cd(CurrentDir)


[~,~,raw] = xlsread('OptoLeverChoiceData');
% [~,~,ratinfo] = xlsread('Christelle Opto Summary Record.xlsx');
[~,~,ratinfo] = xlsread('Christelle Opto Summary Record_dp.xlsx');

VarNames = raw(1,:);
Data = raw(2: end,:);

LeverChoice = struct();


for i=1:18 
    LeverChoice.(VarNames{i}) = Data(1:end,(i));
end

%% assign variables to rats                         
for i = 1 : length(LeverChoice.Subject)
    ind = strcmp(LeverChoice.Subject{i},ratinfo(:,1));
    LeverChoice.Sex{i,1} = ratinfo{ind,3};
    LeverChoice.Expression(i,1)=ratinfo{ind,6};
    LeverChoice.ExpType(i,1)=ratinfo{ind,5};
    LeverChoice.Projection{i,1}=ratinfo{ind,4};
    LeverChoice.RatNum(i,1)=ratinfo{ind,10};    
end

LeverChoice.Session=cell2mat(LeverChoice.Sessions)
LeverChoice.ActiveLeverPress=cell2mat(LeverChoice.ActiveLeverPress)
LeverChoice.InactiveLeverPress=cell2mat(LeverChoice.InactiveLeverPress)
LeverChoice.TrialsCompleted=cell2mat(LeverChoice.TrialsCompleted)
LeverChoice.ActiveLicks=cell2mat(LeverChoice.ActiveLicks)
LeverChoice.InactiveLicks=cell2mat(LeverChoice.InactiveLicks)

%% Elminates animals who didn't lever press enough


%criteria 

% at least 10 trials for proportion & licks per reward calculation


for i =1 : size(LeverChoice.Subject,1)
    if LeverChoice.TrialsCompleted(i,1)>=10
        LeverChoice.Proportion(i,1)=LeverChoice.ActiveLeverPress(i,1)/LeverChoice.TrialsCompleted(i,1);
    else
        LeverChoice.Proportion(i,1)=NaN;
    end
end

for i =1 : size(LeverChoice.Subject,1)
    if LeverChoice.ActiveLeverPress(i,1)>=3 & LeverChoice.TrialsCompleted(i,1)>=10
        LeverChoice.LicksPerReward(i,1)=LeverChoice.ActiveLicks(i,1)/LeverChoice.ActiveLeverPress(i,1);
    else
        LeverChoice.LicksPerReward(i,1)=NaN
    end
end

for i =1 : size(LeverChoice.Subject,1)
    if LeverChoice.InactiveLeverPress(i,1)>=3 & LeverChoice.TrialsCompleted(i,1)>=10
    LeverChoice.LicksPerRewardInactive(i,1)=LeverChoice.InactiveLicks(i,1)/LeverChoice.InactiveLeverPress(i,1); 
    else
        LeverChoice.LicksPerRewardInactive(i,1)=NaN;
    end
end 


%% dp reorganizing data into table for table fxns and easy faceting

choiceTaskTable= table();

%loop thru fields and fill table
allFields= fieldnames(LeverChoice);
for field= 1:numel(allFields)
    choiceTaskTable.(allFields{field})= LeverChoice.(allFields{field});
end


%-dp add virus variable for labelling stim vs inhibition
%initialize
choiceTaskTable(:,"virusType")= {''};


% expType= [0,1]%
expTypesAll= [0,1];
% %1= excitation, 0= inhibition
expTypeLabels= {'inhibition','stimulation'};

%loop thru and assign labels
for thisExpType= 1:numel(expTypesAll)
    %TODO: need to actually match this up w find
    choiceTaskTable(:,"virusType")= expTypeLabels(thisExpType);
    
end

% %1= excitation, 0= inhibition
% ind= [];
% ind= choiceTaskTable.ExpType==1;
% 
% choiceTaskTable(:,"virusType")= {'ChR2'};
% 
% ind= [];
% ind= choiceTaskTable.ExpType==1;
% 
% choiceTaskTable(:,"virusType")= {'eNpHR'};


%% --dp add trainPhaseLabel variable for distinct session types (e.g. active side reversal)

%initialize

choiceTaskTable(:,"trainPhase")= table(nan);
choiceTaskTable(:,"trainPhaseLabel")= {''};

% sessions 1-7 = 'free choice', constant active side
ind= [];
ind= choiceTaskTable.Session < 7;

choiceTaskTable(ind,'trainPhase')= table(1);
choiceTaskTable(ind, "trainPhaseLabel")= {'1-FreeChoice'};

% sessions 8-10 = free choice, 'reversal' of active side
ind= [];
ind= (choiceTaskTable.Session>= 7) & (choiceTaskTable.Session < 10);

choiceTaskTable(ind,'trainPhase')= table(2);
choiceTaskTable(ind, "trainPhaseLabel")= {'2-FreeChoice-Reversal'};

% sessions 10-12 = 'forced choice' trials introduced because of
% perseverating/not sampling stim lever... trials in which only one lever was inserted and the session did not continue until it was pressed.
ind= [];
ind= (choiceTaskTable.Session>= 10) & (choiceTaskTable.Session <= 12);

choiceTaskTable(ind,'trainPhase')= table(3);
choiceTaskTable(ind, "trainPhaseLabel")= {'3-ForcedChoice'};


%for this session 13 = 'Free choice session' post-forced choice
ind= [];
ind= choiceTaskTable.Session == 13;

choiceTaskTable(ind,'trainPhase')= table(4);
choiceTaskTable(ind, "trainPhaseLabel")= {'4-FreeChoice-Test'};


% for this session 14= 'extinction test'  an “extinction test” in which sucrose was no longer delivered, but rats still received optogenetic stimulation during licking after presses on the stimulation lever
ind= [];
ind= choiceTaskTable.Session == 14;

choiceTaskTable(ind,'trainPhase')= table(5);
choiceTaskTable(ind, "trainPhaseLabel")= {'5-Extinction-Test'};

%14 == 'exctinction'

%-dp add trainDayThisPhase for best plotting of trainPhaseLabel facet, for late

%initialize
choiceTaskTable(:, "trainDayThisPhase")= table(nan); %initialize

%use findgroups to groupby subject,trainPhaseLabel and manually cumcount() for
%sessions within-trainPhaseLabel

groupIDs= [];
groupIDs= findgroups(choiceTaskTable.Subject,choiceTaskTable.trainPhaseLabel);

groupIDsUnique= [];
groupIDsUnique= unique(groupIDs);

for thisGroupID= 1:numel(groupIDsUnique)
    %for each groupID, find index matching groupID
    ind= [];
    ind= find(groupIDs==groupIDsUnique(thisGroupID));
    
    %for each groupID, get the table data matching this group
    thisGroup=[];
    thisGroup= choiceTaskTable(ind,:);

    %now cumulative count of observations in this group
    %make default value=1 for each, and then cumsum() to get cumulative count
    thisGroup(:,'cumcount')= table(1);
    thisGroup(:,'cumcount')= table(cumsum(thisGroup.cumcount));
    
    %specific code for trainDayThisPhase
    %assign back into table
    choiceTaskTable(ind, 'trainDayThisPhase')= table(thisGroup.cumcount);
    
end 


%% dp compute N- Count of subjects by sex for each group

expTypesAll= unique(choiceTaskTable.ExpType);
% expTypeLabels= unique(choiceTaskTable.virusType);

for thisExpType= 1:numel(expTypesAll)

%     thisExpTypeLabel= expTypeLabels{expTypesAll==thisExpType};
    thisExpTypeLabel= expTypeLabels{thisExpType};

    
    %subset data- by expType/virus
    ind=[];
    ind= choiceTaskTable.ExpType==expTypesAll(thisExpType);

    data= choiceTaskTable(ind,:);

%     %subset data- by expression %& behavioral criteria
    ind=[];
    ind= data.Expression>0 %& data.Learner==1;

    data= data(ind,:);


    nTable= table;

   
    %initialize variable for cumcount of subjects
    data(:,"cumcountSubj")= table(nan);
    
    %- now limit to one unique subject observation within this subset
    %(findGroups)
    

    groupIDs= [];

    groupIDs= findgroups(data.Projection,data.Sex, data.Subject);

    groupIDsUnique= [];
    groupIDsUnique= unique(groupIDs);

    for thisGroupID= 1:numel(groupIDsUnique)

        %for each groupID, find index matching groupID
        ind= [];
        ind= find(groupIDs==groupIDsUnique(thisGroupID));

        %for each groupID, get the table data matching this group
        thisGroup=[];
        thisGroup= data(ind,:);

        %now cumulative count of observations in this group
        %make default value=1 for each, and then cumsum() to get cumulative count
        thisGroup(:,'cumcount')= table(1);
        thisGroup(:,'cumcount')= table(cumsum(thisGroup.cumcount));    
        
        %assign cumulative count for this subject's sessions back to data
        %table, this will be used to limit to first observation only for
        %count of unique subjects
        data(ind,"cumcountSubject")= thisGroup(:,'cumcount');
        
    end
    
    %- finally subset to 1 row per subject and count this data
    ind=[];
    ind= data.cumcountSubject==1;
    
    data= data(ind,:);
    
    nTable= groupsummary(data, ["ExpType","Projection","Sex"]);
       
    %- save this along with figures
    titleFile= [];
    titleFile= strcat(thisExpTypeLabel,'-N-subjects');

    %save as .csv
    titleFile= strcat(figPath,titleFile,'.csv');
    
    writetable(nTable,titleFile)

end


%% dp analyses- compute probability of each LP type



%% --- dp new plots from table ---

% Calculate *Proportion* of active vs inactive Lever Presses for normalized measure

% first get total count
choiceTaskTable(:,"leverPressTotal")= table(choiceTaskTable.ActiveLeverPress+choiceTaskTable.InactiveLeverPress);

% proportion = count/total count
choiceTaskTable(:,"probActiveLP")= table(choiceTaskTable.ActiveLeverPress./choiceTaskTable.leverPressTotal);

choiceTaskTable(:,"probInactiveLP")= table(choiceTaskTable.InactiveLeverPress./choiceTaskTable.leverPressTotal);


%% dp plot of lever press Count by phase over time- mean and individual
cmapSubj= cmapBlueGraySubj;
cmapGrand= cmapBlueGrayGrand;

%run separately based on stim vs inhibition
expTypesAll= unique(choiceTaskTable.ExpType);

for thisExpType= 1:numel(expTypesAll)

    thisExpTypeLabel= expTypeLabels{thisExpType};

    %subset data- by expType/virus
    ind=[];
    ind= choiceTaskTable.ExpType==expTypesAll(thisExpType);

    data= choiceTaskTable(ind,:);
   
    %stack() to make inactive/active LP a variable
    data= stack(data, {'ActiveLeverPress', 'InactiveLeverPress'}, 'IndexVariableName', 'typeLP', 'NewDataVariableName', 'countLP');

    %generate figure
    figure; clear d;

    %-- individual subj
    group= data.Subject;

    d=gramm('x',data.Session,'y',data.countLP,'color',data.typeLP, 'group', group)

    % %facet by trainPhaseLabel - ideally could set sharex of facets false but idk w gramm
    % d.facet_grid([],data.trainPhaseLabel);

    % %facet by virus, trainPhaseLabel
    d.facet_grid(data.Projection,data.trainPhaseLabel);

    % %facet by virus
    % d.facet_grid(data.Projection,[]);


    d.stat_summary('type','sem','geom','area');
%     d.set_names('x','Session','y','Number of Lever Presses','color','Lever Side')
    d.set_names('row','Target','column','Phase','x','Session','y','Number of Lever Presses','color','Lever Side')

    
    d().set_line_options('base_size',linewidthSubj);
    d.set_color_options('map', cmapSubj);

    d.no_legend(); %prevent legend duplicates if you like


    %set text options
    d.set_text_options(text_options_DefaultStyle{:}); 


    d.draw()

    %-- btwn subj mean as well
    group= [];

    d.update('x',data.Session,'y',data.countLP,'color',data.typeLP, 'group', group)

    d.stat_summary('type','sem','geom','area');
    % d.stat_boxplot();


    d.set_names('x','Session','y','Number of Lever Presses','color','Lever Side')
%     d.set_names('row','Target','column','Phase','x','Session','y','Number of Lever Presses','color','Lever Side')

    
    d().set_line_options('base_size',linewidthGrand);
    d.set_color_options('map', cmapGrand);


    figTitle= strcat('choiceTask-',thisExpTypeLabel,'-','LP-Count-across-sessions-all');   
    d.set_title(figTitle);   

    %Zoom in on lower LP subjects if desired
    % d().axe_property( 'YLim',[0 300]) %low responders
    % d().axe_property( 'YLim',[0, 1200]) %high responders

    % SET X TICK = 1 SESSION
    % d.axe_property('XTick',[min(data.trainDayThisPhase):1:max(data.trainDayThisPhase)]); %,'YLim',[0 75],'YTick',[0:25:75]);


    d.draw();
    
    saveFig(gcf, figPath,figTitle,figFormats);


end %end expType/virus loop


%% dp plot of lever press Proportion by phase over time- mean and individual
cmapSubj= cmapBlueGraySubj;
cmapGrand= cmapBlueGrayGrand;

%run separately based on stim vs inhibition
expTypesAll= unique(choiceTaskTable.ExpType);

for thisExpType= 1:numel(expTypesAll)

    thisExpTypeLabel= expTypeLabels{thisExpType};

    %subset data- by expType/virus
    ind=[];
    ind= choiceTaskTable.ExpType==expTypesAll(thisExpType);

    data= choiceTaskTable(ind,:);
   
    %stack() to make inactive/active LP a variable
    data= stack(data, {'probActiveLP', 'probInactiveLP'}, 'IndexVariableName', 'typeLP', 'NewDataVariableName', 'probLP');

    %generate figure
    figure; clear d;

    %-- individual subj
    group= data.Subject;

    d=gramm('x',data.Session,'y',data.probLP,'color',data.typeLP, 'group', group)

    % %facet by trainPhaseLabel - ideally could set sharex of facets false but idk w gramm
    % d.facet_grid([],data.trainPhaseLabel);

    % %facet by virus, trainPhaseLabel
    d.facet_grid(data.Projection,data.trainPhaseLabel);

    % %facet by virus
    % d.facet_grid(data.Projection,[]);


    d.stat_summary('type','sem','geom','area');
%     d.set_names('x','Session','y','Proportion of Lever Presses','color','Lever Side')
    d.set_names('row','Target','column','Phase','x','Session','y','Proportion of Lever Presses','color','Lever Side')

    d().set_line_options('base_size',linewidthSubj);
    d.set_color_options('map', cmapSubj);

    d.no_legend(); %prevent legend duplicates if you like


    %set text options
    d.set_text_options(text_options_DefaultStyle{:}); 


    d.draw()

    %-- btwn subj mean as well
    group= [];

    d.update('x',data.Session,'y',data.probLP,'color',data.typeLP, 'group', group)

    d.stat_summary('type','sem','geom','area');
    % d.stat_boxplot();


    d.set_names('x','Session','y','Proportion of Lever Presses','color','Lever Side')

    d().set_line_options('base_size',linewidthGrand);
    d.set_color_options('map', cmapGrand);


    figTitle= strcat('choiceTask-',thisExpTypeLabel,'-','LP-Proportion-across-sessions-all');   
    d.set_title(figTitle);   

    %Zoom in on lower LP subjects if desired
    % d().axe_property( 'YLim',[0 300]) %low responders
    % d().axe_property( 'YLim',[0, 1200]) %high responders

    % SET X TICK = 1 SESSION
    % d.axe_property('XTick',[min(data.trainDayThisPhase):1:max(data.trainDayThisPhase)]); %,'YLim',[0 75],'YTick',[0:25:75]);


    d.draw();
    
    saveFig(gcf, figPath,figTitle,figFormats);


end %end expType/virus loop


%% ~~~~~-dp CHOICE TASK FIGURE- Pre-Reversal (Phase 1) ~~~~~~~~~~~~~~~~~~~~~~~~~~~~

%subset data from Phase 1

%1a) Acquisition of lever pressing + Probability
%1b) Proportion of active vs inactive LP
%1c) Licks per reward

cmapSubj= cmapBlueGraySubj;
cmapGrand= cmapBlueGrayGrand;

%run separately based on stim vs inhibition
expTypesAll= unique(choiceTaskTable.ExpType);

for thisExpType= 1:numel(expTypesAll)

    thisExpTypeLabel= expTypeLabels{thisExpType};

    %subset data- by expType/virus
    ind=[];
    ind= choiceTaskTable.ExpType==expTypesAll(thisExpType);

    data0=[];
    data0= choiceTaskTable(ind,:);
    
    %subset data- by trainPhase
    phasesToInclude= [1]; %list of phases to include 
    
    ind=[];
    
    ind= ismember(data0.trainPhase, phasesToInclude);

    data0= data0(ind,:);

    %---manual faceting by target/projection (& data subsetting)
   clear d; figure;
%    d= gramm(numel(projectionsAll),3);
    %---Subset further by projection/target for manual facet------
    projectionsAll= unique(data0.Projection);
    
    for thisProjection= 1:numel(projectionsAll)
        data=[];
        
     % Subset further by projection/target for manual facet
        ind=[]
        ind= strcmp(data0.Projection,projectionsAll{thisProjection});
        
        data= data0(ind,:);
        
       % ~~~~~~~~~~~~~~~A) Count LP ~~~~~~~~~~~~~~~~~~~~~~
    
            %stack() to make inactive/active LP a variable
            data2= [];
            data2= stack(data, {'ActiveLeverPress', 'InactiveLeverPress'}, 'IndexVariableName', 'typeLP', 'NewDataVariableName', 'countLP');

            %generate figure
%             figure; %clear d;
        
        %-- individual subj
        group= data2.Subject;

        d(thisProjection,1)=gramm('x',data2.Session,'y',data2.countLP,'color',data2.typeLP, 'group', group)

        % %facet by trainPhaseLabel - ideally could set sharex of facets false but idk w gramm
        % d.facet_grid([],data2.trainPhaseLabel);

        % %facet by virus, trainPhaseLabel
%         d.facet_grid(data2.Projection,data2.trainPhaseLabel);

        % %facet by virus
%         d.facet_grid(data2.Projection,[]);


        d(thisProjection,1).stat_summary('type','sem','geom','area');
    %     d.set_names('x','Session','y','Number of Lever Presses','color','Lever Side')
        d(thisProjection,1).set_names('row','Target','column','Phase','x','Session','y','Number of Lever Presses','color','Lever Side')


        d(thisProjection,1).set_line_options('base_size',linewidthSubj);
        d(thisProjection,1).set_color_options('map', cmapSubj);

        d(thisProjection,1).no_legend(); %prevent legend duplicates if you like


        %set text options
        d(thisProjection,1).set_text_options(text_options_DefaultStyle{:}); 


%         d(thisProjection,1).draw()
%         d.draw();

        %-- btwn subj mean as well
        group= [];

        d(thisProjection,1).update('x',data2.Session,'y',data2.countLP,'color',data2.typeLP, 'group', group)

        d(thisProjection,1).stat_summary('type','sem','geom','area');
        % d.stat_boxplot();


        d(thisProjection,1).set_names('x','Session','y','Number of Lever Presses','color','Lever Side')
    %     d.set_names('row','Target','column','Phase','x','Session','y','Number of Lever Presses','color','Lever Side')


        d(thisProjection,1).set_line_options('base_size',linewidthGrand);
        d(thisProjection,1).set_color_options('map', cmapGrand);
        d(thisProjection,1).no_legend(); %prevent legend duplicates if you like


        figTitle= strcat('choiceTask-',thisExpTypeLabel,'-','LP-Count-across-sessions-all');   
        d(thisProjection,1).set_title(figTitle);   

        %Zoom in on lower LP subjects if desired
        % d().axe_property( 'YLim',[0 300]) %low responders
        % d().axe_property( 'YLim',[0, 1200]) %high responders

        % SET X TICK = 1 SESSION
        % d.axe_property('XTick',[min(data2.trainDayThisPhase):1:max(data2.trainDayThisPhase)]); %,'YLim',[0 75],'YTick',[0:25:75]);


%         d(thisProjection,1).draw();
%         d.draw();






        %~~~~~~~~~~~~~~~~~~~~~B) Proportion LP ~~~~~~~~~~~~~~~~~~~~~~~~
        %stack() to make inactive/active LP a variable
        data2=[];
        data2= stack(data, {'probActiveLP', 'probInactiveLP'}, 'IndexVariableName', 'typeLP', 'NewDataVariableName', 'probLP');

        %-- individual subj
        group= data2.Subject;

        d(thisProjection,2)=gramm('x',data2.Session,'y',data2.probLP,'color',data2.typeLP, 'group', group)

        % %facet by virus, trainPhaseLabel
    %     d.facet_grid(data2.Projection,data2.trainPhaseLabel);

        % %facet by virus
%          d(thisProjection,2).facet_grid(data2.Projection,[]);


         d(thisProjection,2).stat_summary('type','sem','geom','area');
    %     d.set_names('x','Session','y','Proportion of Lever Presses','color','Lever Side')
         d(thisProjection,2).set_names('row','Target','column','Phase','x','Session','y','Proportion of Lever Presses','color','Lever Side')

        d(thisProjection,2).set_line_options('base_size',linewidthSubj);
        d(thisProjection,2).set_color_options('map', cmapSubj);

        d(thisProjection,2).no_legend(); %prevent legend duplicates if you like


        %set text options
         d(thisProjection,2).set_text_options(text_options_DefaultStyle{:}); 

        
%          d(thisProjection,2).draw()
%          d.draw();   
         
        %-- btwn subj mean as well
        group= [];

         d(thisProjection,2).update('x',data2.Session,'y',data2.probLP,'color',data2.typeLP, 'group', group)

         d(thisProjection,2).stat_summary('type','sem','geom','area');
        % d.stat_boxplot();


         d(thisProjection,2).set_names('x','Session','y','Proportion of Lever Presses','color','Lever Side')

         d(thisProjection,2).set_line_options('base_size',linewidthGrand);
         d(thisProjection,2).set_color_options('map', cmapGrand);

        d(thisProjection,2).no_legend(); %prevent legend duplicates if you like

         
        figTitle= strcat('choiceTask-FIGURE-1-',thisExpTypeLabel,'-','LP-Acquisition');   
        d(thisProjection,2).set_title(figTitle);   

        
        %~~~~~~~~~~~~~~~~~~~C) Licks per Reward ~~~~~~~~~~~~~~~~~~~~~~~
                %TODO: all trials instead of aggregate? confirm how is this
                %calculated

          %stack() to make inactive/active LP a variable
        data2=[];
        data2= stack(data, {'LicksPerReward', 'LicksPerRewardInactive'}, 'IndexVariableName', 'typeLP', 'NewDataVariableName', 'licksPerReward');

        %-- individual subj
        group= data2.Subject;

        d(thisProjection,3)=gramm('x',data2.Session,'y',data2.licksPerReward,'color',data2.typeLP, 'group', group)

        % %facet by virus, trainPhaseLabel
    %     d.facet_grid(data2.Projection,data2.trainPhaseLabel);

        % %facet by virus
%          d(thisProjection,2).facet_grid(data2.Projection,[]);


         d(thisProjection,3).stat_summary('type','sem','geom','area');
    %     d.set_names('x','Session','y','Proportion of Lever Presses','color','Lever Side')
         d(thisProjection,3).set_names('row','Target','column','Phase','x','Session','y','Licks per Reward','color','Lever Side')

        d(thisProjection,3).set_line_options('base_size',linewidthSubj);
        d(thisProjection,3).set_color_options('map', cmapSubj);

        d(thisProjection,3).no_legend(); %prevent legend duplicates if you like


        %set text options
         d(thisProjection,3).set_text_options(text_options_DefaultStyle{:}); 

        
%          d(thisProjection,2).draw()
%          d.draw();   
         
        %-- btwn subj mean as well
        group= [];

         d(thisProjection,3).update('x',data2.Session,'y',data2.licksPerReward,'color',data2.typeLP, 'group', group)

         d(thisProjection,3).stat_summary('type','sem','geom','area');
        % d.stat_boxplot();


         d(thisProjection,3).set_names('x','Session','y','Licks per reward','color','Lever Side')

         d(thisProjection,3).set_line_options('base_size',linewidthGrand);
         d(thisProjection,3).set_color_options('map', cmapGrand);

        d(thisProjection,3).no_legend(); %prevent legend duplicates if you like

        figTitle= strcat(projectionsAll{thisProjection},'licks per reward');   
        d(thisProjection,3).set_title('TEST');   


    end %end projection/target loop
    
    %draw only at end?
            figTitle= strcat('choiceTask-FIGURE-1-',thisExpTypeLabel,'-','LP-Acquisition');   
            d().set_title(figTitle);   
            d.draw(); 
            saveFig(gcf, figPath,figTitle,figFormats);

    
end %end expType/virus loop



%% TODO: could loop through phasesToInclude instead of doubling code

%% ~~~~~-dp CHOICE TASK FIGURE 2- Forced Choice (Phase 3) ~~~~~~~~~~~~~~~~~~~~~~~~~~~~

%subset data from Phase 3

%1a) Acquisition of lever pressing + Probability
%1b) Proportion of active vs inactive LP
%1c) Licks per reward

cmapSubj= cmapBlueGraySubj;
cmapGrand= cmapBlueGrayGrand;

%run separately based on stim vs inhibition
expTypesAll= unique(choiceTaskTable.ExpType);

for thisExpType= 1:numel(expTypesAll)

    thisExpTypeLabel= expTypeLabels{thisExpType};

    %subset data- by expType/virus
    ind=[];
    ind= choiceTaskTable.ExpType==expTypesAll(thisExpType);

    data0=[];
    data0= choiceTaskTable(ind,:);
    
    %subset data- by trainPhase
    phasesToInclude= [3]; %list of phases to include 
    
    ind=[];
    
    ind= ismember(data0.trainPhase, phasesToInclude);

    data0= data0(ind,:);

    %---manual faceting by target/projection (& data subsetting)
   clear d; figure;
%    d= gramm(numel(projectionsAll),3);
    %---Subset further by projection/target for manual facet------
    projectionsAll= unique(data0.Projection);
    
    for thisProjection= 1:numel(projectionsAll)
        data=[];
        
     % Subset further by projection/target for manual facet
        ind=[]
        ind= strcmp(data0.Projection,projectionsAll{thisProjection});
        
        data= data0(ind,:);
        
       % ~~~~~~~~~~~~~~~A) Count LP ~~~~~~~~~~~~~~~~~~~~~~
    
            %stack() to make inactive/active LP a variable
            data2= [];
            data2= stack(data, {'ActiveLeverPress', 'InactiveLeverPress'}, 'IndexVariableName', 'typeLP', 'NewDataVariableName', 'countLP');

            %generate figure
%             figure; %clear d;
        
        %-- individual subj
        group= data2.Subject;

        d(thisProjection,1)=gramm('x',data2.Session,'y',data2.countLP,'color',data2.typeLP, 'group', group)

        % %facet by trainPhaseLabel - ideally could set sharex of facets false but idk w gramm
        % d.facet_grid([],data2.trainPhaseLabel);

        % %facet by virus, trainPhaseLabel
%         d.facet_grid(data2.Projection,data2.trainPhaseLabel);

        % %facet by virus
%         d.facet_grid(data2.Projection,[]);


        d(thisProjection,1).stat_summary('type','sem','geom','area');
    %     d.set_names('x','Session','y','Number of Lever Presses','color','Lever Side')
        d(thisProjection,1).set_names('row','Target','column','Phase','x','Session','y','Number of Lever Presses','color','Lever Side')


        d(thisProjection,1).set_line_options('base_size',linewidthSubj);
        d(thisProjection,1).set_color_options('map', cmapSubj);

        d(thisProjection,1).no_legend(); %prevent legend duplicates if you like


        %set text options
        d(thisProjection,1).set_text_options(text_options_DefaultStyle{:}); 


%         d(thisProjection,1).draw()
%         d.draw();

        %-- btwn subj mean as well
        group= [];

        d(thisProjection,1).update('x',data2.Session,'y',data2.countLP,'color',data2.typeLP, 'group', group)

        d(thisProjection,1).stat_summary('type','sem','geom','area');
        % d.stat_boxplot();


        d(thisProjection,1).set_names('x','Session','y','Number of Lever Presses','color','Lever Side')
    %     d.set_names('row','Target','column','Phase','x','Session','y','Number of Lever Presses','color','Lever Side')


        d(thisProjection,1).set_line_options('base_size',linewidthGrand);
        d(thisProjection,1).set_color_options('map', cmapGrand);
        d(thisProjection,1).no_legend(); %prevent legend duplicates if you like


        figTitle= strcat('choiceTask-',thisExpTypeLabel,'-','LP-Count-across-sessions-all');   
        d(thisProjection,1).set_title(figTitle);   

        %Zoom in on lower LP subjects if desired
        % d().axe_property( 'YLim',[0 300]) %low responders
        % d().axe_property( 'YLim',[0, 1200]) %high responders

        % SET X TICK = 1 SESSION
        % d.axe_property('XTick',[min(data2.trainDayThisPhase):1:max(data2.trainDayThisPhase)]); %,'YLim',[0 75],'YTick',[0:25:75]);


%         d(thisProjection,1).draw();
%         d.draw();






        %~~~~~~~~~~~~~~~~~~~~~B) Proportion LP ~~~~~~~~~~~~~~~~~~~~~~~~
        %stack() to make inactive/active LP a variable
        data2=[];
        data2= stack(data, {'probActiveLP', 'probInactiveLP'}, 'IndexVariableName', 'typeLP', 'NewDataVariableName', 'probLP');

        %-- individual subj
        group= data2.Subject;

        d(thisProjection,2)=gramm('x',data2.Session,'y',data2.probLP,'color',data2.typeLP, 'group', group)

        % %facet by virus, trainPhaseLabel
    %     d.facet_grid(data2.Projection,data2.trainPhaseLabel);

        % %facet by virus
%          d(thisProjection,2).facet_grid(data2.Projection,[]);


         d(thisProjection,2).stat_summary('type','sem','geom','area');
    %     d.set_names('x','Session','y','Proportion of Lever Presses','color','Lever Side')
         d(thisProjection,2).set_names('row','Target','column','Phase','x','Session','y','Proportion of Lever Presses','color','Lever Side')

        d(thisProjection,2).set_line_options('base_size',linewidthSubj);
        d(thisProjection,2).set_color_options('map', cmapSubj);

        d(thisProjection,2).no_legend(); %prevent legend duplicates if you like


        %set text options
         d(thisProjection,2).set_text_options(text_options_DefaultStyle{:}); 

        
%          d(thisProjection,2).draw()
%          d.draw();   
         
        %-- btwn subj mean as well
        group= [];

         d(thisProjection,2).update('x',data2.Session,'y',data2.probLP,'color',data2.typeLP, 'group', group)

         d(thisProjection,2).stat_summary('type','sem','geom','area');
        % d.stat_boxplot();


         d(thisProjection,2).set_names('x','Session','y','Proportion of Lever Presses','color','Lever Side')

         d(thisProjection,2).set_line_options('base_size',linewidthGrand);
         d(thisProjection,2).set_color_options('map', cmapGrand);

        d(thisProjection,2).no_legend(); %prevent legend duplicates if you like

         
        figTitle= strcat('choiceTask-FIGURE-2-',thisExpTypeLabel,'-','LP-ForcedChoice');   
        d(thisProjection,2).set_title(figTitle);   

        
        %~~~~~~~~~~~~~~~~~~~C) Licks per Reward ~~~~~~~~~~~~~~~~~~~~~~~
                %TODO: all trials instead of aggregate? confirm how is this
                %calculated

          %stack() to make inactive/active LP a variable
        data2=[];
        data2= stack(data, {'LicksPerReward', 'LicksPerRewardInactive'}, 'IndexVariableName', 'typeLP', 'NewDataVariableName', 'licksPerReward');

        %-- individual subj
        group= data2.Subject;

        d(thisProjection,3)=gramm('x',data2.Session,'y',data2.licksPerReward,'color',data2.typeLP, 'group', group)

        % %facet by virus, trainPhaseLabel
    %     d.facet_grid(data2.Projection,data2.trainPhaseLabel);

        % %facet by virus
%          d(thisProjection,2).facet_grid(data2.Projection,[]);


         d(thisProjection,3).stat_summary('type','sem','geom','area');
    %     d.set_names('x','Session','y','Proportion of Lever Presses','color','Lever Side')
         d(thisProjection,3).set_names('row','Target','column','Phase','x','Session','y','Licks per Reward','color','Lever Side')

        d(thisProjection,3).set_line_options('base_size',linewidthSubj);
        d(thisProjection,3).set_color_options('map', cmapSubj);

        d(thisProjection,3).no_legend(); %prevent legend duplicates if you like


        %set text options
         d(thisProjection,3).set_text_options(text_options_DefaultStyle{:}); 

        
%          d(thisProjection,2).draw()
%          d.draw();   
         
        %-- btwn subj mean as well
        group= [];

         d(thisProjection,3).update('x',data2.Session,'y',data2.licksPerReward,'color',data2.typeLP, 'group', group)

         d(thisProjection,3).stat_summary('type','sem','geom','area');
        % d.stat_boxplot();


         d(thisProjection,3).set_names('x','Session','y','Licks per reward','color','Lever Side')

         d(thisProjection,3).set_line_options('base_size',linewidthGrand);
         d(thisProjection,3).set_color_options('map', cmapGrand);

        d(thisProjection,3).no_legend(); %prevent legend duplicates if you like

        figTitle= strcat(projectionsAll{thisProjection},'licks per reward');   
        d(thisProjection,3).set_title('TEST');   


    end %end projection/target loop
    
    %draw only at end?
            figTitle= strcat('choiceTask-FIGURE-2-',thisExpTypeLabel,'-','LP-ForcedChoice');   
            d().set_title(figTitle);   
            d.draw(); 
            saveFig(gcf, figPath,figTitle,figFormats);

    
end %end expType/virus loop


%% 



%% ---- OLD Plots ----
%% Plot total active vs inactive LP

figure %Stimulation
selection= LeverChoice.Expression==1 & LeverChoice.ExpType==1 &(strcmp(LeverChoice.Projection,'mdThal') | strcmp(LeverChoice.Projection,'VTA'));
g(1,1)=gramm('x',LeverChoice.Session(selection),'y',LeverChoice.ActiveLeverPress(selection),'color',LeverChoice.Projection(selection));
g(1,1).stat_summary('type','sem','geom','area');
g(1,1).no_legend();
g(1,1).set_names('x','Session','y','Number of Lever Presses','color','Laser(-)');
g(1,1).set_title('Total Lever Presses');
g(1,1).axe_property( 'YLim',[0 150],'XLim',[1 6]);

g(1,1).update('x',LeverChoice.Session(selection),'y',LeverChoice.InactiveLeverPress(selection),'color',LeverChoice.Projection(selection));
g(1,1).stat_summary('type','sem','geom','area');
g(1,1).no_legend();
g(1,1).set_names('x','Session','y','Number of Lever Presses','color','No Laser(--)')
g(1,1).set_title('Choice Task')
g(1,1).set_line_options( 'styles',{':'})


%Stimulation
selection= LeverChoice.Expression==1 & LeverChoice.ExpType==1 &(strcmp(LeverChoice.Projection,'mdThal') | strcmp(LeverChoice.Projection,'VTA'));
g(1,2)=gramm('x',LeverChoice.Session(selection),'y',LeverChoice.ActiveLeverPress(selection),'color',LeverChoice.Projection(selection))
g(1,2).stat_summary('type','sem','geom','area');
g(1,2).no_legend();
g(1,2).set_names('x','Session','y','Number of Lever Presses','color','Laser(-)');
g(1,2).set_title('Reversal');
g(1,2).axe_property('YLim',[0 150],'XLim', [7 12]);

g(1,2).update('x',LeverChoice.Session(selection),'y',LeverChoice.InactiveLeverPress(selection),'color',LeverChoice.Projection(selection));
g(1,2).stat_summary('type','sem','geom','area');
g(1,2).no_legend();
g(1,2).set_names('x','Session','y','Number of Lever Presses','color','No Laser(--)');
g(1,2).set_title('Choice Task');
g(1,2).set_line_options( 'styles',{':'});

selection= LeverChoice.Session==13 & LeverChoice.Expression==1 & LeverChoice.ExpType==1 &(strcmp(LeverChoice.Projection,'mdThal') | strcmp(LeverChoice.Projection,'VTA'));
g(1,3)=gramm('x',LeverChoice.Session(selection),'y',LeverChoice.ActiveLeverPress(selection),'color',LeverChoice.Projection(selection))
g(1,3).stat_boxplot(); 
g(1,3).set_names('x','Session','y','Number of Lever Presses','color','Laser');
%g(1,3).axe_property( 'YLim',[0 150],'XLim',[13 13]);
g(1,3).axe_property( 'YLim',[0 150])
g(1,3).set_title('Choice Session')

% selection= LeverChoice.Session==13 & LeverChoice.Expression==1 & LeverChoice.ExpType==1 &(strcmp(LeverChoice.Projection,'mdThal') | strcmp(LeverChoice.Projection,'VTA'));
% g(1,4)=gramm('x',LeverChoice.Session(selection),'y',LeverChoice.InactiveLeverPress(selection),'color',LeverChoice.Projection(selection));
% g(1,4).stat_boxplot(); 
% g(1,4).set_names('x','Session','y','Number of Lever Presses','color','No Laser(--)');
% %g(1,4).axe_property( 'YLim',[0 150],'XLim',[13 13]);
% g(1,4).set_title('Choice Session')


selection= LeverChoice.Session==13 & LeverChoice.Expression==1 & LeverChoice.ExpType==1 &(strcmp(LeverChoice.Projection,'mdThal') | strcmp(LeverChoice.Projection,'VTA'));
g(1,4)=gramm('x',LeverChoice.Session(selection),'y',LeverChoice.InactiveLeverPress(selection),'color',LeverChoice.Projection(selection))
g(1,4).stat_boxplot(); 
g(1,4).set_names('x','Session','y','Number of Lever Presses','color','No Laser');
g(1,4).axe_property( 'YLim',[0 150])
g(1,4).set_title('Choice Session')


selection= LeverChoice.Session==14 & LeverChoice.Expression==1 & LeverChoice.ExpType==1 &(strcmp(LeverChoice.Projection,'mdThal') | strcmp(LeverChoice.Projection,'VTA'));
g(1,5)=gramm('x',LeverChoice.Session(selection),'y',LeverChoice.ActiveLeverPress(selection),'color',LeverChoice.Projection(selection))
g(1,5).stat_boxplot(); 
g(1,5).axe_property( 'YLim',[0 150])
g(1,5).set_title('Extinction')
%g(1,5).axe_property( 'YLim',[0 150])
g(1,5).set_names('x','Session','y','Number of Lever Presses','color','Laser');

selection= LeverChoice.Session==14 & LeverChoice.Expression==1 & LeverChoice.ExpType==1 &(strcmp(LeverChoice.Projection,'mdThal') | strcmp(LeverChoice.Projection,'VTA'));
g(1,6)=gramm('x',LeverChoice.Session(selection),'y',LeverChoice.InactiveLeverPress(selection),'color',LeverChoice.Projection(selection))
g(1,6).stat_boxplot(); 
g(1,6).set_title('Extinction')
g(1,6).axe_property( 'YLim',[0 150])
g(1,6).set_names('x','Session','y','Number of Lever Presses','color','No Laser');


% % Plot proportion by projection
% 
% %Stimulation
selection= LeverChoice.Expression==1 & LeverChoice.ExpType==1 &(strcmp(LeverChoice.Projection,'mdThal') | strcmp(LeverChoice.Projection,'VTA'));
g(2,1)=gramm('x',LeverChoice.Session(selection),'y',LeverChoice.Proportion(selection),'color',LeverChoice.Projection(selection))
g(2,1).stat_summary('type','sem','geom','area');
g(2,1).no_legend();
g(2,1).set_names('x','Session','y','Probability','color','Stim(-)')
g(2,1).set_title('Probability by Projection')
g(2,1).axe_property( 'YLim',[0 1],'XLim', [1 6])


selection= LeverChoice.Expression==1 & LeverChoice.ExpType==1 &(strcmp(LeverChoice.Projection,'mdThal') | strcmp(LeverChoice.Projection,'VTA'));
g(2,2)=gramm('x',LeverChoice.Session(selection),'y',LeverChoice.Proportion(selection),'color',LeverChoice.Projection(selection))
g(2,2).stat_summary('type','sem','geom','area');
g(2,2).no_legend();
g(2,2).set_names('x','Session','y','Probability','color','Stim(-)')
g(2,2).set_title('Reversal')
g(2,2).axe_property( 'YLim',[0 1],'XLim', [7 12])

selection= LeverChoice.Session==13 & LeverChoice.Expression==1 & LeverChoice.ExpType==1 &(strcmp(LeverChoice.Projection,'mdThal') | strcmp(LeverChoice.Projection,'VTA'));
g(2,3)=gramm('x',LeverChoice.Session(selection),'y',LeverChoice.Proportion(selection),'color',LeverChoice.Projection(selection))
g(2,3).stat_boxplot(); 
g(2,3).set_names('x','Session','y','PRrobability','color','Laser');
g(2,3).axe_property( 'YLim',[0 1])
g(2,3).no_legend()
g(2,3).set_title('Choice Session')

selection= LeverChoice.Session==14 & LeverChoice.Expression==1 & LeverChoice.ExpType==1 &(strcmp(LeverChoice.Projection,'mdThal') | strcmp(LeverChoice.Projection,'VTA'));
g(2,4)=gramm('x',LeverChoice.Session(selection),'y',LeverChoice.Proportion(selection),'color',LeverChoice.Projection(selection))
g(2,4).stat_boxplot(); 
g(2,4).set_names('x','Session','y','Probability','color','Laser');
g(2,4).axe_property( 'YLim',[0 1])
g(2,4).no_legend()
g(2,4).set_title('Extinction')


% % Plot proportion by sex
% %Stimulation
% selection=LeverChoice.Expression==1 & LeverChoice.ExpType==1 &(strcmp(LeverChoice.Projection,'mdThal') | strcmp(LeverChoice.Projection,'VTA')) ;
% g(2,1)=gramm('x',LeverChoice.Session(selection),'y',LeverChoice.Proportion(selection),'color',LeverChoice.Projection(selection))
% g(2,1).stat_summary('type','sem','geom','area');
% g(2,1).facet_grid([],LeverChoice.Sex(selection))
% g(2,1).no_legend();
% g(2,1).set_names('x','Session','y','Probability','color','Projection(-)')
% g(2,1).set_title('Probability by Sex')
% g(2,1).axe_property( 'YLim',[0 1], 'XLim', [1 6])
% 
% g(2,1).update('x',LeverChoice.Session(selection),'y',LeverChoice.Proportion(selection),'color',LeverChoice.Projection(selection))
% g(2,1).stat_summary('type','sem','geom','area');
% g(2,1).no_legend();
% g(2,1).set_names('x','Session','y','Probability','color','Projection')
% g(2,1).set_title('Probability by Sex')
% g(2,1).set_line_options( 'styles',{':'})
% % 
% selection=LeverChoice.Expression==1 & LeverChoice.ExpType==1 &(strcmp(LeverChoice.Projection,'mdThal') | strcmp(LeverChoice.Projection,'VTA')) ;
% g(2,2)=gramm('x',LeverChoice.Session(selection),'y',LeverChoice.Proportion(selection),'color',LeverChoice.Projection(selection))
% g(2,2).stat_summary('type','sem','geom','area');
% g(2,2).facet_grid([],LeverChoice.Sex(selection))
% g(2,2).no_legend();
% g(2,2).set_names('x','Session','y','Probability','color','Projection(-)')
% g(2,2).set_title('Probability by Sex (Reversal)')
% g(2,2).axe_property( 'YLim',[0 1], 'XLim', [7 14])
% 
% g(2,2).update('x',LeverChoice.Session(selection),'y',LeverChoice.Proportion(selection),'color',LeverChoice.Projection(selection))
% g(2,2).stat_summary('type','sem','geom','area');
% g(2,2).no_legend();
% g(2,2).set_names('x','Session','y','Probability','color','Projection')
% g(2,2).set_title('Probability by Sex (Reversal)')
% g(2,2).set_line_options( 'styles',{':'})


% %% Plot Licks per reward 
%Projection
selection= LeverChoice.Expression==1 & LeverChoice.ExpType==1 &(strcmp(LeverChoice.Projection,'mdThal') | strcmp(LeverChoice.Projection,'VTA'));
g(2,5)=gramm('x',LeverChoice.Session(selection),'y',LeverChoice.LicksPerReward(selection),'color',LeverChoice.Projection(selection))
g(2,5).stat_summary('type','sem','geom','area');
g(2,5).no_legend();
g(2,5).set_names('x','Session','y','Licks per Reward','color','Stim(-)')
g(2,5).set_title('Licks per reward')
g(2,5).axe_property( 'YLim',[0 50],'XLim', [1 6])

g(2,5).update('x',LeverChoice.Session(selection),'y',LeverChoice.LicksPerRewardInactive(selection),'color',LeverChoice.Projection(selection))
g(2,5).stat_summary('type','sem','geom','area');
g(2,5).no_legend();
g(2,5).set_names('x','Session','y','Licks per Reward','color','No Stim(--)')
g(2,5).set_title('Licks per reward')
g(2,5).set_line_options( 'styles',{':'})

selection= LeverChoice.Expression==1 & LeverChoice.ExpType==1 &(strcmp(LeverChoice.Projection,'mdThal') | strcmp(LeverChoice.Projection,'VTA'));
g(2,6)=gramm('x',LeverChoice.Session(selection),'y',LeverChoice.LicksPerReward(selection),'color',LeverChoice.Projection(selection))
g(2,6).stat_summary('type','sem','geom','area');
g(2,6).no_legend();
g(2,6).set_names('x','Session','y','Licks per Reward','color','Stim(-)')
g(2,6).set_title('Licks per reward')
g(2,6).axe_property( 'YLim',[0 50],'XLim', [7 12])

g(2,6).update('x',LeverChoice.Session(selection),'y',LeverChoice.LicksPerRewardInactive(selection),'color',LeverChoice.Projection(selection))
g(2,6).stat_summary('type','sem','geom','area');
g(2,6).no_legend();
g(2,6).set_names('x','Session','y','Licks per Reward','color','No Stim(--)')
g(2,6).set_title('Licks per reward')
g(2,6).set_line_options( 'styles',{':'})
g.draw();
% g.export('file_name','Lever Choice Task Data','export_path','/Volumes/nsci_richard/Christelle/Data/Opto Project/Figures','file_type','pdf') 

%error w size savefig of this fig specifically, still saves ok tho

figTitle= 'lever_choice_task_data';
saveFig(gcf, figPath,figTitle,figFormats);






 %Sex and Projection
% selection= LeverChoice.Expression==1 & LeverChoice.ExpType==1 &(strcmp(LeverChoice.Projection,'mdThal') | strcmp(LeverChoice.Projection,'VTA'));
% g=gramm('x',LeverChoice.Session(selection),'y',LeverChoice.LicksPerReward(selection),'color',LeverChoice.Projection(selection))
% g.stat_summary('type','sem','geom','area');
% g.facet_grid([],LeverChoice.Sex(selection))
% g.set_names('x','Session','y','Licks per Reward','color','Stim(-)')
% g.set_title('Stimulation Lever Choice Licks per reward--Sex')
% g.axe_property( 'YLim',[0 50])
% g.draw()
% 
% g.update('x',LeverChoice.Session(selection),'y',LeverChoice.LicksPerRewardInactive(selection),'color',LeverChoice.Projection(selection))
% g.stat_summary('type','sem','geom','area');
% g.set_names('x','Session','y','Licks per Reward','color','No Stim(--)')
% g.set_title('Stimulation Lever Choice Licks per reward--Sex')
% g.set_line_options( 'styles',{':'})
%%%%%%%%%%%%%%%%%%%%%%%%%%%
% %% Individual Data
% 
% % %% Plot individual total active vs inactive LP
% 
% selection= LeverChoice.Expression==1 & LeverChoice.ExpType==1 &(strcmp(LeverChoice.Projection,'mdThal') | strcmp(LeverChoice.Projection,'VTA'));
% g(2,1)=gramm('x',LeverChoice.Session(selection),'y',LeverChoice.ActiveLeverPress(selection),'color',LeverChoice.Subject(selection))
% g(2,1).stat_summary('type','sem','geom','area');
% g(2,1).set_names('x','Session','y','Number of Lever Presses','color','Stim(-)')
% g(2,1).set_title('Choice Task Individual Data')
% g(2,1).axe_property( 'YLim',[0 200], 'XLim', [1 6])
% 
% selection= LeverChoice.Expression==1 & LeverChoice.ExpType==1 &(strcmp(LeverChoice.Projection,'VTA'));
% g(2,2)=gramm('x',LeverChoice.Session(selection),'y',LeverChoice.ActiveLeverPress(selection),'color',LeverChoice.Subject(selection))
% g(2,2).stat_summary('type','sem','geom','area');
% g(2,2).set_names('x','Session','y','Number of Lever Presses','color','Stim(-)')
% g(2,2).set_title('Choice Task Individual Data')
% g(2,2).axe_property( 'YLim',[0 200],'XLim', [7 14])


%% ==== DP Figure 5 2022-10-17 ----------------------

% highly manual, specific subplotting here


% %run separately based on stim vs inhibition
expTypesAll= unique(choiceTaskTable.ExpType);

for thisExpType= 1:numel(expTypesAll)

    thisExpTypeLabel= expTypeLabels{thisExpType};

% == Figure 5a

%subset data

cmapSubj= cmapBlueGraySubj;
cmapGrand= cmapBlueGrayGrand;


    %subset data- by expType/virus
    ind=[];
    ind= choiceTaskTable.ExpType==expTypesAll(thisExpType);

    data0=[];
    data0= choiceTaskTable(ind,:);
    
    % ~~~~~ ROW 1: ACQUISITION

        
    % ~~ A) Acquisition VTA only raw count LP ~~~~~~~~~~~~~~~~~~~~~~~

        %subset data- by trainPhase
        phasesToInclude= [1]; %list of phases to include 

        ind=[];

        ind= ismember(data0.trainPhase, phasesToInclude);

        data= data0(ind,:);
    
       %stack() to make inactive/active LP a variable
        data2= [];
        data2= stack(data, {'ActiveLeverPress', 'InactiveLeverPress'}, 'IndexVariableName', 'typeLP', 'NewDataVariableName', 'countLP');

        data3= data2;
      
        %subset- by projection
        ind=[]
        ind= strcmp(data3.Projection,'VTA');
        
        data3= data2(ind,:);

        
        %Make figure
        figure; clear d;
        
        
        cmapSubj= cmapBlueGraySubj;
        cmapGrand= cmapBlueGrayGrand;
        
        %-- individual subj
        group= data3.Subject;

        d(1,1)=gramm('x',data3.Session,'y',data3.countLP,'color',data3.typeLP, 'group', group)

       
        d(1,1).stat_summary('type','sem','geom','area');
        d(1,1).set_line_options('base_size',linewidthSubj);
        d(1,1).set_color_options('map', cmapSubj);

        %- Things to do before first draw call-
        d(1,1).set_names('column', '', 'x', 'Time from Cue (s)','y','GCaMP (Z-score)','color','Trial type'); %row/column labels must be set before first draw call

        d(1,1).no_legend(); %avoid duplicate legend from other plots (e.g. subject & grand colors)
       

           %first draw call-
           
        d(1,1).set_title('Acquistion- VTA');
        
        d(1,1).draw()
           

        %------ btwn subj mean as well
        group= [];

        d(1,1).update('x',data3.Session,'y',data3.countLP,'color',data3.typeLP, 'group', group)

        d(1,1).stat_summary('type','sem','geom','area');

        d(1,1).set_names('x','Session','y','Number of Lever Presses','color','Lever Side')
    %     d.set_names('row','Target','column','Phase','x','Session','y','Number of Lever Presses','color','Lever Side')


        d(1,1).set_line_options('base_size',linewidthGrand);
        d(1,1).set_color_options('map', cmapGrand);
        d(1,1).no_legend(); %prevent legend duplicates if you like
        
        %need to leave something for final draw call to know all of the subplots. Either don't draw this update (max 1 update) or draw all initial subplots first prior to updates.
%         d(1,1).draw(); 


    % ~~ B) Acquisition mdThal only raw count LP ~~~~~~~~~~~~~~~~~~~~~~~
        %subset data- by trainPhase
        phasesToInclude= [1]; %list of phases to include 

        ind=[];

        ind= ismember(data0.trainPhase, phasesToInclude);

        data= data0(ind,:);
    
       %stack() to make inactive/active LP a variable
        data2= [];
        data2= stack(data, {'ActiveLeverPress', 'InactiveLeverPress'}, 'IndexVariableName', 'typeLP', 'NewDataVariableName', 'countLP');


        %subset- by projection
        data3= data2;

        ind=[]
        ind= strcmp(data3.Projection,'mdThal');
        
        data3= data2(ind,:);
                
        cmapSubj= cmapBlueGraySubj;
        cmapGrand= cmapBlueGrayGrand;
        
        %-- individual subj
        
        group= data3.Subject;

        d(1,2)=gramm('x',data3.Session,'y',data3.countLP,'color',data3.typeLP, 'group', group)

       
        d(1,2).stat_summary('type','sem','geom','area');
        d(1,2).set_line_options('base_size',linewidthSubj);
        d(1,2).set_color_options('map', cmapSubj);

        d(1,2).set_names('x','Session','y','Number of Lever Presses','color','Lever Side')

        d(1,2).no_legend(); %avoid duplicate legend from other plots (e.g. subject & grand colors)
           
        d(1,2).set_title('Acquistion- mdThal');
        
        d(1,2).draw()
           

        %------ btwn subj mean as well
        group= [];

        d(1,2).update('x',data3.Session,'y',data3.countLP,'color',data3.typeLP, 'group', group)

        d(1,2).stat_summary('type','sem','geom','area');

        d(1,2).set_names('x','Session','y','Number of Lever Presses','color','Lever Side')
    %     d.set_names('row','Target','column','Phase','x','Session','y','Number of Lever Presses','color','Lever Side')


        d(1,2).set_line_options('base_size',linewidthGrand);
        d(1,2).set_color_options('map', cmapGrand);
        d(1,2).no_legend(); %prevent legend duplicates if you like
        
%         d(1,2).draw(); %Leave for final draw call
        

     % ~~ C)Acquisition VTA & mdThal Active Proportion LP ~~~~~~~~~~~~~~~~~~~~~~~

             y= 'probActiveLP';
%         y= 'ActiveLeverPress';
     
        %subset data- by trainPhase
        phasesToInclude= [1]; %list of phases to include 

        ind=[];

        ind= ismember(data0.trainPhase, phasesToInclude);

        data= data0(ind,:);
    
       %stack() not necessary
        data2= data

        %subset- by projection not necessary
        data3= data2;
        
        %cmap for Projection comparisons
        cmapGrand= 'brewer_dark';
        cmapSubj= 'brewer2';
        
        %-- individual subj
        group= data3.Subject;

        d(1,3)=gramm('x',data3.Session,'y',data3.(y),'color',data3.Projection, 'group', group)

       
        d(1,3).stat_summary('type','sem','geom','area');
        d(1,3).set_line_options('base_size',linewidthSubj);
        d(1,3).set_color_options('map', cmapSubj);

%         d(1,3).set_names('x','Session','y','Proportion Active Lever Presses','color','Lever Side')

%         d(1,3).no_legend(); %avoid duplicate legend from other plots (e.g. subject & grand colors)
           
        d(1,3).set_title('Acquistion- Active Proportion');
        
        d(1,3).draw()
           

        %------ btwn subj mean as well
        group= [];

        d(1,3).update('x',data3.Session,'y',data3.(y),'color',data3.Projection, 'group', group)

        d(1,3).stat_summary('type','sem','geom','area');

        d(1,3).set_names('x','Session','y','Proportion Active Lever Presses','color','Projection')


        d(1,3).set_line_options('base_size',linewidthGrand);
        d(1,3).set_color_options('map', cmapGrand);
        d(1,3).no_legend(); %prevent legend duplicates if you like
                
        d(1,3).geom_hline('yintercept',0.5, 'style', 'k--', 'linewidth', linewidthReference); %overlay t=0
        
%         d(1,3).draw(); %Leave for final draw call
        
           
        
     % ~~ D) Reversal VTA & mdThal Active Proportion LP ~~~~~~~~~~~~~~~~~~~~~~~

     % try diff versions with raw vs proportion 
    
     
        %subset data- by trainPhase
        phasesToInclude= [2]; %list of phases to include 

        ind=[];

        ind= ismember(data0.trainPhase, phasesToInclude);

        data= data0(ind,:);
    
       %stack() not necessary
        data2= data

        %subset- by projection not necessary
        data3= data2;
        
        %cmap for Projection comparisons
        cmapGrand= 'brewer_dark';
        cmapSubj= 'brewer2';   
        
        %-- individual subj
        group= data3.Subject;

        d(2,1)=gramm('x',data3.Session,'y',data3.(y),'color',data3.Projection, 'group', group)

       
        d(2,1).stat_summary('type','sem','geom','area');
        d(2,1).set_line_options('base_size',linewidthSubj);
        d(2,1).set_color_options('map', cmapSubj);

%         d(1,3).set_names('x','Session','y','Proportion Active Lever Presses','color','Lever Side')

        d(2,1).no_legend(); %avoid duplicate legend from other plots (e.g. subject & grand colors)
           
        d(2,1).set_title('Reversal- Active Proportion');
        
        d(2,1).draw()
           

        %------ btwn subj mean as well
        group= [];

        d(2,1).update('x',data3.Session,'y',data3.(y),'color',data3.Projection, 'group', group)

        d(2,1).stat_summary('type','sem','geom','area');

        d(2,1).set_names('x','Session','y','Proportion Active Lever Presses','color','Projection')

       
        d(2,1).set_line_options('base_size',linewidthGrand);
        d(2,1).set_color_options('map', cmapGrand);
        d(2,1).no_legend(); %prevent legend duplicates if you like
        
        d(2,1).geom_hline('yintercept',0.5, 'style', 'k--', 'linewidth', linewidthReference); %overlay t=0

        
%         d(1,3).draw(); %Leave for final draw call
        
      
     % ~~ E) Forced Choice VTA & mdThal Active Proportion LP ~~~~~~~~~~~~~~~~~~~~~~~

        %subset data- by trainPhase
        phasesToInclude= [3]; %list of phases to include 

        ind=[];

        ind= ismember(data0.trainPhase, phasesToInclude);

        data= data0(ind,:);
    
       %stack() not necessary
        data2= data

        %subset- by projection not necessary
        data3= data2;
        
        %cmap for Projection comparisons
        cmapGrand= 'brewer_dark';
        cmapSubj= 'brewer2';   
        
        %-- individual subj
        group= data3.Subject;

        d(2,2)=gramm('x',data3.Session,'y',data3.(y),'color',data3.Projection, 'group', group)

       
        d(2,2).stat_summary('type','sem','geom','area');
        d(2,2).set_line_options('base_size',linewidthSubj);
        d(2,2).set_color_options('map', cmapSubj);

%         d(1,3).set_names('x','Session','y','Proportion Active Lever Presses','color','Lever Side')

        d(2,2).no_legend(); %avoid duplicate legend from other plots (e.g. subject & grand colors)
           
        d(2,2).set_title('Forced Choice- Active Proportion');
        
        d(2,2).draw()
           

        %------ btwn subj mean as well
        group= [];

        d(2,2).update('x',data3.Session,'y',data3.(y),'color',data3.Projection, 'group', group)

        d(2,2).stat_summary('type','sem','geom','area');

        d(2,2).set_names('x','Session','y','Proportion Active Lever Presses','color','Projection')


        d(2,2).set_line_options('base_size',linewidthGrand);
        d(2,2).set_color_options('map', cmapGrand);
        d(2,2).no_legend(); %prevent legend duplicates if you like
        
        
        d(2,2).geom_hline('yintercept',0.5, 'style', 'k--', 'linewidth', linewidthReference); %overlay t=0

        
%         d(1,3).draw(); %Leave for final draw call     


     % ~~ F) Final Test & Extinction; VTA & mdThal Active Proportion LP ~~~~~~~~~~~~~~~~~~~~~~~
     
        %subset data- by trainPhase
        phasesToInclude= [4,5]; %list of phases to include 

        ind=[];

        ind= ismember(data0.trainPhase, phasesToInclude);

        data= data0(ind,:);
    
       %stack() not necessary
        data2= data

        %subset- by projection not necessary
        data3= data2;
        
        %cmap for Projection comparisons
        cmapGrand= 'brewer_dark';
        cmapSubj= 'brewer2';   
        
        %-- individual subj
        group= data3.Subject;

        d(2,3)=gramm('x',data3.trainPhaseLabel,'y',data3.(y),'color',data3.Projection, 'group', group)

       
        d(2,3).stat_summary('type','sem','geom','area');
        d(2,3).set_line_options('base_size',linewidthSubj);
        d(2,3).set_color_options('map', cmapSubj);

%         d(1,3).set_names('x','Session','y','Proportion Active Lever Presses','color','Lever Side')

        d(2,3).no_legend(); %avoid duplicate legend from other plots (e.g. subject & grand colors)
           
        d(2,3).set_title('Free Choice- Active Proportion');
        
        d(2,3).draw()
           

        %------ btwn subj mean as well
        group= [];

        d(2,3).update('x',data3.trainPhaseLabel,'y',data3.(y),'color',data3.Projection, 'group', group)

        d(2,3).stat_summary('type','sem','geom','area');

        d(2,3).set_names('x','Session','y','Proportion Active Lever Presses','color','Projection')


        d(2,3).set_line_options('base_size',linewidthGrand);
        d(2,3).set_color_options('map', cmapGrand);
        d(2,3).no_legend(); %prevent legend duplicates if you like
        
        
        d(2,3).geom_hline('yintercept',0.5, 'style', 'k--', 'linewidth', linewidthReference); %overlay t=0

        
%         d(1,3).draw(); %Leave for final draw call     


% ~~~~~~~~~~~~~~~FINAL ROW: Licks/Reward 
        

        %~~~ 3,1 Reversal
        %subset data- by trainPhase
        phasesToInclude= [2]; %list of phases to include 

        ind=[];

        ind= ismember(data0.trainPhase, phasesToInclude);

        data= data0(ind,:);
    
       %stack() - to make active/inactive a variable
        data2= stack(data, {'LicksPerReward', 'LicksPerRewardInactive'}, 'IndexVariableName', 'typeLP', 'NewDataVariableName', 'rewardLicks');

        %subset- by projection not necessary
        data3= data2;
        
        %cmap for Projection comparisons
        cmapGrand= 'brewer_dark';
        cmapSubj= 'brewer2';   
        
        %-- individual subj
        group= data3.Subject;

            %add style facet for active/inactive
        d(3,1)=gramm('x',data3.Session,'y',data3.rewardLicks,'color',data3.Projection, 'linestyle', data3.typeLP, 'group', group)

       
        d(3,1).stat_summary('type','sem','geom','area');
        d(3,1).set_line_options('base_size',linewidthSubj);
        d(3,1).set_color_options('map', cmapSubj);

%         d(3,1).set_names('x','Session','y','Licks per Reward','color','Lever Side')

        d(3,1).no_legend(); %avoid duplicate legend from other plots (e.g. subject & grand colors)
           
        d(3,1).set_title('Reversal- Licks per Reward');
        
        d(3,1).draw()
           

        %------ btwn subj mean as well
        group= [];

        d(3,1).update('x',data3.Session,'y',data3.rewardLicks,'color',data3.Projection, 'linestyle', data3.typeLP, 'group', group)

        d(3,1).stat_summary('type','sem','geom','area');

        d(3,1).set_names('x','Session','y','Licks per Reward','color','Projection')


        d(3,1).set_line_options('base_size',linewidthGrand);
        d(3,1).set_color_options('map', cmapGrand);
        d(3,1).no_legend(); %prevent legend duplicates if you like
        
        
        %~~~ 3,2 Reversal
        %subset data- by trainPhase
        phasesToInclude= [3]; %list of phases to include 

        ind=[];

        ind= ismember(data0.trainPhase, phasesToInclude);

        data= data0(ind,:);
    
       %stack() - to make active/inactive a variable
        data2= stack(data, {'LicksPerReward', 'LicksPerRewardInactive'}, 'IndexVariableName', 'typeLP', 'NewDataVariableName', 'rewardLicks');

        %subset- by projection not necessary
        data3= data2;
        
        %cmap for Projection comparisons
        cmapGrand= 'brewer_dark';
        cmapSubj= 'brewer2';   
        
        %-- individual subj
        group= data3.Subject;

            %add style facet for active/inactive
        d(3,2)=gramm('x',data3.Session,'y',data3.rewardLicks,'color',data3.Projection, 'linestyle', data3.typeLP, 'group', group)

       
        d(3,2).stat_summary('type','sem','geom','area');
        d(3,2).set_line_options('base_size',linewidthSubj);
        d(3,2).set_color_options('map', cmapSubj);

%         d(3,2).set_names('x','Session','y','Licks per Reward','color','Lever Side')

        d(3,2).no_legend(); %avoid duplicate legend from other plots (e.g. subject & grand colors)
           
        d(3,2).set_title('Reversal- Licks per Reward');
        
        d(3,2).draw()
           

        %------ btwn subj mean as well
        group= [];

        d(3,2).update('x',data3.Session,'y',data3.rewardLicks,'color',data3.Projection, 'linestyle', data3.typeLP, 'group', group)

        d(3,2).stat_summary('type','sem','geom','area');

        d(3,2).set_names('x','Session','y','Licks per Reward','color','Projection')


        d(3,2).set_line_options('base_size',linewidthGrand);
        d(3,2).set_color_options('map', cmapGrand);
        d(3,2).no_legend(); %prevent legend duplicates if you like
        

          
        %~~~ 3,3 Test
        %subset data- by trainPhase
        phasesToInclude= [4,5]; %list of phases to include 

        ind=[];

        ind= ismember(data0.trainPhase, phasesToInclude);

        data= data0(ind,:);
    
       %stack() - to make active/inactive a variable
        data2= stack(data, {'LicksPerReward', 'LicksPerRewardInactive'}, 'IndexVariableName', 'typeLP', 'NewDataVariableName', 'rewardLicks');

        %subset- by projection not necessary
        data3= data2;
        
        %cmap for Projection comparisons
        cmapGrand= 'brewer_dark';
        cmapSubj= 'brewer2';   
        
        %-- individual subj
        group= data3.Subject;

            %add style facet for active/inactive
        d(3,3)=gramm('x',data3.trainPhaseLabel,'y',data3.rewardLicks,'color',data3.Projection, 'linestyle', data3.typeLP, 'group', group)

       
        d(3,3).stat_summary('type','sem','geom','area');
        d(3,3).set_line_options('base_size',linewidthSubj);
        d(3,3).set_color_options('map', cmapSubj);

%         d(3,3).set_names('x','Session','y','Licks per Reward','color','Lever Side')

        d(3,3).no_legend(); %avoid duplicate legend from other plots (e.g. subject & grand colors)
           
        d(3,3).set_title('Free Choice- Licks per Reward');
        
        d(3,3).draw()
           

        %------ btwn subj mean as well
        group= [];

        d(3,3).update('x',data3.trainPhaseLabel,'y',data3.rewardLicks,'color',data3.Projection, 'linestyle', data3.typeLP, 'group', group)

        d(3,3).stat_summary('type','sem','geom','area');

        d(3,3).set_names('x','Session','y','Licks per Reward','color','Projection')


        d(3,3).set_line_options('base_size',linewidthGrand);
        d(3,3).set_color_options('map', cmapGrand);
        d(3,3).no_legend(); %prevent legend duplicates if you like
        



        % --- Overall Fig things to do before final overall draw call ---
        d.set_text_options(text_options_DefaultStyle{:}); %apply default text sizes/styles

        titleFig= ('Fig 5');   
        d.set_title(titleFig); %overarching fig title must be set before first draw call

        

    %--- Final Draw call ---
        d.draw(); %Final Draw call
        
        figTitle= strcat('choiceTask-',thisExpTypeLabel,'-','Figure5-draft-',y);   
    
         saveFig(gcf, figPath,figTitle,figFormats);

       
        %% TODO improvements to above
        
        
%         
% - manually relabel trialType for clarity
% %e.g. either simply "DS" or "NS"
% %convert categorical to string then search 
% data(:,"trialTypeLabel")= {''};
% 
%  %make labels matching each 'trialType' and loop thru to search/match
% trialTypes= {'DSblue', 'NSblue'};
% trialTypeLabels= {'DS','NS'};


% - Use Facet_Grid within subplots instead of manually making each one.
        
end %end expType loop (stim vs inhibition virus)




%% Testing some alt layouts


%subset data

cmapSubj= cmapBlueGraySubj;
cmapGrand= cmapBlueGrayGrand;


    %subset data- by expType/virus
    ind=[];
    ind= choiceTaskTable.ExpType==expTypesAll(thisExpType);

    data0=[];
    data0= choiceTaskTable(ind,:);
    
    % ~~~~~ ROW 1: ACQUISITION

        
    % ~~ A) Acquisition VTA only raw count LP ~~~~~~~~~~~~~~~~~~~~~~~

        %subset data- by trainPhase
        phasesToInclude= [1:9]; %list of phases to include 

        ind=[];

        ind= ismember(data0.trainPhase, phasesToInclude);

        data= data0(ind,:);
    
       %stack() to make inactive/active LP a variable
        data2= [];
        data2= stack(data, {'ActiveLeverPress', 'InactiveLeverPress'}, 'IndexVariableName', 'typeLP', 'NewDataVariableName', 'countLP');

        data3= data2;
      
        %subset- by projection
%         ind=[]
%         ind= strcmp(data3.Projection,'VTA');
        
%         data3= data2(ind,:);
% 
        
        %Make figure
        figure; clear d;
        
        
        cmapSubj= cmapBlueGraySubj;
        cmapGrand= cmapBlueGrayGrand;
        
        %-- individual subj
        group= data3.Subject;

        d(1,1)=gramm('x',data3.Session,'y',data3.countLP,'color',data3.typeLP, 'group', group)

       d(1,1).facet_grid([], data3.Projection);
        
        d(1,1).stat_summary('type','sem','geom','area');
        d(1,1).set_line_options('base_size',linewidthSubj);
        d(1,1).set_color_options('map', cmapSubj);

        %- Things to do before first draw call-
        d(1,1).set_names('column', '', 'x', 'Time from Cue (s)','y','GCaMP (Z-score)','color','Trial type'); %row/column labels must be set before first draw call

        d(1,1).no_legend(); %avoid duplicate legend from other plots (e.g. subject & grand colors)
       

           %first draw call-
           
        d(1,1).set_title('Acquistion- VTA');
        
        d(1,1).draw()
           

        %------ btwn subj mean as well
        group= [];

        d(1,1).update('x',data3.Session,'y',data3.countLP,'color',data3.typeLP, 'group', group)

        d(1,1).stat_summary('type','sem','geom','area');

        d(1,1).set_names('x','Session','y','Number of Lever Presses','color','Lever Side')
    %     d.set_names('row','Target','column','Phase','x','Session','y','Number of Lever Presses','color','Lever Side')


        d(1,1).set_line_options('base_size',linewidthGrand);
        d(1,1).set_color_options('map', cmapGrand);
        d(1,1).no_legend(); %prevent legend duplicates if you like
        
        %need to leave something for final draw call to know all of the subplots. Either don't draw this update (max 1 update) or draw all initial subplots first prior to updates.
%         d(1,1).draw(); 
