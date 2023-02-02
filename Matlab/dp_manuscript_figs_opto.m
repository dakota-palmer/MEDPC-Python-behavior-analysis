%% set output path & formats

figPath= "C:\Users\Dakota\Documents\GitHub\DS-Training\Matlab\_output\_Manuscript_Fig_mockups\"

%SVG good for exporting for final edits
% figFormats= {'.svg'} %list of formats to save figures as (for saveFig.m)

%PNG good for quickly viewing many
% figFormats= {'.png'} %list of formats to save figures as (for saveFig.m)
figFormats= {'.svg','.fig'} %list of formats to save figures as (for saveFig.m)


%% set gramm defaults
set_gramm_plot_defaults();

%% fig 4

dp_manuscript_figs_opto_Fig4();

%% fig 5