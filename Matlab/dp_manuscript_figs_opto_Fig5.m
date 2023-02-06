%% Load Opto choice task data

load("C:\Users\Dakota\Documents\GitHub\DS-Training\Matlab\_output\_choiceTask\VP-OPTO-choiceTask-02-Feb-2023-choiceTaskTable.mat");

data=[];
data= choiceTaskTable;

%% Note that prior script excluded observations based on behavioral criteria


%% EXCLUDE data 
%- Based on virusType
include= [];
include= 'stimulation';

ind=[];
ind= strcmp(data.virusType, include);

data= data(ind, :);

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
choiceTaskTable= data;


%% Make fig w UIpanels

%% set defaults

% for JNeuro, 1.5 Col max width = 11.6cm (~438 pixels); 2 col max width = 17.6cm (~665 pixels)
figSize1= [100, 100, 430, 600];

figSize2= [100, 100, 650, 600];

%make appropriate size
figSize= figSize2

%% Initialize a figure with Drawable Area padding appropriately
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

  
%% Figure 5

%% aesthetics

% bar widths
width= .9;
dodge= 	width; %if dodge constant between point and bar, will align correctly

% y lims
% 
% ylimLatency= [0,10];
% 
% yTickLatency= [0:2:10] % ticks every 2s

ylimProb= [0,1];
    
yTickProb= [0:0.2:1] % ticks every 0.2


