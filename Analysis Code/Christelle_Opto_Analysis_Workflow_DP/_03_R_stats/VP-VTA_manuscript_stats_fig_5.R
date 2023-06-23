
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

#%- fig 5 Stats-- Phase 1- Free Choice ####

#0%%-- Clear vars between tests ####
# #clear workspace (R environment) # Except paths, Python packages (pandas)
rm(list = setdiff(ls(), c("pathWorking", "pathOutput", "pd")))


#1%%-- Load data from .pkl ####

pathData <- "C:\\Users\\Dakota\\Documents\\GitHub\\FP-analysis\\python\\_output\\fig5.pkl"

df <- pd$read_pickle(pathData)


###### summarize data
summary(df)

#verify dtypes imported properly
sapply(df, class)



#%%-- Subset data ##
#Remove missing/invalid observations
#- eliminate duplicate proportion values 
# currently active proportion is session level but df has 2 per session (1 per npTy1pe)
# so just remove from one trialType. This way can use same df for multiple models easily
df[df$typeLP=='ActiveLeverPress','probActiveLP']= NaN
df[df$typeLP=='ActiveLeverPress','LicksPerReward']= NaN



# #- Subset by session type 
df_Sub_A= df[df$trainPhaseLabel == '1-FreeChoice',]





df_Sub_A_VTA= df_Sub_A[df_Sub_A$Projection=='VTA',]

df_Sub_A_mdThal= df_Sub_A[df_Sub_A$Projection=='mdThal',]


#since we've dropped levels(categories) from the factor(categorical) variable trainDayThisPhase, drop accordingly for stats to work out
# droplevels(df_Sub_A$trainDayThisPhase)
# droplevels(df_Sub_A$trainPhase)


#2%%-- Run LME ####

#-- Pooled
# model= lmerTest::lmer('countNP ~ Projection * typeNP * Session *  trainPhase + (1|Subject)', data=df_Sub_A)
model= lmerTest::lmer('countLP ~ Projection * typeLP * Session + (1|Subject)', data=df_Sub_A)

modelProportion= lmerTest::lmer('probActiveLP ~ Projection * Session + (1|Subject)', data=df_Sub_A)


modelLicks=  lmerTest::lmer('licksPerRewardTypeLP ~ typeLP* Projection * Session + (1|Subject)', data=df_Sub_A)



model_pooled= model
model_anova_pooled<- anova(model)
modelProportion_pooled= modelProportion
modelProportion_anova_pooled= anova(modelProportion)
modelLicks_pooled= modelLicks
modelLicks_anova_pooled= anova(modelLicks)


#3%%-- Posthoc tests ####

#-- VTA
#VTA projection
#-Count
model_VTA= lmerTest::lmer('countLP ~ typeLP * Session + (1|Subject)', data=df_Sub_A_VTA)
model_anova_VTA<- anova(model_VTA)
#-Proportion
modelProportion_VTA= lmerTest::lmer('probActiveLP ~ Session + (1|Subject)', data=df_Sub_A_VTA)
modelProportion_anova_VTA<- anova(modelProportion_VTA)

#-licks/reward
modelLicks_VTA= lmerTest::lmer('licksPerRewardTypeLP ~ typeLP* Session + (1|Subject)', data=df_Sub_A_VTA)
modelLicks_anova_VTA<- anova(modelLicks_VTA)


#-- mdThal
#mdThal projection
#-Probability
model_mdThal= lmerTest::lmer('countLP ~ typeLP * Session + (1|Subject)', data=df_Sub_A_mdThal)
model_anova_mdThal<- anova(model_mdThal)
#-Proportion
modelProportion_mdThal= lmerTest::lmer('probActiveLP ~ Session + (1|Subject)', data=df_Sub_A_mdThal)
modelProportion_anova_mdThal<- anova(modelProportion_mdThal)
#-licks/reward
modelLicks_mdThal= lmerTest::lmer('licksPerRewardTypeLP ~ typeLP * Session + (1|Subject)', data=df_Sub_A_mdThal)
modelLicks_anova_mdThal<- anova(modelLicks_mdThal)


# -- Interaction plot
#- Viz interaction plot & save
figName= "vp-vta_fig5_stats_A_npCount_Session_pooled_interactionPlot.pdf"
setwd(pathOutput)
pdf(file=figName)

