clear all
close all
clc

%% Figure options

%--- Set output folder and format for figures to be saved
figPath= strcat(pwd,'\_output\_ICSS\');

figFormats= {'.svg'} %list of formats to save figures as (for saveFig.m)

%% Set GRAMM defaults for plots

set_gramm_plot_defaults();

% 
% %--- Set some "Main"/"Default" settings for GRAMM plots
% % Saving at once in single vars so dont have to always use
% % so much code when constructing individual plots
% 
% % altering things like color and text size in matlab can save a ton of time manually changing in external program like illustrator 
% 
% % -text options
% %Need to store mixed data types (str for argument/variable names and some num for values), so store as
% %a cell array. 
% 
% % When you want to call on the gramm object to set_text_options, retrieve values with {:} like so:
%     % g.set_text_options(text_options_MainStyle{:}); 
% 
% text_options_DefaultStyle= {'font'; 'Arial'; 
%     'interpreter'; 'none'; 
%     'base_size'; 22; 
%     'label_scaling'; 1;
%    'legend_scaling'; 1; 
%    'legend_title_scaling'; 1.1;
%    'facet_scaling'; 1.2; 
%    'title_scaling'; 1.4;
%    'big_title_scaling'; 1.4};
% 
% %-- Default plot linestyles 
% %To be used to set the 'base_size' of lines e.g. like:
% %     d().set_line_options('base_size',linewidthSubj);
% 
% %may consider using the group argument in gramm as a logic gate for these (e.g. if group= subject, use subject settings, if group=[] use grand settings)
% 
% %thin, light lines for individual subj
% linewidthSubj= 0.5;
% lightnessRangeSubj= [100,100]; %lightness facet with lightness range doesn't work with custom colormap color facet? Issue is I think unknown/too many lightness 'categories' gramm wants to make but can't do it well for custom colors. would be nice if could use alpha but dont think this works... better to have distinct color
% 
% 
% %dark, thick lines for between subj grand mean
% linewidthGrand= 1.5;
% lightnessRangeGrand= [10,10]; %lightness facet with lightness range doesn't work with custom colormap color facet? Issue is I think unknown/too many lightness 'categories' gramm wants to make but can't do it well for custom colors. would be nice if could use alpha but dont think this works... better to have distinct color
% 
% 
% %--COLOR MAPS and notes about faceting Color & Lightness
%  %- 2 strategies for plotting individual subject observations 'lighter' with darker
%  % grand means:
%  
%  % 1) Use built in colormaps (ultimately not good in long run if you want to change colors). Using same map for individuals & mean plots but facet 'lightness' = subject.
%  % This works well with built in gramm colormaps I think bc they can generate a lot of lightness categories (e.g. many subjects)
%  
%  % 2)*recommended* Use custom different map for individuals and mean plots without faceting
%  % lightness. This way you have total control over the colors without
%  % relying on gramm to figure out lightness categories. All you have to do
%  % is define color map to use for each group 
% 
% %-- Default plot colormaps
% 
% %-brewer2 and brewerDark are two cmaps that are built-in and are good for
% %plotting subjects, means respectively (different shades of same colors)
% %if only 2 groupings being plotted, brewer2 and brewer_dark work well 
% paletteSubj= 'brewer2';
% paletteGrand= 'brewer_dark';
% 
% 
% %-- Also have made some custom maps, examples follow (made using colorbrewer2.org)
% % all you need is to make the map you want on the site, copy the RGB values
% % and divide by 255 for matlab to recognize them as a colormap 
% 
% %--- Custom colormap examples for plots
% 
% % - Custom colormap updated from below. want alternating distinct hues for auto faceting
% % will make different maps with diff lightness for diff 'groups' (e.g. subject lighter vs darker grand means) 
% 
% % alternatively add lighness facet for subjects? with fixed lightness range
% % of single value should be able to export to illustrator and select same
% % stroke
% 
% 
% % - Examples: Colormap for 465nm vs 405nm comparisons (7 class PRGn, purple vs green)
% %green and purple %3 levels each, dark to light extremes + neutral middle
% mapCustomFP= [ 27,120,55;
%             127,191,123;
%             217,240,211;
%             247,247,247
%             231,212,232
%             175,141,195;
%             118,42,131;
%            ];
% 
%         mapCustomFP= mapCustomFP/255;
%         
%         %viz this colormap in colorbar to side of rgbplot
%         rgbplot(mapCustomFP);
%         hold on
%         colormap(mapCustomFP)
%         colorbar('Ticks',[])
%         title('mapCustomFP');
% 
% % - Colormap for DS vs NS comparisons (7 class BrBG; teal blue vs. brown orange)
% mapCustomCue= [90,180,172;
%             199,234,229;
%             245,245,245;
%             1,102,94
%             246,232,195;
%             216,179,101;
%             140,81,10;   
%             ];
%             
%         mapCustomCue= mapCustomCue/255;
% 
%                 %viz this colormap in colorbar to side of rgbplot
%         rgbplot(mapCustomCue);
%         hold on
%         colormap(mapCustomCue)
%         colorbar('Ticks',[])
%         title('mapCustomCue');
% 
%         %if you want to specific colors from this map, remember each color is= RGB values so each row is 1 color and you can just index single row.
%         %alternatively for auto faceting you may need to reorganize the
%         %cmap order such that the colors alternate between hues (e.g. since
%         %gramm() will facet in order of the colors in the cmap)

%% load data
%CurrentDir ='/Volumes/nsci_richard/Christelle/Codes/Matlab';
%SavingDir = '/Volumes/nsci_richard/Christelle/Codes/Matlab';
%cd(CurrentDir)


% %--christelle opto data
% CurrentDir = 'C:\Users\Dakota\Desktop\_christelle_opto_copy';
CurrentDir = 'C:\Users\Dakota\Desktop\_dp_christelle_opto_workingDir';
cd(CurrentDir)


% [~,~,raw] = xlsread('Opto ICSS Data');

%dp reextracted data
[~,~,raw]= xlsread("F:\_Github\Richard Lab\data-vp-opto\_Excel_Sheets\_dp_reextracted\dp_reextracted_ICSS.xlsx");

