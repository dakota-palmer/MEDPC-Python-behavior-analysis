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

##### try computations on groups

#see https://cran.r-project.org/web/packages/dplyr/vignettes/grouping.html 
#Computing on grouping information


  