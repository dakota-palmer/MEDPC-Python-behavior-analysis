cmapSubj= cmapBlueGraySubj;
cmapGrand= cmapBlueGrayGrand;


%---- Row 1: Pre-Reversal

% subset data
data= ICSStable;

% subset data- by trainPhase
ind= [];
ind= contains(data.trainPhase, {'ICSS-OG-active-side'}); 

data= data(ind,:);

%stack() to make inactive/active NPtype a variable
data= stack(data, {'ActiveNP', 'InactiveNP'}, 'IndexVariableName', 'typeNP', 'NewDataVariableName', 'countNP');

dataFig6A=[];
dataFig6A= data;

% Plot Raw Count of nosepokes
y= 'countNP';


%generate figure
figure; clear d;

%-- individual subj
group= dataFig6A.Subject;

d(1,1)=gramm('x',dataFig6A.trainDayThisPhase,'y',dataFig6A.(y),'color',dataFig6A.typeNP, 'group', group)

%facet by trainPhase - ideally could set sharex of facets false but idk w gramm
% d.facet_grid(dataFig6A.Projection,dataFig6A.trainPhase, 'scale', 'free_x');
d(1,1).facet_grid([], dataFig6A.Projection, 'scale', 'free_x');


% d(1,1).stat_summary('type','sem','geom','line');
d(1,1).set_names('x','Session','y','Number of Nose Pokes','color','Nosepoke Side', 'column','')

d(1,1).set_line_options('base_size',linewidthSubj);
d(1,1).set_color_options('map', cmapSubj);

d(1,1).no_legend(); %prevent legend duplicates if you like


%set text options
d(1,1).set_text_options(text_options_DefaultStyle{:}); 


figTitle= strcat('A) ICSS OG side');   
% d(1,1).set_title(figTitle)

d(1,1).draw()

%-- btwn subj mean as well
group= [];

d(1,1).update('x',dataFig6A.trainDayThisPhase,'y',dataFig6A.(y),'color',dataFig6A.typeNP, 'group', group)

d(1,1).stat_summary('type','sem','geom','area');

% d(1,1).set_names('x','Session','y','Number of Nose Pokes','color','Nosepoke Side')

d(1,1).set_line_options('base_size',linewidthGrand);
d(1,1).set_color_options('map', cmapGrand);

d(1,1).no_legend();

figTitle= strcat('ICSS-dp-npType');   
% d(1,1).set_title(figTitle);   

%Zoom in on lower NP subjects if desired
% d().axe_property( 'YLim',[0 300]) %low responders
% d(1,1).axe_property( 'YLim',[0, 1200]) %high responders

d(1,1).axe_property( 'YLim', ylimLP);
d(1,1).axe_property( 'YTick', yTickLP);


% SET X TICK = 1 SESSION
d(1,1).axe_property('XTick',[min(dataFig6A.trainDayThisPhase):1:max(dataFig6A.trainDayThisPhase)]); %,'YLim',[0 75],'YTick',[0:25:75]);

% d(:,1).axe_property('XLim',limXog); %,'YLim',[0 75],'YTick',[0:25:75]);
% d(:,2).axe_property('XLim',limXreversal); %,'YLim',[0 75],'YTick',[0:25:75]);
% 





%---- Row 2: Reversal

% subset data
data= ICSStable;

% subset data- by trainPhase
ind= [];
ind= contains(data.trainPhase, {'ICSS-Reversed-active-side'}); 

data= data(ind,:);

%stack() to make inactive/active NPtype a variable
data= stack(data, {'ActiveNP', 'InactiveNP'}, 'IndexVariableName', 'typeNP', 'NewDataVariableName', 'countNP');

dataFig6B=[];
dataFig6B= data;

%-- individual subj
group= dataFig6B.Subject;

d(2,1)=gramm('x',dataFig6B.trainDayThisPhase,'y',dataFig6B.(y),'color',dataFig6B.typeNP, 'group', group, 'column', '')

%facet by trainPhase - ideally could set sharex of facets false but idk w gramm
% d.facet_grid(data6B.Projection,data6B.trainPhase, 'scale', 'free_x');
d(2,1).facet_grid([], dataFig6B.Projection, 'scale', 'free_x');


% d(2,1).stat_summary('type','sem','geom','line');
d(2,1).set_names('x','Session','y',y,'color','Nosepoke Side','column','');

d(2,1).set_line_options('base_size',linewidthSubj);
d(2,1).set_color_options('map', cmapSubj);

d(2,1).no_legend(); %prevent legend duplicates if you like


%set text options
d(2,1).set_text_options(text_options_DefaultStyle{:}); 


figTitle= strcat('D) ICSS Reversal');   
% d(2,1).set_title(figTitle);  


d(2,1).draw()

%-- btwn subj mean as well
group= [];

d(2,1).update('x',dataFig6B.trainDayThisPhase,'y',dataFig6B.(y),'color',dataFig6B.typeNP, 'group', group)

d(2,1).stat_summary('type','sem','geom','area');

% d(2,1).set_names('x','Session','y','Number of Nose Pokes','color','Nosepoke Side')