% [~,~,ratinfo] = xlsread('Christelle Opto Summary Record.xlsx');
[~,~,ratinfo] = xlsread('Christelle Opto Summary Record_dp.xlsx');


VarNames = raw(1,:);
Data = raw(2: end,:);

ICSS = struct();

for i=1:9 
    ICSS.(VarNames{i}) = Data(1:end,(i));
end

%% dp manually exclude extra sessions from analysis (from Opto Group 2)

datesExclude=[];
datesToExclude= [190812, 190820];

ICSS.StartDate= cell2mat(ICSS.StartDate);

ind=[];
ind= ismember(ICSS.StartDate,datesToExclude);


%loop through struct fields and remove data
allFields= fieldnames(ICSS);
for field= 1:numel(allFields)
    ICSS.(allFields{field})(ind)= [];
end


%% DP- Find duplicate sessions in spreadsheet
% find duplicate sessions?


% convert to table to use table functions
data= struct2table(ICSS);

% use groupsummary() to get count grouped by subj,date
% data.StartDate= cell2mat(data.StartDate);

dupes=[];
dupes= groupsummary(data, ["Subject", "StartDate"]);

dupes= dupes(dupes.GroupCount>1,:)


% convert to table to use table functions
data= struct2table(ICSS);

groupIDs= [];

% data.StartDate= cell2mat(data.StartDate);
groupIDs= findgroups(data.Subject, data.StartDate);

groupIDsUnique= [];
groupIDsUnique= unique(groupIDs);

%table to collect duplicate flagged sessions
dupes =table();

for thisGroupID= 1:numel(groupIDsUnique)
    %for each groupID, find index matching groupID
    ind= [];
    ind= find(groupIDs==groupIDsUnique(thisGroupID));
    
    %for each groupID, get the table data matching this group
    thisGroup=[];
    thisGroup= data(ind,:);

    % Check if >1 observation here in group
    % if so, flag for review
    if height(thisGroup)>1
       disp('duplicate ses found!')
        dupes(ind, :)= thisGroup;

    end
    
end 

%subset only nonzero startdates for concise view , lazy
if ~isempty(dupes)
    dupes= dupes(dupes.StartDate~=0,:);
end
%% DP- add "Sessions" column if absent from spreadsheet
% christelle seems to have manually added a "Sessions" column
% post-extraction to excel, a cumcount() of sessions for each subject

% convert to table to use table functions
data= struct2table(ICSS);

%initialize new col
data(:,'Session')= table(nan);

%use findgroups to groupby subject,trainPhaseLabel and manually cumcount() for
%sessions within-trainPhaseLabel

groupIDs= [];
%actually just need to group by Subject, assuming 1 row = 1 session 
groupIDs= findgroups(data.Subject);

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
    
    %assign back into table
    data(ind, 'Session')= table(thisGroup.cumcount);
    
end 

%assign back into struct
ICSS.Session= data.Session;


%% assign variables to rats                         
for i = 1 : length(ICSS.Subject)
    ind = strcmp(ICSS.Subject{i},ratinfo(:,1));
    ICSS.Sex{i,1} = ratinfo{ind,3};
    ICSS.Expression(i,1)=ratinfo{ind,6};
    ICSS.ExpType(i,1)=ratinfo{ind,5};
    ICSS.Projection{i,1}=ratinfo{ind,4};
    ICSS.RatNum(i,1)=ratinfo{ind,10};
    if strcmp(ICSS.Projection(i,1),'VTA')
        ICSS.ProjGroup(i,1)=1
    else if strcmp(ICSS.Projection(i,1),'mdThal')
            ICSS.ProjGroup(i,1)=2
        else ICSS.ProjGroup(i,1)=NaN
        end
    end
end

% ICSS.Session=cell2mat(ICSS.Session)
ICSS.ActiveNP=cell2mat(ICSS.ActiveNP)
ICSS.InactiveNP=cell2mat(ICSS.InactiveNP)
ICSS.TotalLengthActiveNP=cell2mat(ICSS.TotalLengthActiveNP)
ICSS.TotalLengthInactiveNP=cell2mat(ICSS.TotalLengthInactiveNP)
ICSS.TotalStimulations=cell2mat(ICSS.TotalStimulations)

%%
selection=ICSS.Expression==1 & ICSS.ExpType==1
ICSSTable=table(ICSS.RatNum(selection),ICSS.ActiveNP(selection),ICSS.InactiveNP(selection),ICSS.Session(selection),ICSS.ProjGroup(selection),'VariableNames',{'Rat','Active','Inactive','Session','Projection'})


lmeActive=fitlme(ICSSTable,'Active~Projection+(Session|Rat)')
lmeInactive=fitlme(ICSSTable,'Inactive~Projection+(Session|Rat)')

%
selection=ICSS.Expression==1 & ICSS.ExpType==1 & strcmp(ICSS.Projection,'VTA')
VTATable=table(ICSS.RatNum(selection),ICSS.ActiveNP(selection),ICSS.InactiveNP(selection),ICSS.Session(selection),'VariableNames',{'Rat','Active','Inactive','Session'})

lmeVTAActive=fitlme(VTATable,'Active~Session+(1|Rat)')
lmeVTAInactive=fitlme(VTATable,'Inactive~Session+(1|Rat)')


%% DP Subset data for specific projection (vp--> vta / MDthal) group only
% 
% modeProjection= 1; %VTA
% % modeProjection= 0; % MDthal
% 
% 
% 
% ind=[];
% ind= ~(ICSS.ProjGroup==modeProjection);
% 
% %loop thru fields and eliminate data
% allFields= fieldnames(ICSS);
% for field= 1:numel(allFields)
%     ICSS.(allFields{field})(ind)= [];
% end




%% plot ICSS Active vs Inactive NP Group

%dp adding xlim accounting for difference in group2
limXog= [1, 6];
limXreversal= [6, 10];

figure %projection
selection= ICSS.Expression==1 & ICSS.ExpType==1 & (strcmp(ICSS.Projection,'mdThal') | strcmp(ICSS.Projection,'VTA'));
g(1,1)=gramm('x',ICSS.Session(selection),'y',ICSS.ActiveNP(selection),'color',ICSS.Projection(selection))
g(1,1).stat_summary('type','sem','geom','area');
g(1,1).no_legend();
%g(1,1).set_names('x','Session','y','Number of Nose Pokes','color','Stim(-)')
g(1,1).set_title('ICSS Nosepoke')
g(1,1).axe_property( 'YLim',[0 500])
g(1,1).axe_property( 'XLim', limXog)