% %% More refactoring 
% 
% %% refactoring fig 5 even more, trying sub-facets
% 
%         
% % %         %- count
% %         y= 'countLP'
% % 
% % % %         stack() to make inactive/active LP a variable
% %         data3= stack(data3, {'ActiveLeverPress', 'InactiveLeverPress'}, 'IndexVariableName', 'typeLP', 'NewDataVariableName', 'countLP');
% % 
% % %         % - proportion 
% % % %        stack() to make inactive/active LP a variable
% % %         data3= stack(data3, {'probActiveLP', 'probInactiveLP'}, 'IndexVariableName', 'typeLP', 'NewDataVariableName', 'probLP');
% % % 
% % %         y= 'probLP'
% 
% % highly manual, specific subplotting here
% 
% 
% % %run separately based on stim vs inhibition
% thisExpType=1;
% 
% expTypesAll= unique(choiceTaskTable.ExpType);
% expTypeLabels= unique(choiceTaskTable.virusType);
% 
%     thisExpTypeLabel= expTypeLabels{thisExpType};
% 
% % == Figure 5a
% 
% %subset data
% 
% cmapSubj= cmapBlueGraySubj;
% cmapGrand= cmapBlueGrayGrand;
% 
% 
%     %subset data- by expType/virus
%     ind=[];
%     ind= choiceTaskTable.ExpType==expTypesAll(thisExpType);
% 
%     data0=[];
%     data0= choiceTaskTable(ind,:);
%     
%     % ~~~~~ ROW 1: ACQUISITION
% 
%         
%     % ~~ A) Acquisition VTA only raw count LP ~~~~~~~~~~~~~~~~~~~~~~~
% 
%         %subset data- by trainPhase
%         phasesToInclude= [1]; %list of phases to include 
% 
%         ind=[];
% 
%         ind= ismember(data0.trainPhase, phasesToInclude);
% 
%         data= data0(ind,:);
%     
%        %stack() to make inactive/active LP a variable
%         data2= [];
%         data2= stack(data, {'ActiveLeverPress', 'InactiveLeverPress'}, 'IndexVariableName', 'typeLP', 'NewDataVariableName', 'countLP');
% 
%         data3= data2;
%       
% %         %subset- by projection
% %         ind=[]
% %         ind= strcmp(data3.Projection,'VTA');
% %         
% %         data3= data2(ind,:);
% 
%         
%         %Make figure
%         figure; clear d;
%         
%         
%         cmapSubj= cmapBlueGraySubj;
%         cmapGrand= cmapBlueGrayGrand;
%         
%         %-- individual subj
%         group= data3.Subject;
% 
%         d(1,1)=gramm('x',data3.Session,'y',data3.countLP,'color',data3.typeLP, 'group', group)
% 
%         d(1,1).facet_grid([], data3.Projection);
%         
%         d(1,1).stat_summary('type','sem','geom','area');
%         d(1,1).set_line_options('base_size',linewidthSubj);
%         d(1,1).set_color_options('map', cmapSubj);
% 
%         %- Things to do before first draw call-
%         d(1,1).set_names('column', '', 'x', 'Time from Cue (s)','y','GCaMP (Z-score)','color','Trial type'); %row/column labels must be set before first draw call
% 
%         d(1,1).no_legend(); %avoid duplicate legend from other plots (e.g. subject & grand colors)
%        
% 
%            %first draw call-
%            
%         d(1,1).set_title('Acquistion- VTA');
%         
%         d(1,1).draw()
%            
% 
%         %------ btwn subj mean as well
%         group= [];
% 
%         d(1,1).update('x',data3.Session,'y',data3.countLP,'color',data3.typeLP, 'group', group)
% 
%         d(1,1).stat_summary('type','sem','geom','area'), 'dodge', dodge, 'width', width;
% 
%         d(1,1).set_names('x','Session','y','Number of Lever Presses','color','Lever Side')
%     %     d.set_names('row','Target','column','Phase','x','Session','y','Number of Lever Presses','color','Lever Side')
% 
% 
%         d(1,1).set_line_options('base_size',linewidthGrand);
%         d(1,1).set_color_options('map', cmapGrand);
%         d(1,1).no_legend(); %prevent legend duplicates if you like
%         
%         %need to leave something for final draw call to know all of the subplots. Either don't draw this update (max 1 update) or draw all initial subplots first prior to updates.
% %         d(1,1).draw(); 
% 
% % % 
% % %     % ~~ B) Acquisition mdThal only raw count LP ~~~~~~~~~~~~~~~~~~~~~~~
% % %         %subset data- by trainPhase
% % %         phasesToInclude= [1]; %list of phases to include 
% % % 
% % %         ind=[];
% % % 
% % %         ind= ismember(data0.trainPhase, phasesToInclude);
% % % 
% % %         data= data0(ind,:);
% % %     
% % %        %stack() to make inactive/active LP a variable
% % %         data2= [];
% % %         data2= stack(data, {'ActiveLeverPress', 'InactiveLeverPress'}, 'IndexVariableName', 'typeLP', 'NewDataVariableName', 'countLP');
% % % 
% % % 
% % %         %subset- by projection
% % %         data3= data2;
% % % 
% % %         ind=[]
% % %         ind= strcmp(data3.Projection,'mdThal');
% % %         
% % %         data3= data2(ind,:);
% % %                 
% % %         cmapSubj= cmapBlueGraySubj;
% % %         cmapGrand= cmapBlueGrayGrand;
% % %         
% % %         %-- individual subj
% % %         
% % %         group= data3.Subject;
% % % 
% % %         d(1,2)=gramm('x',data3.Session,'y',data3.countLP,'color',data3.typeLP, 'group', group)
% % % 
% % % %        
% % % %         d(1,2).stat_summary('type','sem','geom','area');
% % % %         d(1,2).set_line_options('base_size',linewidthSubj);
% % % %         d(1,2).set_color_options('map', cmapSubj);
% % % % 
% % % %         d(1,2).set_names('x','Session','y','Number of Lever Presses','color','Lever Side')
% % % 
% % %         d(1,2).no_legend(); %avoid duplicate legend from other plots (e.g. subject & grand colors)
% % %            
% % %         d(1,2).set_title('Acquistion- mdThal');
% % %         
% % %         d(1,2).draw()
% % %            
% % 
% %         %------ btwn subj mean as well
% %         group= [];
% % 
% %         d(1,2).update('x',data3.Session,'y',data3.countLP,'color',data3.typeLP, 'group', group)
% % 
% %         d(1,2).stat_summary('type','sem','geom','area');
% % 
% %         d(1,2).set_names('x','Session','y','Number of Lever Presses','color','Lever Side')
% %     %     d.set_names('row','Target','column','Phase','x','Session','y','Number of Lever Presses','color','Lever Side')
% % 
% % 
% %         d(1,2).set_line_options('base_size',linewidthGrand);
% %         d(1,2).set_color_options('map', cmapGrand);
% %         d(1,2).no_legend(); %prevent legend duplicates if you like
% %         
% % %         d(1,2).draw(); %Leave for final draw call
% %         
% 
%      % ~~ C)Acquisition VTA & mdThal Active Proportion LP ~~~~~~~~~~~~~~~~~~~~~~~
% 
%              y= 'probActiveLP';
% %         y= 'ActiveLeverPress';
%      
%         %subset data- by trainPhase
%         phasesToInclude= [1]; %list of phases to include 
% 
%         ind=[];
% 
%         ind= ismember(data0.trainPhase, phasesToInclude);
% 
%         data= data0(ind,:);
% 
%        %stack() not necessary
%         data2= data
% 
%         %subset- by projection not necessary
%         data3= data2;
%         
%         
% %     -stack() to make inactive/active LP a variable
%         
% %         %- count
%         y= 'countLP'
% 
% % %         stack() to make inactive/active LP a variable
%         data3= stack(data3, {'ActiveLeverPress', 'InactiveLeverPress'}, 'IndexVariableName', 'typeLP', 'NewDataVariableName', y);
% 
% %         % - proportion 
% % %        stack() to make inactive/active LP a variable
% %         data3= stack(data3, {'probActiveLP', 'probInactiveLP'}, 'IndexVariableName', 'typeLP', 'NewDataVariableName', 'probLP');
% % 
% %         y= 'probLP'
% 
%         
%         %cmap for Projection comparisons
%         cmapGrand= cmapBlueGrayGrand;
%         cmapSubj= cmapBlueGraySubj;   
%         
%         %-- individual subj
%         group= data3.Subject;
% 
% %         d(1,2)=gramm('x',data3.Session,'y',data3.(y),'color',data3.Projection, 'group', group)
%         d(1,2)=gramm('x',data3.Session,'y',data3.(y),'color',data3.typeLP, 'group', group)
% 
%         %facet by projection
%         d(1,2).facet_grid([], data3.Projection);
%         
% %        
% %         d(1,2).stat_summary('type','sem','geom','area');
% %         d(1,2).set_line_options('base_size',linewidthSubj);
% %         d(1,2).set_color_options('map', cmapSubj);
% 
% % %         d(1,2).set_names('x','Session','y','Proportion Active Lever Presses','color','Lever Side')
% % % 
% % %         d(1,2).no_legend(); %avoid duplicate legend from other plots (e.g. subject & grand colors)
%            
%         d(1,2).set_title('Acquistion- Active Proportion');
%         
%         d(1,2).axe_property('YLim',ylimProb);
%         d(1,2).axe_property('YTick',yTickProb);
% 
%         
%         d(1,2).draw()
%            
% 
%         %------ btwn subj mean as well
%         group= [];
% 
% %         d(1,2).update('x',data3.Session,'y',data3.(y),'color',data3.Projection, 'group', group)
%         d(1,2).update('x',data3.Session,'y',data3.(y),'color',data3.typeLP, 'group', group)
% 
%         d(1,2).stat_summary('type','sem','geom','area');
% 
% %         d(1,2).set_names('x','Session','y','Proportion Active Lever Presses','color','Projection')
%         d(1,2).set_names('x','Session','y',y,'color','Projection')
% 
% 
%         d(1,2).set_line_options('base_size',linewidthGrand);
%         d(1,2).set_color_options('map', cmapGrand);
%         d(1,2).no_legend(); %prevent legend duplicates if you like
%                 
%         d(1,2).geom_hline('yintercept',0.5, 'style', 'k--', 'linewidth', linewidthReference); %overlay t=0
%         
% %         d(1,2).draw(); %Leave for final draw call
%         
%            
%         
%      % ~~ D) Reversal VTA & mdThal Active Proportion LP ~~~~~~~~~~~~~~~~~~~~~~~
% 
%      % try diff versions with raw vs proportion 
%     
%      
%         %subset data- by trainPhase
%         phasesToInclude= [2]; %list of phases to include 
% 
%         ind=[];
% 
%         ind= ismember(data0.trainPhase, phasesToInclude);
% 
%         data= data0(ind,:);
%     
%        %stack() not necessary
%         data2= data
% 
%         %subset- by projection not necessary
%         data3= data2;
%         
%         
% %     -stack() to make inactive/active LP a variable
%         
% %         %- count
%         y= 'countLP'
% 
% % %         stack() to make inactive/active LP a variable
%         data3= stack(data3, {'ActiveLeverPress', 'InactiveLeverPress'}, 'IndexVariableName', 'typeLP', 'NewDataVariableName', y);
% 
% %         % - proportion 
% % %        stack() to make inactive/active LP a variable
% %         data3= stack(data3, {'probActiveLP', 'probInactiveLP'}, 'IndexVariableName', 'typeLP', 'NewDataVariableName', 'probLP');
% % 
% %         y= 'probLP'
% 
%         
%            %cmap for Laser comparisons
%         cmapGrand= cmapBlueGrayGrand;
%         cmapSubj= cmapBlueGraySubj;  
%         
%         %-- individual subj
%         group= data3.Subject;
% 
% %         d(2,1)=gramm('x',data3.Session,'y',data3.(y),'color',data3.Projection, 'group', group)
% 
%            d(2,1)=gramm('x',data3.Session,'y',data3.(y),'color',data3.typeLP, 'group', group)
% 
%            %Facet by projection
%            d(2,1).facet_grid([], data3.Projection);
%            
% %         d(2,1).stat_summary('type','sem','geom','area');
% %         d(2,1).set_line_options('base_size',linewidthSubj);
% %         d(2,1).set_color_options('map', cmapSubj);
% % 
% % %         d(1,2).set_names('x','Session','y','Proportion Active Lever Presses','color','Lever Side')
% 
%         d(2,1).no_legend(); %avoid duplicate legend from other plots (e.g. subject & grand colors)
%            
%         d(2,1).set_title('Reversal- Active Proportion');
%         
%         d(2,1).draw()
%            
% 
%         %------ btwn subj mean as well
%         group= [];
% 
% %         d(2,1).update('x',data3.Session,'y',data3.(y),'color',data3.Projection, 'group', group)
%         d(2,1).update('x',data3.Session,'y',data3.(y),'color',data3.typeLP, 'group', group)
% 
%         d(2,1).stat_summary('type','sem','geom','area');
% 
%         d(2,1).set_names('x','Session','y','Proportion Active Lever Presses','color','Projection')
% 
%        
%         d(2,1).set_line_options('base_size',linewidthGrand);
%         d(2,1).set_color_options('map', cmapGrand);
%         d(2,1).no_legend(); %prevent legend duplicates if you like
%         
%         d(2,1).geom_hline('yintercept',0.5, 'style', 'k--', 'linewidth', linewidthReference); %overlay t=0
% 
%         
% %         d(1,2).draw(); %Leave for final draw call
%         
%       
%      % ~~ E) Forced Choice VTA & mdThal Active Proportion LP ~~~~~~~~~~~~~~~~~~~~~~~
% 
%         %subset data- by trainPhase
%         phasesToInclude= [3]; %list of phases to include 
% 
%         ind=[];
% 
%         ind= ismember(data0.trainPhase, phasesToInclude);
% 
%         data= data0(ind,:);
%     
%        %stack() not necessary
%         data2= data
% 
%         %subset- by projection not necessary
%         data3= data2;
%         
%         %     -stack() to make inactive/active LP a variable
%         
% %         %- count
%         y= 'countLP'
% 
% % %         stack() to make inactive/active LP a variable
%         data3= stack(data3, {'ActiveLeverPress', 'InactiveLeverPress'}, 'IndexVariableName', 'typeLP', 'NewDataVariableName', y);
% 
% %         % - proportion 
% % %        stack() to make inactive/active LP a variable
% %         data3= stack(data3, {'probActiveLP', 'probInactiveLP'}, 'IndexVariableName', 'typeLP', 'NewDataVariableName', 'probLP');
% % 
% %         y= 'probLP'
%         
%             %cmap for Laser comparisons
%         cmapGrand= cmapBlueGrayGrand;
%         cmapSubj= cmapBlueGraySubj;  
%         
%         %-- individual subj
%         group= data3.Subject;
% 
% %         d(2,2)=gramm('x',data3.Session,'y',data3.(y),'color',data3.Projection, 'group', group)
%         
%         d(2,2)=gramm('x',data3.Session,'y',data3.(y),'color',data3.typeLP, 'group', group)
%         %facet by Projection
%         d(2,2).facet_grid([], data3.Projection);
%        
% %         d(2,2).stat_summary('type','sem','geom','area');
% %         d(2,2).set_line_options('base_size',linewidthSubj);
% %         d(2,2).set_color_options('map', cmapSubj);
% % 
% % %         d(1,3).set_names('x','Session','y','Proportion Active Lever Presses','color','Lever Side')
% 
%         d(2,2).no_legend(); %avoid duplicate legend from other plots (e.g. subject & grand colors)
%            
%         d(2,2).set_title('Forced Choice- Active Proportion');
%         
%         d(2,2).draw()
%            
% 
%         %------ btwn subj mean as well
%         group= [];
% 
% %         d(2,2).update('x',data3.Session,'y',data3.(y),'color',data3.Projection, 'group', group)
%         d(2,2).update('x',data3.Session,'y',data3.(y),'color',data3.typeLP, 'group', group)
% 
%         d(2,2).stat_summary('type','sem','geom','area');
% 
%         d(2,2).set_names('x','Session','y','Proportion Active Lever Presses','color','Projection')
% 
% 
%         d(2,2).set_line_options('base_size',linewidthGrand);
%         d(2,2).set_color_options('map', cmapGrand);
%         d(2,2).no_legend(); %prevent legend duplicates if you like
%         
%         
%         d(2,2).geom_hline('yintercept',0.5, 'style', 'k--', 'linewidth', linewidthReference); %overlay t=0
% 
%         
% %         d(1,3).draw(); %Leave for final draw call     
% 
% 
%      % ~~ F) Final Test & Extinction; VTA & mdThal Active Proportion LP ~~~~~~~~~~~~~~~~~~~~~~~
%      
%         %subset data- by trainPhase
%         phasesToInclude= [4,5]; %list of phases to include 
% 
%         ind=[];
% 
%         ind= ismember(data0.trainPhase, phasesToInclude);
% 
%         data= data0(ind,:);
%     
%        %stack() not necessary
%         data2= data
% 
%         %subset- by projection not necessary
%         data3= data2;
%         
%         
% %         %- count
%         y= 'countLP'
% 
% % %         stack() to make inactive/active LP a variable
%         data3= stack(data3, {'ActiveLeverPress', 'InactiveLeverPress'}, 'IndexVariableName', 'typeLP', 'NewDataVariableName', 'countLP');
% 
% %         % - proportion 
% % %        stack() to make inactive/active LP a variable
% %         data3= stack(data3, {'probActiveLP', 'probInactiveLP'}, 'IndexVariableName', 'typeLP', 'NewDataVariableName', 'probLP');
% % 
% %         y= 'probLP'
% 
%         
%         %cmap for Projection comparisons
%         cmapGrand= cmapBlueGrayGrand;
%         cmapSubj= cmapBlueGraySubj;   
%         
%         %-- individual subj
%         group= data3.Subject;
% 
% % %         d(2,3)=gramm('x',data3.trainPhaseLabel,'y',data3.(y),'color',data3.typeLP, 'group', group)
% % % 
% % %         Facet by Projection target
% % %         d(2,3).facet_grid([], data3.Projection);
% % % 
%         d(2,3)=gramm('x',data3.Projection,'y',data3.(y),'color',data3.typeLP, 'group', group)
% 
%         %Facet by trainPhase target
% %         d(2,3).facet_grid([], data3.trainPhaseLabel, 'scale', 'independent');
%           d(2,3).facet_grid([], data3.trainPhaseLabel);
% 
% %        
% %         d(2,3).stat_summary('type','sem','geom','area');
%         d(2,3).geom_point('dodge',dodge);
%         d(2,3).set_line_options('base_size',linewidthSubj);
%         d(2,3).set_color_options('map', cmapSubj);
% % 
% % %         d(1,3).set_names('x','Session','y','Proportion Active Lever Presses','color','Lever Side')
% 
%         d(2,3).no_legend(); %avoid duplicate legend from other plots (e.g. subject & grand colors)
%            
%         d(2,3).set_title('Free Choice- Active Proportion');
%         
%         d(2,3).draw()
%            
% 
%         %------ btwn subj mean as well
%         group= [];
% 
% %         d(2,3).update('x',data3.trainPhaseLabel,'y',data3.(y),'color',data3.typeLP, 'group', group)
%         d(2,3).update('x',data3.Projection,'y',data3.(y),'color',data3.typeLP, 'group', group)
% 
%         
% %         d(2,3).stat_summary('type','sem','geom','area');
%         d(2,3).stat_summary('type','sem','geom',{'bar', 'black_errorbar'}, 'dodge', dodge)%,'bar' 'black_errorbar'});
% 
% 
% %         d(2,3).set_names('x','Session','y','Proportion Active Lever Presses','color','Projection')
%         d(2,3).set_names('x','Session','y',y,'color','Projection')
% 
% 
%         d(2,3).set_line_options('base_size',linewidthGrand);
%         d(2,3).set_color_options('map', cmapGrand);
%         d(2,3).no_legend(); %prevent legend duplicates if you like
%         
%         
%         d(2,3).geom_hline('yintercept',0.5, 'style', 'k--', 'linewidth', linewidthReference); %overlay t=0
% 
%         
% %         d(1,3).draw(); %Leave for final draw call     
% 
% 
% % ~~~~~~~~~~~~~~~FINAL ROW: Licks/Reward 
%         
% 
%         %~~~ 3,1 Reversal
%         %subset data- by trainPhase
%         phasesToInclude= [2]; %list of phases to include 
% 
%         ind=[];
% 
%         ind= ismember(data0.trainPhase, phasesToInclude);
% 
%         data= data0(ind,:);
%     
%        %stack() - to make active/inactive a variable
%         data2= stack(data, {'LicksPerReward', 'LicksPerRewardInactive'}, 'IndexVariableName', 'typeLP', 'NewDataVariableName', 'rewardLicks');
% 
%         %subset- by projection not necessary
%         data3= data2;
%         
%         %cmap for Laser comparisons
%         cmapGrand= cmapBlueGrayGrand;
%         cmapSubj= cmapBlueGraySubj;   
%         
%         %-- individual subj
%         group= data3.Subject;
% 
%             %add style facet for active/inactive
% %         d(3,1)=gramm('x',data3.Session,'y',data3.rewardLicks,'color',data3.Projection, 'linestyle', data3.typeLP, 'group', group)
%         d(3,1)=gramm('x',data3.Session,'y',data3.rewardLicks,'color',data3.typeLP, 'group', group)
% 
%         %facet by projection
%         d(3,1).facet_grid([], data3.Projection);
%         
% %        
% %         d(3,1).stat_summary('type','sem','geom','area');
% %         d(3,1).set_line_options('base_size',linewidthSubj);
% %         d(3,1).set_color_options('map', cmapSubj);
% % 
% % %         d(3,1).set_names('x','Session','y','Licks per Reward','color','Lever Side')
% 
%         d(3,1).no_legend(); %avoid duplicate legend from other plots (e.g. subject & grand colors)
%            
%         d(3,1).set_title('Reversal- Licks per Reward');
%         
%         d(3,1).draw()
%            
% 
%         %------ btwn subj mean as well
%         group= [];
% 
%         d(3,1).update('x',data3.Session,'y',data3.rewardLicks,'color',data3.typeLP, 'group', group)
% 
%         d(3,1).stat_summary('type','sem','geom','area');
% 
%         d(3,1).set_names('x','Session','y','Licks per Reward','color','Projection')
% 
% 
%         d(3,1).set_line_options('base_size',linewidthGrand);
%         d(3,1).set_color_options('map', cmapGrand);
%         d(3,1).no_legend(); %prevent legend duplicates if you like
%         
%         
%         %~~~ 3,2 Reversal
%         %subset data- by trainPhase
%         phasesToInclude= [3]; %list of phases to include 
% 
%         ind=[];
% 
%         ind= ismember(data0.trainPhase, phasesToInclude);
% 
%         data= data0(ind,:);
%     
%        %stack() - to make active/inactive a variable
%         data2= stack(data, {'LicksPerReward', 'LicksPerRewardInactive'}, 'IndexVariableName', 'typeLP', 'NewDataVariableName', 'rewardLicks');
% 
%         %subset- by projection not necessary
%         data3= data2;
%         
%         %cmap for Projection comparisons
%         cmapGrand= 'brewer_dark';
%         cmapSubj= 'brewer2';   
%         
%         %-- individual subj
%         group= data3.Subject;
% 
%             %add style facet for active/inactive
%         d(3,2)=gramm('x',data3.Session,'y',data3.rewardLicks,'color',data3.Projection,'group', group)
% 
%         
% %         d(3,2).stat_summary('type','sem','geom','area');
% %         d(3,2).set_line_options('base_size',linewidthSubj);
% %         d(3,2).set_color_options('map', cmapSubj);
% % 
% % %         d(3,2).set_names('x','Session','y','Licks per Reward','color','Lever Side')
% 
%         d(3,2).no_legend(); %avoid duplicate legend from other plots (e.g. subject & grand colors)
%            
%         d(3,2).set_title('Forced Choice- Licks per Reward');
%         
%         d(3,2).draw()
%            
% 
%         %------ btwn subj mean as well
%         group= [];
% 
%         d(3,2).update('x',data3.Session,'y',data3.rewardLicks,'color',data3.Projection, 'linestyle', data3.typeLP, 'group', group)
% 
%         d(3,2).stat_summary('type','sem','geom','area');
% 
%         d(3,2).set_names('x','Session','y','Licks per Reward','color','Projection')
% 
% 
%         d(3,2).set_line_options('base_size',linewidthGrand);
%         d(3,2).set_color_options('map', cmapGrand);
%         d(3,2).no_legend(); %prevent legend duplicates if you like
%         
% 
%           
%         %~~~ 3,3 Test
%         %subset data- by trainPhase       
%         phasesToInclude= [4]; %list of phases to include 
% 
%         ind=[];
% 
%         ind= ismember(data0.trainPhase, phasesToInclude);
% 
%         data= data0(ind,:);
%     
%        %stack() - to make active/inactive a variable
%         data2= stack(data, {'LicksPerReward', 'LicksPerRewardInactive'}, 'IndexVariableName', 'typeLP', 'NewDataVariableName', 'rewardLicks');
% 
%         %subset- by projection not necessary
%         data3= data2;
%         
%         %cmap for Laser comparisons
%         cmapGrand= cmapBlueGrayGrand;
%         cmapSubj= cmapBlueGraySubj;   
%         
%    
%         %------ btwn subj bar
%         group= [];
% %         group= data3.Projection
% 
%             %  2 sems for some reason here?
% %         d(3,3).update('x',data3.trainPhaseLabel,'y',data3.rewardLicks,'color',data3.Projection, 'linestyle', data3.typeLP, 'group', group)
% %         d(3,3)= gramm('x',data3.typeLP,'y',data3.rewardLicks,'color',data3.Projection, 'linestyle', data3.typeLP, 'group', group)
%         d(3,3)= gramm('x',data3.Projection,'y',data3.rewardLicks,'color',data3.typeLP, 'group', group)
% 
% %         %add facet by projection
% %         d(3,3).facet_grid([], data3.Projection);
%         
% %         d(3,3).stat_summary('type','sem','geom','bar');
%         d(3,3).stat_summary('type','sem','geom',{'bar', 'black_errorbar'}, 'dodge', dodge, 'width', width)%,'bar' 'black_errorbar'});
% 
%         
%         d(3,3).set_names('x','Lever Type','y','Licks per Reward','color','Projection')
% 
% 
%         d(3,3).set_line_options('base_size',linewidthGrand);
%         d(3,3).set_color_options('map', cmapGrand);
%         d(3,3).no_legend(); %prevent legend duplicates if you like
%         
%         % first draw
%         d(3,3).draw()
% 
%     %-- individual subj points
%         group= data3.Subject;
% 
%             %add style facet for active/inactive
% %         d(3,3)=gramm('x',data3.trainPhaseLabel,'y',data3.rewardLicks,'color',data3.Projection, 'linestyle', data3.typeLP, 'group', group)
% 
% %           d(3,3).update('x',data3.typeLP,'y',data3.rewardLicks,'color',data3.Projection, 'group', group)
%           d(3,3).update('x',data3.Projection,'y',data3.rewardLicks,'color',data3.typeLP, 'group', group)
% 
% %         d(3,3).stat_summary('type','sem','geom','area');
%         d(3,3).stat_summary('type','sem','geom',{'point'}, 'dodge', dodge, 'width',width)%,'bar' 'black_errorbar'});
% 
%         d(3,3).set_line_options('base_size',linewidthSubj);
%         d(3,3).set_color_options('map', cmapSubj);
% 
% %         d(3,3).set_names('x','Session','y','Licks per Reward','color','Lever Side')
% 
%         d(3,3).no_legend(); %avoid duplicate legend from other plots (e.g. subject & grand colors)
%            
%         d(3,3).set_title('Free Choice- Licks per Reward');
%                    
%         
% 
% 
%         % --- Overall Fig things to do before final overall draw call ---
%         d.set_text_options(text_options_DefaultStyle{:}); %apply default text sizes/styles
% 
%         titleFig= ('Fig 5');   
%         d.set_title(titleFig); %overarching fig title must be set before first draw call
% 
%         
% 
%     %--- Final Draw call ---
%         d.draw(); %Final Draw call
%         
%          figTitle= strcat('choiceTask-',thisExpTypeLabel,'-','Figure5-draft-',y);   
%     
% %          saveFig(gcf, figPath,figTitle,figFormats);
% 
% 
% 
% 
% 