d(2,1).set_line_options('base_size',linewidthGrand);
d(2,1).set_color_options('map', cmapGrand);

d(2,1).no_legend(); 

%Zoom in on lower NP subjects if desired
% d().axe_property( 'YLim',[0 300]) %low responders
% d(2,1).axe_property( 'YLim',[0, 1200]) %high responders

d(2,1).axe_property( 'YLim', ylimLP);
d(2,1).axe_property( 'YTick', yTickLP);


% SET X TICK = 1 SESSION
d(2,1).axe_property('XTick',[min(dataFig6B.trainDayThisPhase):1:max(dataFig6B.trainDayThisPhase)]); %,'YLim',[0 75],'YTick',[0:25:75]);

% d(:,1).axe_property('XLim',limXog); %,'YLim',[0 75],'YTick',[0:25:75]);
% d(:,2).axe_property('XLim',limXreversal); %,'YLim',[0 75],'YTick',[0:25:75]);
% 

%------ Column 2: last day log scale bars

%-- Row 1 col 2- last day OG side LOG

cmapSubj= cmapBlueGraySubj;
cmapGrand= cmapBlueGrayGrand;

%subset data
data= ICSStable;
% 
% sesToPlot= 5; %plot last da y before reversal
% 
% ind= [];
% ind= ICSStable.Session== sesToPlot;

% subset last day prior to reversal; and last day of reversal (for AUCs)
sesToPlot= [];

sesToPlot= [5];

ind= ismember(data.Session, sesToPlot);

data2= data(ind, :);

%-stack() to make inactive/active NPtype a variable
data2= stack(data2, {'ActiveNP', 'InactiveNP'}, 'IndexVariableName', 'typeNP', 'NewDataVariableName', 'countNP');


%--Calculate Log scale NPs

data2.logNP = log(data2.countNP);
% 
% %-** Alternatively, Calculate Log(x+1) to avoid invalid values
% data2.logNP = log(data2.countNP);


% % if countNP is == 0, log returns -inf. Make these nan
% data2(data2.logNP==-inf, "logNP")= table(nan);

% if countNP is == 0, log returns -inf. Make these 0!
data2(data2.logNP==-inf, "logNP")= table(0);

dataFig6C= [];
dataFig6C= data2;

% - Plot raw NP count
y= 'countNP';

% % Plot log NP count
% y= 'logNP';


%- Bar of btwn subj means (group = [])
group= []; %var by which to group

% d(1,2)=gramm('x',dataFig6C.Projection,'y',dataFig6C.logNP,'color',dataFig6C.typeNP, 'group', group)
d(1,2)=gramm('x',dataFig6C.typeNP,'y',dataFig6C.(y),'color',dataFig6C.typeNP, 'group', group)

% d(1,2).facet_grid(dataFig6C.trainPhase, []);
d(1,2).facet_grid([], dataFig6C.Projection);


d(1,2).stat_summary('type','sem', 'geom',{'bar'}, 'dodge', dodge, 'width', width) 
d(1,2).set_color_options('map',cmapGrand); 

% d(1,2).set_names('x','Nosepoke Side','y','Log(Number of Nose Pokes)','color','Nosepoke Side')
d(1,2).set_names('x','Projection','y',y,'color','Nosepoke Side', 'column', '');

figTitle= 'B) Final OGside session';

% d(1,2).set_title(figTitle)

%set text options- do before first draw() call so applied on subsequent updates()
d(1,2).set_text_options(text_options_DefaultStyle{:}); 
d(1,2).no_legend(); %prevent legend duplicates if you like

% d(1,2).set_parent(p2);

d(1,2).axe_property( 'YLim', ylimLP);
d(1,2).axe_property( 'YTick', yTickLP);


d(1,2).draw()

%- Draw lines between individual subject points (group= subject, color=[]);
group= dataFig6C.Subject;
d(1,2).update('x', dataFig6C.typeNP,'y',dataFig6C.(y),'color',[], 'group', group)

% d(1,1).stat_summary('geom',{'line'});
d(1,2).geom_line('alpha',0.3, 'dodge', dodge);
d(1,2).set_line_options('base_size',linewidthSubj);

d(1,2).set_color_options('chroma', 0); %black lines connecting points
d(1,2).no_legend(); %prevent legend duplicates if you like

d(1,2).draw()

%- Update with point of individual subj points (group= subject)
group= dataFig6C.Subject;
d(1,2).update('x', dataFig6C.typeNP,'y',dataFig6C.(y),'color',dataFig6C.typeNP, 'group', group)
d(1,2).stat_summary('type','sem','geom',{'point'}, 'dodge', dodge)%,'bar' 'black_errorbar'});

d(1,2).set_color_options('map',cmapSubj); 
d(1,2).no_legend(); %prevent legend duplicates if you like

d(1,2).draw();

%- update error bar on top
group=[];
d(1,2).update('x',dataFig6C.typeNP,'y',dataFig6C.(y),'color',dataFig6C.typeNP, 'group', group);

d(1,2).stat_summary('type','sem', 'geom',{'black_errorbar'}, 'dodge', dodge, 'width', width);
d(1,2).no_legend(); %prevent legend duplicates if you like

