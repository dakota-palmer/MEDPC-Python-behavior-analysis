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
CurrentDir = 'C:\Users\Dakota\Desktop\_christelle_opto_copy';
cd(CurrentDir)


[~,~,raw] = xlsread('Opto ICSS Data');
% [~,~,ratinfo] = xlsread('Christelle Opto Summary Record.xlsx');
[~,~,ratinfo] = xlsread('Christelle Opto Summary Record_dp.xlsx');


VarNames = raw(1,:);
Data = raw(2: end,:);

ICSS = struct();

for i=1:9 
    ICSS.(VarNames{i}) = Data(1:end,(i));
end

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

ICSS.Session=cell2mat(ICSS.Session)
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


%% DP Subset data for vp--> vta group only

ind=[];
ind= ~(ICSS.ProjGroup==1);

%loop thru fields and eliminate data
allFields= fieldnames(ICSS);
for field= 1:numel(allFields)
    ICSS.(allFields{field})(ind)= [];
end



%% plot ICSS Active vs Inactive NP Group

figure %projection
selection= ICSS.Expression==1 & ICSS.ExpType==1 & (strcmp(ICSS.Projection,'mdThal') | strcmp(ICSS.Projection,'VTA'));
g(1,1)=gramm('x',ICSS.Session(selection),'y',ICSS.ActiveNP(selection),'color',ICSS.Projection(selection))
g(1,1).stat_summary('type','sem','geom','area');
g(1,1).no_legend();
%g(1,1).set_names('x','Session','y','Number of Nose Pokes','color','Stim(-)')
g(1,1).set_title('ICSS Nosepoke')
g(1,1).axe_property( 'YLim',[0 500])
g(1,1).axe_property( 'XLim',[1 5])

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
g(1,2).axe_property( 'XLim',[6 8])

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
g(2,1).axe_property( 'XLim',[1 5])
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
g(2,2).axe_property( 'XLim',[6 8])
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

%- plot individual rats active proportion NP
figure; clear d;

selection= ICSS.Expression==1 & ICSS.ExpType==1 & (strcmp(ICSS.Projection,'mdThal') | strcmp(ICSS.Projection,'VTA'));

d(1,1)=gramm('x',ICSS.Session(selection),'y',ICSS.npActiveProportion(selection),'color',ICSS.Subject(selection))
d(1,1).stat_summary('type','sem','geom','line');
d(1,1).set_names('x','Session','y','Proportion active nosepokes (active/total NP)','color','Stim(-)')
d(1,1).set_title('ICSS Active Proportion Nospoke Individual')
d(1,1).axe_property( 'YLim',[0 1],'XLim',[1 8])

d(1,1).geom_hline('yintercept', 0.5, 'style', 'k--'); %horizontal line @ 0.5 (equal preference)
% d(1,1).draw();

%- plot delta NP
d(1,2)=gramm('x',ICSS.Session(selection),'y',ICSS.npDelta(selection),'color',ICSS.Subject(selection))
d(1,2).stat_summary('type','sem','geom','line');
d(1,2).set_names('x','Session','y','Delta nosepokes (Active - Inactive NP)','color','Stim(-)')
d(1,2).set_title('ICSS Delta Nospoke Individual')
d(1,2).axe_property( 'YLim',[0 150],'XLim',[1 8])
d(1,2).geom_hline('yintercept', 0, 'style', 'k--'); %horizontal line @ 0 (equal preference)


% d(1,2).draw();

%- plot active fold NP
d(1,3)=gramm('x',ICSS.Session(selection),'y',ICSS.npActiveFold(selection),'color',ICSS.Subject(selection))
d(1,3).stat_summary('type','sem','geom','line');
d(1,3).set_names('x','Session','y','Active Fold nosepokes (Active / Inactive NP)','color','Stim(-)')
d(1,3).set_title('ICSS Delta Nospoke Individual')
d(1,3).axe_property( 'YLim',[0 10],'XLim',[1 8])
d(1,3).geom_hline('yintercept', 1, 'style', 'k--'); %horizontal line @ 1 (equal preference)

d.draw();


%% dp reorganizing data into table for table fxns and easy faceting

ICSStable= table();

%loop thru fields and fill table
allFields= fieldnames(ICSS);
for field= 1:numel(allFields)
    ICSStable.(allFields{field})= ICSS.(allFields{field});
end


%--dp add trainPhase variable for distinct session types (e.g. active side reversal)

%initialize
ICSStable(:,"trainPhase")= {''};

%for this ICSS ses 1-5= same side, >6 = reversal
ind= [];
ind= ICSStable.Session <= 5;

ICSStable(ind, "trainPhase")= {'ICSS-OG-active-side'};

ind= [];
ind= ICSStable.Session >= 6;

ICSStable(ind, "trainPhase")= {'ICSS-Reversed-active-side'};

%-dp add trainDayThisPhase for best plotting of trainPhase facet, for late
%days this will be session-5 (assume all ran 5 days of first phase)
ICSStable(:, "trainDayThisPhase")= table(nan); %initialize

ICSStable(:, "trainDayThisPhase")= table(ICSStable.Session); %start by prefilling w session