%% ---------------------------------------------------------****---------


%% refactoring fig 5 even more, trying sub-facets

% highly manual, specific subplotting here


% %run separately based on stim vs inhibition
thisExpType=1;

expTypesAll= unique(choiceTaskTable.ExpType);
expTypeLabels= unique(choiceTaskTable.virusType);

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
      
%         %subset- by projection
%         ind=[]
%         ind= strcmp(data3.Projection,'VTA');
%         
%         data3= data2(ind,:);

        
        %Make figure
        figure; clear d;
        
        
        cmapSubj= cmapBlueGraySubj;
        cmapGrand= cmapBlueGrayGrand;
        
        %-- individual subj
        group= data3.Subject;

        d(1,2)=gramm('x',data3.Session,'y',data3.countLP,'color',data3.typeLP, 'group', group)

        d(1,2).facet_grid([], data3.Projection);
        
        d(1,2).stat_summary('type','sem','geom','area');
        d(1,2).set_line_options('base_size',linewidthSubj);
        d(1,2).set_color_options('map', cmapSubj);

        %- Things to do before first draw call-
        d(1,2).set_names('column', '', 'x', 'Time from Cue (s)','y','GCaMP (Z-score)','color','Trial type'); %row/column labels must be set before first draw call

        d(1,2).no_legend(); %avoid duplicate legend from other plots (e.g. subject & grand colors)
       

           %first draw call-
           
        d(1,2).set_title('Acquistion- VTA');
        
        d(1,2).draw()
           

        %------ btwn subj mean as well
        group= [];

        d(1,2).update('x',data3.Session,'y',data3.countLP,'color',data3.typeLP, 'group', group)

        d(1,2).stat_summary('type','sem','geom','area'), 'dodge', dodge, 'width', width;

        d(1,2).set_names('x','Session','y','Number of Lever Presses','color','Lever Side')
    %     d.set_names('row','Target','column','Phase','x','Session','y','Number of Lever Presses','color','Lever Side')


        d(1,2).set_line_options('base_size',linewidthGrand);
        d(1,2).set_color_options('map', cmapGrand);
        d(1,2).no_legend(); %prevent legend duplicates if you like
        
        %need to leave something for final draw call to know all of the subplots. Either don't draw this update (max 1 update) or draw all initial subplots first prior to updates.