% d(1,2).draw();


%-- Row 2 col 2- last day reversal side 

cmapSubj= cmapBlueGraySubj;
cmapGrand= cmapBlueGrayGrand;

%subset data
data= ICSStable;
% 
% sesToPlot= 5; %plot last day before reversal
% 
% ind= [];
% ind= ICSStable.Session== sesToPlot;

% subset last day prior to reversal; and last day of reversal (for AUCs)
sesToPlot= [];

sesToPlot= [8];

ind= ismember(data.Session, sesToPlot);

data2= data(ind, :);

%-stack() to make inactive/active NPtype a variable
data2= stack(data2, {'ActiveNP', 'InactiveNP'}, 'IndexVariableName', 'typeNP', 'NewDataVariableName', 'countNP');


%--Calculate Log scale NPs

data2.logNP = log(data2.countNP);
% 
% % if countNP is == 0, log returns -inf. Make these nan
% data2(data2.logNP==-inf, "logNP")= table(nan);

% if countNP is == 0, log returns -inf. Make these 0!
data2(data2.logNP==-inf, "logNP")= table(0);

dataFig6D= [];
dataFig6D= data2;


% Plot Raw NP count
y= 'countNP';

% % Plot log NP count
% y= 'logNP';

%- Bar of btwn subj means (group = [])
group= []; %var by which to group

% d(2,2)=gramm('x',data2.Projection,'y',data2.logNP,'color',dataFig6D.typeNP, 'group', group)
d(2,2)=gramm('x',dataFig6D.typeNP,'y',dataFig6D.(y),'color',dataFig6D.typeNP, 'group', group)

% d(2,2).facet_grid(dataFig6D.trainPhase, []);
% d(2,2).facet_grid([], dataFig6D.Projection);

% d(2,2).facet_grid([], dataFig6D.Projection);
d(2,2).facet_grid([], dataFig6D.Projection, 'scale','independent');


d(2,2).stat_summary('type','sem', 'geom',{'bar'}, 'dodge', dodge, 'width', width) 
d(2,2).set_color_options('map',cmapGrand); 

% d(2,2).set_names('x','Nosepoke Side','y','Log(Number of Nose Pokes)','color','Nosepoke Side')
d(2,2).set_names('x','Projection','y',y,'color','Nosepoke Side', 'column', '')

figTitle= 'E) Final Reversal session';

% d(2,2).set_title(figTitle)

%set text options- do before first draw() call so applied on subsequent updates()
d(2,2).set_text_options(text_options_DefaultStyle{:}); 
d(2,2).no_legend(); %prevent legend duplicates if you like

% d(2,2).set_parent(p2);
d(2,2).axe_property( 'YLim', ylimLP);
d(2,2).axe_property( 'YTick', yTickLP);

d(2,2).draw()

%- Draw lines between individual subject points (group= subject, color=[]);
group= dataFig6D.Subject;
d(2,2).update('x', dataFig6D.typeNP,'y',dataFig6D.(y),'color',[], 'group', group)

% d(1,1).stat_summary('geom',{'line'});
d(2,2).geom_line('alpha',0.3, 'dodge', dodge);
d(2,2).set_line_options('base_size',linewidthSubj);

d(2,2).set_color_options('chroma', 0); %black lines connecting points
d(2,2).no_legend(); %prevent legend duplicates if you like

d(2,2).draw()

%- Update with point of individual subj points (group= subject)
group= dataFig6D.Subject;
d(2,2).update('x', dataFig6D.typeNP,'y',dataFig6D.(y),'color',dataFig6D.typeNP, 'group', group)
d(2,2).stat_summary('type','sem','geom',{'point'}, 'dodge', dodge)%,'bar' 'black_errorbar'});

d(2,2).set_color_options('map',cmapSubj); 
d(2,2).no_legend(); %prevent legend duplicates if you like

d(2,2).draw();

%- update error bar on top
group=[];
d(2,2).update('x',dataFig6D.typeNP,'y',dataFig6D.(y),'color',dataFig6D.typeNP, 'group', group);

d(2,2).stat_summary('type','sem', 'geom',{'black_errorbar'}, 'dodge', dodge, 'width', width);
d(2,2).no_legend(); %prevent legend duplicates if you like

% d(1,2).draw();

%%%---------- Column 3 
%-- Row 1 col 3- last day OG side Active Proportion


%-- Row 2 col 3- last day reversal side Active Proportion
%cmap for Projection comparisons
cmapGrand= 'brewer_dark';
cmapSubj= 'brewer2'; 

%subset data
data= ICSStable;
% 
% sesToPlot= 5; %plot last day before reversal
% 
% ind= [];
% ind= ICSStable.Session== sesToPlot;

% subset last day prior to reversal; and last day of reversal (for AUCs)
sesToPlot= [];

sesToPlot= [5];

ind= ismember(data.Session, sesToPlot);

data2= data(ind, :);

% %-stack() to make inactive/active NPtype a variable
% data2= stack(data2, {'ActiveNP', 'InactiveNP'}, 'IndexVariableName', 'typeNP', 'NewDataVariableName', 'countNP');