emmip(model_pooled, Session ~ typeLP | Projection )


dev.off()
setwd(pathWorking)

#pooled proportion interaction plot
figName= "vp-vta_fig5_stats_B_proportion_pooled_interactionPlot.pdf"
setwd(pathOutput)
pdf(file=figName)

emmip(modelProportion_pooled, Session ~ Projection )

dev.off()
setwd(pathWorking)

#-- Grand Interaction plot (all phases)
model_grand= lmerTest::lmer('countLP ~ Projection * typeLP * Session  + (1|Subject)', data=df)


figName= "vp-vta_fig5_stats_A_Grand_interactionPlot_all_Phases.pdf"
setwd(pathOutput)
pdf(file=figName)

emmip(model_grand,  typeLP ~  Session | Projection )

dev.off()
setwd(pathWorking)

# Lick Grand interaction plot (all phases)
modelLicks_grand= lmerTest::lmer('licksPerRewardTypeLP ~ Projection* typeLP* Session + (1|Subject)', data=df)


figName= "vp-vta_fig5_stats_A_Grand_interactionPlotLicksPerReward_all_Phases.pdf"
setwd(pathOutput)
pdf(file=figName)

emmip(modelLicks_grand,  typeLP ~  Session | Projection )

dev.off()


#- Pairwise T- tests--

#-- Pooled
  #-npCount
EMM <- emmeans(model_pooled, ~ typeLP | Session | Projection)   # where treat has 2 levels
tPairwise= pairs(EMM, adjust = "sidak")   # adjustment is ignored - only 1 test per group
summary(tPairwise, by = NULL, adjust = "sidak")   # all are in one group now

tPairwise_Pooled= tPairwise

  #npActiveProportion
EMM <- emmeans(modelProportion_pooled, ~ Session | Projection)   # where treat has 2 levels
tPairwise= pairs(EMM, adjust = "sidak")   # adjustment is ignored - only 1 test per group
summary(tPairwise, by = NULL, adjust = "sidak")   # all are in one group now

tPairwise_proportion_Pooled= tPairwise

# for active proportion, check if each level significantly different from 0.5 (chance)
t_proportion_Pooled= test(EMM, null=0.5, adjust='sidak')


#-- VTA
  #-npCount
EMM <- emmeans(model_VTA, ~ typeLP | Session)   # where treat has 2 levels
tPairwise= pairs(EMM, adjust = "sidak")   # adjustment is ignored - only 1 test per group
summary(tPairwise, by = NULL, adjust = "sidak")   # all are in one group now

tPairwise_VTA= tPairwise
  
  #-npActiveProportion
EMM <- emmeans(modelProportion_VTA, ~ Session)   # where treat has 2 levels
tPairwise= pairs(EMM, adjust = "sidak")   # adjustment is ignored - only 1 test per group
summary(tPairwise, by = NULL, adjust = "sidak")   # all are in one group now

tPairwise_proportion_VTA= tPairwise

# for active proportion, check if each level significantly different from 0.5 (chance)
t_proportion_VTA= test(EMM, null=0.5, adjust='sidak')


#-- mdThal

  #-npCount
EMM <- emmeans(model_mdThal, ~ typeLP | Session)   # where treat has 2 levels
tPairwise= pairs(EMM, adjust = "sidak")   # adjustment is ignored - only 1 test per group
summary(tPairwise, by = NULL, adjust = "sidak")   # all are in one group now

tPairwise_mdThal= tPairwise

  #-npActiveProportion
EMM <- emmeans(modelProportion_mdThal, ~ Session)   # where treat has 2 levels
tPairwise= pairs(EMM, adjust = "sidak")   # adjustment is ignored - only 1 test per group
summary(tPairwise, by = NULL, adjust = "sidak")   # all are in one group now

tPairwise_proportion_mdThal= tPairwise

# for active proportion, check if each level significantly different from 0.5 (chance)
t_proportion_mdThal= test(EMM, null=0.5, adjust='sidak')


#4%%-- Save output to variables between tests  ####
# trying to keep code mostly generalizable and just save custom names at end
# all the results into descriptive variables between tests

