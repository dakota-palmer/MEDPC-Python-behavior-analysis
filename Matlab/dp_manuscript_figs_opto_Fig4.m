%% Load Opto DS task data

load("C:\Users\Dakota\Documents\GitHub\DS-Training\Matlab\_output\_DS_task_stimDay\VP-OPTO-DStaskTest-31-Jan-2023-stimTable.mat");

data=[];
data= stimTable;

%% Note that prior script excluded subjects based on behavioral criteria


%% EXCLUDE data 
%- Based on virusType
include= [];
include= 'stimulation';

ind=[];
ind= strcmp(data.virusType, include);

data= data(ind, :);

%- Based on laserDur (StimLength)
% exclude the 20s duration (post laser manipulation session)
exclude=[];
exclude= [20];

ind= [];
ind= ismember(data.StimLength,exclude);

data= data(~ind, :);

%- Based on projection target
exclude= [];
exclude= 'PFC';

ind=[];
ind= strcmp(data.Projection, exclude);

data= data(~ind,:);

%- Based on Histology
ind= [];
ind= data.Expression==1;

data= data(ind,:);

%-overwrite stimTable
stimTable= data;


%% Make fig w UIpanels

%% set defaults

% for JNeuro, 1.5 Col max width = 11.6cm (~438 pixels); 2 col max width = 17.6cm (~665 pixels)
figSize1= [100, 100, 430, 600];

figSize2= [100, 100, 650, 600];

%make appropriate size
figSize= figSize2

% text_options_DefaultStyle

% %- set default axes limits between plots for consistency
% %default lims for traces 
% ylimTraces= [-2,5];
% xlimTraces= [-2,10];
% 
% %default lims for AUC plots
% %note xlims best to calculate dynamically for bar plots based on num x categories
% ylimAUC= [-1,16];
%% Scrap copying approach, use uipanels and draw one at a time

%% Figure 2

%for this simply not making figures between gramm objects (dont call
%figure()) then copy to one fig in positions I want 

clear i i2 i1 fig2
close all



% Create the uipanels, the 'Position' property is what will allow to create different sizes (it works the same as the corresponding argument in subplot() )


% Subplots : 2 Rows of 5
    % 1 row of 2 %normalized units of size (% of figure)
    
    
%%
% Initialize a figure with Drawable Area padding appropriately
% f = figure('Position',[100 100 1200 800])

% make figure of desired final size
f = figure('Position',figSize)



% padFigure= 0.05;
% figWidth= 1200;
% figHeight= 800;
% f = figure('Position',[1-padFigure, 1-padFigure, figWidth, figHeight])


% - Debugging/placement - With Visualization Borders / colors to help 
    % 'Position' Units are pixels (distance from left, distance from bottom, width, height)
    %but can use 'Units' 'Normalized'
    % e.g. so [.9,.1, .3, .4] is 90% from bottom, 10% from left with width of 30% and height of 40% 

    % Make width/height dependent on Position     
    panelPos= [.01, .8, .95, .3];
    lPos= panelPos(1);
    bPos= panelPos(2);
    w= panelPos(3);
    h= panelPos(4);
    
    %make half-width
    w= w / 2; %- padWidth;

    
    %amount of padding for uipanels
    padPanel= 0.0025;
    
%todo- Adjust width,height based on the whole figure size? assumes equal
%size though so not useful really

%   Full-Width panel: adjust width and height dependent on position    
    w2= 1- panelPos(1);
    h2= 1-panelPos(2);
    
%     p1 = uipanel('Position',[lPos bPos w2 h2],'Parent',f,'BackgroundColor',[1 1 1],'BorderType','etchedin')

%-Adjust lPos,bPos position based on width and height... so padding is good
   %e.g. Full-Width panel:
    lPos= 1-padPanel-w; %- lPos;
    bPos= 1-h; %h- bPos;
    
%todo - Manually Refine position... alter values
% padWidth= 0.0025; %padding from width of Figure

%note that having issues with padding on left side of figure... greater than right side padWidth > 0.005? 
% seems to be feature of figures
padWidth= 0.005; %padding from left side of figure

padHeight= 0.001; %todo- padding from bottom of figure

padPanel= 0.0025; %padding between other uiPanels

    % Panel A- Top row, full width
    w= 1-padWidth;
    
        %make half-width
    w= w / 2; %- padWidth;
    
        %dynamically adjust bPos based on padHeight and height desired
    h= 0.49; %CHANGE HEIGHT

    bPos= 1- h - padHeight;  
    
        %iterations here
%     p1 = uipanel('Position',[padWidth, .7, .95, .3],'Units','Normalized','Parent',f,'BackgroundColor',[1 1 1],'BorderType','etchedout')
%     p1 = uipanel('Position',[padWidth, .7, w, .30],'Units','Normalized','Parent',f,'BackgroundColor',[1 1 1],'BorderType','etchedout')
%     p1 = uipanel('Position',[padWidth, bPos, w, .32],'Units','Normalized','Parent',f,'BackgroundColor',[1 1 1],'BorderType','etchedout')
    p1 = uipanel('Position',[padWidth, bPos, w, h],'Units','Normalized','Parent',f,'BackgroundColor',[1 1 1],'BorderType','etchedout')

    
    %Position subsequent panels based on prior panels' Position
    
    % Panel B-  2nd row, 2nd half 
    lPos= (w + p1.Position(1) - padPanel + padWidth);
    
    p2 = uipanel('Position',[lPos+padWidth, bPos, w, h],'Units','Normalized','Parent',f,'BackgroundColor',[1 1 1],'BorderType','etchedout')

    
    % Panel C- 2nd row, 1st half width
        %... height of row 1 + 2 + padding
    % redeclare height now for this panel
    h= .49;
    bPos= (p2.Position(2)) - (h) - padPanel;


        %... width of A/B
    w= p2.Position(3)
        