% %--Calculate Log scale NPs
% 
% data2.logNP = log(data2.countNP);
% % 
% % % if countNP is == 0, log returns -inf. Make these nan
% % data2(data2.logNP==-inf, "logNP")= table(nan);
% 
% % if countNP is == 0, log returns -inf. Make these 0!
% data2(data2.logNP==-inf, "logNP")= table(0);

dataFig6H= [];
dataFig6H= data2;

y='npActiveProportion';

% y='npDelta';


%- Bar of btwn subj means (group = [])
group= []; %var by which to group

% d(2,2)=gramm('x',data2.Projection,'y',data2.logNP,'color',dataFig6D.typeNP, 'group', group)
d(1,3)=gramm('x',dataFig6H.Projection,'y',dataFig6H.(y),'color',dataFig6H.Projection, 'group', group)

% d(1,3).facet_grid(dataFig6D.trainPhase, []);
% d(1,3).facet_grid([], dataFig6F.Projection);


d(1,3).stat_summary('type','sem', 'geom',{'bar'}, 'dodge', dodge, 'width', width) 
d(1,3).set_color_options('map',cmapGrand); 

% d(1,3).set_names('x','Nosepoke Side','y','Log(Number of Nose Pokes)','color','Nosepoke Side')
d(1,3).set_names('x','Projection','y',y,'color','Nosepoke Side', 'column', '')

figTitle= 'C) Final OGside session ';

% d(1,3).set_title(figTitle)

%set text options- do before first draw() call so applied on subsequent updates()
d(1,3).set_text_options(text_options_DefaultStyle{:}); 
d(1,3).no_legend(); %prevent legend duplicates if you like

% d(1,3).set_parent(p2);


d(1,3).draw()

%- Draw lines between individual subject points (group= subject, color=[]);
group= dataFig6H.Subject;
d(1,3).update('x', dataFig6H.Projection,'y',dataFig6H.(y),'color',[], 'group', group)

% d(1,1).stat_summary('geom',{'line'});
d(1,3).geom_line('alpha',0.3, 'dodge', dodge);
d(1,3).set_line_options('base_size',linewidthSubj);

d(1,3).set_color_options('chroma', 0); %black lines connecting points
d(1,3).no_legend(); %prevent legend duplicates if you like

d(1,3).draw()

%- Update with point of individual subj points (group= subject)
group= dataFig6H.Subject;
d(1,3).update('x', dataFig6H.Projection,'y',dataFig6H.(y),'color',dataFig6H.Projection, 'group', group)
d(1,3).stat_summary('type','sem','geom',{'point'}, 'dodge', dodge)%,'bar' 'black_errorbar'});

d(1,3).set_color_options('map',cmapSubj); 
d(1,3).no_legend(); %prevent legend duplicates if you like

d(1,3).draw();

%- update error bar on top
group=[];
d(1,3).update('x',dataFig6H.Projection,'y',dataFig6H.(y),'color',dataFig6H.Projection, 'group', group);

d(1,3).stat_summary('type','sem', 'geom',{'black_errorbar'}, 'dodge', dodge, 'width', width);
d(1,3).no_legend(); %prevent legend duplicates if you like

d(1,3).geom_hline('yintercept',0.5, 'style', 'k--', 'linewidth', linewidthReference); %overlay t=0


%-- Row 2 col 3- last day reversal side Active Proportion
%cmap for Projection comparisons
cmapGrand= 'brewer_dark';
cmapSubj= 'brewer2'; 

%subset data
data= ICSStable;
% 
% sesToPlot= 5; %plot last day before reversal
% 
% ind= [];
% ind= ICSStable.Session== sesToPlot;

% subset last day prior to reversal; and last day of reversal (for AUCs)
sesToPlot= [];

sesToPlot= [8];

ind= ismember(data.Session, sesToPlot);

data2= data(ind, :);

% %-stack() to make inactive/active NPtype a variable
% data2= stack(data2, {'ActiveNP', 'InactiveNP'}, 'IndexVariableName', 'typeNP', 'NewDataVariableName', 'countNP');


% %--Calculate Log scale NPs
% 
% data2.logNP = log(data2.countNP);
% % 
% % % if countNP is == 0, log returns -inf. Make these nan
% % data2(data2.logNP==-inf, "logNP")= table(nan);
% 
% % if countNP is == 0, log returns -inf. Make these 0!
% data2(data2.logNP==-inf, "logNP")= table(0);

dataFig6F= [];
dataFig6F= data2;

y='npActiveProportion';

% y='npDelta';

%- Bar of btwn subj means (group = [])
group= []; %var by which to group

% d(2,2)=gramm('x',data2.Projection,'y',data2.logNP,'color',dataFig6D.typeNP, 'group', group)
d(2,3)=gramm('x',dataFig6F.Projection,'y',dataFig6F.(y),'color',dataFig6F.Projection, 'group', group)

% d(2,3).facet_grid(dataFig6D.trainPhase, []);
% d(2,3).facet_grid([], dataFig6F.Projection);


d(2,3).stat_summary('type','sem', 'geom',{'bar'}, 'dodge', dodge, 'width', width) 
d(2,3).set_color_options('map',cmapGrand); 

