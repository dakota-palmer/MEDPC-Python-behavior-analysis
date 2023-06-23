
###### enter python env ####
Sys.setenv(RETICULATE_PYTHON = "C:/Users/Dakota/anaconda3/envs/spyder-env-seaborn-update")

pd <- import("pandas")


#%%-- Import dependencies ####
# library(lme4)
library(reticulate)
library(lmerTest)
library(emmeans)

#%% -- Set Paths ####

#- NOTE: manually change working directory in RStudio to source file location! (up top session -> set working directory -> to source file location)
# https://statisticsglobe.com/set-working-directory-to-source-file-location-automatically-in-rstudio

#-Note: To read .pickles, pandas version in R environment has to match pandas version of .pkl created!

pathWorking= getwd()

pathOutput= paste(pathWorking,'/_output', sep="")
#get rid of space introduced by paste()
gsub(" ", "", pathOutput)


# __________________________________________________ ####


#%- Fig 6 Stats A/B-- OG Side, Acquisition Phase ####

#0%%-- Clear vars between tests ####
# #clear workspace (R environment) # Except paths, Python packages (pandas)
rm(list = setdiff(ls(), c("pathWorking", "pathOutput", "pd")))


#1%%-- Load data from .pkl ####

pathData <- "C:\\Users\\Dakota\\Documents\\GitHub\\FP-analysis\\python\\_output\\fig6.pkl"

df <- pd$read_pickle(pathData)


###### summarize data
summary(df)

#verify dtypes imported properly
sapply(df, class)

#%% Figure 4D Stats A -- Laser Sessions

#%%-- Subset data ##
#Remove missing/invalid observations
#- eliminate duplicate proportion values 
# currently active proportion is session level but df has 2 per session (1 per npType)
# so just remove from one trialType. This way can use same df for multiple models easily
df[df$typeNP=='InactiveNP','npActiveProportion']= NaN



# #- Subset by session type 
df_Sub_A= df[df$trainPhase == 'ICSS-OG-active-side',]


df_Sub_A_VTA= df_Sub_A[df_Sub_A$Projection=='VTA',]

df_Sub_A_mdThal= df_Sub_A[df_Sub_A$Projection=='mdThal',]


#since we've dropped levels(categories) from the factor(categorical) variable trainDayThisPhase, drop accordingly for stats to work out
# droplevels(df_Sub_A$trainDayThisPhase)
# droplevels(df_Sub_A$trainPhase)


#2%%-- Run LME ####

#-- Pooled
# model= lmerTest::lmer('countNP ~ Projection * typeNP * Session *  trainPhase + (1|Subject)', data=df_Sub_A)
model= lmerTest::lmer('countNP ~ Projection * typeNP * Session + (1|Subject)', data=df_Sub_A)

modelProportion= lmerTest::lmer('npActiveProportion ~ Projection * Session + (1|Subject)', data=df_Sub_A)

model_pooled= model
model_anova_pooled<- anova(model)
modelProportion_pooled= modelProportion
modelProportion_anova_pooled= anova(modelProportion)


#-- VTA
#VTA projection
#-Count
model_VTA= lmerTest::lmer('countNP ~ typeNP * Session  + (1|Subject)', data=df_Sub_A_VTA)
model_anova_VTA<- anova(model_VTA)
#-Proportion
modelProportion_VTA= lmerTest::lmer('npActiveProportion ~ Session + (1|Subject)', data=df_Sub_A_VTA)
modelProportion_anova_VTA<- anova(modelProportion_VTA)

#-- mdThal
#mdThal projection
#-Probability
model_mdThal= lmerTest::lmer('countNP ~ typeNP * Session  + (1|Subject)', data=df_Sub_A_mdThal)
model_anova_mdThal<- anova(model_mdThal)
#-Proportion
modelProportion_mdThal= lmerTest::lmer('npActiveProportion ~ Session + (1|Subject)', data=df_Sub_A_mdThal)
modelProportion_anova_mdThal<- anova(modelProportion_mdThal)



