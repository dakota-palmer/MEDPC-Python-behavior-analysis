%% SIMPLIFIED; FIGURE 5 ACQUISITION ONLY

%- 2x2 panels

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



%% Aesthetics

% dodge/width for 2 categories
dodge=  0.05;
width= 1.9;


% Axes limits

% ylimLPcount= [0,155];
% 
% ylimActiveProportion= [0,40];


%% Initialize a figure with Drawable Area padding appropriately
% f = figure('Position',[100 100 1200 800])

% make figure of desired final size
f = figure('Position',figSize)

%- set size appropriately in cm
set(f, 'Units', 'centimeters', 'Position', figSize);
% outerpos makes it tighter, just in case UIpanels go over
set(f, 'Units', 'centimeters', 'OuterPosition', figSize);

% % % works well for pdf, not SVG (SVG is larger for some reason)
% % % but pdf still has big white space borders
% % % https://stackoverflow.com/questions/5150802/how-to-save-a-plot-into-a-pdf-file-without-a-large-margin-around
set(f, 'PaperPosition', [0, 0, figWidth, figHeight], 'PaperUnits', 'centimeters', 'Units', 'centimeters'); %Set the paper to have width 5 and height 5.

set(f, 'PaperUnits', 'centimeters', 'PaperSize', [figWidth, figHeight]); %Set the paper to have width 5 and height 5.



%% 2023-02-14 less licks


% highly manual, specific subplotting here
%JR: So the first row could be A) acquisition lever presses, B) acquisition proportion, C) acquisition licks
% Then reversal, forced choice and free choice test each for lever presses and active proportion (one row per measure?)

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
%         figure; clear d; 
        clear d;
        
        
        cmapSubj= cmapBlueGraySubj;
        cmapGrand= cmapBlueGrayGrand;
        
        %-- individual subj
        group= data3.Subject;

        d(2,1)=gramm('x',data3.Session,'y',data3.countLP,'color',data3.typeLP, 'group', group)

        d(2,1).facet_grid([], data3.Projection);
        
% %         d(1,2).stat_summary('type','sem','geom','area');
        d(2,1).set_line_options('base_size',linewidthSubj);
        d(2,1).set_color_options('map', cmapSubj);

        %- Things to do before first draw call-
        d(2,1).set_names('column', '', 'x', 'Time from Cue (s)','y','GCaMP (Z-score)','color','Trial type'); %row/column labels must be set before first draw call

        d(2,1).no_legend(); %avoid duplicate legend from other plots (e.g. subject & grand colors)
       
        d(2,1).set_text_options(text_options_DefaultStyle{:}); %apply default text sizes/styles

           %first draw call-
           
           
        ylimLPcount1= [0,100];
                        
        yTickLPcount1= [ylimLPcount1(1):20:ylimLPcount1(2)]; %steps

        d(2,1).axe_property('YLim',ylimLPcount1);
        d(2,1).axe_property('YTick',yTickLPcount1);
                
        
%         yTickProb= [0:0.2:1] % ticks every 0.2
%         g2.axe_property('YTick',yTickProb);

           
%         d(1,2).set_title('Acquistion');
        
        d(2,1).draw()
           

        %------ btwn subj mean as well
        group= [];

        d(2,1).update('x',data3.Session,'y',data3.countLP,'color',data3.typeLP, 'group', group)

        d(2,1).stat_summary('type','sem','geom','area');
%         d(2,1).stat_summary('type','sem','geom','area', 'dodge', dodge, 'width', width);

        d(2,1).set_names('x','Session','y','Number of Lever Presses','color','Lever Side', 'column', '')
    %     d.set_names('row','Target','column','Phase','x','Session','y','Number of Lever Presses','color','Lever Side')


        d(2,1).set_line_options('base_size',linewidthGrand);
        d(2,1).set_color_options('map', cmapGrand);
        d(2,1).no_legend(); %prevent legend duplicates if you like
        
        %need to leave something for final draw call to know all of the subplots. Either don't draw this update (max 1 update) or draw all initial subplots first prior to updates.
%         d(1,2).draw(); 



     %--- C) Acquisition Licks/Reward
     
        %~~~ 3,1 Reversal
        %subset data- by trainPhase
        phasesToInclude= [1]; %list of phases to include 

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

%         d(1,3)=gramm('x',data3.Session,'y',data3.rewardLicks,'color',data3.Projection, 'linestyle', data3.typeLP, 'group', group)

        % facet by virus
        d(1,2)=gramm('x',data3.Session,'y',data3.rewardLicks,'color',data3.typeLP, 'group', group)

        d(1,2).facet_grid([], data3.Projection)
%        
%         d(1,3).stat_summary('type','sem','geom','area');
        d(1,2).set_line_options('base_size',linewidthSubj);
        d(1,2).set_color_options('map', cmapSubj);
% 
% %         d(1,3).set_names('x','Session','y','Licks per Reward','color','Lever Side')

        d(1,2).no_legend(); %avoid duplicate legend from other plots (e.g. subject & grand colors)
           
