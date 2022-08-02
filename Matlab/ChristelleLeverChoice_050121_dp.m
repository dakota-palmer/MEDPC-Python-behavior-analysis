clear all
close all
clc
%% Figure options
figPath= strcat(pwd,'\_output\_choiceTask\');

figFormats= {'.svg'} %list of formats to save figures as (for saveFig.m)



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

LeverChoice.Sessions=cell2mat(LeverChoice.Sessions)
LeverChoice.ActiveLeverPress=cell2mat(LeverChoice.ActiveLeverPress)
LeverChoice.InactiveLeverPress=cell2mat(LeverChoice.InactiveLeverPress)
LeverChoice.TrialsCompleted=cell2mat(LeverChoice.TrialsCompleted)
LeverChoice.ActiveLicks=cell2mat(LeverChoice.ActiveLicks)
LeverChoice.InactiveLicks=cell2mat(LeverChoice.InactiveLicks)

%% Elminates animals who didn't lever press enough


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

%% Plot total active vs inactive LP

figure %Stimulation
selection= LeverChoice.Expression==1 & LeverChoice.ExpType==1 &(strcmp(LeverChoice.Projection,'mdThal') | strcmp(LeverChoice.Projection,'VTA'));
g(1,1)=gramm('x',LeverChoice.Sessions(selection),'y',LeverChoice.ActiveLeverPress(selection),'color',LeverChoice.Projection(selection));
g(1,1).stat_summary('type','sem','geom','area');
g(1,1).no_legend();
g(1,1).set_names('x','Session','y','Number of Lever Presses','color','Laser(-)');
g(1,1).set_title('Total Lever Presses');
g(1,1).axe_property( 'YLim',[0 150],'XLim',[1 6]);

g(1,1).update('x',LeverChoice.Sessions(selection),'y',LeverChoice.InactiveLeverPress(selection),'color',LeverChoice.Projection(selection));
g(1,1).stat_summary('type','sem','geom','area');
g(1,1).no_legend();
g(1,1).set_names('x','Session','y','Number of Lever Presses','color','No Laser(--)')
g(1,1).set_title('Choice Task')
g(1,1).set_line_options( 'styles',{':'})


%Stimulation
selection= LeverChoice.Expression==1 & LeverChoice.ExpType==1 &(strcmp(LeverChoice.Projection,'mdThal') | strcmp(LeverChoice.Projection,'VTA'));
g(1,2)=gramm('x',LeverChoice.Sessions(selection),'y',LeverChoice.ActiveLeverPress(selection),'color',LeverChoice.Projection(selection))
g(1,2).stat_summary('type','sem','geom','area');
g(1,2).no_legend();
g(1,2).set_names('x','Session','y','Number of Lever Presses','color','Laser(-)');
g(1,2).set_title('Reversal');
g(1,2).axe_property('YLim',[0 150],'XLim', [7 12]);

g(1,2).update('x',LeverChoice.Sessions(selection),'y',LeverChoice.InactiveLeverPress(selection),'color',LeverChoice.Projection(selection));
g(1,2).stat_summary('type','sem','geom','area');
g(1,2).no_legend();
g(1,2).set_names('x','Session','y','Number of Lever Presses','color','No Laser(--)');
g(1,2).set_title('Choice Task');
g(1,2).set_line_options( 'styles',{':'});

selection= LeverChoice.Sessions==13 & LeverChoice.Expression==1 & LeverChoice.ExpType==1 &(strcmp(LeverChoice.Projection,'mdThal') | strcmp(LeverChoice.Projection,'VTA'));
g(1,3)=gramm('x',LeverChoice.Sessions(selection),'y',LeverChoice.ActiveLeverPress(selection),'color',LeverChoice.Projection(selection))
g(1,3).stat_boxplot(); 
g(1,3).set_names('x','Session','y','Number of Lever Presses','color','Laser');
%g(1,3).axe_property( 'YLim',[0 150],'XLim',[13 13]);
g(1,3).axe_property( 'YLim',[0 150])
g(1,3).set_title('Choice Session')

% selection= LeverChoice.Sessions==13 & LeverChoice.Expression==1 & LeverChoice.ExpType==1 &(strcmp(LeverChoice.Projection,'mdThal') | strcmp(LeverChoice.Projection,'VTA'));
% g(1,4)=gramm('x',LeverChoice.Sessions(selection),'y',LeverChoice.InactiveLeverPress(selection),'color',LeverChoice.Projection(selection));
% g(1,4).stat_boxplot(); 
% g(1,4).set_names('x','Session','y','Number of Lever Presses','color','No Laser(--)');
% %g(1,4).axe_property( 'YLim',[0 150],'XLim',[13 13]);
% g(1,4).set_title('Choice Session')


selection= LeverChoice.Sessions==13 & LeverChoice.Expression==1 & LeverChoice.ExpType==1 &(strcmp(LeverChoice.Projection,'mdThal') | strcmp(LeverChoice.Projection,'VTA'));
g(1,4)=gramm('x',LeverChoice.Sessions(selection),'y',LeverChoice.InactiveLeverPress(selection),'color',LeverChoice.Projection(selection))
g(1,4).stat_boxplot(); 
g(1,4).set_names('x','Session','y','Number of Lever Presses','color','No Laser');
g(1,4).axe_property( 'YLim',[0 150])
g(1,4).set_title('Choice Session')


selection= LeverChoice.Sessions==14 & LeverChoice.Expression==1 & LeverChoice.ExpType==1 &(strcmp(LeverChoice.Projection,'mdThal') | strcmp(LeverChoice.Projection,'VTA'));
g(1,5)=gramm('x',LeverChoice.Sessions(selection),'y',LeverChoice.ActiveLeverPress(selection),'color',LeverChoice.Projection(selection))
g(1,5).stat_boxplot(); 
g(1,5).axe_property( 'YLim',[0 150])
g(1,5).set_title('Extinction')
%g(1,5).axe_property( 'YLim',[0 150])
g(1,5).set_names('x','Session','y','Number of Lever Presses','color','Laser');

selection= LeverChoice.Sessions==14 & LeverChoice.Expression==1 & LeverChoice.ExpType==1 &(strcmp(LeverChoice.Projection,'mdThal') | strcmp(LeverChoice.Projection,'VTA'));
g(1,6)=gramm('x',LeverChoice.Sessions(selection),'y',LeverChoice.InactiveLeverPress(selection),'color',LeverChoice.Projection(selection))
g(1,6).stat_boxplot(); 
g(1,6).set_title('Extinction')
g(1,6).axe_property( 'YLim',[0 150])
g(1,6).set_names('x','Session','y','Number of Lever Presses','color','No Laser');


% % Plot proportion by projection
% 
% %Stimulation
selection= LeverChoice.Expression==1 & LeverChoice.ExpType==1 &(strcmp(LeverChoice.Projection,'mdThal') | strcmp(LeverChoice.Projection,'VTA'));
g(2,1)=gramm('x',LeverChoice.Sessions(selection),'y',LeverChoice.Proportion(selection),'color',LeverChoice.Projection(selection))
g(2,1).stat_summary('type','sem','geom','area');
g(2,1).no_legend();
g(2,1).set_names('x','Session','y','Probability','color','Stim(-)')
g(2,1).set_title('Probability by Projection')
g(2,1).axe_property( 'YLim',[0 1],'XLim', [1 6])


selection= LeverChoice.Expression==1 & LeverChoice.ExpType==1 &(strcmp(LeverChoice.Projection,'mdThal') | strcmp(LeverChoice.Projection,'VTA'));
g(2,2)=gramm('x',LeverChoice.Sessions(selection),'y',LeverChoice.Proportion(selection),'color',LeverChoice.Projection(selection))
g(2,2).stat_summary('type','sem','geom','area');
g(2,2).no_legend();
g(2,2).set_names('x','Session','y','Probability','color','Stim(-)')
g(2,2).set_title('Reversal')
g(2,2).axe_property( 'YLim',[0 1],'XLim', [7 12])

selection= LeverChoice.Sessions==13 & LeverChoice.Expression==1 & LeverChoice.ExpType==1 &(strcmp(LeverChoice.Projection,'mdThal') | strcmp(LeverChoice.Projection,'VTA'));
g(2,3)=gramm('x',LeverChoice.Sessions(selection),'y',LeverChoice.Proportion(selection),'color',LeverChoice.Projection(selection))
g(2,3).stat_boxplot(); 
g(2,3).set_names('x','Session','y','PRrobability','color','Laser');
g(2,3).axe_property( 'YLim',[0 1])
g(2,3).no_legend()
g(2,3).set_title('Choice Session')

selection= LeverChoice.Sessions==14 & LeverChoice.Expression==1 & LeverChoice.ExpType==1 &(strcmp(LeverChoice.Projection,'mdThal') | strcmp(LeverChoice.Projection,'VTA'));
g(2,4)=gramm('x',LeverChoice.Sessions(selection),'y',LeverChoice.Proportion(selection),'color',LeverChoice.Projection(selection))
g(2,4).stat_boxplot(); 
g(2,4).set_names('x','Session','y','Probability','color','Laser');
g(2,4).axe_property( 'YLim',[0 1])
g(2,4).no_legend()
g(2,4).set_title('Extinction')


% % Plot proportion by sex
% %Stimulation
% selection=LeverChoice.Expression==1 & LeverChoice.ExpType==1 &(strcmp(LeverChoice.Projection,'mdThal') | strcmp(LeverChoice.Projection,'VTA')) ;
% g(2,1)=gramm('x',LeverChoice.Sessions(selection),'y',LeverChoice.Proportion(selection),'color',LeverChoice.Projection(selection))
% g(2,1).stat_summary('type','sem','geom','area');
% g(2,1).facet_grid([],LeverChoice.Sex(selection))
% g(2,1).no_legend();
% g(2,1).set_names('x','Session','y','Probability','color','Projection(-)')
% g(2,1).set_title('Probability by Sex')
% g(2,1).axe_property( 'YLim',[0 1], 'XLim', [1 6])
% 
% g(2,1).update('x',LeverChoice.Sessions(selection),'y',LeverChoice.Proportion(selection),'color',LeverChoice.Projection(selection))
% g(2,1).stat_summary('type','sem','geom','area');
% g(2,1).no_legend();
% g(2,1).set_names('x','Session','y','Probability','color','Projection')
% g(2,1).set_title('Probability by Sex')
% g(2,1).set_line_options( 'styles',{':'})
% % 
% selection=LeverChoice.Expression==1 & LeverChoice.ExpType==1 &(strcmp(LeverChoice.Projection,'mdThal') | strcmp(LeverChoice.Projection,'VTA')) ;
% g(2,2)=gramm('x',LeverChoice.Sessions(selection),'y',LeverChoice.Proportion(selection),'color',LeverChoice.Projection(selection))
% g(2,2).stat_summary('type','sem','geom','area');
% g(2,2).facet_grid([],LeverChoice.Sex(selection))
% g(2,2).no_legend();
% g(2,2).set_names('x','Session','y','Probability','color','Projection(-)')
% g(2,2).set_title('Probability by Sex (Reversal)')
% g(2,2).axe_property( 'YLim',[0 1], 'XLim', [7 14])
% 
% g(2,2).update('x',LeverChoice.Sessions(selection),'y',LeverChoice.Proportion(selection),'color',LeverChoice.Projection(selection))
% g(2,2).stat_summary('type','sem','geom','area');
% g(2,2).no_legend();
% g(2,2).set_names('x','Session','y','Probability','color','Projection')
% g(2,2).set_title('Probability by Sex (Reversal)')
% g(2,2).set_line_options( 'styles',{':'})


% %% Plot Licks per reward 
%Projection
selection= LeverChoice.Expression==1 & LeverChoice.ExpType==1 &(strcmp(LeverChoice.Projection,'mdThal') | strcmp(LeverChoice.Projection,'VTA'));
g(2,5)=gramm('x',LeverChoice.Sessions(selection),'y',LeverChoice.LicksPerReward(selection),'color',LeverChoice.Projection(selection))
g(2,5).stat_summary('type','sem','geom','area');
g(2,5).no_legend();
g(2,5).set_names('x','Session','y','Licks per Reward','color','Stim(-)')
g(2,5).set_title('Licks per reward')
g(2,5).axe_property( 'YLim',[0 50],'XLim', [1 6])

g(2,5).update('x',LeverChoice.Sessions(selection),'y',LeverChoice.LicksPerRewardInactive(selection),'color',LeverChoice.Projection(selection))
g(2,5).stat_summary('type','sem','geom','area');
g(2,5).no_legend();
g(2,5).set_names('x','Session','y','Licks per Reward','color','No Stim(--)')
g(2,5).set_title('Licks per reward')
g(2,5).set_line_options( 'styles',{':'})

selection= LeverChoice.Expression==1 & LeverChoice.ExpType==1 &(strcmp(LeverChoice.Projection,'mdThal') | strcmp(LeverChoice.Projection,'VTA'));
g(2,6)=gramm('x',LeverChoice.Sessions(selection),'y',LeverChoice.LicksPerReward(selection),'color',LeverChoice.Projection(selection))
g(2,6).stat_summary('type','sem','geom','area');
g(2,6).no_legend();
g(2,6).set_names('x','Session','y','Licks per Reward','color','Stim(-)')
g(2,6).set_title('Licks per reward')
g(2,6).axe_property( 'YLim',[0 50],'XLim', [7 12])

g(2,6).update('x',LeverChoice.Sessions(selection),'y',LeverChoice.LicksPerRewardInactive(selection),'color',LeverChoice.Projection(selection))
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
% g=gramm('x',LeverChoice.Sessions(selection),'y',LeverChoice.LicksPerReward(selection),'color',LeverChoice.Projection(selection))
% g.stat_summary('type','sem','geom','area');
% g.facet_grid([],LeverChoice.Sex(selection))
% g.set_names('x','Session','y','Licks per Reward','color','Stim(-)')
% g.set_title('Stimulation Lever Choice Licks per reward--Sex')
% g.axe_property( 'YLim',[0 50])
% g.draw()
% 
% g.update('x',LeverChoice.Sessions(selection),'y',LeverChoice.LicksPerRewardInactive(selection),'color',LeverChoice.Projection(selection))
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
% g(2,1)=gramm('x',LeverChoice.Sessions(selection),'y',LeverChoice.ActiveLeverPress(selection),'color',LeverChoice.Subject(selection))
% g(2,1).stat_summary('type','sem','geom','area');
% g(2,1).set_names('x','Session','y','Number of Lever Presses','color','Stim(-)')
% g(2,1).set_title('Choice Task Individual Data')
% g(2,1).axe_property( 'YLim',[0 200], 'XLim', [1 6])
% 
% selection= LeverChoice.Expression==1 & LeverChoice.ExpType==1 &(strcmp(LeverChoice.Projection,'VTA'));
% g(2,2)=gramm('x',LeverChoice.Sessions(selection),'y',LeverChoice.ActiveLeverPress(selection),'color',LeverChoice.Subject(selection))
% g(2,2).stat_summary('type','sem','geom','area');
% g(2,2).set_names('x','Session','y','Number of Lever Presses','color','Stim(-)')
% g(2,2).set_title('Choice Task Individual Data')
% g(2,2).axe_property( 'YLim',[0 200],'XLim', [7 14])