%     p3= uipanel('Position',[padWidth, bPos, w, .32],'Units','Normalized','Parent',f,'BackgroundColor',[1 1 1],'BorderType','etchedout')
    p3= uipanel('Position',[padWidth, bPos, w, h],'Units','Normalized','Parent',f,'BackgroundColor',[1 1 1],'BorderType','etchedout')
        

    % Panel D- 3rd row, 2nd half width
    lPos= (w + p3.Position(1) - padPanel + padWidth);

    p4= uipanel('Position',[lPos, bPos, w, h],'Units','Normalized','Parent',f,'BackgroundColor',[1 1 1],'BorderType','etchedout')

  
%% Figure 4

%% aesthetics

% bar widths
dodge= 	.6; %if dodge constant between point and bar, will align correctly
width= .58;

% y lims

ylimLatency= [0,10];

yTickLatency= [0:2:10] % ticks every 2s

ylimProb= [0,1];
    
yTickProb= [0:0.2:1] % ticks every 0.2


%% Fig 4c - PE probability

cmapGrand= cmapCueLaserGrand;
cmapSubj= cmapCueLaserSubj;

%subsset data
data= stimTable;

%dp make stimLength categorical
data.StimLength= categorical(data.StimLength);

clear g2;

% -- 1 = subplot of stimulation PE latency
%- Bar of btwn subj means (group = [] or Group)
group= []; %var by which to group

% dp changing faceting- x cueType so can connect dots and facet by virus Group as rows

g2(1,1)=gramm('x',data.StimLength,'y',data.ResponseProb,'color',data.CueTypeLabel, 'group', group);
g2(1,1).facet_grid(data.Projection, [])

g2(1,1).stat_summary('type','sem', 'geom',{'bar' 'black_errorbar'}, 'dodge', dodge, 'width', width) 
g2(1,1).set_color_options('map',cmapGrand); 

g2(1,1).set_names('row','','x','Laser Duration (s)','y','PE Probability')

figTitle= strcat('C');   
g2(1,1).set_title(figTitle);

g2.set_text_options(text_options_DefaultStyle{:}); 

g2.no_legend();

g2.axe_property('YLim',ylimProb);
g2.axe_property('YTick',yTickProb);


g2.set_parent(p3);

%- First Draw call
g2.draw();

%- Update with point of individual subj points (group= subject)
group= data.Subject;
g2(1,1).update('x',data.StimLength,'y',data.ResponseProb,'color',data.CueTypeLabel, 'group', group);
g2(1,1).stat_summary('type','sem','geom',{'point'}, 'dodge', dodge)%,'bar' 'black_errorbar'});

g2(1,1).set_color_options('map',cmapSubj);

g2.no_legend(); %avoid duplicate legend for subj


g2.draw();


%% 4d- PE Latency
cmapGrand= cmapCueLaserGrand;
cmapSubj= cmapCueLaserSubj;

%subsset data
data= stimTable;


%%Stimulation Latency
clear g;

%dp make stimLength categorical
data.StimLength= categorical(data.StimLength);

% -- 1 = subplot of stimulation PE latency
%- Bar of btwn subj means (group = [] or Group)
group= []; %var by which to group

% dp changing faceting- x cueType so can connect dots and facet by virus Group as rows
g=gramm('x',data.StimLength,'y',data.RelLatency,'color',data.CueTypeLabel, 'group', group);
g.facet_grid(data.Projection,[]);%data.StimLength)

g.stat_summary('type','sem', 'geom',{'bar' 'black_errorbar'}, 'dodge', dodge,'width',width) 


g(1,1).set_color_options('map',cmapGrand); 

g(1,1).set_names('row','','x','Laser Duration (s)','y','PE Latency (s)')


figTitle= strcat('D');   
g(1,1).set_title(figTitle);

g.set_text_options(text_options_DefaultStyle{:}); 

g.no_legend();

g.axe_property('YLim',ylimLatency);
g.axe_property('YTick',yTickLatency);


% set parent uipanel
g.set_parent(p4);


%- first draw call
g.draw();

%- Update with point of individual subj points (group= subject)
group= data.Subject;
g(1,1).update('x',data.StimLength,'y',data.RelLatency,'color',data.CueTypeLabel, 'group', group);
g(1,1).stat_summary('type','sem','geom',{'point'}, 'dodge', dodge)%,'bar' 'black_errorbar'});


g(1,1).set_color_options('map',cmapSubj);

g.no_legend(); %avoid duplicate legend for subj

g.draw();


%% EXPORT DATA FOR STATS ANALYSIS IN PYTHON/R



%% Save the figure

%-Declare Size of Figure at time of creation (up top), not time of saving.

%- Remove borders of UIpanels prior to save
p1.BorderType= 'none'
p2.BorderType= 'none'
p3.BorderType= 'none'
p4.BorderType= 'none'


%-Save the figure
titleFig='vp-vta_Figure4_uiPanels';
saveFig(gcf, figPath, titleFig, figFormats, figSize);