#-pooled
fig5_stats_Phase_1_FreeChoice_A_Pooled_0_description= "Figure 5: Lever Choice, Phase 1- Free Choice, Active vs Inactive NP Count, pooled projections"
fig5_stats_Phase_1_FreeChoice_A_Pooled_1_model= model_pooled
fig5_stats_Phase_1_FreeChoice_A_Pooled_2_model_anova= model_anova_pooled
fig5_stats_Phase_1_FreeChoice_A_Pooled_3_model_post_hoc_pairwise= tPairwise_Pooled

fig5_stats_Phase_1_FreeChoice_B_Pooled_0_description= "Figure 5: Lever Choice, Phase 1- Free Choice, Active NP Proportion, pooled projections"
fig5_stats_Phase_1_FreeChoice_B_Pooled_1_model= modelProportion_pooled
fig5_stats_Phase_1_FreeChoice_B_Pooled_2_model_anova= modelProportion_anova_pooled
fig5_stats_Phase_1_FreeChoice_B_Pooled_3_model_post_hoc_t= t_proportion_Pooled


fig5_stats_Phase_1_FreeChoice_C_licks_Pooled_0_description= "Figure 5: Lever Choice, Phase 1- Free Choice, licks/reward, pooled projections"
fig5_stats_Phase_1_FreeChoice_C_licks_Pooled_1_model= modelLicks_pooled
fig5_stats_Phase_1_FreeChoice_C_licks_Pooled_2_model_anova= modelLicks_anova_pooled
# fig5_stats_Phase_1_FreeChoice_C_licks_Pooled_3_model_post_hoc_tPairwise= tPairwise_licks_projection


#-VTA
fig5_stats_Phase_1_FreeChoice_A_VTA_0_description= "Figure 5: Lever Choice, Phase 1- Free Choice, Active vs Inactive NP Count, VTA projections"
fig5_stats_Phase_1_FreeChoice_A_VTA_1_model= model_VTA
fig5_stats_Phase_1_FreeChoice_A_VTA_2_model_anova= model_anova_VTA
fig5_stats_Phase_1_FreeChoice_A_VTA_3_model_post_hoc_pairwise= tPairwise_VTA

fig5_stats_Phase_1_FreeChoice_B_VTA_0_description= "Figure 5: Lever Choice, Phase 1- Free Choice, Active NP Proportion, VTA projections"
fig5_stats_Phase_1_FreeChoice_B_VTA_1_model= modelProportion_VTA
fig5_stats_Phase_1_FreeChoice_B_VTA_2_model_anova= modelProportion_anova_VTA
fig5_stats_Phase_1_FreeChoice_B_VTA_3_model_post_hoc_t= t_proportion_VTA

fig5_stats_Phase_1_FreeChoice_C_licks_VTA_0_description= "Figure 5: Lever Choice, Phase 1- Free Choice, licks/reward, VTA projections"
fig5_stats_Phase_1_FreeChoice_C_licks_VTA_1_model= modelLicks_VTA
fig5_stats_Phase_1_FreeChoice_C_licks_VTA_2_model_anova= modelLicks_anova_VTA

#-mdThal
fig5_stats_Phase_1_FreeChoice_A_mdThal_0_description= "Figure 5: Lever Choice, Phase 1- Free Choice, Active vs Inactive NP Count, mdThal projections"
fig5_stats_Phase_1_FreeChoice_A_mdThal_1_model= model_mdThal
fig5_stats_Phase_1_FreeChoice_A_mdThal_2_model_anova= model_anova_mdThal
fig5_stats_Phase_1_FreeChoice_A_mdThal_3_model_post_hoc_pairwise= tPairwise_mdThal

fig5_stats_Phase_1_FreeChoice_B_mdThal_0_description= "Figure 5: Lever Choice, Phase 1- Free Choice, Active NP Proportion, mdThal projections"
fig5_stats_Phase_1_FreeChoice_B_mdThal_1_model= modelProportion_mdThal
fig5_stats_Phase_1_FreeChoice_B_mdThal_2_model_anova= modelProportion_anova_mdThal
fig5_stats_Phase_1_FreeChoice_B_mdThal_3_model_post_hoc_t= t_proportion_mdThal

fig5_stats_Phase_1_FreeChoice_C_licks_VTA_0_description= "Figure 5: Lever Choice, Phase 1- Free Choice, licks/reward, mdThal"
fig5_stats_Phase_1_FreeChoice_C_licks_mdThal_1_model= modelLicks_mdThal
fig5_stats_Phase_1_FreeChoice_C_licks_mdTh