%         d(1,2).draw(); 

% % 
% %     % ~~ B) Acquisition mdThal only raw count LP ~~~~~~~~~~~~~~~~~~~~~~~
% %         %subset data- by trainPhase
% %         phasesToInclude= [1]; %list of phases to include 
% % 
% %         ind=[];
% % 
% %         ind= ismember(data0.trainPhase, phasesToInclude);
% % 
% %         data= data0(ind,:);
% %     
% %        %stack() to make inactive/active LP a variable
% %         data2= [];
% %         data2= stack(data, {'ActiveLeverPress', 'InactiveLeverPress'}, 'IndexVariableName', 'typeLP', 'NewDataVariableName', 'countLP');
% % 
% % 
% %         %subset- by projection
% %         data3= data2;
% % 
% %         ind=[]
% %         ind= strcmp(data3.Projection,'mdThal');
% %         
% %         data3= data2(ind,:);
% %                 
% %         cmapSubj= cmapBlueGraySubj;
% %         cmapGrand= cmapBlueGrayGrand;
% %         
% %         %-- individual subj
% %         
% %         group= data3.Subject;
% % 
% %         d(1,2)=gramm('x',data3.Session,'y',data3.countLP,'color',data3.typeLP, 'group', group)
% % 
% % %        
% % %         d(1,2).stat_summary('type','sem','geom','area');
% % %         d(1,2).set_line_options('base_size',linewidthSubj);
% % %         d(1,2).set_color_options('map', cmapSubj);
% % % 
% % %         d(1,2).set_names('x','Session','y','Number of Lever Presses','color','Lever Side')
% % 
% %         d(1,2).no_legend(); %avoid duplicate legend from other plots (e.g. subject & grand colors)
% %            
% %         d(1,2).set_title('Acquistion- mdThal');
% %         
% %         d(1,2).draw()
% %            
% 
%         %------ btwn subj mean as well
%         group= [];
% 
%         d(1,2).update('x',data3.Session,'y',data3.countLP,'color',data3.typeLP, 'group', group)
% 
%         d(1,2).stat_summary('type','sem','geom','area');
% 
%         d(1,2).set_names('x','Session','y','Number of Lever Presses','color','Lever Side')
%     %     d.set_names('row','Target','column','Phase','x','Session','y','Number of Lever Presses','color','Lever Side')
% 
% 
%         d(1,2).set_line_options('base_size',linewidthGrand);
%         d(1,2).set_color_options('map', cmapGrand);
%         d(1,2).no_legend(); %prevent legend duplicates if you like
%         
% %         d(1,2).draw(); %Leave for final draw call
%         

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