%         d(1,3).set_title('Acquisition- Licks per Reward');
        
        ylimLickcount1= [0,50];
                
        yTickLickcount1= [ylimLickcount1(1):10:ylimLickcount1(2)]; %steps

        d(1,2).axe_property('YLim',ylimLickcount1);
        d(1,2).axe_property('YTick',yTickLickcount1);

                       
        d(1,2).set_text_options(text_options_DefaultStyle{:}); %apply default text sizes/styles

        d(1,2).set_names('x','Session','y','Licks per Reward','color','Projection', 'column', '')

        
        d(1,2).draw()
           

        %------ btwn subj mean as well
        group= [];

%         d(1,3).update('x',data3.Session,'y',data3.rewardLicks,'color',data3.Projection, 'linestyle', data3.typeLP, 'group', group)
        d(1,2).update('x',data3.Session,'y',data3.rewardLicks,'color',data3.typeLP, 'group', group)


        d(1,2).stat_summary('type','sem','geom','area');



        d(1,2).set_line_options('base_size',linewidthGrand);
        d(1,2).set_color_options('map', cmapGrand);
        d(1,2).no_legend(); %prevent legend duplicates if you like
        
    
    %---------- E) Acquisition  LP count
% 
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
%         %------ btwn subj bar first
%         group= [];
% 
% %         d(2,3).update('x',data3.trainPhaseLabel,'y',data3.(y),'color',data3.typeLP, 'group', group)
% %         d(2,3)= gramm('x',data3.Projection,'y',data3.(y),'color',data3.typeLP, 'group', group)
% %         d(2,3).facet_grid([], data3.trainPhaseLabel);
%         d(2,1)= gramm('x',data3.typeLP,'y',data3.(y),'color',data3.typeLP, 'group', group)
%         d(2,1).facet_grid([], data3.Projection);
% 
%         
% %         d(2,3).stat_summary('type','sem','geom','area');
%         d(2,1).stat_summary('type','sem','geom',{'bar'}, 'dodge', dodge, 'width', width)%,'bar' 'black_errorbar'});
% 
% 
% %         d(2,3).set_names('x','Session','y','Proportion Active Lever Presses','color','Projection')
% %         d(2,3).set_names('x','Session','y',y,'color','Projection')
%         d(2,1).set_names('x','Lever Side','y','Number of Lever Presses','color','Projection', 'column', '')
% 
% 
% %         d(2,3).set_title('Test- Active Proportion');
% 
%         d(2,1).set_line_options('base_size',linewidthGrand);
%         d(2,1).set_color_options('map', cmapGrand);
%         d(2,1).no_legend(); %prevent legend duplicates if you like
%         
%         ylimLPcount4= [0,170];
%         yTickLPcount4= [ylimLPcount4(1):25:ylimLPcount4(2)]; %steps
%         
%         d(2,1).axe_property('YLim',ylimLPcount4);        
%         d(2,1).axe_property('YTick',yTickLPcount4);        
% 
%         d(2,1).set_text_options(text_options_DefaultStyle{:}); %apply default text sizes/styles
% 
%         d(2,1).geom_hline('yintercept',0.5, 'style', 'k--', 'linewidth', linewidthReference); %overlay t=0
% 
%         d(2,1).draw();
% %         d(1,3).draw(); %Leave for final draw call     
% 
%    %-- individual subj points over
%         group= data3.Subject;
% 
% % %         d(2,3)=gramm('x',data3.trainPhaseLabel,'y',data3.(y),'color',data3.typeLP, 'group', group)
% % % 
% % %         Facet by Projection target
% % %         d(2,3).facet_grid([], data3.Projection);
% % % 
%         d(2,1).update('x',data3.typeLP,'y',data3.(y),'color',data3.typeLP, 'group', group)
%         
%         %Facet by trainPhase target
% %         d(2,3).facet_grid([], data3.trainPhaseLabel, 'scale', 'independent');
% %           d(2,3).facet_grid([], data3.trainPhaseLabel);
% 
% %        
% %         d(2,3).stat_summary('type','sem','geom','area');
%         d(2,1).geom_point('dodge',dodge);
%         d(2,1).set_line_options('base_size',linewidthSubj);
%         d(2,1).set_color_options('map', cmapSubj);
%                 
%   % 
% % %         d(1,3).set_names('x','Session','y','Proportion Active Lever Presses','color','Lever Side')
% 
%         d(2,1).no_legend(); %avoid duplicate legend from other plots (e.g. subject & grand colors)
%            
%         
%         d(2,1).draw()
%         
%         
%         %-- connect ind subj lines
%         group= data3.Subject
%         d(2,1).update('x',data3.typeLP,'y',data3.(y),'color',[], 'group', group)
% 
%  
% % %         d(2,3).stat_summary('geom',{'line'});
%         d(2,1).geom_line('alpha',0.3, 'dodge', dodge);
%         d(2,1).set_line_options('base_size',linewidthSubj);
% 
%         d(2,1).set_color_options('chroma', 0); %black lines connecting points
%         d(2,1).no_legend(); %prevent legend duplicates if you like
% 
%         d(2,1).draw()

        
        