% d(2,3).set_names('x','Nosepoke Side','y','Log(Number of Nose Pokes)','color','Nosepoke Side')
d(2,3).set_names('x','Projection','y',y,'color','Nosepoke Side')

figTitle= 'F) Final Reversal session';

% d(2,3).set_title(figTitle)

%set text options- do before first draw() call so applied on subsequent updates()
d(2,3).set_text_options(text_options_DefaultStyle{:}); 
d(2,3).no_legend(); %prevent legend duplicates if you like

% d(2,3).set_parent(p2);
d(2,3).axe_property( 'YLim', [0,1]);
d(2,3).axe_property( 'YTick', [0:0.1:1]);


d(2,3).draw()

%- Draw lines between individual subject points (group= subject, color=[]);
group= dataFig6F.Subject;
d(2,3).update('x', dataFig6F.Projection,'y',dataFig6F.(y),'color',[], 'group', group)

% d(1,1).stat_summary('geom',{'line'});
d(2,3).geom_line('alpha',0.3, 'dodge', dodge);
d(2,3).set_line_options('base_size',linewidthSubj);

d(2,3).set_color_options('chroma', 0); %black lines connecting points
d(2,3).no_legend(); %prevent legend duplicates if you like

d(2,3).draw()

%- Update with point of individual subj points (group= subject)
group= dataFig6F.Subject;
d(2,3).update('x', dataFig6F.Projection,'y',dataFig6F.(y),'color',dataFig6F.Projection, 'group', group)
d(2,3).stat_summary('type','sem','geom',{'point'}, 'dodge', dodge)%,'bar' 'black_errorbar'});

d(2,3).set_color_options('map',cmapSubj); 
d(2,3).no_legend(); %prevent legend duplicates if you like

d(2,3).draw();

%- update error bar on top
group=[];
d(2,3).update('x',dataFig6F.Projection,'y',dataFig6F.(y),'color',dataFig6F.Projection, 'group', group);

d(2,3).stat_summary('type','sem', 'geom',{'black_errorbar'}, 'dodge', dodge, 'width', width);
d(2,3).no_legend(); %prevent legend duplicates if you like

d(2,3).geom_hline('yintercept',0.5, 'style', 'k--', 'linewidth', linewidthReference); %overlay t=0