# -- Interaction plot
#- Viz interaction plot & save
figName= "vp-vta_fig6_stats_A_npCount_Session_pooled_interactionPlot.pdf"
setwd(pathOutput)
pdf(file=figName)

emmip(model_pooled, Session ~ typeNP | Projection )

# emmip(model_pooled, Projection ~ typeNP | Session )


dev.off()
setwd(pathWorking)

#pooled proportion interaction plot
figName= "vp-vta_fig6_stats_B_proportion_pooled_interactionPlot.pdf"
setwd(pathOutput)
pdf(file=figName)

emmip(modelProportion_pooled, Session ~ Projection )

dev.off()
setwd(pathWorking)


#3%%-- Run Follow-up post-hoc tests ####

# Pairwise comparisons between Sessions

#-- Pooled
EMM <- emmeans(model_pooled, ~ typeNP | Session | Projection)   # where treat has 2 levels
tPairwise= pairs(EMM, adjust = "sidak")   # adjustment is ignored - only 1 test per group
summary(tPairwise, by = NULL, adjust = "sidak")   # all are in one group now

tPairwise_Pooled= tPairwise

  #pooled followup tests reveal significant differences in npCount by npType in VTA session 3,4,5

EMM <- emmeans(modelProportion_pooled, ~ Session | Projection)   # where treat has 2 levels
tPairwise= pairs(EMM, adjust = "sidak")   # adjustment is ignored - only 1 test per group
summary(tPairwise, by = NULL, adjust = "sidak")   # all are in one group now

tPairwise_proportion_Pooled= tPairwise

# for active proportion, check if each level significantly different from 0.5 (chance)
t_Proportion_Pooled= test(EMM, null=0.5, adjust='sidak')




#-- VTA
#-npCount
EMM <- emmeans(model_VTA, ~ typeNP | Session)   # where treat has 2 levels
tPairwise= pairs(EMM, adjust = "sidak")   # adjustment is ignored - only 1 test per group
summary(tPairwise, by = NULL, adjust = "sidak")   # all are in one group now

tPairwise_VTA= tPairwise
  
#-npActiveProportion
EMM <- emmeans(modelProportion_VTA, ~ Session)   # where treat has 2 levels
tPairwise= pairs(EMM, adjust = "sidak")   # adjustment is ignored - only 1 test per group
summary(tPairwise, by = NULL, adjust = "sidak")   # all are in one group now

tPairwise_proportion_VTA= tPairwise

# for active proportion, check if each level significantly different from 0.5 (chance)
t_Proportion_VTA= test(EMM, null=0.5, adjust='sidak')


# for active proportion, check if each level significantly different from 0.5 (chance)
#example test() with emmeans here- https://cran.r-project.org/web/packages/emmeans/vignettes/confidence-intervals.html
# example of how to do 1 sample t test at each level with emmmeans 

test2= test(EMM, null=0.5, adjust='sidak')


#-- mdThal

#-npCount
EMM <- emmeans(model_mdThal, ~ typeNP | Session)   # where treat has 2 levels
tPairwise= pairs(EMM, adjust = "sidak")   # adjustment is ignored - only 1 test per group
summary(tPairwise, by = NULL, adjust = "sidak")   # all are in one group now

tPairwise_mdThal= tPairwise

#-npActiveProportion
EMM <- emmeans(modelProportion_mdThal, ~ Session)   # where treat has 2 levels
tPairwise= pairs(EMM, adjust = "sidak")   # adjustment is ignored - only 1 test per group
summary(tPairwise, by = NULL, adjust = "sidak")   # all are in one group now

tPairwise_proportion_mdThal= tPairwise

# for active proportion, check if each level significantly different from 0.5 (chance)
t_Proportion_mdThal= test(EMM, null=0.5, adjust='sidak')


#4%%-- Save output to variables between tests  ####
# trying to keep code mostly generalizable and just save custom names at end
# all the results into descriptive variables between tests

