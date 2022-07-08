
%% Set GRAMM defaults for plots

%--- Set some "Main"/"Default" settings for GRAMM plots
% Saving at once in single vars so dont have to always use
% so much code when constructing individual plots

%--- Altering things like color and text size in matlab can save 
% a ton of time vs. manually changing in external program 
% like illustrator 

%--- see Gramm Cheatsheet pdf for some of the specific arguments/methods/variables
% being saved & set below. Use the cheatsheet to find other variables to set and save more time 

%% - Default Text options

%Need to store mixed data types (str for argument/variable names and some num for values), so store as
%a cell array. 

% When you want to call on the gramm object to set_text_options, retrieve values with {:} like so:
    % g.set_text_options(text_options_MainStyle{:}); 

text_options_DefaultStyle= {'font'; 'Arial'; 
    'interpreter'; 'none'; 
    'base_size'; 22; 
    'label_scaling'; 1;
   'legend_scaling'; 1; 
   'legend_title_scaling'; 1.02;
   'facet_scaling'; 1.2; 
   'title_scaling'; 1.4;
   'big_title_scaling'; 1.4};

%% -- Default plot linestyles 
%To be used to set the 'base_size' of lines e.g. like:
%     d().set_line_options('base_size',linewidthSubj);

%may consider using the group argument in gramm as a logic gate for these (e.g. if group= subject, use subject settings, if group=[] use grand settings)

%thin, light lines for individual subj
linewidthSubj= 0.5;
lightnessRangeSubj= [100,100]; %lightness facet with lightness range doesn't work with custom colormap color facet? Issue is I think unknown/too many lightness 'categories' gramm wants to make but can't do it well for custom colors. would be nice if could use alpha but dont think this works... better to have distinct color


%dark, thick lines for between subj grand mean
linewidthGrand= 1.5;
lightnessRangeGrand= [10,10]; %lightness facet with lightness range doesn't work with custom colormap color facet? Issue is I think unknown/too many lightness 'categories' gramm wants to make but can't do it well for custom colors. would be nice if could use alpha but dont think this works... better to have distinct color


%% ------ Notes about faceting Color & Lightness ----------
 %- 2 strategies for plotting individual subject observations 'lighter' with darker
 % grand means:
 
 % 1) Use built in colormaps (ultimately not good in long run if you want to change colors). Using same map for individuals & mean plots but facet 'lightness' = subject.
 % This works well with built in gramm colormaps I think bc they can generate a lot of lightness categories (e.g. many subjects)
 
 % 2)*recommended* Use custom different map for individuals and mean plots without faceting
 % lightness. This way you have total control over the colors without
 % relying on gramm to figure out lightness categories. All you have to do
 % is define color map to use for each group 

%% -- Default built-in plot colormaps

%-brewer2 and brewerDark are two cmaps that are built-in and are good for
%plotting subjects, means respectively (different shades of same colors)
%if only 2 groupings being plotted, brewer2 and brewer_dark work well 
cmapSubj= 'brewer2';
cmapGrand= 'brewer_dark';

%% -- Custom Colormaps
%making some custom maps here for common comparisons in the Richard Lab.
%Will have 1 map with individual subj lightness and 1 darker map for grand mean
% consider that you may want another even lighter map with shades for
% individual trials/observations. want alternating distinct hues within each map for auto faceting

%Here's a good tool for making custom maps: 
% https://learnui.design/tools/data-color-picker.html
% also here are commonly used palettes with RGB https://public.tableau.com/views/TableauColors/ColorPaletteswithRGBValues?%3Aembed=y&%3AshowVizHome=no&%3Adisplay_count=y&%3Adisplay_static_image=y

%-- tab10 palette


%-- Cue Type cmap colormap for DS vs NS comparisons (7 class BrBG; teal blue vs. brown orange)
cmapCustomCue= [90,180,172; %dark teal
            199,234,229;
            245,245,245; %light teal 
            1,102,94 %neutral
            246,232,195; %light orange
            216,179,101;
            140,81,10;  %dark orange 
            ];
            
cmapCustomCue= cmapCustomCue/255;

cmapCueGrand= cmapCustomCue([1,7],:); %dark
cmapCueSubj= cmapCustomCue([2,5],:); %light


%--TODO: Active vs Inactive cmaps (e.g. laser-paired vs unpaired operand)