% %---------- Col 4? Time in Port
% 
% %-- Row 2 col 4- last day reversal side
% 
% cmapSubj= cmapBlueGraySubj;
% cmapGrand= cmapBlueGrayGrand;
% 
% %subset data
% data= ICSStable;
% % 
% % sesToPlot= 5; %plot last day before reversal
% % 
% % ind= [];
% % ind= ICSStable.Session== sesToPlot;
% 
% % subset last day prior to reversal; and last day of reversal (for AUCs)
% sesToPlot= [];
% 
% sesToPlot= [8];
% 
% ind= ismember(data.Session, sesToPlot);
% 
% data2= data(ind, :);
% 
% %-stack() to make inactive/active NPtype a variable
% data2= stack(data2, {'TotalLengthActiveNP', 'TotalLengthInactiveNP'}, 'IndexVariableName', 'typeNP', 'NewDataVariableName', 'timeInNP');
% 
% 
% dataFig6G= [];
% dataFig6G= data2;
% 
% % Plot log NP count
% y= 'timeInNP';
% 
% %- Bar of btwn subj means (group = [])
% group= []; %var by which to group
% 
% % d(2,2)=gramm('x',data2.Projection,'y',data2.logNP,'color',dataFig6D.typeNP, 'group', group)
% d(2,4)=gramm('x',dataFig6G.typeNP,'y',dataFig6G.(y),'color',dataFig6G.typeNP, 'group', group)
% 
% % d(2,4).facet_grid(dataFig6D.trainPhase, []);
% d(2,4).facet_grid([], dataFig6G.Projection);
% 
% 
% d(2,4).stat_summary('type','sem', 'geom',{'bar'}, 'dodge', dodge, 'width', width) 
% d(2,4).set_color_options('map',cmapGrand); 
% 
% % d(2,4).set_names('x','Nosepoke Side','y','Log(Number of Nose Pokes)','color','Nosepoke Side')
% d(2,4).set_names('x','Projection','y',y,'color','Nosepoke Side', 'column', '')
% 
% figTitle= 'E) Final Reversal session';
% 
% d(2,4).set_title(figTitle)
% 
% %set text options- do before first draw() call so applied on subsequent updates()
% d(2,4).set_text_options(text_options_DefaultStyle{:}); 
% d(2,4).no_legend(); %prevent legend duplicates if you like
% 
% % d(2,4).set_parent(p2);
% 
% 
% d(2,4).draw()
% 
% %- Draw lines between individual subject points (group= subject, color=[]);
% group= dataFig6G.Subject;
% d(2,4).update('x', dataFig6G.typeNP,'y',dataFig6G.(y),'color',[], 'group', group)
% 
% % d(2,4).stat_summary('geom',{'line'});
% d(2,4).geom_line('alpha',0.3, 'dodge', dodge);
% d(2,4).set_line_options('base_size',linewidthSubj);
% 
% d(2,4).set_color_options('chroma', 0); %black lines connecting points
% d(2,4).no_legend(); %prevent legend duplicates if you like
% 
% d(2,4).draw()
% 
% %- Update with point of individual subj points (group= subject)
% group= dataFig6G.Subject;
% d(2,4).update('x', dataFig6G.typeNP,'y',dataFig6G.(y),'color',dataFig6G.typeNP, 'group', group)
% d(2,4).stat_summary('type','sem','geom',{'point'}, 'dodge', dodge)%,'bar' 'black_errorbar'});
% 
% d(2,4).set_color_options('map',cmapSubj); 
% d(2,4).no_legend(); %prevent legend duplicates if you like
% 
% d(2,4).draw();
% 
% %- update error bar on top
% group=[];
% d(2,4).update('x',dataFig6G.typeNP,'y',dataFig6G.(y),'color',dataFig6G.typeNP, 'group', group);
% 
% d(2,4).stat_summary('type','sem', 'geom',{'black_errorbar'}, 'dodge', dodge, 'width', width);
% d(2,4).no_legend(); %prevent legend duplicates if you like
% 
% % d(1,2).draw();
% 
% %-- Row 2 col 4- last day reversal side
% 
% cmapSubj= cmapBlueGraySubj;
% cmapGrand= cmapBlueGrayGrand;
% 
% %subset data
% data= ICSStable;
% % 
% % sesToPlot= 5; %plot last day before reversal
% % 
% % ind= [];
% % ind= ICSStable.Session== sesToPlot;
% 
% % subset last day prior to reversal; and last day of reversal (for AUCs)
% sesToPlot= [];
% 
% sesToPlot= [5];
% 
% ind= ismember(data.Session, sesToPlot);
% 
% data2= data(ind, :);
% 
% %-stack() to make inactive/active NPtype a variable
% data2= stack(data2, {'TotalLengthActiveNP', 'TotalLengthInactiveNP'}, 'IndexVariableName', 'typeNP', 'NewDataVariableName', 'timeInNP');
% 
% 
% dataFig6H= [];
% dataFig6H= data2;
% 
% % Plot log NP count
% y= 'timeInNP';
% 
% %- Bar of btwn subj means (group = [])
% group= []; %var by which to group
% 
% % d(2,2)=gramm('x',data2.Projection,'y',data2.logNP,'color',dataFig6D.typeNP, 'group', group)
% d(1,4)=gramm('x',dataFig6H.typeNP,'y',dataFig6H.(y),'color',dataFig6H.typeNP, 'group', group)
% 
% % d(1,4).facet_grid(dataFig6D.trainPhase, []);
% d(1,4).facet_grid([], dataFig6H.Projection);
% 
% 
% d(1,4).stat_summary('type','sem', 'geom',{'bar'}, 'dodge', dodge, 'width', width) 
% d(1,4).set_color_options('map',cmapGrand); 
% 
% % d(1,4).set_names('x','Nosepoke Side','y','Log(Number of Nose Pokes)','color','Nosepoke Side')
% d(1,4).set_names('x','Projection','y',y,'color','Nosepoke Side', 'column', '')
% 
% figTitle= 'H) Final OGSide session';
% 
% d(1,4).set_title(figTitle)
% 
% %set text options- do before first draw() call so applied on subsequent updates()
% d(1,4).set_text_options(text_options_DefaultStyle{:}); 
% d(1,4).no_legend(); %prevent legend duplicates if you like
% 
% % d(1,4).set_parent(p2);
% 
% 
% d(1,4).draw()
% 
% %- Draw lines between individual subject points (group= subject, color=[]);
% group= dataFig6G.Subject;
% d(1,4).update('x', dataFig6H.typeNP,'y',dataFig6H.(y),'color',[], 'group', group)
% 
% % d(1,4).stat_summary('geom',{'line'});
% d(1,4).geom_line('alpha',0.3, 'dodge', dodge);
% d(1,4).set_line_options('base_size',linewidthSubj);
% 
% d(1,4).set_color_options('chroma', 0); %black lines connecting points
% d(1,4).no_legend(); %prevent legend duplicates if you like
% 
% d(1,4).draw()
% 
% %- Update with point of individual subj points (group= subject)
% group= dataFig6H.Subject;
% d(1,4).update('x', dataFig6H.typeNP,'y',dataFig6H.(y),'color',dataFig6H.typeNP, 'group', group)
% d(1,4).stat_summary('type','sem','geom',{'point'}, 'dodge', dodge)%,'bar' 'black_errorbar'});
% 
% d(1,4).set_color_options('map',cmapSubj); 
% d(1,4).no_legend(); %prevent legend duplicates if you like
% 
% d(1,4).draw();
% 
% %- update error bar on top
% group=[];
% d(1,4).update('x',dataFig6H.typeNP,'y',dataFig6H.(y),'color',dataFig6H.typeNP, 'group', group);
% 
% d(1,4).stat_summary('type','sem', 'geom',{'black_errorbar'}, 'dodge', dodge, 'width', width);
% d(1,4).no_legend(); %prevent legend duplicates if you like
% 
% 