#-pooled
fig6_stats_Acquisition_A_Pooled_0_description= "Figure 6: ICSS, OG Active Side, Active vs Inactive NP Count, pooled projections"
fig6_stats_Acquisition_A_Pooled_1_model= model_pooled
fig6_stats_Acquisition_A_Pooled_2_model_anova= model_anova_pooled
fig6_stats_Acquisition_A_Pooled_3_model_post_hoc_pairwise= tPairwise_Pooled

fig6_stats_Acquisition_B_Pooled_0_description= "Figure 6: ICSS, OG Active Side, Active NP Proportion, pooled projections"
fig6_stats_Acquisition_B_Pooled_1_model= modelProportion_pooled
fig6_stats_Acquisition_B_Pooled_2_model_anova= modelProportion_anova_pooled
fig6_stats_Acquisition_B_Pooled_3_model_post_hoc_t= t_Proportion_Pooled

#-VTA
fig6_stats_Acquisition_A_VTA_0_description= "Figure 6: ICSS, OG Active Side, Active vs Inactive NP Count, VTA projections"
fig6_stats_Acquisition_A_VTA_1_model= model_VTA
fig6_stats_Acquisition_A_VTA_2_model_anova= model_anova_VTA
fig6_stats_Acquisition_A_VTA_3_model_post_hoc_pairwise= tPairwise_VTA

fig6_stats_Acquisition_B_VTA_0_description= "Figure 6: ICSS, OG Active Side, Active NP Proportion, VTA projections"
fig6_stats_Acquisition_B_VTA_1_model= modelProportion_VTA
fig6_stats_Acquisition_B_VTA_2_model_anova= modelProportion_anova_VTA
fig6_stats_Acquisition_B_VTA_3_model_post_hoc_t= t_Proportion_VTA

#-mdThal
fig6_stats_Acquisition_A_mdThal_0_description= "Figure 6: ICSS, OG Active Side, Active vs Inactive NP Count, mdThal projections"
fig6_stats_Acquisition_A_mdThal_1_model= model_mdThal
fig6_stats_Acquisition_A_mdThal_2_model_anova= model_anova_mdThal
fig6_stats_Acquisition_A_mdThal_3_model_post_hoc_pairwise= tPairwise_mdThal

fig6_stats_Acquisition_B_mdThal_0_description= "Figure 6: ICSS, OG Active Side, Active NP Proportion, mdThal projections"
fig6_stats_Acquisition_B_mdThal_1_model= modelProportion_mdThal
fig6_stats_Acquisition_B_mdThal_2_model_anova= modelProportion_anova_mdThal
fig6_stats_Acquisition_B_mdThal_3_model_post_hoc_t= t_Proportion_mdThal



#5%% -- Figure 6 Save output ####

#- move to output directory prior to saving
setwd(pathOutput)

#------Pooled

sink("vp-vta_fig6_stats_Acquisition_A_npCount_Pooled.txt")
'------------------------------------------------------------------------------'
'0)---- Description --: '
print(fig6_stats_Acquisition_A_Pooled_0_description)
'------------------------------------------------------------------------------'
print('1)---- LME:')
print(summary(fig6_stats_Acquisition_A_Pooled_1_model))
'------------------------------------------------------------------------------'
print('2)---- ANOVA of LME:')
print(fig6_stats_Acquisition_A_Pooled_2_model_anova)
'------------------------------------------------------------------------------'
# print('3)---- Posthoc pairwise:') # Make sure for posthocs the summary is printed with pval correction
# print(fig6C_stats_A_3_model_post_hoc_pairwise)
'---- END ---------------------------------------------------------------------'
sink()  # returns output to the console


sink("vp-vta_fig6_stats_Acquisition_B_proportion_Pooled.txt")
'------------------------------------------------------------------------------'
'0)---- Description --: '
print(fig6_stats_Acquisition_B_Pooled_0_description)
'------------------------------------------------------------------------------'
print('1)---- LME:')
print(summary(fig6_stats_Acquisition_B_Pooled_1_model))
'------------------------------------------------------------------------------'
print('2)---- ANOVA of LME:')
print(fig6_stats_Acquisition_B_Pooled_2_model_anova)
'------------------------------------------------------------------------------'
# print('3)---- Posthoc pairwise:') # Make sure for posthocs the summary is printed with pval correction
# print(summary(fig6C_stats_A_VTA_3_model_post_hoc_pairwise, by = NULL, adjust = "sidak"))
'---- END ---------------------------------------------------------------------'
sink()  # returns output to the console


