clear all
close all
clc

%% Figure options
figPath= strcat(pwd,'\_output\_ICSS\');

figFormats= {'.fig','.svg'} %list of formats to save figures as (for saveFig.m)



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
g(2,2)=gramm('x',ICSS.Session(selection),'y',ICSS.TotalLengthActiveNP(selection),'color',ICSS.Projection(selection))
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

title= 'ICSS_nosepoke_data_verified';
saveFig(gcf, figPath,title,figFormats);

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

title= 'ICSS_nosepoke_data_individuals_verified';
saveFig(gcf, figPath,title,figFormats);

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