g(1,1).update('x',ICSS.Session(selection),'y',ICSS.InactiveNP(selection),'color',ICSS.Projection(selection))
g(1,1).stat_summary('type','sem','geom','area');
g(1,1).set_names('x','Session','y','Number of Nose Pokes','color','No Stim(--)')
g(1,1).no_legend();
g(1,1).set_title('ICSS')
g(1,1).set_line_options( 'styles',{':'})
%g.export( 'file_name','Verified ICSS Stim vs No Stim NP','export_path','/Volumes/nsci_richard/Christelle/Data/Opto Project/Figures','file_type','pdf') 

selection= ICSS.Expression==1 & ICSS.ExpType==1 & (strcmp(ICSS.Projection,'mdThal') | strcmp(ICSS.Projection,'VTA'));
g(1,2)=gramm('x',ICSS.Session(selection),'y',ICSS.ActiveNP(selection),'color',ICSS.Projection(selection))
g(1,2).stat_summary('type','sem','geom','area');
g(1,2).set_names('x','Session','y','Number of Nose Pokes','color','Stim(-)')
g(1,2).set_title('Reversal')
g(1,2).axe_property( 'YLim',[0 500])
g(1,2).axe_property( 'XLim',[limXreversal])

g(1,2).update('x',ICSS.Session(selection),'y',ICSS.InactiveNP(selection),'color',ICSS.Projection(selection))
g(1,2).stat_summary('type','sem','geom','area');
g(1,2).set_names('x','Session','y','Number of Nose Pokes','color','No Stim(--)')
g(1,2).set_title('Reversal')
g(1,2).set_line_options( 'styles',{':'})


% %projection and sex
% selection= ICSS.Expression==1 & ICSS.ExpType==1 & (strcmp(ICSS.Projection,'mdThal') | strcmp(ICSS.Projection,'VTA'));
% g(2,1)=gramm('x',ICSS.Session(selection),'y',ICSS.ActiveNP(selection),'color',ICSS.Projection(selection))
% g(2,1).stat_summary('type','sem','geom','area');
% g(2,1).facet_grid([],ICSS.Sex(selection))
% g(2,1).set_names('x','Session','y','Number of Nose Pokes','color','Stim(-)')
% g(2,1).no_legend();
% %g(2,1).set_title('ICSS Nosepoke--Projection and Sex')
% g(2,1).axe_property( 'YLim',[0 800])
% g(2,1).axe_property( 'XLim',[1 5])
% 
% g(2,1).update('x',ICSS.Session(selection),'y',ICSS.InactiveNP(selection),'color',ICSS.Projection(selection))
% g(2,1).stat_summary('type','sem','geom','area');
% g(2,1).no_legend();
% g(2,1).set_names('x','Session','y','Number of Nose Pokes','color','No Stim(--)')
% g(2,1).set_title('ICSS')
% g(2,1).set_line_options( 'styles',{':'})
% 
% g(2,2)=gramm('x',ICSS.Session(selection),'y',ICSS.ActiveNP(selection),'color',ICSS.Projection(selection))
% g(2,2).stat_summary('type','sem','geom','area');
% g(2,2).facet_grid([],ICSS.Sex(selection))
% g(2,2).set_names('x','Session','y','Number of Nose Pokes','color','Stim(-)')
% %g(2,2).set_title('Reversal')
% g(2,2).axe_property( 'YLim',[0 800])
% g(2,2).axe_property( 'XLim',[6 8])
% 
% g(2,2).update('x',ICSS.Session(selection),'y',ICSS.InactiveNP(selection),'color',ICSS.Projection(selection))
% g(2,2).stat_summary('type','sem','geom','area');
% g(2,2).set_names('x','Session','y','Number of Nose Pokes','color','No Stim(--)')
% g(2,2).set_title('ICSS')
% g(2,2).set_line_options( 'styles',{':'})


% plot ICSS Active vs Inactive Total Time in NP Group

selection= ICSS.Expression==1 & ICSS.ExpType==1 & (strcmp(ICSS.Projection,'mdThal') | strcmp(ICSS.Projection,'VTA'));
g(2,1)=gramm('x',ICSS.Session(selection),'y',ICSS.TotalLengthActiveNP(selection),'color',ICSS.Projection(selection))
g(2,1).stat_summary('type','sem','geom','area');
g(2,1).no_legend();
g(2,1).set_names('x','Session','y','Time in Nosepoke (s)','color','Stim(-)')
%g(3,1).set_title('VERIFIED ICSS Time in Nosepoke')
g(2,1).axe_property( 'XLim',limXog)
g(2,1).axe_property( 'YLim',[0 250])

g(2,1).update('x',ICSS.Session(selection),'y',ICSS.TotalLengthInactiveNP(selection),'color',ICSS.Projection(selection))
g(2,1).stat_summary('type','sem','geom','area');
g(2,1).no_legend();
g(2,1).set_names('x','Session','y','Time in Nosepoke(s)','color','No Stim(--)')
%g(2,1).set_title('VERIFIED ICSS Time in Nosepoke')
g(2,1).set_line_options( 'styles',{':'})
%g.export( 'file_name','VERIFIED ICSS Total Length Active vs Inactive NP','export_path','/Volumes/nsci_richard/Christelle/Data/Opto Project/Figures','file_type','pdf')


selection= ICSS.Expression==1 & ICSS.ExpType==1 & (strcmp(ICSS.Projection,'mdThal') | strcmp(ICSS.Projection,'VTA'));
g(2,2)=gramm('x',ICSS.Session(selection),'y',ICSS.TotalLengthActiveNP(selection),'color',ICSS.Projection(selection));
g(2,2).stat_summary('type','sem','geom','area');
g(2,2).set_names('x','Session','y','Time in Nosepoke(s)','color','Stim(-)')
%g(2,2).set_title('VERIFIED Reversal ICSS Time in Nosepoke')
g(2,2).axe_property( 'XLim',limXreversal)
g(2,2).axe_property( 'YLim',[0 250])