#------ VTA

sink("vp-vta_fig6_stats_Acquisition_A_npCount_VTA.txt")
'------------------------------------------------------------------------------'
'0)---- Description --: '
print(fig6_stats_Acquisition_A_VTA_0_description)
'------------------------------------------------------------------------------'
print('1)---- LME:')
print(summary(fig6_stats_Acquisition_A_VTA_1_model))
'------------------------------------------------------------------------------'
print('2)---- ANOVA of LME:')
print(fig6_stats_Acquisition_A_VTA_2_model_anova)
'------------------------------------------------------------------------------'
print('3)---- Posthoc pairwise:') # Make sure for posthocs the summary is printed with pval correction
print(summary(fig6_stats_Acquisition_A_VTA_3_model_post_hoc_pairwise, by = NULL, adjust = "sidak"))
'---- END ---------------------------------------------------------------------'
sink()  # returns output to the console


sink("vp-vta_fig6_stats_Acquisition_B_proportion_VTA.txt")
'------------------------------------------------------------------------------'
'0)---- Description --: '
print(fig6_stats_Acquisition_B_VTA_0_description)
'------------------------------------------------------------------------------'
print('1)---- LME:')
print(summary(fig6_stats_Acquisition_B_VTA_1_model))
'------------------------------------------------------------------------------'
print('2)---- ANOVA of LME:')
print(fig6_stats_Acquisition_B_VTA_2_model_anova)
'------------------------------------------------------------------------------'
print('3)---- Posthoc t tests:') # Make sure for posthocs the summary is printed with pval correction
print(fig6_stats_Acquisition_B_VTA_3_model_post_hoc_t, by = NULL, adjust = "sidak")
'---- END ---------------------------------------------------------------------'
sink()  # returns output to the console


#------ mdThal

sink("vp-vta_fig6_stats_Acquisition_A_npCount_mdThal.txt")
'------------------------------------------------------------------------------'
'0)---- Description --: '
print(fig6_stats_Acquisition_A_mdThal_0_description)
'------------------------------------------------------------------------------'
print('1)---- LME:')
print(summary(fig6_stats_Acquisition_A_mdThal_1_model))
'------------------------------------------------------------------------------'
print('2)---- ANOVA of LME:')
print(fig6_stats_Acquisition_A_mdThal_2_model_anova)
'------------------------------------------------------------------------------'
print('3)---- Posthoc pairwise:') # Make sure for posthocs the summary is printed with pval correction
print(fig6_stats_Acquisition_A_mdThal_3_model_post_hoc_pairwise, by = NULL, adjust = "sidak")
'---- END ---------------------------------------------------------------------'
sink()  # returns output to the console


sink("vp-vta_fig6_stats_Acquisition_B_proportion_mdThal.txt")
'------------------------------------------------------------------------------'
'0)---- Description --: '
print(fig6_stats_Acquisition_B_mdThal_0_description)
'------------------------------------------------------------------------------'
print('1)---- LME:')
print(summary(fig6_stats_Acquisition_B_mdThal_1_model))
'------------------------------------------------------------------------------'
print('2)---- ANOVA of LME:')
print(fig6_stats_Acquisition_B_mdThal_2_model_anova)
'------------------------------------------------------------------------------'
print('3)---- Posthoc t tests:') # Make sure for posthocs the summary is printed with pval correction
print(fig6_stats_Acquisition_B_mdThal_3_model_post_hoc_t, by = NULL, adjust = "sidak")
'---- END ---------------------------------------------------------------------'
sink()  # returns output to the console


#- return to working directory after saving
setwd(pathWorking)






# __________________________________________________ ####


#%- Fig 6 Stats A/B-- Final Session, OG Side, Acquisition Phase ####