#5%% -- Save output to File####

#- move to output directory prior to saving
setwd(pathOutput)

#------Pooled

sink("vp-vta_fig5_stats_Phase_1_FreeChoice_A_lpCount_Pooled.txt")
'------------------------------------------------------------------------------'
'0)---- Description --: '
print(fig5_stats_Phase_1_FreeChoice_A_Pooled_0_description)
'------------------------------------------------------------------------------'
print('1)---- LME:')
print(summary(fig5_stats_Phase_1_FreeChoice_A_Pooled_1_model))
'------------------------------------------------------------------------------'
print('2)---- ANOVA of LME:')
print(fig5_stats_Phase_1_FreeChoice_A_Pooled_2_model_anova)
'------------------------------------------------------------------------------'
# print('3)---- Posthoc pairwise:') # Make sure for posthocs the summary is printed with pval correction
# print(fig5C_stats_C_3_model_post_hoc_pairwise)
'---- END ---------------------------------------------------------------------'
sink()  # returns output to the console


sink("vp-vta_fig5_stats_Phase_1_FreeChoice_B_proportion_Pooled.txt")
'------------------------------------------------------------------------------'
'0)---- Description --: '
print(fig5_stats_Phase_1_FreeChoice_B_Pooled_0_description)
'------------------------------------------------------------------------------'
print('1)---- LME:')
print(summary(fig5_stats_Phase_1_FreeChoice_B_Pooled_1_model))
'------------------------------------------------------------------------------'
print('2)---- ANOVA of LME:')
print(fig5_stats_Phase_1_FreeChoice_B_Pooled_2_model_anova)
'------------------------------------------------------------------------------'
# print('3)---- Posthoc pairwise:') # Make sure for posthocs the summary is printed with pval correction
# print(summary(fig5C_stats_C_VTA_3_model_post_hoc_pairwise, by = NULL, adjust = "sidak"))
'---- END ---------------------------------------------------------------------'
sink()  # returns output to the console

sink("vp-vta_fig5_stats_Phase_1_FreeChoice_C_licks_Pooled.txt")
'------------------------------------------------------------------------------'
'0)---- Description --: '
print(fig5_stats_Phase_1_FreeChoice_C_licks_Pooled_0_description)
'------------------------------------------------------------------------------'
print('1)---- LME:')
print(summary(fig5_stats_Phase_1_FreeChoice_C_licks_Pooled_1_model))
'------------------------------------------------------------------------------'
print('2)---- ANOVA of LME:')
print(fig5_stats_Phase_1_FreeChoice_C_licks_Pooled_2_model_anova)
'------------------------------------------------------------------------------'
# print('3)---- Posthoc pairwise:') # Make sure for posthocs the summary is printed with pval correction
'---- END ---------------------------------------------------------------------'
sink()  # returns output to the console



#------ VTA

sink("vp-vta_fig5_stats_Phase_1_FreeChoice_A_lpCount_VTA.txt")
'------------------------------------------------------------------------------'
'0)---- Description --: '
print(fig5_stats_Phase_1_FreeChoice_A_VTA_0_description)
'------------------------------------------------------------------------------'
print('1)---- LME:')
print(summary(fig5_stats_Phase_1_FreeChoice_A_VTA_1_model))
'------------------------------------------------------------------------------'
print('2)---- ANOVA of LME:')
print(fig5_stats_Phase_1_FreeChoice_A_VTA_2_model_anova)
'------------------------------------------------------------------------------'
print('3)---- Posthoc pairwise:') # Make sure for posthocs the summary is printed with pval correction
print(fig5_stats_Phase_1_FreeChoice_A_VTA_3_model_post_hoc_pairwise, by = NULL, adjust = "sidak")
'---- END ---------------------------------------------------------------------'
sink()  # returns output to the console