%-- FINAL DRAW CALL
d.draw()

%% -- Breakaway plots of high count NP (in VTA group >500)
figure; clear d;

ylimLPfull= [500,1300];
    
yTickLPfull= [0:50:max(ylimLPfull)]; % ticks every 


%-- Row 1 col 2- last day OG side 

cmapSubj= cmapBlueGraySubj;
cmapGrand= cmapBlueGrayGrand;

%subset data
data= ICSStable;
% 
% sesToPlot= 5; %plot last da y before reversal
% 
% ind= [];
% ind= ICSStable.Session== sesToPlot;

% subset last day prior to reversal; and last day of reversal (for AUCs)
sesToPlot= [];

sesToPlot= [5];

ind= ismember(data.Session, sesToPlot);

data2= data(ind, :);

%-stack() to make inactive/active NPtype a variable
data2= stack(data2, {'ActiveNP', 'InactiveNP'}, 'IndexVariableName', 'typeNP', 'NewDataVariableName', 'countNP');


%--Calculate Log scale NPs

data2.logNP = log(data2.countNP);
% 
% %-** Alternatively, Calculate Log(x+1) to avoid invalid values
% data2.logNP = log(data2.countNP);


% % if countNP is == 0, log returns -inf. Make these nan
% data2(data2.logNP==-inf, "logNP")= table(nan);

% if countNP is == 0, log returns -inf. Make these 0!
data2(data2.logNP==-inf, "logNP")= table(0);

dataFig6C= [];
dataFig6C= data2;

% - Plot raw NP count
y= 'countNP';

% % Plot log NP count
% y= 'logNP';


%- Bar of btwn subj means (group = [])
group= []; %var by which to group

% d(1,2)=gramm('x',dataFig6C.Projection,'y',dataFig6C.logNP,'color',dataFig6C.typeNP, 'group', group)
d(1,2)=gramm('x',dataFig6C.typeNP,'y',dataFig6C.(y),'color',dataFig6C.typeNP, 'group', group)

% d(1,2).facet_grid(dataFig6C.trainPhase, []);
d(1,2).facet_grid([], dataFig6C.Projection);


d(1,2).stat_summary('type','sem', 'geom',{'bar'}, 'dodge', dodge, 'width', width) 
d(1,2).set_color_options('map',cmapGrand); 

% d(1,2).set_names('x','Nosepoke Side','y','Log(Number of Nose Pokes)','color','Nosepoke Side')
d(1,2).set_names('x','Projection','y',y,'color','Nosepoke Side', 'column', '');

figTitle= 'B) Final OGside session';

% d(1,2).set_title(figTitle)

%set text options- do before first draw() call so applied on subsequent updates()
d(1,2).set_text_options(text_options_DefaultStyle{:}); 
d(1,2).no_legend(); %prevent legend duplicates if you like

% d(1,2).set_parent(p2);

d(1,2).axe_property( 'YLim', ylimLPfull);
d(1,2).axe_property( 'YTick', yTickLPfull);


d(1,2).draw()

%- Draw lines between individual subject points (group= subject, color=[]);
group= dataFig6C.Subject;
d(1,2).update('x', dataFig6C.typeNP,'y',dataFig6C.(y),'color',[], 'group', group)

% d(1,1).stat_summary('geom',{'line'});
d(1,2).geom_line('alpha',0.3, 'dodge', dodge);
d(1,2).set_line_options('base_size',linewidthSubj);

d(1,2).set_color_options('chroma', 0); %black lines connecting points
d(1,2).no_legend(); %prevent legend duplicates if you like

d(1,2).draw()

%- Update with point of individual subj points (group= subject)
group= dataFig6C.Subject;
d(1,2).update('x', dataFig6C.typeNP,'y',dataFig6C.(y),'color',dataFig6C.typeNP, 'group', group)
d(1,2).stat_summary('type','sem','geom',{'point'}, 'dodge', dodge)%,'bar' 'black_errorbar'});

d(1,2).set_color_options('map',cmapSubj); 
d(1,2).no_legend(); %prevent legend duplicates if you like

d(1,2).draw();

%- update error bar on top
group=[];
d(1,2).update('x',dataFig6C.typeNP,'y',dataFig6C.(y),'color',dataFig6C.typeNP, 'group', group);

d(1,2).stat_summary('type','sem', 'geom',{'black_errorbar'}, 'dodge', dodge, 'width', width);
d(1,2).no_legend(); %prevent legend duplicates if you like

% d(1,2).draw();

%-- Row 2 col 2- last day reversal side 

cmapSubj= cmapBlueGraySubj;
cmapGrand= cmapBlueGrayGrand;

%subset data
data= ICSStable;
% 
% sesToPlot= 5; %plot last day before reversal
% 
% ind= [];
% ind= ICSStable.Session== sesToPlot;

% subset last day prior to reversal; and last day of reversal (for AUCs)
sesToPlot= [];

sesToPlot= [8];

ind= ismember(data.Session, sesToPlot);

data2= data(ind, :);