%- Blue vs. Grey
% based on colorbrewer2 5 class RdGy, replaced red w blues
cmapCustomRedGray= [202,0,32;
                244,165,130;
                255,255,255;
                186,186,186;
                64,64,64]

cmapCustomRedGray= cmapCustomRedGray/255;

            
cmapCustomBlueGray= [44,123,182;
    171,217,233;
    255,255,255;
    186,186,186;
    64,64,64]

cmapCustomBlueGray= cmapCustomBlueGray/255;


cmapBlueGrayGrand= cmapCustomBlueGray([1,5],:);
cmapBlueGraySubj= cmapCustomBlueGray([2,4],:);

%% if you want to specific colors from this map, remember each color is= RGB values so each row is 1 color and you can just index single row.
%alternatively for auto faceting you may need to reorganize the
%cmap order such that the colors alternate between hues (e.g. since
%gramm() will facet in order of the colors in the cmap)

%% old, additional custom colormap examples
%-- Also have made some custom maps, examples follow (made using colorbrewer2.org)
% all you need is to make the map you want on the site, copy the RGB values
% and divide by 255 for matlab to recognize them as a colormap 

%--- Custom colormap examples for plots

% - Custom colormap updated from below. want alternating distinct hues for auto faceting
% will make different maps with diff lightness for diff 'groups' (e.g. subject lighter vs darker grand means) 


% - Examples: Colormap for 465nm vs 405nm comparisons (7 class PRGn, purple vs green)
%green and purple %3 levels each, dark to light extremes + neutral middle
mapCustomFP= [ 27,120,55;
            127,191,123;
            217,240,211;
            247,247,247
            231,212,232
            175,141,195;
            118,42,131;
           ];

        mapCustomFP= mapCustomFP/255;
        
        %viz this colormap in colorbar to side of rgbplot
        figure();
        rgbplot(mapCustomFP);
        hold on
        colormap(mapCustomFP)
        colorbar('Ticks',[])
        title('mapCustomFP');

% - Colormap for DS vs NS comparisons (7 class BrBG; teal blue vs. brown orange)
cmapCustomCue= [90,180,172;
            199,234,229;
            245,245,245;
            1,102,94
            246,232,195;
            216,179,101;
            140,81,10;   
            ];
            
        cmapCustomCue= cmapCustomCue/255;

                %viz this colormap in colorbar to side of rgbplot
        figure();
        rgbplot(cmapCustomCue);
        hold on
        colormap(cmapCustomCue)
        colorbar('Ticks',[])
        title('mapCustomCue');

%%---- more complicated custom colormap with varying lightness notes ---
%% - If you want to use lightness faceting with gramm and custom maps, will need more complex:
% It is also possible to provide a custom
% colormap by providing a N-by-3 matrix (columns are R,G,B), with N
% corresponding to n_color categories times n_lightness categories (see
% below). Row ordering should be color#1/lightness#1 ; color#1/lightness#2 ;
% ... ; color#1/lightness#n ; color#2/lightness#1 ; ... ; color#n/lightness#n
%
% 'n_color' number of color categories when using a custom colormap
% 'n_lightness' number of lightness categories when using a custom colormap

%essentially every time you will need to tell gramm how many n_lightness
%per color are in the color map, which 1) means more code and 2) means more
%work generating the colormaps to begin with. 

%It should definitely possible tho with interpolation...not worth it atm

%% Attempt at custom map with big lightness range for lightness faceting
%- good start below but don't think it's worth it... 
% - trying some colormap interpolation for plenty of lightness categories

%pick two colors between which to interpolate colors for custom map
colorA= [90,180,172];
colorB= [140,81,10];
colorC= [1,102,94];


%will go between color A -- C -- B

% Create a matrix where each row is a color triple
T = [colorA         
     colorC        
     colorB]./255; 
% And now make a vector of what range each color should be at (i.e. this vector defines the spacing of the colours, they need not be regularly/equally spaced):

x = [0
     50
     100];
%  And finally you can create the entire map with one simple interpolation:

map = interp1(x/255,T,linspace(0,1,255));
 
 % test 
 I = linspace(0,1,255);
imagesc(I(ones(1,10),:)')
colormap(map)




%% CLOSE ALL example figures 
close all;