%        
%         d(1,3).stat_summary('type','sem','geom','area');
%         d(1,3).set_line_options('base_size',linewidthSubj);
%         d(1,3).set_color_options('map', cmapSubj);

% %         d(1,3).set_names('x','Session','y','Proportion Active Lever Presses','color','Lever Side')
% % 
% %         d(1,3).no_legend(); %avoid duplicate legend from other plots (e.g. subject & grand colors)
           
        d(1,3).set_title('Acquistion- Active Proportion');
        
        d(1,3).axe_property('YLim',ylimProb);
        d(1,3).axe_property('YTick',yTickProb);

        
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
        
%         d(1,2).draw(); %Leave for final draw call
        
           
        
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

       
%         d(2,1).stat_summary('type','sem','geom','area');
%         d(2,1).set_line_options('base_size',linewidthSubj);
%         d(2,1).set_color_options('map', cmapSubj);
% 
% %         d(1,2).set_names('x','Session','y','Proportion Active Lever Presses','color','Lever Side')

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

        
%         d(1,2).draw(); %Leave for final draw call
        
      
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

       
%         d(2,2).stat_summary('type','sem','geom','area');
%         d(2,2).set_line_options('base_size',linewidthSubj);
%         d(2,2).set_color_options('map', cmapSubj);
% 
% %         d(1,3).set_names('x','Session','y','Proportion Active Lever Presses','color','Lever Side')

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
        
        
%         %- count
        y= 'countLP'