sink("vp-vta_fig5_stats_Phase_1_FreeChoice_B_proportion_VTA.txt")
'------------------------------------------------------------------------------'
'0)---- Description --: '
print(fig5_stats_Phase_1_FreeChoice_B_VTA_0_description)
'------------------------------------------------------------------------------'
print('1)---- LME:')
print(summary(fig5_stats_Phase_1_FreeChoice_B_VTA_1_model))
'------------------------------------------------------------------------------'
print('2)---- ANOVA of LME:')
print(fig5_stats_Phase_1_FreeChoice_B_VTA_2_model_anova)
'------------------------------------------------------------------------------'
print('3)---- Posthoc t tests:') # Make sure for posthocs the summary is printed with pval correction
print(fig5_stats_Phase_1_FreeChoice_B_VTA_3_model_post_hoc_t, by = NULL, adjust = "sidak")
'---- END ---------------------------------------------------------------------'
sink()  # returns output to the console


sink("vp-vta_fig5_stats_Phase_1_FreeChoice_C_licks_VTA.txt")
'------------------------------------------------------------------------------'
'0)---- Description --: '
print(fig5_stats_Phase_1_FreeChoice_C_licks_VTA_0_description)
'------------------------------------------------------------------------------'
print('1)---- LME:')
print(summary(fig5_stats_Phase_1_FreeChoice_C_licks_VTA_1_model))
'------------------------------------------------------------------------------'
print('2)---- ANOVA of LME:')
print(fig5_stats_Phase_1_FreeChoice_C_licks_VTA_2_model_anova)
'------------------------------------------------------------------------------'
# print('3)---- Posthoc pairwise:') # Make sure for posthocs the summary is printed with pval correction
'---- END ---------------------------------------------------------------------'
sink()  # returns output to the console



#------ mdThal

sink("vp-vta_fig5_stats_Phase_1_FreeChoice_A_lpCount_mdThal.txt")
'------------------------------------------------------------------------------'
'0)---- Description --: '
print(fig5_stats_Phase_1_FreeChoice_A_mdThal_0_description)
'------------------------------------------------------------------------------'
print('1)---- LME:')
print(summary(fig5_stats_Phase_1_FreeChoice_A_mdThal_1_model))
'------------------------------------------------------------------------------'
print('2)---- ANOVA of LME:')
print(fig5_stats_Phase_1_FreeChoice_A_mdThal_2_model_anova)
'------------------------------------------------------------------------------'
print('3)---- Posthoc pairwise:') # Make sure for posthocs the summary is printed with pval correction
print(fig5_stats_Phase_1_FreeChoice_A_mdThal_3_model_post_hoc_pairwise, by = NULL, adjust = "sidak")
'---- END ---------------------------------------------------------------------'
sink()  # returns output to the console

sink("vp-vta_fig5_stats_Phase_1_FreeChoice_B_proportion_mdThal.txt")
'------------------------------------------------------------------------------'
'0)---- Description --: '
print(fig5_stats_Phase_1_FreeChoice_B_mdThal_0_description)
'------------------------------------------------------------------------------'
print('1)---- LME:')
print(summary(fig5_stats_Phase_1_FreeChoice_B_mdThal_1_model))
'------------------------------------------------------------------------------'
print('2)---- ANOVA of LME:')
print(fig5_stats_Phase_1_FreeChoice_B_mdThal_2_model_anova)
'------------------------------------------------------------------------------'
print('3)---- Posthoc t tests:') # Make sure for posthocs the summary is printed with pval correction
print(fig5_stats_Phase_1_FreeChoice_B_mdThal_3_model_post_hoc_t, by = NULL, adjust = "sidak")
'---- END ---------------------------------------------------------------------'
sink()  # returns output to the console

sink("vp-vta_fig5_stats_Phase_1_FreeChoice_C_licks_mdThal.txt")
'------------------------------------------------------------------------------'
'0)---- Description --: '
print(fig5_stats_Phase_1_FreeChoice_C_licks_mdThal_0_description)
'------------------------------------------------------------------------------'
print('1)---- LME:')
print(summary(fig5_stats_Phase_1_FreeChoice_C_licks_mdThal_1_model))
'------------------------------------------------------------------------------'
print('2)---- ANOVA of LME:')
print(fig5_stats_Phase_1_FreeChoice_C_licks_mdThal_2_model_anova)
'------------------------------------------------------------------------------'
# print('3)---- Posthoc pairwise:') # Make sure for posthocs the summary is printed with pval correction
'---- END ---------------------------------------------------------------------'
sink()  # returns output to the console




# __________________________________________________ ####


#%% END ####
