## Importing library
library(stringdist)
library(stringr)


## Source the functions file
source("feature_creation_functions.R")


##Reading file,dropping "DROPPED" reviews, remove unwanted columns(id & 4 last columns)
dataset<- do.call(rbind,strsplit(readLines('D:/scraper/playstore/labelled/labelled_5000_new.csv'),'||::',fixed=T))
col_names<-dataset[1,]
dataset<-as.data.frame(dataset[1:nrow(dataset),])
dataset<-dataset[-1,]
names(dataset)<-col_names
dataset<-dataset[which(dataset$label_drop=="NULL"),]
dataset<-dataset[,1:13]


##Remove all punctuations
#print("Removing all punctuations..")
#for(x in seq(1,nrow(dataset))){
dataset[x,"revTitle"]<- gsub(dataset[x,"revTitle"],pattern = "[[:punct:]]",replacement = "")
dataset[x,"revText"]<- gsub(dataset[x,"revText"],pattern = "[[:punct:]]",replacement = "")
}
#

##Converting date to real date type
print("Converting date data to real date type.")
month_list<-list()
{
  month_list[["Januari"]]<-"01"
  month_list[["Februari"]]<-"02"
  month_list[["Mac"]]<-"03"
  month_list[["April"]]<-"04"
  month_list[["Mei"]]<-"05"
  month_list[["Jun"]]<-"06"
  month_list[["Julai"]]<-"07"
  month_list[["Ogos"]]<-"08"
  month_list[["September"]]<-"09"
  month_list[["Oktober"]]<-"10"
  month_list[["November"]]<-"11"
  month_list[["Disember"]]<-"12"
}
dataset$revDate<-as.character.factor(dataset$revDate)
for(x in seq(1,nrow(dataset))){
  tempsplit<-strsplit(x=dataset[x,"revDate"],split =" ")
  dataset[x,"reasvDate"]<-paste(tempsplit[[1]][1],month_list[[tempsplit[[1]][2]]],tempsplit[[1]][3],sep = "-")
}
dataset$revDate<-as.Date(dataset$revDate,"%d-%m-%Y")


##Features Extraction: Total 24
print("Extracting features.")
##Continuos values features
app_price<-as.double(obs$appPrice)
app_score<-as.double(obs$appScore)
rev_title_len<-len(obs$revTitle)
rev_body_len<-len(obs$revText)
rev_pos_ascend<-func_rev_pos_ascend(obs)
rev_pos_descend<-func_rev_pos_descend(obs)
avg_cosine_similarity_title<-func_avg_cosine_similarity_title(obs)
avg_cosine_similarity_text<-func_avg_cosine_similarity_text(obs)
avg_levenshtein_dist_title<-func_avg_levenshtein_dist_title(obs)
avg_levenshtein_dist_text<-func_avg_levenshtein_dist_text(obs)
numeric_title_ratio<-length(as.numeric(unlist(strsplit(gsub("[^0-9]", "", unlist(obs$revTitle)), ""))))/length(obs$revTitle)
numeric_text_ratio<-length(as.numeric(unlist(strsplit(gsub("[^0-9]", "", unlist(obs$revText)), ""))))/length(obs$revText)
avg_num_ratio<-mean(c(num_title_ratio,num_text_ratio))
cap_words_ratio<-length(unlist(str_extract_all(obs$revText, '\\b[A-Z]+\\b')))/length(unlist(str_split(obs$revText,pattern = " ")))
num_cap_letters_ratio<-length(unlist(str_extract_all(obs$revText, '[A-Z]')))/length(unlist(str_extract_all(obs$revText, '[A-Za-z]')))
rev_rating<-as.double(obs$label_rating)
stdev_revApp_rating<-sd(c(as.double(obs$label_rating),as.double(obs$appScore)))
##Categorical features
first_rev<-func_first_rev(obs)
only_rev<-func_only_rev(obs)
brand_names_in_title<-func_brand_names_in_title(obs)
brand_names_in_text<-func_brand_names_in_text(obs)
rev_semantic_orient<-if(obs$label_sentiment=="positive"){2}else if(obs$label_sentiment=="neutral"){1}else{0}
bad_rev_before<-func_bad_rev_before(obs)
bad_rev_after<-func_bad_rev_after(obs)
##Label
class<-if(obs$label_authenticity=="fake"){1}else{0}