% %         stack() to make inactive/active LP a variable
        data3= stack(data3, {'ActiveLeverPress', 'InactiveLeverPress'}, 'IndexVariableName', 'typeLP', 'NewDataVariableName', 'countLP');

%         % - proportion 
% %        stack() to make inactive/active LP a variable
%         data3= stack(data3, {'probActiveLP', 'probInactiveLP'}, 'IndexVariableName', 'typeLP', 'NewDataVariableName', 'probLP');
% 
%         y= 'probLP'

        
        %cmap for Projection comparisons
        cmapGrand= cmapBlueGrayGrand;
        cmapSubj= cmapBlueGraySubj;   
           

        %------ btwn subj bar first
        group= [];

%         d(2,3).update('x',data3.trainPhaseLabel,'y',data3.(y),'color',data3.typeLP, 'group', group)
        d(2,3)= gramm('x',data3.Projection,'y',data3.(y),'color',data3.typeLP, 'group', group)
        d(2,3).facet_grid([], data3.trainPhaseLabel);

        
%         d(2,3).stat_summary('type','sem','geom','area');
        d(2,3).stat_summary('type','sem','geom',{'bar'}, 'dodge', dodge)%,'bar' 'black_errorbar'});


%         d(2,3).set_names('x','Session','y','Proportion Active Lever Presses','color','Projection')
        d(2,3).set_names('x','Session','y',y,'color','Projection')

        d(2,3).set_title('Test- Active Proportion');

        d(2,3).set_line_options('base_size',linewidthGrand);
        d(2,3).set_color_options('map', cmapGrand);
        d(2,3).no_legend(); %prevent legend duplicates if you like
        
        
        d(2,3).geom_hline('yintercept',0.5, 'style', 'k--', 'linewidth', linewidthReference); %overlay t=0

        d(2,3).draw();
%         d(1,3).draw(); %Leave for final draw call     

   %-- individual subj points over
        group= data3.Subject;

% %         d(2,3)=gramm('x',data3.trainPhaseLabel,'y',data3.(y),'color',data3.typeLP, 'group', group)
% % 
% %         Facet by Projection target
% %         d(2,3).facet_grid([], data3.Projection);
% % 
        d(2,3).update('x',data3.Projection,'y',data3.(y),'color',data3.typeLP, 'group', group)

        %Facet by trainPhase target
%         d(2,3).facet_grid([], data3.trainPhaseLabel, 'scale', 'independent');
%           d(2,3).facet_grid([], data3.trainPhaseLabel);

%        
%         d(2,3).stat_summary('type','sem','geom','area');
        d(2,3).geom_point('dodge',dodge);
        d(2,3).set_line_options('base_size',linewidthSubj);
        d(2,3).set_color_options('map', cmapSubj);
                
  % 
% %         d(1,3).set_names('x','Session','y','Proportion Active Lever Presses','color','Lever Side')

        d(2,3).no_legend(); %avoid duplicate legend from other plots (e.g. subject & grand colors)
           
        
        d(2,3).draw()
        
        %- error bar on top
        group= [];

        d(2,3).update('x',data3.Projection,'y',data3.(y),'color',data3.typeLP, 'group', group)
        d(2,3).stat_summary('type','sem','geom',{'black_errorbar'}, 'dodge', dodge)%,'bar' 'black_errorbar'});

        d(2,3).no_legend();
        
         %save final draw til end for facetgrid
        
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
        
%         %cmap for Projection comparisons
%         cmapGrand= 'brewer_dark';
%         cmapSubj= 'brewer2';   
    %cmap for laser comparison
        cmapGrand= cmapBlueGrayGrand;
        cmapSubj= cmapBlueGraySubj;   
        
        %-- individual subj
        group= data3.Subject;

%         d(3,1)=gramm('x',data3.Session,'y',data3.rewardLicks,'color',data3.Projection, 'linestyle', data3.typeLP, 'group', group)

        % facet by virus
        d(3,1)=gramm('x',data3.Session,'y',data3.rewardLicks,'color',data3.typeLP, 'group', group)

        d(3,1).facet_grid([], data3.Projection)
%        
%         d(3,1).stat_summary('type','sem','geom','area');
%         d(3,1).set_line_options('base_size',linewidthSubj);
%         d(3,1).set_color_options('map', cmapSubj);
% 
% %         d(3,1).set_names('x','Session','y','Licks per Reward','color','Lever Side')

        d(3,1).no_legend(); %avoid duplicate legend from other plots (e.g. subject & grand colors)
           
        d(3,1).set_title('Reversal- Licks per Reward');
        
        d(3,1).draw()
           

        %------ btwn subj mean as well
        group= [];

%         d(3,1).update('x',data3.Session,'y',data3.rewardLicks,'color',data3.Projection, 'linestyle', data3.typeLP, 'group', group)
        d(3,1).update('x',data3.Session,'y',data3.rewardLicks,'color',data3.typeLP, 'group', group)


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
        
%         %cmap for Projection comparisons
%         cmapGrand= 'brewer_dark';
%         cmapSubj= 'brewer2';   
    %cmap for laser comparisons
        cmapGrand= cmapBlueGrayGrand;
        cmapSubj= cmapBlueGraySubj;   

        
        %-- individual subj
        group= data3.Subject;

            %add style facet for active/inactive
%         d(3,2)=gramm('x',data3.Session,'y',data3.rewardLicks,'color',data3.Projection, 'linestyle', data3.typeLP, 'group', group)
          d(3,2)=gramm('x',data3.Session,'y',data3.rewardLicks,'color',data3.typeLP, 'group', group)

          d(3,2).facet_grid([], data3.Projection);
          
%         d(3,2).stat_summary('type','sem','geom','area');
%         d(3,2).set_line_options('base_size',linewidthSubj);
%         d(3,2).set_color_options('map', cmapSubj);
% 
% %         d(3,2).set_names('x','Session','y','Licks per Reward','color','Lever Side')

        d(3,2).no_legend(); %avoid duplicate legend from other plots (e.g. subject & grand colors)
           
        d(3,2).set_title('Forced Choice- Licks per Reward');
        
        d(3,2).draw()
           

        %------ btwn subj mean as well
        group= [];