#0%%-- Clear vars between tests ####
# #clear workspace (R environment) # Except paths, Python packages (pandas)
rm(list = setdiff(ls(), c("pathWorking", "pathOutput", "pd")))


#1%%-- Load data from .pkl ####

pathData <- "C:\\Users\\Dakota\\Documents\\GitHub\\FP-analysis\\python\\_output\\fig6.pkl"

df <- pd$read_pickle(pathData)


###### summarize data
summary(df)

#verify dtypes imported properly
sapply(df, class)

#%% Figure 4D Stats A -- Laser Sessions

#%%-- Subset data ##
#Remove missing/invalid observations
#- eliminate duplicate proportion values 
# currently active proportion is session level but df has 2 per session (1 per npType)
# so just remove from one trialType. This way can use same df for multiple models easily
df[df$typeNP=='InactiveNP','npActiveProportion']= NaN


# #- Subset by session type 
df_Sub_A= df[df$trainPhase == 'ICSS-OG-active-side',]

# -- Subset to final session ONLY
df_Sub_A_finalSes= df_Sub_A[df_Sub_A$Session==5,]


df_Sub_A_finalSes_VTA= df_Sub_A_finalSes[df_Sub_A_finalSes$Projection=='VTA',]

df_Sub_A_finalSes_mdThal= df_Sub_A_finalSes[df_Sub_A_finalSes$Projection=='mdThal',]



#since we've dropped levels(categories) from the factor(categorical) variable trainDayThisPhase, drop accordingly for stats to work out
# droplevels(df_Sub_A_finalSes$trainDayThisPhase)
# droplevels(df_Sub_A_finalSes$trainPhase)


#2%%-- Run LME ####

#-- Pooled
# model= lmerTest::lmer('countNP ~ Projection * typeNP * Session *  trainPhase + (1|Subject)', data=df_Sub_A_finalSes)
model= lmerTest::lmer('countNP ~ Projection * typeNP  + (1|Subject)', data=df_Sub_A_finalSes)

# # for proportion only 1 observation per subj so cant be mixed effect, and cant run lmerTest lmer() without mixed effects so just lm
# modelProportion= lmerTest::lmer('npActiveProportion ~ Projection + (1|Subject)', data=df_Sub_A_finalSes)
# really just need 1 sample t test here
modelProportion= lm('npActiveProportion ~ Projection', data=df_Sub_A_finalSes)

model_pooled= model
model_anova_pooled<- anova(model)
modelProportion_pooled= modelProportion
modelProportion_anova_pooled= anova(modelProportion)


#-- VTA
#VTA projection
#-Count
model_VTA= lmerTest::lmer('countNP ~ typeNP  + (1|Subject)', data=df_Sub_A_finalSes_VTA)
model_anova_VTA<- anova(model_VTA)
#-Proportion
# modelProportion_VTA= lmerTest::lmer('npActiveProportion ~ Session + (1|Subject)', data=df_Sub_A_finalSes_VTA)
modelProportion_VTA= lm('npActiveProportion ~ Subject', data=df_Sub_A_finalSes_VTA)

# # Only 1 observation per subject so need for model/anova, just t test 
# modelProportion_anova_VTA<- anova(modelProportion_VTA)

#-- mdThal
#mdThal projection
#-Probability
model_mdThal= lmerTest::lmer('countNP ~ typeNP  + (1|Subject)', data=df_Sub_A_finalSes_mdThal)
model_anova_mdThal<- anova(model_mdThal)
#-Proportion
# modelProportion_mdThal= lmerTest::lmer('npActiveProportion ~ Session + (1|Subject)', data=df_Sub_A_finalSes_mdThal)
modelProportion_mdThal= lm('npActiveProportion ~ Subject', data=df_Sub_A_finalSes_mdThal)

# # Only 1 observation per subject so need for model/anova, just t test 



# -- Interaction plot
#- Viz interaction plot & save
figName= "vp-vta_fig6_stats_A_npCount_finalSes_pooled_interactionPlot.pdf"
setwd(pathOutput)
pdf(file=figName)