g(2,2).update('x',ICSS.Session(selection),'y',ICSS.TotalLengthInactiveNP(selection),'color',ICSS.Projection(selection))
g(2,2).stat_summary('type','sem','geom','area');
g(2,2).set_names('x','Session','y','Time in Nosepoke(s)','color','No Stim(--)')
%g(2,2).set_title('VERIFIED Reversal ICSS Time in Nosepoke')
g(2,2).set_line_options( 'styles',{':'})
%g.export( 'file_name','VERIFIED Reversal ICSS Total Length Active vs Inactive NP','export_path','/Volumes/nsci_richard/Christelle/Data/Opto Project/Figures','file_type','pdf')

g.draw();

figTitle= 'ICSS_nosepoke_data_verified';
saveFig(gcf, figPath,figTitle,figFormats);

% g.export('file_name','ICSS Nosepoke Data','export_path','/Volumes/nsci_richard/Christelle/Data/Opto Project/Figures','file_type','pdf') 


%% -- DP calculate active nosepoke preference & deltas

%-calculate active proportion (active/total)
ICSS.npTotal= ICSS.ActiveNP + ICSS.InactiveNP;

ICSS.npActiveProportion= ICSS.ActiveNP ./ ICSS.npTotal;

%calculate active nosepoke delta (active-inactive)
ICSS.npDelta= (ICSS.ActiveNP - ICSS.InactiveNP);


%calculate active fold NP relative to inactive (Active NP / Inactive NP)
ICSS.npActiveFold= (ICSS.ActiveNP ./ ICSS.InactiveNP);
%% DP plot of individual active nosepoke preference proportion (active/total)
%dp adding xlim accounting for difference in group2
limXall= [1,10];
limXog= [1, 6];
limXreversal= [6, 10];

%- plot individual rats active proportion NP
figure; clear d;

selection= ICSS.Expression==1 & ICSS.ExpType==1 & (strcmp(ICSS.Projection,'mdThal') | strcmp(ICSS.Projection,'VTA'));

d(1,1)=gramm('x',ICSS.Session(selection),'y',ICSS.npActiveProportion(selection),'color',ICSS.Subject(selection))
d(1,1).stat_summary('type','sem','geom','line');
d(1,1).set_names('x','Session','y','Proportion active nosepokes (active/total NP)','color','Stim(-)')
d(1,1).set_title('ICSS Active Proportion Nospoke Individual')
d(1,1).axe_property( 'YLim',[0 1],'XLim',limXall)

d(1,1).geom_hline('yintercept', 0.5, 'style', 'k--'); %horizontal line @ 0.5 (equal preference)
% d(1,1).draw();

%- plot delta NP
d(1,2)=gramm('x',ICSS.Session(selection),'y',ICSS.npDelta(selection),'color',ICSS.Subject(selection))
d(1,2).stat_summary('type','sem','geom','line');
d(1,2).set_names('x','Session','y','Delta nosepokes (Active - Inactive NP)','color','Stim(-)')
d(1,2).set_title('ICSS Delta Nospoke Individual')
d(1,2).axe_property( 'YLim',[0 150],'XLim',limXall)
d(1,2).geom_hline('yintercept', 0, 'style', 'k--'); %horizontal line @ 0 (equal preference)


% d(1,2).draw();

%- plot active fold NP
d(1,3)=gramm('x',ICSS.Session(selection),'y',ICSS.npActiveFold(selection),'color',ICSS.Subject(selection))
d(1,3).stat_summary('type','sem','geom','line');
d(1,3).set_names('x','Session','y','Active Fold nosepokes (Active / Inactive NP)','color','Stim(-)')
d(1,3).set_title('ICSS Delta Nospoke Individual')
d(1,3).axe_property( 'YLim',[0 10],'XLim',limXall)
d(1,3).geom_hline('yintercept', 1, 'style', 'k--'); %horizontal line @ 1 (equal preference)

d.draw();


%% dp reorganizing data into table for table fxns and easy faceting

ICSStable= table();

%loop thru fields and fill table
allFields= fieldnames(ICSS);
for field= 1:numel(allFields)
    ICSStable.(allFields{field})= ICSS.(allFields{field});
end


