%% set output path & formats

figPath= "C:\Users\Dakota\Documents\GitHub\DS-Training\Matlab\_output\_Manuscript_Fig_mockups\"

%SVG good for exporting for final edits
% figFormats= {'.svg'} %list of formats to save figures as (for saveFig.m)

%PNG good for quickly viewing many
% figFormats= {'.png'} %list of formats to save figures as (for saveFig.m)
% figFormats= {'.svg','.fig'} %list of formats to save figures as (for saveFig.m)

% % pdf seems to save at appropriate size but svg wont?
% https://www.mathworks.com/matlabcentral/answers/519666-size-of-exported-svg-incorrect
figFormats= {'.svg', '.pdf'} %list of formats to save figures as (for saveFig.m)
% figFormats= {'.pdf'} %list of formats to save figures as (for saveFig.m)


%% set gramm defaults
set_gramm_plot_defaults();

close all;

%% fig 4 - DS task + opto

dp_manuscript_figs_opto_Fig4();

%% fig 5 - Lever choice task
% dp_manuscript_figs_opto_Fig5();
fig5_new();

%% Fig 6 - ICSS 
% dp_manuscript_figs_opto_Fig6();
fig6_new();