emmip(model_pooled, ~ typeNP | Projection )

# emmip(model_pooled, Projection ~ typeNP | Session )


dev.off()
setwd(pathWorking)

#pooled proportion interaction plot
figName= "vp-vta_fig6_stats_B_proportion_finalSes_pooled_interactionPlot.pdf"
setwd(pathOutput)
pdf(file=figName)

emmip(modelProportion_pooled, ~ Projection )

dev.off()
setwd(pathWorking)


#3%%-- Run Follow-up post-hoc tests ####

# Pairwise comparisons between Sessions

#-- Pooled
EMM <- emmeans(model_pooled, ~ typeNP | Projection)   # where treat has 2 levels
tPairwise= pairs(EMM, adjust = "sidak")   # adjustment is ignored - only 1 test per group
summary(tPairwise, by = NULL, adjust = "sidak")   # all are in one group now

tPairwise_Pooled= tPairwise

#pooled followup tests reveal significant differences in npCount by npType in VTA session 3,4,5

EMM <- emmeans(modelProportion_pooled, ~ Projection)   # where treat has 2 levels
tPairwise= pairs(EMM, adjust = "sidak")   # adjustment is ignored - only 1 test per group
summary(tPairwise, by = NULL, adjust = "sidak")   # all are in one group now

tPairwise_proportion_Pooled= tPairwise

# for active proportion, check if each level significantly different from 0.5 (chance)
t_Proportion_Pooled= test(EMM, null=0.5, adjust='sidak')

#- compare between projections
EMM <- emmeans(model_pooled, ~ Projection| typeNP)   # where treat has 2 levels
tPairwise= pairs(EMM, adjust = "sidak")   # adjustment is ignored - only 1 test per group
summary(tPairwise, by = NULL, adjust = "sidak")   # all are in one group now

tPairwiseProjection_Pooled= tPairwise



#-- VTA
#-npCount
EMM <- emmeans(model_VTA, ~ typeNP )   # where treat has 2 levels
tPairwise= pairs(EMM, adjust = "sidak")   # adjustment is ignored - only 1 test per group
summary(tPairwise, by = NULL, adjust = "sidak")   # all are in one group now

tPairwise_VTA= tPairwise

# #-npActiveProportion
 
# # for active proportion, check if each level significantly different from 0.5 (chance)

# #-npActiveProportion
# just need 1 sample t test
t_Proportion_VTA= t.test(df_Sub_A_finalSes_VTA$npActiveProportion, mu=0.5)


#-- mdThal

#-npCount
EMM <- emmeans(model_mdThal, ~ typeNP)   # where treat has 2 levels
tPairwise= pairs(EMM, adjust = "sidak")   # adjustment is ignored - only 1 test per group
summary(tPairwise, by = NULL, adjust = "sidak")   # all are in one group now

tPairwise_mdThal= tPairwise
# 
# #-npActiveProportion
# # for active proportion, check if each level significantly different from 0.5 (chance)
# just need 1 sample t test
t_Proportion_mdThal= t.test(df_Sub_A_finalSes_mdThal$npActiveProportion, mu=0.5)



#4%%-- Save output to variables between tests  ####
# trying to keep code mostly generalizable and just save custom names at end
# all the results into descriptive variables between tests

#-pooled
fig6_stats_Acquisition_finalSes_A_Pooled_0_description= "Figure 6: ICSS, OG Active Side, Active vs Inactive NP Count, pooled projections"
fig6_stats_Acquisition_finalSes_A_Pooled_1_model= model_pooled
fig6_stats_Acquisition_finalSes_A_Pooled_2_model_anova= model_anova_pooled
fig6_stats_Acquisition_finalSes_A_Pooled_3_model_post_hoc_pairwise= tPairwise_Pooled

fig6_stats_Acquisition_finalSes_B_Pooled_0_description= "Figure 6: ICSS, OG Active Side, Active NP Proportion, pooled projections"
fig6_stats_Acquisition_finalSes_B_Pooled_1_model= modelProportion_pooled
fig6_stats_Acquisition_finalSes_B_Pooled_2_model_anova= modelProportion_anova_pooled
fig6_stats_Acquisition_finalSes_B_Pooled_3_model_post_hoc_t= t_Proportion_Pooled

