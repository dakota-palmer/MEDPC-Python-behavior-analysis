######################################################
## script for importing .pkls from Python
##
## 2021-10-11
####################################################

###### enter python env
Sys.setenv(RETICULATE_PYTHON = "C:/Users/Dakota/anaconda3/envs/r-env")


###### method A
library(reticulate)
pd <- import("pandas")
pickle_data <- pd$read_pickle("C:\\Users\\Dakota\\Documents\\GitHub\\DS-Training\\Python\\_output\\dfTidy.pkl")

# ##### method B
# require("reticulate")
# 
# source_python("pickle_reader.py")
# pickle_data <- read_pickle_file("C:\\Users\\Dakota\\Documents\\GitHub\\DS-Training\\Python\\_output\\dfTidy.pkl")

###### summarize data
summary(pickle_data)


##### try some dplyer grouping
library(dplyr)
by_file<-group_by(pickle_data,fileID)

# You can see underlying group data with group_keys(). It has one row for each group and one column for each grouping variable:
by_file_keys<- group_keys(by_file)

# You can see which group each row belongs to with group_indices():
by_file_ind<- group_indices(by_file)

# And which rows each group contains with group_rows():
by_file_rows<- group_rows(by_file)


# playing

by_many$stage<- as.factor(by_many$stage)

by_sex<- group_by(pickle_data, sex)

by_many<- group_by(pickle_data, virus, sex, stage, laserDur, subject, fileID, trialType)

by_many<- summarize(by_many, eventCount= n(), eventCount2= n_distinct())

#trying with chaining, need to figure out how to assign output?
pickle_data %>%
  group_by(virus, sex, stage, laserDur, subject, fileID, trialType) %>%
  (eventCount= n(), eventCount2= n_distinct())
  

#ggplot aes aesthetics + geom geometry
library(ggplot2)
ggplot(by_many, aes(x=trialType, y=eventCount)) + 
  geom_point(alpha=0.2, color="orchid")+
  geom_bar(stat= 'summary', fun= 'mean', alpha=0.4) #bar requires stat attribute

g<- ggplot(by_many, aes(x=trialType, y=eventCount, color=virus)) 
  g+ geom_point(alpha=0.2) 
  g+ geom_bar(stat= 'summary', fun= 'mean', alpha=0.4, 
            aes(fill=virus), position='dodge') +
     scale_fill_brewer(palette= 'Paired')
     scale_color_brewer(palette= 'Paired')
    
 
g<- ggplot(by_many, aes(x=virus, y=eventCount, color=trialType)) 
  g+ geom_point(alpha=0.2) 
  g+ geom_bar(stat= 'summary', fun= 'mean', alpha=0.4, 
              aes(fill=trialType), position='stack')+
  scale_fill_brewer(palette= 'Paired')+
  scale_color_brewer(palette= 'Paired')+
  facet_wrap(~sex)
  
g<- ggplot(by_many, aes(x=virus, y=eventCount, color=trialType)) 
  g+ geom_point(alpha=0.2) 
  g+ geom_bar(stat= 'summary', fun= 'mean', alpha=0.4, 
            aes(fill=trialType), position='stack')+
  scale_fill_brewer(palette= 'Paired')+
  scale_color_brewer(palette= 'Paired')+
  facet_grid(~stage)

  
  
  ##%% plot some preanalyzed data from python
  
  library(reticulate)
  pd <- import("pandas")
  py_data <- pd$read_pickle("C:\\Users\\Dakota\\Documents\\GitHub\\DS-Training\\Python\\_output\\dfTidyAnalyzed.pkl")
  
  #group for hierarchy and get the behavioral outcomes for each trialtype
  by_many<- group_by(py_data, virus, sex, stage, laserDur, subject, fileID, trialType, trialOutcomeBeh10s)
  
  by_many<- summarize(by_many, eventCount= n(), eventCount2= n_distinct())
  
  g<- ggplot(by_many, aes(x=trialOutcomeBeh10s, y=eventCount, color=trialType)) 
  g+ geom_point(alpha=0.2) 
  g+ geom_bar(stat= 'summary', fun= 'mean', alpha=0.4, 
              aes(fill=trialType), position='stack')+
    scale_fill_brewer(palette= 'Paired')+
    scale_color_brewer(palette= 'Paired')+
    facet_grid(virus ~ laserDur)
  
  g<- ggplot(by_many, aes(x=trialType, y=eventCount, color=trialOutcomeBeh10s)) 
    g+ geom_bar(stat= 'summary', fun= 'mean', alpha=0.4, 
                aes(fill=trialOutcomeBeh10s), position='fill')+
      scale_fill_brewer(palette= 'Paired')+
      scale_color_brewer(palette= 'Paired')+
      geom_jitter(color= 'black', alpha=0.9) 
      facet_grid(virus ~ laserDur)
      
      #count of outcomes by trialType
  g<- ggplot(by_many, aes(x=trialType, y=eventCount, color=trialOutcomeBeh10s)) 
      g+ geom_bar(stat= 'summary', fun= 'mean', alpha=0.6, 
                  aes(fill=trialOutcomeBeh10s), position='stack')+
        scale_fill_brewer(palette= 'Paired')+
        scale_color_brewer(palette= 'Paired')+
        geom_point(alpha=0.3, position='jitter') 
      facet_grid(virus ~ laserDur)
      
      #calculate proportion
      test<- py_data %>%
        count(virus, sex, stage, laserDur, subject, fileID, trialType, trialOutcomeBeh10s) %>%
        mutate(prop = prop.table(n))  
  
##### try computations on groups

#see https://cran.r-project.org/web/packages/dplyr/vignettes/grouping.html 
#Computing on grouping information


  