%--dp add trainPhase variable for distinct session types (e.g. active side `al)

%initialize
ICSStable(:,"trainPhase")= {''};

%for this ICSS ses 1-5= same side, >6 = reversal
ind= [];
ind= ICSStable.Session <= 5;

ICSStable(ind, "trainPhase")= {'ICSS-OG-active-side'};

ind= [];
ind= ICSStable.Session >= 6;

ICSStable(ind, "trainPhase")= {'ICSS-Reversed-active-side'};

%note some subjects have >8 sessions, looks like some extinction?
 % ^^ No?, there's no metadata at all suggesting this. they ran on the same
 % MSN and the sessions christelle left out in her excel sheet for matlab plotting
 % were 20190812 and 20190820. no reason as to why, presume it was just to
 % make neat 3 day plots or simply missed file from MPC2XL somehow.
 
 %will manually exclude below
 
 % could be just drop in response due to time shifted reversal,and those
 % rats were already responding at low levels?
 
% 2023-01-25 side reversal isn't as clean as previously suggested. paper
% notes show reversal for Group 2 was done on 2019-08-13, so they had
% sessions 1-6 on left side and sessions 7-10 on right side. need to make
% exception for these:
% ICSStable.StartDate= cell2mat(ICSStable.StartDate);

%overwrite 'OG side' days for group 2
datesManual= [];

datesManual= [190806, 190807, 190808, 190809, 190811, 190812]; 

ind= [];

ind= ismember(ICSStable.StartDate,datesManual);

ICSStable(ind, "trainPhase")= {'ICSS-OG-active-side'};

%overwrite 'reversal' days for group 2
datesManual= [];

datesManual= [190813, 190814, 190819, 190820];

ind= [];

ind= ismember(ICSStable.StartDate,datesManual);

ICSStable(ind, "trainPhase")= {'ICSS-Reversed-active-side'};


% %-dp add trainDayThisPhase for best plotting of trainPhase facet, for late
% %days this will be session-5 (assume all ran 5 days of first phase)
% ICSStable(:, "trainDayThisPhase")= table(nan); %initialize
% 
% ICSStable(:, "trainDayThisPhase")= table(ICSStable.Session); %start by prefilling w session
% 
% ICSStable(ind, "trainDayThisPhase")= table(ICSStable.Session(ind)-5); %carrying over ind of later phase, subtract n first phase sessions from this

% use findgruops for more robust counting (not assuming n sessions per
% phase since we know group 2 didn't follow assumption)
%initialize new col
data= ICSStable;
data(:,'trainDayThisPhase')= table(nan);

%use findgroups to groupby subject,trainPhase and manually cumcount() for
%sessions within-trainPhaseLabel

groupIDs= [];
groupIDs= findgroups(data.Subject, data.trainPhase);

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
    
    %assign back into table
    ICSStable(ind, 'trainDayThisPhase')= table(thisGroup.cumcount);
    
end 

%assign back into struct
% ICSStable.trainDayThisPhase= data.trainDayThisPhase;


%-dp add virus variable for labelling stim vs inhibition
%initialize
ICSStable(:,"virusType")= {''};


% expType= [0,1]%
expTypesAll= [0,1];
% %1= excitation, 0= inhibition
expTypeLabels= {'inhibition','stimulation'};

%loop thru and assign labels
for thisExpType= 1:numel(expTypesAll)
    
    %TODO- label actually needs to match with find
    
    ICSStable(:,"virusType")= expTypeLabels(thisExpType);
    
end



%% dp compute N- Count of subjects by sex for each group

expTypesAll= unique(ICSStable.ExpType);
expTypeLabels= unique(ICSStable.virusType);

for thisExpType= 1:numel(expTypesAll)

    thisExpTypeLabel= expTypeLabels{expTypesAll==thisExpType};

    %subset data- by expType/virus
    ind=[];
    ind= ICSStable.ExpType==expTypesAll(thisExpType);

    data= ICSStable(ind,:);

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
    
    nTable= groupsummary(data, ["virusType","Projection","Sex"]);
       
    %- save this along with figures
    titleFile= [];
    titleFile= strcat(thisExpTypeLabel,'-N-subjects');

    %save as .csv
    titleFile= strcat(figPath,titleFile,'.csv');
    
    writetable(nTable,titleFile)

end



%% DP SAVE DATA TO RELOAD AND MAKE MANUSCRIPT FIGS
save(fullfile(figPath,strcat('VP-OPTO-ICSS','-',date, '-ICSStable')), 'ICSStable', '-v7.3');





%% dp plot mean and individuals 

% cmapSubj= 'brewer2';
% cmapGrand= 'brewer_dark';

% cmapSubj= cmapCueSubj;
% cmapGrand= cmapCueGrand;

cmapSubj= cmapBlueGraySubj;
cmapGrand= cmapBlueGrayGrand;

%subset data
selection= ICSS.Expression==1 & ICSS.ExpType==1 & (strcmp(ICSS.Projection,'mdThal') | strcmp(ICSS.Projection,'VTA'));

data= ICSStable(selection,:);

%stack() to make inactive/active NPtype a variable
data= stack(data, {'ActiveNP', 'InactiveNP'}, 'IndexVariableName', 'typeNP', 'NewDataVariableName', 'countNP');

%generate figure
figure; clear d;

%-- individual subj
group= data.Subject;

d=gramm('x',data.trainDayThisPhase,'y',data.countNP,'color',data.typeNP, 'group', group)

%facet by trainPhase - ideally could set sharex of facets false but idk w gramm
d.facet_grid(data.Projection,data.trainPhase, 'scale', 'free_x');

d.stat_summary('type','sem','geom','line');
d.set_names('x','Session','y','Number of Nose Pokes','color','Nosepoke Side')

d().set_line_options('base_size',linewidthSubj);
d.set_color_options('map', cmapSubj);

d.no_legend(); %prevent legend duplicates if you like


%set text options
d.set_text_options(text_options_DefaultStyle{:}); 


d.draw()

%-- btwn subj mean as well
group= [];

d.update('x',data.trainDayThisPhase,'y',data.countNP,'color',data.typeNP, 'group', group)

d.stat_summary('type','sem','geom','area');

d.set_names('x','Session','y','Number of Nose Pokes','color','Nosepoke Side')

d().set_line_options('base_size',linewidthGrand);
d.set_color_options('map', cmapGrand);


figTitle= strcat('ICSS-dp-npType');   
d.set_title(figTitle);   

%Zoom in on lower NP subjects if desired
% d().axe_property( 'YLim',[0 300]) %low responders
d().axe_property( 'YLim',[0, 1200]) %high responders

% SET X TICK = 1 SESSION
d.axe_property('XTick',[min(data.trainDayThisPhase):1:max(data.trainDayThisPhase)]); %,'YLim',[0 75],'YTick',[0:25:75]);

% d(:,1).axe_property('XLim',limXog); %,'YLim',[0 75],'YTick',[0:25:75]);
% d(:,2).axe_property('XLim',limXreversal); %,'YLim',[0 75],'YTick',[0:25:75]);
% 


d.draw()

saveFig(gcf, figPath,figTitle,figFormats);

%% - dp try log scale of above (might help since extreme variability)

% cmapSubj= cmapBlueGraySubj;
% cmapGrand= cmapBlueGrayGrand;

%subset data
% selection= ICSS.Expression==1 & ICSS.ExpType==1 & (strcmp(ICSS.Projection,'mdThal') | strcmp(ICSS.Projection,'VTA'));

% data= ICSStable(selection,:);

%stack() to make inactive/active NPtype a variable
% data= stack(data, {'ActiveNP', 'InactiveNP'}, 'IndexVariableName', 'typeNP', 'NewDataVariableName', 'countNP');

data.logNP = log(data.countNP);

% if countNP is == 0, log returns -inf. Make these nan
data(data.logNP==-inf, "logNP")= table(nan);

%generate figure
figure; clear d;

%-- individual subj
group= data.Subject;

d=gramm('x',data.trainDayThisPhase,'y',data.logNP,'color',data.typeNP, 'group', group)

%facet by trainPhase - ideally could set sharex of facets false but idk w gramm
d.facet_grid(data.Projection,data.trainPhase, 'scale','free_x');

d.stat_summary('type','sem','geom','line');
d.set_names('x','Session','y','Log(Number of Nose Pokes)','color','Nosepoke Side')

d().set_line_options('base_size',linewidthSubj);
d.set_color_options('map', cmapSubj);

d.no_legend(); %prevent legend duplicates if you like


%set text options
d.set_text_options(text_options_DefaultStyle{:}); 


d.draw()

%-- btwn subj mean as well
group= [];

d.update('x',data.trainDayThisPhase,'y',data.logNP,'color',data.typeNP, 'group', group)

d.stat_summary('type','sem','geom','area');

d.set_names('x','Session','y','Log(Number of Nose Pokes)','color','Nosepoke Side')

d().set_line_options('base_size',linewidthGrand);
d.set_color_options('map', cmapGrand);


figTitle= strcat('ICSS-dp-npType-logScale');   
d.set_title(figTitle);   

% d().axe_property( 'YLim',[0 300]) %low responders
% d().axe_property( 'YLim',[0, 1200]) %high responders

% SET X TICK = 1 SESSION
d.axe_property('XTick',[min(data.trainDayThisPhase):1:max(data.trainDayThisPhase)]); %,'YLim',[0 75],'YTick',[0:25:75]);

d.draw()

saveFig(gcf, figPath,figTitle,figFormats);


%% -- dp inset bar plot of last ICSS day prior to reversal

%subset data
sesToPlot= 5; %plot last day before reversal

ind= [];
ind= data.Session== sesToPlot;

data= data(ind, :);

% dodge= 	.2; %if dodge constant between point and bar, will align correctly
% width= 1; %bar width

%make fig
clear d; figure();

%- Bar of btwn subj means (group = [])
group= []; %var by which to group

d=gramm('x',data.typeNP,'y',data.countNP,'color',data.typeNP, 'group', group)

d.facet_grid(data.Projection,[]);

d(1,1).stat_summary('type','sem', 'geom',{'bar' 'black_errorbar'}, 'dodge', dodge);
% d(1,1).stat_summary('type','sem', 'geom',{'bar' 'black_errorbar'}, 'dodge', dodge, 'width', width) 

d(1,1).set_color_options('map',cmapGrand); 

d.set_names('x','Nosepoke Side','y','Number of Nose Pokes','color','Nosepoke Side')

figTitle= 'ICSS inset final session preReversal';

d().set_title(figTitle)

%set text options- do before first draw() call so applied on subsequent updates()
d.set_text_options(text_options_DefaultStyle{:}); 

%set x lims and ticks (a bit more manual good for bars)
lims= [1-.6,numel(unique(data.typeNP))+.6];

d.axe_property('XLim',lims);
d.axe_property('XTick',round([lims(1):1:lims(2)]));



d.draw()

%- Draw lines between individual subject points (group= subject, color=[]);
group= data.Subject;
d.update('x', data.typeNP,'y',data.countNP,'color',[], 'group', group)

% d(1,1).stat_summary('geom',{'line'});
d(1,1).geom_line('alpha',0.3);
d().set_line_options('base_size',linewidthSubj);

d(1,1).set_color_options('chroma', chromaLineSubj); %black lines connecting points

d.draw()

%- Update with point of individual subj points (group= subject)
group= data.Subject;
d.update('x', data.typeNP,'y',data.countNP,'color',data.typeNP, 'group', group)
d(1,1).stat_summary('type','sem','geom',{'point'}, 'dodge', dodge)%,'bar' 'black_errorbar'});

d(1,1).set_color_options('map',cmapSubj);

d.draw();


saveFig(gcf, figPath,figTitle,figFormats);


%% dp log scale inset bar plot of last ICSS day prior to reversal

%subset data
sesToPlot= 5; %plot last day before reversal

ind= [];
ind= data.Session== sesToPlot;

data= data(ind, :);

%make fig
clear d; figure();

%- Bar of btwn subj means (group = [])
group= []; %var by which to group

d=gramm('x',data.typeNP,'y',data.logNP,'color',data.typeNP, 'group', group)

d.facet_grid(data.Projection,[]);

d(1,1).stat_summary('type','sem', 'geom',{'bar' 'black_errorbar'}, 'dodge', dodge) 
d(1,1).set_color_options('map',cmapGrand); 

d.set_names('x','Nosepoke Side','y','Log(Number of Nose Pokes)','color','Nosepoke Side')

figTitle= 'ICSS inset final session preReversal logScale';

d().set_title(figTitle)

%set text options- do before first draw() call so applied on subsequent updates()
d.set_text_options(text_options_DefaultStyle{:}); 

d.draw()

%- Draw lines between individual subject points (group= subject, color=[]);
group= data.Subject;
d.update('x', data.typeNP,'y',data.logNP,'color',[], 'group', group)

% d(1,1).stat_summary('geom',{'line'});
d(1,1).geom_line('alpha',0.3);
d().set_line_options('base_size',linewidthSubj);

d(1,1).set_color_options('chroma', 0); %black lines connecting points

d.draw()

%- Update with point of individual subj points (group= subject)
group= data.Subject;
d.update('x', data.typeNP,'y',data.logNP,'color',data.typeNP, 'group', group)
d(1,1).stat_summary('type','sem','geom',{'point'}, 'dodge', dodge)%,'bar' 'black_errorbar'});

d(1,1).set_color_options('map',cmapSubj); 

d.draw();


saveFig(gcf, figPath,figTitle,figFormats);


%% === ---------------------DP Figure 6 2022-10-17 ----------

% do figure 5 first. use that as template

%% ----Stat comparison of ICSS active v inactive nosepokes

%% Prior to stats, viz the distribution 
%wondering if should run stats on log or raw nosepoke counts

figure(); clear g;

g(1,1)= gramm('x', data.countNP, 'color', data.typeNP);

g(1,1).set_names('x','Number of Nose Pokes','color','Nosepoke Side')

g(1,1).stat_bin()

g(2,1)= gramm('x', data.logNP, 'color', data.typeNP);

g(2,1).stat_bin()

g(1,1).set_names('x','Log(Number of Nose Pokes)','color','Nosepoke Side')

figTitle= 'ICSS inset final session preReversal-Stats Distribution';

g().set_title(figTitle)

g.set_text_options(text_options_DefaultStyle{:}); %set text options- do before first draw() call so applied on subsequent updates()

g.set_color_options('map',cmapGrand); 

g.draw();

saveFig(gcf, figPath,figTitle,figFormats);

%% Run Stats on log np count from single session

%copying dataset above prior to reformatting/dummy coding variables
data2= data; 

% STAT Testing
%are mean nosepokes different by laser state/virus etc?... lme with random subject intercept

%- dummy variable conversion
% converting to dummies(retains only one column, as 2+ is redundant)

%convert typeNP to dummy variable 
dummy=[];
dummy= categorical(data2.typeNP);
dummy= dummyvar(dummy); 

data2.typeNP= dummy(:,1);

%--Run LME
lme1=[];

lme1= fitlme(data2, 'logNP~ typeNP + (1|Subject)');

lme1


%print and save results to file
%seems diary keeps running log to same file (e.g. if code rerun seems prior output remains)
diary('ICSS inset final session preReversal-Stats lmeDetails.txt')
lme1
diary off

%% Run stats on log np count from all sessions

% subset data
selection= ICSS.Expression==1 & ICSS.ExpType==1 & (strcmp(ICSS.Projection,'mdThal') | strcmp(ICSS.Projection,'VTA'));

data= ICSStable(selection,:);

% stack() to make inactive/active NPtype a variable
data= stack(data, {'ActiveNP', 'InactiveNP'}, 'IndexVariableName', 'typeNP', 'NewDataVariableName', 'countNP');

%add log NP
data(:,"logNP") = table(log(data.countNP));

% % if countNP is == 0, log returns -inf. Make these 0
% data(data.logNP==-inf, "logNP")= table(0);
% % if countNP is == 0, log returns -inf. Make these nan
data(data.logNP==-inf, "logNP")= table(nan);


%copying dataset above prior to dummy coding variables
data2= data; 


%- dummy variable conversion
% converting to dummies(retains only one column, as 2+ is redundant)

%convert typeNP to dummy variable 
dummy=[];
dummy= categorical(data.typeNP);
dummy= dummyvar(dummy); 

data2.typeNP= dummy(:,1);

%convert trainPhase as dummyVar too
dummy=[];
dummy= categorical(data.trainPhase);
dummy= dummyvar(dummy);

data2(:,"activeSideReversal")= table(dummy(:,1)); %(rename as activeSideReversal)


%--run LME
lme1=[];

lme1= fitlme(data2, 'logNP~ typeNP* Session * activeSideReversal + (1|Subject)');


%print and save results to file
%seems diary keeps running log to same file (e.g. if code rerun seems prior output remains)
diary('ICSS allSessions-Stats lmeDetails.txt')
lme1
diary off



%% Individual Data

limXall= [1,10]; %accounting for the group2 difference

%plot individual rats Active vs Inactive NP
figure; clear d;
selection= ICSS.Expression==1 & ICSS.ExpType==1 & (strcmp(ICSS.Projection,'mdThal') | strcmp(ICSS.Projection,'VTA'));
d(1,1)=gramm('x',ICSS.Session(selection),'y',ICSS.ActiveNP(selection),'color',ICSS.Subject(selection))
d(1,1).stat_summary('type','sem','geom','line');
d(1,1).set_names('x','Session','y','Number of Nose Pokes','color','Stim(-)')
d(1,1).set_title('ICSS Nospoke Individual')
d(1,1).axe_property( 'YLim',[0 1500],'XLim',[limXall])

%d.export( 'file_name','Verified ICSS Individual Data','export_path','/Volumes/nsci_richard/Christelle/Data/Opto Project/Figures','file_type','pdf')
d(1,1).draw();

%- dp add inactive np lines for individuals
d(1,1).update('x',ICSS.Session(selection),'y',ICSS.InactiveNP(selection),'color',ICSS.Subject(selection))
d(1,1).stat_summary('type','sem','geom','line');
d(1,1).set_names('x','Session','y','Number of Nose Pokes','color','No Stim(--)')
d(1,1).set_line_options( 'styles',{':'})

% dp zoom in (can always have inlay or try log scale for highly responsive subj)
d(1,1).axe_property( 'YLim',[0 100])

% d(1,1).draw();

%plot ICSS Active vs Inactive Total Time in NP Individual
selection= ICSS.Expression==1 & ICSS.ExpType==1 & (strcmp(ICSS.Projection,'mdThal') | strcmp(ICSS.Projection,'VTA'));
d(1,2)=gramm('x',ICSS.Session(selection),'y',ICSS.TotalLengthActiveNP(selection),'color',ICSS.Subject(selection))
d(1,2).stat_summary('type','sem','geom','area');
d(1,2).set_names('x','Session','y','Time in Nosepoke','color','Active(-)')
d(1,2).set_title('ICSS Time in Nosepoke Individual')
d(1,2).axe_property( 'YLim',[0 150])
d.draw()


d(1,2).update('x',ICSS.Session(selection),'y',ICSS.TotalLengthInactiveNP(selection),'color',ICSS.Subject(selection))
d(1,2).stat_summary('type','sem','geom','area');
d(1,2).set_names('x','Session','y','Time in Nosepoke','color','Inactive(--)')
d(1,2).set_title('ICSS Time in Nosepoke')
d(1,2).set_line_options( 'styles',{':'})
d(1,2).draw()

figTitle= 'ICSS_nosepoke_data_individuals_verified';
saveFig(gcf, figPath,figTitle,figFormats);

%Calculate how many animals/sex per group on each session day
Fmdthal= ICSS.Expression==1 & ICSS.ExpType==1 & ICSS.Session==1 & strcmp(ICSS.Sex,'F') & strcmp(ICSS.Projection,'mdThal');
Mmdthal=ICSS.Expression==1 & ICSS.ExpType==1 & ICSS.Session==1 & strcmp(ICSS.Sex,'M') & strcmp(ICSS.Projection,'mdThal');
FVTA= ICSS.Expression==1 & ICSS.ExpType==1 & ICSS.Session==1 & strcmp(ICSS.Sex,'F') & strcmp(ICSS.Projection,'VTA');
MVTA= ICSS.Expression==1 & ICSS.ExpType==1 & ICSS.Session==1 & strcmp(ICSS.Sex,'M') & strcmp(ICSS.Projection,'VTA');

Fmdthal= ICSS.Expression==1 & ICSS.ExpType==1 & ICSS.Session==2 & strcmp(ICSS.Sex,'F') & strcmp(ICSS.Projection,'mdThal');
Mmdthal=ICSS.Expression==1 & ICSS.ExpType==1 & ICSS.Session==2 & strcmp(ICSS.Sex,'M') & strcmp(ICSS.Projection,'mdThal');
FVTA= ICSS.Expression==1 & ICSS.ExpType==1 & ICSS.Session==2 & strcmp(ICSS.Sex,'F') & strcmp(ICSS.Projection,'VTA');
MVTA= ICSS.Expression==1 & ICSS.ExpType==1 & ICSS.Session==2 & strcmp(ICSS.Sex,'M') & strcmp(ICSS.Projection,'VTA');

Fmdthal= ICSS.Expression==1 & ICSS.ExpType==1 & ICSS.Session==3 & strcmp(ICSS.Sex,'F') & strcmp(ICSS.Projection,'mdThal');
Mmdthal=ICSS.Expression==1 & ICSS.ExpType==1 & ICSS.Session==3 & strcmp(ICSS.Sex,'M') & strcmp(ICSS.Projection,'mdThal');
FVTA= ICSS.Expression==1 & ICSS.ExpType==1 & ICSS.Session==3 & strcmp(ICSS.Sex,'F') & strcmp(ICSS.Projection,'VTA');
MVTA= ICSS.Expression==1 & ICSS.ExpType==1 & ICSS.Session==3 & strcmp(ICSS.Sex,'M') & strcmp(ICSS.Projection,'VTA');


Fmdthal= ICSS.Expression==1 & ICSS.ExpType==1 & ICSS.Session==4 & strcmp(ICSS.Sex,'F') & strcmp(ICSS.Projection,'mdThal');
Mmdthal=ICSS.Expression==1 & ICSS.ExpType==1 & ICSS.Session==4 & strcmp(ICSS.Sex,'M') & strcmp(ICSS.Projection,'mdThal');
FVTA= ICSS.Expression==1 & ICSS.ExpType==1 & ICSS.Session==4 & strcmp(ICSS.Sex,'F') & strcmp(ICSS.Projection,'VTA');
MVTA= ICSS.Expression==1 & ICSS.ExpType==1 & ICSS.Session==4 & strcmp(ICSS.Sex,'M') & strcmp(ICSS.Projection,'VTA');

Fmdthal= ICSS.Expression==1 & ICSS.ExpType==1 & ICSS.Session==5 & strcmp(ICSS.Sex,'F') & strcmp(ICSS.Projection,'mdThal');
Mmdthal=ICSS.Expression==1 & ICSS.ExpType==1 & ICSS.Session==5 & strcmp(ICSS.Sex,'M') & strcmp(ICSS.Projection,'mdThal');
FVTA= ICSS.Expression==1 & ICSS.ExpType==1 & ICSS.Session==5 & strcmp(ICSS.Sex,'F') & strcmp(ICSS.Projection,'VTA');
MVTA= ICSS.Expression==1 & ICSS.ExpType==1 & ICSS.Session==5 & strcmp(ICSS.Sex,'M') & strcmp(ICSS.Projection,'VTA');

Fmdthal= ICSS.Expression==1 & ICSS.ExpType==1 & ICSS.Session==6 & strcmp(ICSS.Sex,'F') & strcmp(ICSS.Projection,'mdThal');
Mmdthal=ICSS.Expression==1 & ICSS.ExpType==1 & ICSS.Session==6 & strcmp(ICSS.Sex,'M') & strcmp(ICSS.Projection,'mdThal');
FVTA= ICSS.Expression==1 & ICSS.ExpType==1 & ICSS.Session==6 & strcmp(ICSS.Sex,'F') & strcmp(ICSS.Projection,'VTA');
MVTA= ICSS.Expression==1 & ICSS.ExpType==1 & ICSS.Session==6 & strcmp(ICSS.Sex,'M') & strcmp(ICSS.Projection,'VTA');

Fmdthal= ICSS.Expression==1 & ICSS.ExpType==1 & ICSS.Session==7 & strcmp(ICSS.Sex,'F') & strcmp(ICSS.Projection,'mdThal');
Mmdthal=ICSS.Expression==1 & ICSS.ExpType==1 & ICSS.Session==7 & strcmp(ICSS.Sex,'M') & strcmp(ICSS.Projection,'mdThal');
FVTA= ICSS.Expression==1 & ICSS.ExpType==1 & ICSS.Session==7 & strcmp(ICSS.Sex,'F') & strcmp(ICSS.Projection,'VTA');
MVTA= ICSS.Expression==1 & ICSS.ExpType==1 & ICSS.Session==7 & strcmp(ICSS.Sex,'M') & strcmp(ICSS.Projection,'VTA');

Fmdthal= ICSS.Expression==1 & ICSS.ExpType==1 & ICSS.Session==8 & strcmp(ICSS.Sex,'F') & strcmp(ICSS.Projection,'mdThal');
Mmdthal=ICSS.Expression==1 & ICSS.ExpType==1 & ICSS.Session==8 & strcmp(ICSS.Sex,'M') & strcmp(ICSS.Projection,'mdThal');
FVTA= ICSS.Expression==1 & ICSS.ExpType==1 & ICSS.Session==8 & strcmp(ICSS.Sex,'F') & strcmp(ICSS.Projection,'VTA');
MVTA= ICSS.Expression==1 & ICSS.ExpType==1 & ICSS.Session==8 & strcmp(ICSS.Sex,'M') & strcmp(ICSS.Projection,'VTA');

% sum(Fmdthal)
% sum(Mmdthal)
% sum(FVTA)
% sum(MVTA)
% 

%d.export( 'file_name','ICSS Individual Date (Total NP and NP Times)','export_path','/Volumes/nsci_richard/Christelle/Data/Opto Project/Figures','file_type','pdf')