#-VTA
fig6_stats_Acquisition_finalSes_A_VTA_0_description= "Figure 6: ICSS, OG Active Side, Active vs Inactive NP Count, VTA projections"
fig6_stats_Acquisition_finalSes_A_VTA_1_model= model_VTA
fig6_stats_Acquisition_finalSes_A_VTA_2_model_anova= model_anova_VTA
fig6_stats_Acquisition_finalSes_A_VTA_3_model_post_hoc_pairwise= tPairwise_VTA

fig6_stats_Acquisition_finalSes_B_VTA_0_description= "Figure 6: ICSS, OG Active Side, Active NP Proportion, VTA projections"
fig6_stats_Acquisition_finalSes_B_VTA_1_model= modelProportion_VTA
fig6_stats_Acquisition_finalSes_B_VTA_2_model_anova= modelProportion_anova_VTA
fig6_stats_Acquisition_finalSes_B_VTA_3_model_post_hoc_t= t_Proportion_VTA 

#-mdThal
fig6_stats_Acquisition_finalSes_A_mdThal_0_description= "Figure 6: ICSS, OG Active Side, Active vs Inactive NP Count, mdThal projections"
fig6_stats_Acquisition_finalSes_A_mdThal_1_model= model_mdThal
fig6_stats_Acquisition_finalSes_A_mdThal_2_model_anova= model_anova_mdThal
fig6_stats_Acquisition_finalSes_A_mdThal_3_model_post_hoc_pairwise= tPairwise_mdThal

fig6_stats_Acquisition_finalSes_B_mdThal_0_description= "Figure 6: ICSS, OG Active Side, Active NP Proportion, mdThal projections"
fig6_stats_Acquisition_finalSes_B_mdThal_1_model= modelProportion_mdThal
fig6_stats_Acquisition_finalSes_B_mdThal_2_model_anova= modelProportion_anova_mdThal
fig6_stats_Acquisition_finalSes_B_mdThal_3_model_post_hoc_t= t_Proportion_mdThal



#5%% -- Figure 6 Save output ####

#- move to output directory prior to saving
setwd(pathOutput)

#------Pooled

sink("vp-vta_fig6_stats_Acquisition_finalSes_A_npCount_Pooled.txt")
'------------------------------------------------------------------------------'
'0)---- Description --: '
print(fig6_stats_Acquisition_finalSes_A_Pooled_0_description)
'------------------------------------------------------------------------------'
print('1)---- LME:')
print(summary(fig6_stats_Acquisition_finalSes_A_Pooled_1_model))
'------------------------------------------------------------------------------'
print('2)---- ANOVA of LME:')
print(fig6_stats_Acquisition_finalSes_A_Pooled_2_model_anova)
'------------------------------------------------------------------------------'
# print('3)---- Posthoc pairwise:') # Make sure for posthocs the summary is printed with pval correction
print(fig6_stats_Acquisition_finalSes_A_Pooled_3_model_post_hoc_pairwise, by = NULL, adjust = "sidak")
'---- END ---------------------------------------------------------------------'
sink()  # returns output to the console


sink("vp-vta_fig6_stats_Acquisition_finalSes_B_proportion_Pooled.txt")
'------------------------------------------------------------------------------'
'0)---- Description --: '
print(fig6_stats_Acquisition_finalSes_B_Pooled_0_description)
'------------------------------------------------------------------------------'
print('1)---- LME:')
print(summary(fig6_stats_Acquisition_finalSes_B_Pooled_1_model))
'------------------------------------------------------------------------------'
print('2)---- ANOVA of LME:')
print(fig6_stats_Acquisition_finalSes_B_Pooled_2_model_anova)
'------------------------------------------------------------------------------'
print('3)---- Posthoc pairwise:') # Make sure for posthocs the summary is printed with pval correction
print(fig6_stats_Acquisition_finalSes_B_Pooled_3_model_post_hoc_t, by = NULL, adjust = "sidak")
'---- END ---------------------------------------------------------------------'
sink()  # returns output to the console