%         %- error bar on top
%         group= [];
% 
%         d(2,1).update('x',data3.typeLP,'y',data3.(y),'color',data3.typeLP, 'group', group)
%         d(2,1).stat_summary('type','sem','geom',{'black_errorbar'}, 'dodge', dodge, 'width', width)%,'bar' 'black_errorbar'});
% 
%         d(2,1).no_legend();
        
        %--- LAST ROW ---- ACTIVE PROPORTION
        
        %-- Acquisition active proportion
        
        %subset data- by trainPhase
        phasesToInclude= [1]; %list of phases to include 

        ind=[];

        ind= ismember(data0.trainPhase, phasesToInclude);

        data= data0(ind,:);
    
        data2= data

        %subset- by projection not necessary
        data3= data2;
        
% %         %         %- count
% %         y= 'countLP'
% % 
% % % %         stack() to make inactive/active LP a variable
% %         data3= stack(data3, {'ActiveLeverPress', 'InactiveLeverPress'}, 'IndexVariableName', 'typeLP', 'NewDataVariableName', 'countLP');
% 
%         % - proportion 
% %        stack() to make inactive/active LP a variable
%         data3= stack(data3, {'probActiveLP', 'probInactiveLP'}, 'IndexVariableName', 'typeLP', 'NewDataVariableName', 'probLP');
% 
%         y= 'probLP'
        
        %- proportion (active only)
        y= 'probActiveLP'


        %cmap for Projection comparisons
        cmapGrand= 'brewer_dark';
        cmapSubj= 'brewer2';   
        
        %-- individual subj
        group= data3.Subject;

        d(2,2)=gramm('x',data3.Session,'y',data3.(y),'color',data3.Projection, 'group', group)

       
% %         d(3,1).stat_summary('type','sem','geom','area');
%         d(3,1).geom_line();
        d(2,2).set_line_options('base_size',linewidthSubj);
        d(2,2).set_color_options('map', cmapSubj);
% 
% %         d(1,2).set_names('x','Session','y','Proportion Active Lever Presses','color','Lever Side')

        d(2,2).no_legend(); %avoid duplicate legend from other plots (e.g. subject & grand colors)
           
%         d(3,1).set_title('Reversal- Active Proportion');
        
%         ylimLPproportion2= [0,1];
%         yTickLPproportion2= [ylimLPproportion2(1):.2:ylimLPproportion2(2)]; %steps
%         
        ylimLPproportion2= [0.3,0.8];
        yTickLPproportion2= [ylimLPproportion2(1):.1:ylimLPproportion2(2)]; %steps
        

        d(2,2).axe_property('YLim',ylimLPproportion2);        
        d(2,2).axe_property('YTick',yTickLPproportion2);        

        d(2,2).set_text_options(text_options_DefaultStyle{:}); %apply default text sizes/styles

        d(2,2).set_names('x','Session','y','Proportion Active Lever Presses','color','Projection', 'column', '')

        d(2,2).draw()
           

        %------ btwn subj mean as well
        group= [];

        d(2,2).update('x',data3.Session,'y',data3.(y),'color',data3.Projection, 'group', group)

        d(2,2).stat_summary('type','sem','geom','area');

       
        d(2,2).set_line_options('base_size',linewidthGrand);
        d(2,2).set_color_options('map', cmapGrand);
        d(2,2).no_legend(); %prevent legend duplicates if you like
        
        d(2,2).geom_hline('yintercept',0.5, 'style', 'k--', 'linewidth', linewidthReference); %overlay t=0

        
%         d(1,2).draw(); %Leave for final draw call

    
        
    % % FINAL DRAW
        d.draw()
        
%% Save the figure

%-Declare Size of Figure at time of creation (up top), not time of saving.

% %- Remove borders of UIpanels prior to save
% p1.BorderType= 'none'
% p2.BorderType= 'none'
% p3.BorderType= 'none'
% p4.BorderType= 'none'

%- set size appropriately in cm
set(f, 'Units', 'centimeters', 'Position', figSize);
% outerpos makes it tighter, just in case UIpanels go over
set(f, 'Units', 'centimeters', 'OuterPosition', figSize);

% % % works well for pdf, not SVG (SVG is larger for some reason)
% % % but pdf still has big white space borders
% % % https://stackoverflow.com/questions/5150802/how-to-save-a-plot-into-a-pdf-file-without-a-large-margin-around
set(f, 'PaperPosition', [0, 0, figWidth, figHeight], 'PaperUnits', 'centimeters', 'Units', 'centimeters'); %Set the paper to have width 5 and height 5.

set(f, 'PaperUnits', 'centimeters', 'PaperSize', [figWidth, figHeight]); %Set the paper to have width 5 and height 5.



%-Save the figure
titleFig='vp-vta_Figure5_Simplified_uiPanels';
saveFig(gcf, figPath, titleFig, figFormats, figSize);

    
        