%         d(3,2).update('x',data3.Session,'y',data3.rewardLicks,'color',data3.Projection, 'linestyle', data3.typeLP, 'group', group)
        d(3,2).update('x',data3.Session,'y',data3.rewardLicks,'color',data3.typeLP, 'group', group)

        d(3,2).stat_summary('type','sem','geom','area');

        d(3,2).set_names('x','Session','y','Licks per Reward','color','Projection')


        d(3,2).set_line_options('base_size',linewidthGrand);
        d(3,2).set_color_options('map', cmapGrand);
        d(3,2).no_legend(); %prevent legend duplicates if you like
        

          
        %~~~ 3,3 Test
        %subset data- by trainPhase       
        phasesToInclude= [4]; %list of phases to include 

        ind=[];

        ind= ismember(data0.trainPhase, phasesToInclude);

        data= data0(ind,:);
    
       %stack() - to make active/inactive a variable
        data2= stack(data, {'LicksPerReward', 'LicksPerRewardInactive'}, 'IndexVariableName', 'typeLP', 'NewDataVariableName', 'rewardLicks');

        %subset- by projection not necessary
        data3= data2;
        
        %cmap for Laser comparisons
        cmapGrand= cmapBlueGrayGrand;
        cmapSubj= cmapBlueGraySubj;   
        
   
        %------ btwn subj bar
        group= [];
%         group= data3.Projection

            %  2 sems for some reason here?
%         d(3,3).update('x',data3.trainPhaseLabel,'y',data3.rewardLicks,'color',data3.Projection, 'linestyle', data3.typeLP, 'group', group)
%         d(3,3)= gramm('x',data3.typeLP,'y',data3.rewardLicks,'color',data3.Projection, 'linestyle', data3.typeLP, 'group', group)
        d(3,3)= gramm('x',data3.Projection,'y',data3.rewardLicks,'color',data3.typeLP, 'group', group)

%         %add facet by projection
%         d(3,3).facet_grid([], data3.Projection);
        
%         d(3,3).stat_summary('type','sem','geom','bar');
        d(3,3).stat_summary('type','sem','geom',{'bar'}, 'dodge', dodge, 'width', width)%,'bar' 'black_errorbar'});

        
        d(3,3).set_names('x','Lever Type','y','Licks per Reward','color','Projection')

        d(3,3).set_title('Free Choice- Licks per Reward');

        d(3,3).set_line_options('base_size',linewidthGrand);
        d(3,3).set_color_options('map', cmapGrand);
        d(3,3).no_legend(); %prevent legend duplicates if you like
        
        % first draw
        d(3,3).draw()

    %-- individual subj points
        group= data3.Subject;

            %add style facet for active/inactive
%         d(3,3)=gramm('x',data3.trainPhaseLabel,'y',data3.rewardLicks,'color',data3.Projection, 'linestyle', data3.typeLP, 'group', group)

%           d(3,3).update('x',data3.typeLP,'y',data3.rewardLicks,'color',data3.Projection, 'group', group)
          d(3,3).update('x',data3.Projection,'y',data3.rewardLicks,'color',data3.typeLP, 'group', group)

%         d(3,3).stat_summary('type','sem','geom','area');
        d(3,3).stat_summary('type','sem','geom',{'point'}, 'dodge', dodge, 'width',width)%,'bar' 'black_errorbar'});

        d(3,3).set_line_options('base_size',linewidthSubj);
        d(3,3).set_color_options('map', cmapSubj);

%         d(3,3).set_names('x','Session','y','Licks per Reward','color','Lever Side')

        d(3,3).no_legend(); %avoid duplicate legend from other plots (e.g. subject & grand colors)
           
                
        d(3,3).draw;
        
        %- update with sem bar on top
        group=[];
        d(3,3).update('x',data3.Projection,'y',data3.rewardLicks,'color',data3.typeLP, 'group', group)

        d(3,3).stat_summary('type','sem','geom',{'black_errorbar'}, 'dodge', dodge, 'width', width)%,'bar' 'black_errorbar'});

        d(3,3).no_legend();
        %save last draw til end
        

        % --- Overall Fig things to do before final overall draw call ---
        d.set_text_options(text_options_DefaultStyle{:}); %apply default text sizes/styles

        titleFig= ('Fig 5');   
        d.set_title(titleFig); %overarching fig title must be set before first draw call

        

    %--- Final Draw call ---
        d.draw(); %Final Draw call
        
         figTitle= strcat('choiceTask-',thisExpTypeLabel,'-','Figure5-draft-',y);   
    
%          saveFig(gcf, figPath,figTitle,figFormats);



%% refactoring fig 5, unintelligible og draft

% highly manual, specific subplotting here


% %run separately based on stim vs inhibition
thisExpType=1;

expTypesAll= unique(choiceTaskTable.ExpType);
expTypeLabels= unique(choiceTaskTable.virusType);

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

       
%         d(1,1).stat_summary('type','sem','geom','area');
%         d(1,1).set_line_options('base_size',linewidthSubj);
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

%        
%         d(1,2).stat_summary('type','sem','geom','area');
%         d(1,2).set_line_options('base_size',linewidthSubj);
%         d(1,2).set_color_options('map', cmapSubj);
% 
%         d(1,2).set_names('x','Session','y','Number of Lever Presses','color','Lever Side')

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

%        
%         d(1,3).stat_summary('type','sem','geom','area');
%         d(1,3).set_line_options('base_size',linewidthSubj);
%         d(1,3).set_color_options('map', cmapSubj);

% %         d(1,3).set_names('x','Session','y','Proportion Active Lever Presses','color','Lever Side')
% % 
% %         d(1,3).no_legend(); %avoid duplicate legend from other plots (e.g. subject & grand colors)
           
        d(1,3).set_title('Acquistion- Active Proportion');
        
        d(1,3).axe_property('YLim',ylimProb);
        d(1,3).axe_property('YTick',yTickProb);

        
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

       
%         d(2,1).stat_summary('type','sem','geom','area');
%         d(2,1).set_line_options('base_size',linewidthSubj);
%         d(2,1).set_color_options('map', cmapSubj);
% 
% %         d(1,3).set_names('x','Session','y','Proportion Active Lever Presses','color','Lever Side')

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

       
%         d(2,2).stat_summary('type','sem','geom','area');
%         d(2,2).set_line_options('base_size',linewidthSubj);
%         d(2,2).set_color_options('map', cmapSubj);
% 
% %         d(1,3).set_names('x','Session','y','Proportion Active Lever Presses','color','Lever Side')

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
        
        %cmap for Laser comparisons
        cmapGrand= cmapBlueGrayGrand;
        cmapSubj= cmapBlueGraySubj;   
        
        %-- individual subj
        group= data3.Subject;

%         d(2,3)=gramm('x',data3.trainPhaseLabel,'y',data3.(y),'color',data3.Projection, 'group', group)

        d(2,3)=gramm('x',data3.Projection,'y',data3.(y),'color',data3.typeLP, 'group', group)

        %Facet by trainPhaseLabel
        d(2,3).facet_grid([], data3.trainPhaseLabel);
        
        