%-stack() to make inactive/active NPtype a variable
data2= stack(data2, {'ActiveNP', 'InactiveNP'}, 'IndexVariableName', 'typeNP', 'NewDataVariableName', 'countNP');


%--Calculate Log scale NPs

data2.logNP = log(data2.countNP);
% 
% % if countNP is == 0, log returns -inf. Make these nan
% data2(data2.logNP==-inf, "logNP")= table(nan);

% if countNP is == 0, log returns -inf. Make these 0!
data2(data2.logNP==-inf, "logNP")= table(0);

dataFig6D= [];
dataFig6D= data2;


% Plot Raw NP count
y= 'countNP';

% % Plot log NP count
% y= 'logNP';

%- Bar of btwn subj means (group = [])
group= []; %var by which to group

% d(2,2)=gramm('x',data2.Projection,'y',data2.logNP,'color',dataFig6D.typeNP, 'group', group)
d(2,2)=gramm('x',dataFig6D.typeNP,'y',dataFig6D.(y),'color',dataFig6D.typeNP, 'group', group)

% d(2,2).facet_grid(dataFig6D.trainPhase, []);
% d(2,2).facet_grid([], dataFig6D.Projection);

% d(2,2).facet_grid([], dataFig6D.Projection);
d(2,2).facet_grid([], dataFig6D.Projection, 'scale','independent');


d(2,2).stat_summary('type','sem', 'geom',{'bar'}, 'dodge', dodge, 'width', width) 
d(2,2).set_color_options('map',cmapGrand); 

% d(2,2).set_names('x','Nosepoke Side','y','Log(Number of Nose Pokes)','color','Nosepoke Side')
d(2,2).set_names('x','Projection','y',y,'color','Nosepoke Side', 'column', '')

figTitle= 'E) Final Reversal session';

% d(2,2).set_title(figTitle)

%set text options- do before first draw() call so applied on subsequent updates()
d(2,2).set_text_options(text_options_DefaultStyle{:}); 
d(2,2).no_legend(); %prevent legend duplicates if you like

% d(2,2).set_parent(p2);
d(2,2).axe_property( 'YLim', ylimLPfull);
d(2,2).axe_property( 'YTick', yTickLPfull);

d(2,2).draw()

%- Draw lines between individual subject points (group= subject, color=[]);
group= dataFig6D.Subject;
d(2,2).update('x', dataFig6D.typeNP,'y',dataFig6D.(y),'color',[], 'group', group)

% d(1,1).stat_summary('geom',{'line'});
d(2,2).geom_line('alpha',0.3, 'dodge', dodge);
d(2,2).set_line_options('base_size',linewidthSubj);

d(2,2).set_color_options('chroma', 0); %black lines connecting points
d(2,2).no_legend(); %prevent legend duplicates if you like

d(2,2).draw()

%- Update with point of individual subj points (group= subject)
group= dataFig6D.Subject;
d(2,2).update('x', dataFig6D.typeNP,'y',dataFig6D.(y),'color',dataFig6D.typeNP, 'group', group)
d(2,2).stat_summary('type','sem','geom',{'point'}, 'dodge', dodge)%,'bar' 'black_errorbar'});

d(2,2).set_color_options('map',cmapSubj); 
d(2,2).no_legend(); %prevent legend duplicates if you like

d(2,2).draw();

%- update error bar on top
group=[];
d(2,2).update('x',dataFig6D.typeNP,'y',dataFig6D.(y),'color',dataFig6D.typeNP, 'group', group);

d(2,2).stat_summary('type','sem', 'geom',{'black_errorbar'}, 'dodge', dodge, 'width', width);
d(2,2).no_legend(); %prevent legend duplicates if you like


%-- keeping empty subplots to match with actual fig
d(1,3)= gramm('x',dataFig6D.typeNP,'y',dataFig6D.(y),'color',dataFig6D.typeNP, 'group', group);
d(1,3).no_legend();
d(2,3)= gramm('x',dataFig6D.typeNP,'y',dataFig6D.(y),'color',dataFig6D.typeNP, 'group', group);
d(2,3).no_legend();


%---Final draw call
d.draw();

%% EXPORT DATA FOR STATS ANALYSIS IN PYTHON/R

%subset data
data= ICSStable;

data2= data;%(ind, :);

%-stack() to make inactive/active NPtype a variable
data2= stack(data2, {'ActiveNP', 'InactiveNP'}, 'IndexVariableName', 'typeNP', 'NewDataVariableName', 'countNP');

%--Calculate Log scale NPs
data2.logNP = log(data2.countNP);
% if countNP is == 0, log returns -inf. Make these 0!
data2(data2.logNP==-inf, "logNP")= table(0);

%export as parquet for python
dataTableFig6= data2;

%remove columns not needed
dataTableFig6= removevars(dataTableFig6,{'Experiment'});

% %changing dtypes, parquet doesn't like cells
dataTableFig6.Box= [dataTableFig6.Box{:}]';

% save table as Parquet file
% % https://www.quora.com/When-should-I-use-parquet-file-to-store-data-instead-of-csv

parquetwrite(strcat('vp-vta-fp_stats_fig6Table'), dataTableFig6);