#------ VTA

sink("vp-vta_fig6_stats_Acquisition_finalSes_A_npCount_VTA.txt")
'------------------------------------------------------------------------------'
'0)---- Description --: '
print(fig6_stats_Acquisition_finalSes_A_VTA_0_description)
'------------------------------------------------------------------------------'
print('1)---- LME:')
print(summary(fig6_stats_Acquisition_finalSes_A_VTA_1_model))
'------------------------------------------------------------------------------'
print('2)---- ANOVA of LME:')
print(fig6_stats_Acquisition_finalSes_A_VTA_2_model_anova)
'------------------------------------------------------------------------------'
print('3)---- Posthoc pairwise:') # Make sure for posthocs the summary is printed with pval correction
print(summary(fig6_stats_Acquisition_finalSes_A_VTA_3_model_post_hoc_pairwise, by = NULL, adjust = "sidak"))
'---- END ---------------------------------------------------------------------'
sink()  # returns output to the console


sink("vp-vta_fig6_stats_Acquisition_finalSes_B_proportion_VTA.txt")
'------------------------------------------------------------------------------'
'0)---- Description --: '
print(fig6_stats_Acquisition_finalSes_B_VTA_0_description)
'------------------------------------------------------------------------------'
# print('1)---- LME:')
# print(summary(fig6_stats_Acquisition_finalSes_B_VTA_1_model))
# '------------------------------------------------------------------------------'
# print('2)---- ANOVA of LME:')
# print(fig6_stats_Acquisition_finalSes_B_VTA_2_model_anova)
# '------------------------------------------------------------------------------'
print('3)---- t test:') # Make sure for posthocs the summary is printed with pval correction
print(fig6_stats_Acquisition_finalSes_B_VTA_3_model_post_hoc_t, by = NULL, adjust = "sidak")
'---- END ---------------------------------------------------------------------'
sink()  # returns output to the console


#------ mdThal

sink("vp-vta_fig6_stats_Acquisition_finalSes_A_npCount_mdThal.txt")
'------------------------------------------------------------------------------'
'0)---- Description --: '
print(fig6_stats_Acquisition_finalSes_A_mdThal_0_description)
'------------------------------------------------------------------------------'
print('1)---- LME:')
print(summary(fig6_stats_Acquisition_finalSes_A_mdThal_1_model))
'------------------------------------------------------------------------------'
print('2)---- ANOVA of LME:')
print(fig6_stats_Acquisition_finalSes_A_mdThal_2_model_anova)
'------------------------------------------------------------------------------'
print('3)---- Posthoc pairwise:') # Make sure for posthocs the summary is printed with pval correction
print(fig6_stats_Acquisition_finalSes_A_mdThal_3_model_post_hoc_pairwise, by = NULL, adjust = "sidak")
'---- END ---------------------------------------------------------------------'
sink()  # returns output to the console


sink("vp-vta_fig6_stats_Acquisition_finalSes_B_proportion_mdThal.txt")
'------------------------------------------------------------------------------'
'0)---- Description --: '
print(fig6_stats_Acquisition_finalSes_B_mdThal_0_description)
'------------------------------------------------------------------------------'
# print('1)---- LME:')
# print(summary(fig6_stats_Acquisition_finalSes_B_mdThal_1_model))
# '------------------------------------------------------------------------------'
# print('2)---- ANOVA of LME:')
# print(fig6_stats_Acquisition_finalSes_B_mdThal_2_model_anova)
# '------------------------------------------------------------------------------'
print('3)---- t test:') # Make sure for posthocs the summary is printed with pval correction
print(fig6_stats_Acquisition_finalSes_B_mdThal_3_model_post_hoc_t, by = NULL, adjust = "sidak")
'---- END ---------------------------------------------------------------------'
sink()  # returns output to the console


#- return to working directory after saving
setwd(pathWorking)


# __________________________________________________ ####


##%% END ####