%        
%         d(2,3).stat_summary('type','sem','geom','area');
%         d(2,3).set_line_options('base_size',linewidthSubj);
%         d(2,3).set_color_options('map', cmapSubj);
% 
% %         d(1,3).set_names('x','Session','y','Proportion Active Lever Presses','color','Lever Side')

        d(2,3).no_legend(); %avoid duplicate legend from other plots (e.g. subject & grand colors)
           
        d(2,3).set_title('Free Choice- Active Proportion');
        
        d(2,3).draw()
           

        %------ btwn subj mean as well
        group= [];

%         d(2,3).update('x',data3.trainPhaseLabel,'y',data3.(y),'color',data3.Projection, 'group', group)
        d(2,3).update('x',data3.Projection,'y',data3.(y),'color',data3.typeLP, 'group', group)

%         d(2,3).stat_summary('type','sem','geom','area');
        d(2,3).stat_summary('type','sem','geom',{'bar', 'black_errorbar'}, 'dodge', dodge, 'width', width)%,'bar' 'black_errorbar'});


%         d(2,3).set_names('x','Projection','y','Proportion Active Lever Presses','color','LP type')
        d(2,3).set_names('x','Projection','y',y,'color','LP type')


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

%        
%         d(3,1).stat_summary('type','sem','geom','area');
%         d(3,1).set_line_options('base_size',linewidthSubj);
%         d(3,1).set_color_options('map', cmapSubj);
% 
% %         d(3,1).set_names('x','Session','y','Licks per Reward','color','Lever Side')

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

       
%         d(3,2).stat_summary('type','sem','geom','area');
%         d(3,2).set_line_options('base_size',linewidthSubj);
%         d(3,2).set_color_options('map', cmapSubj);
% 
% %         d(3,2).set_names('x','Session','y','Licks per Reward','color','Lever Side')

        d(3,2).no_legend(); %avoid duplicate legend from other plots (e.g. subject & grand colors)
           
        d(3,2).set_title('Forced Choice- Licks per Reward');
        
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
        phasesToInclude= [4]; %list of phases to include 

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
        
   
        %------ btwn subj bar
        group= [];
%         group= data3.Projection

            %  2 sems for some reason here?
%         d(3,3).update('x',data3.trainPhaseLabel,'y',data3.rewardLicks,'color',data3.Projection, 'linestyle', data3.typeLP, 'group', group)
        d(3,3)= gramm('x',data3.typeLP,'y',data3.rewardLicks,'color',data3.Projection, 'linestyle', data3.typeLP, 'group', group)

        
%         d(3,3).stat_summary('type','sem','geom','bar');
        d(3,3).stat_summary('type','sem','geom',{'bar', 'black_errorbar'}, 'dodge', dodge)%,'bar' 'black_errorbar'});

        
        d(3,3).set_names('x','Lever Type','y','Licks per Reward','color','Projection')


        d(3,3).set_line_options('base_size',linewidthGrand);
        d(3,3).set_color_options('map', cmapGrand);
        d(3,3).no_legend(); %prevent legend duplicates if you like
        
        % first draw
        d(3,3).draw()

    %-- individual subj points
        group= data3.Subject;

            %add style facet for active/inactive
%         d(3,3)=gramm('x',data3.trainPhaseLabel,'y',data3.rewardLicks,'color',data3.Projection, 'linestyle', data3.typeLP, 'group', group)

          d(3,3).update('x',data3.typeLP,'y',data3.rewardLicks,'color',data3.Projection, 'group', group)

%         d(3,3).stat_summary('type','sem','geom','area');
        d(3,3).stat_summary('type','sem','geom',{'point'}, 'dodge', dodge)%,'bar' 'black_errorbar'});

        d(3,3).set_line_options('base_size',linewidthSubj);
        d(3,3).set_color_options('map', cmapSubj);

%         d(3,3).set_names('x','Session','y','Licks per Reward','color','Lever Side')

        d(3,3).no_legend(); %avoid duplicate legend from other plots (e.g. subject & grand colors)
           
        d(3,3).set_title('Free Choice- Licks per Reward');
                   
        


        % --- Overall Fig things to do before final overall draw call ---
        d.set_text_options(text_options_DefaultStyle{:}); %apply default text sizes/styles

        titleFig= ('Fig 5');   
        d.set_title(titleFig); %overarching fig title must be set before first draw call

        

    %--- Final Draw call ---
        d.draw(); %Final Draw call
        
         figTitle= strcat('choiceTask-',thisExpTypeLabel,'-','Figure5-draft-',y);   
    
%          saveFig(gcf, figPath,figTitle,figFormats);


%% og version below
%% ==== DP Figure 5 2022-10-17 ----------------------

% highly manual, specific subplotting here


% %run separately based on stim vs inhibition
thisExpType=1;

expTypesAll= unique(choiceTaskTable.ExpType);
expTypeLabels= unique(choiceTaskTable.virusType);

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
        
        d(1,3).axe_property('YLim',ylimProb);
        d(1,3).axe_property('YTick',yTickProb);

        
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
        
        %-- individual subj points
        group= data3.Subject;

            %add style facet for active/inactive
        d(3,3)=gramm('x',data3.trainPhaseLabel,'y',data3.rewardLicks,'color',data3.Projection, 'linestyle', data3.typeLP, 'group', group)

       
%         d(3,3).stat_summary('type','sem','geom','area');
        d(3,3).stat_summary('type','sem','geom',{'point'}, 'dodge', dodge)%,'bar' 'black_errorbar'});

        d(3,3).set_line_options('base_size',linewidthSubj);
        d(3,3).set_color_options('map', cmapSubj);

%         d(3,3).set_names('x','Session','y','Licks per Reward','color','Lever Side')

        d(3,3).no_legend(); %avoid duplicate legend from other plots (e.g. subject & grand colors)
           
        d(3,3).set_title('Free Choice- Licks per Reward');
        
        d(3,3).draw()
           

        %------ btwn subj mean as well
        group= [];
%         group= data3.Projection

        d(3,3).update('x',data3.trainPhaseLabel,'y',data3.rewardLicks,'color',data3.Projection, 'linestyle', data3.typeLP, 'group', group)

%         d(3,3).stat_summary('type','sem','geom','bar');
        d(3,3).stat_summary('type','sem','geom',{'bar', 'black_errorbar'}, 'dodge', dodge)%,'bar' 'black_errorbar'});

        
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
    
%          saveFig(gcf, figPath,figTitle,figFormats);

%% EXPORT DATA FOR STATS ANALYSIS IN PYTHON/R



%% Save the figure

%-Declare Size of Figure at time of creation (up top), not time of saving.

%- Remove borders of UIpanels prior to save
p1.BorderType= 'none'
p2.BorderType= 'none'
p3.BorderType= 'none'
p4.BorderType= 'none'


%-Save the figure
titleFig='vp-vta_Figure5_uiPanels';
% saveFig(gcf, figPath, titleFig, figFormats, figSize);