ICSStable(ind, "trainDayThisPhase")= table(ICSStable.Session(ind)-5); %carrying over ind of later phase, subtract n first phase sessions from this


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

% d(1,1)=gramm('x',ICSS.Session(selection),'y',ICSS.ActiveNP(selection),'color',ICSS.Subject(selection))
d=gramm('x',data.trainDayThisPhase,'y',data.countNP,'color',data.typeNP, 'group', group)
% d=gramm('x',data.trainDayThisPhase,'y',data.countNP,'color',data.typeNP, 'group', group, 'lightness',group)

%facet by trainPhase - ideally could set sharex of facets false but idk w gramm
d.facet_grid([],data.trainPhase);

d.stat_summary('type','sem','geom','line');
d.set_names('x','Session','y','Number of Nose Pokes','color','Nosepoke Side')

d().set_line_options('base_size',linewidthSubj);
d.set_color_options('map', cmapSubj);

% d.set_color_options('lightness_range', lightnessRangeSubj);
% d.no_legend() %if faceting with lightness for individual observations, dont add legend since lighntess labels can be huge

d.draw()

%-- btwn subj mean as well
group= [];

d.update('x',data.trainDayThisPhase,'y',data.countNP,'color',data.typeNP, 'group', group)
% d.update('x',data.trainDayThisPhase,'y',data.countNP,'color',data.typeNP, 'group', group, 'lightness', [])

d.stat_summary('type','sem','geom','area');

d.set_names('x','Session','y','Number of Nose Pokes','color','Nosepoke Side')

d().set_line_options('base_size',linewidthGrand);
d.set_color_options('map', cmapGrand);

% d.set_color_options('lightness_range', lightnessRangeGrand);

figTitle= strcat('ICSS-dp-npType');   
d.set_title(figTitle);   

%Zoom in on lower NP subjects, can comment out and make inlay for high
%responders?
% d().axe_property( 'YLim',[0 300]) %low responders
d().axe_property( 'YLim',[0, 1200]) %high responders

% SET X TICK = 1 SESSION
d.axe_property('XTick',[min(data.trainDayThisPhase):1:max(data.trainDayThisPhase)]); %,'YLim',[0 75],'YTick',[0:25:75]);

%set text options
d.set_text_options(text_options_DefaultStyle{:}); 



%TODO: Explore inlay options in matlab
%g(1,1).set_layout_options('Position',[0.5 .33 0.5 0.33],'legend_position',[0.65 0.38 0.1 0.1]);
    % First 2 in 'position': halfway over, 1/3 of the way up; next 2 may be size
    
d.draw()


saveFig(gcf, figPath,figTitle,figFormats);


%% -- dp inset bar plot of last ICSS day prior to reversal

%subset data
sesToPlot= 5; %plot last day before reversal

ind= [];
ind= data.Session== sesToPlot;

data= data(ind, :);

%make fig
clear d; figure();

%- Bar of btwn subj means (group = [])
group= []; %var by which to group

d=gramm('x',data.typeNP,'y',data.countNP,'color',data.typeNP, 'group', group)

d(1,1).stat_summary('type','sem', 'geom',{'bar' 'black_errorbar'}, 'dodge', dodge) 
d(1,1).set_color_options('map',cmapGrand); 

d.set_names('x','Nosepoke Side','y','Number of Nose Pokes','color','Nosepoke Side')
d(1,1).set_title('ICSS Final day before reversal nosepoke inset')

%set text options- do before first draw() call so applied on subsequent updates()
d.set_text_options(text_options_DefaultStyle{:}); 

d.draw()

%- Draw lines between individual subject points (group= subject, color=[]);
group= data.Subject;
d.update('x', data.typeNP,'y',data.countNP,'color',[], 'group', group)

% d(1,1).stat_summary('geom',{'line'});
d(1,1).geom_line('alpha',0.3);
d().set_line_options('base_size',linewidthSubj);

d(1,1).set_color_options('chroma', 0); %black lines connecting points

d.draw()

%- Update with point of individual subj points (group= subject)
group= data.Subject;
d.update('x', data.typeNP,'y',data.countNP,'color',data.typeNP, 'group', group)
d(1,1).stat_summary('type','sem','geom',{'point'}, 'dodge', dodge)%,'bar' 'black_errorbar'});

d(1,1).set_color_options('map',cmapSubj); 

d.draw();


figTitle= 'ICSS_inset_final_session_preReversal';

saveFig(gcf, figPath,figTitle,figFormats);


%% Individual Data


%plot individual rats Active vs Inactive NP
figure; clear d;
selection= ICSS.Expression==1 & ICSS.ExpType==1 & (strcmp(ICSS.Projection,'mdThal') | strcmp(ICSS.Projection,'VTA'));
d(1,1)=gramm('x',ICSS.Session(selection),'y',ICSS.ActiveNP(selection),'color',ICSS.Subject(selection))
d(1,1).stat_summary('type','sem','geom','line');
d(1,1).set_names('x','Session','y','Number of Nose Pokes','color','Stim(-)')
d(1,1).set_title('ICSS Nospoke Individual')
d(1,1).axe_property( 'YLim',[0 1500],'XLim',[1 8])
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