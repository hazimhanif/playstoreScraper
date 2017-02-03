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

##Removing factors. Change to double/numerical value
dataset$id<-as.numeric(as.character(dataset$id))
dataset$appPrice<-as.numeric(as.character(dataset$appPrice))
dataset$appScore<-as.numeric(as.character(dataset$appScore))
dataset$revRating<-as.numeric(as.character(dataset$revRating))
dataset$label_rating<-as.numeric(as.character(dataset$label_rating))

##Remove all punctuations
#print("Removing all punctuations..")
#for(x in seq(1,nrow(dataset))){
#dataset[x,"revTitle"]<- gsub(dataset[x,"revTitle"],pattern = "[[:punct:]]",replacement = "")
#dataset[x,"revText"]<- gsub(dataset[x,"revText"],pattern = "[[:punct:]]",replacement = "")
#}


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
  dataset[x,"revDate"]<-paste(tempsplit[[1]][1],month_list[[tempsplit[[1]][2]]],tempsplit[[1]][3],sep = "-")
}
dataset$revDate<-as.Date(dataset$revDate,"%d-%m-%Y")

##List init
mylist<-list()

print("Features extraction...")

for(x in seq(1,nrow(dataset))){
  obs<-dataset[x,]
  ##Features Extraction: Total 37
  print(x)
  ##Continuos values features
  app_price<-as.double(obs$appPrice)
  app_score<-as.double(obs$appScore)
  rev_title_len<-length(obs$revTitle)
  rev_body_len<-length(obs$revText)
  rev_pos_ascend<-func_rev_pos_ascend(obs)
  rev_pos_descend<-func_rev_pos_descend(obs)
  avg_cosine_similarity_title<-func_avg_cosine_similarity_title(obs)
  avg_cosine_similarity_text<-func_avg_cosine_similarity_text(obs)
  avg_levenshtein_dist_title<-func_avg_levenshtein_dist_title(obs)
  avg_levenshtein_dist_text<-func_avg_levenshtein_dist_text(obs)
  numeric_title_ratio<-length(as.numeric(unlist(strsplit(gsub("[^0-9]", "", unlist(obs$revTitle)), ""))))/length(obs$revTitle)
  numeric_text_ratio<-length(as.numeric(unlist(strsplit(gsub("[^0-9]", "", unlist(obs$revText)), ""))))/length(obs$revText)
  avg_num_ratio<-mean(c(numeric_title_ratio,numeric_text_ratio))
  cap_words_ratio<-length(unlist(str_extract_all(obs$revText, '\\b[A-Z]+\\b')))/length(unlist(str_split(obs$revText,pattern = " ")))
  num_cap_letters_ratio<-length(unlist(str_extract_all(obs$revText, '[A-Z]')))/length(unlist(str_extract_all(obs$revText, '[A-Za-z]')))
  rev_rating<-as.numeric(obs$label_rating)
  stdev_revApp_rating<-sd(c(as.double(obs$label_rating),as.double(obs$appScore)))
  avg_words_freq_title<-func_avg_words_freq_title(obs)
  avg_words_freq_text<-func_avg_words_freq_title(obs)
  num_unique_words_title<-func_num_unique_words_title(obs)
  num_unique_words_text<-func_num_unique_words_text(obs)
  unique_words_to_words_title_ratio<-func_unique_words_to_words_title_ratio(obs)
  unique_words_to_words_text_ratio<-func_unique_words_to_words_text_ratio(obs)
  stdev_num_words_title_text<-func_stdev_num_words_title_text(obs)
  stdev_num_unique_words_title_text<-sd(c(num_unique_words_title,num_unique_words_text))
  stdev_length_title_text<-sd(c(rev_title_len,rev_body_len))
  levenshtein_title_text<-stringdist(obs$revTitle,obs$revText, method ="lv")
  cosine_sim_title_text<-stringdist(obs$revTitle,obs$revText, method ="cosine")
  stdev_avg_lev_dist_title_text<-sd(c(avg_levenshtein_dist_title,avg_levenshtein_dist_text))
  stdev_avg_cosine_sim_title_text<-sd(c(avg_cosine_similarity_title,avg_cosine_similarity_text))
  
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
  
  mylist[[x]]<-c(app_price,app_score,rev_title_len,rev_body_len,rev_pos_ascend,rev_pos_descend,avg_cosine_similarity_title,avg_cosine_similarity_text,avg_levenshtein_dist_title,avg_levenshtein_dist_text,numeric_title_ratio,numeric_text_ratio,avg_num_ratio,cap_words_ratio,num_cap_letters_ratio,rev_rating,stdev_revApp_rating,avg_words_freq_title,avg_words_freq_text,num_unique_words_title,num_unique_words_text,unique_words_to_words_title_ratio,unique_words_to_words_text_ratio,stdev_num_words_title_text,stdev_num_unique_words_title_text,stdev_length_title_text,levenshtein_title_text,cosine_sim_title_text,stdev_avg_lev_dist_title_text,stdev_avg_cosine_sim_title_text,first_rev,only_rev,brand_names_in_title,brand_names_in_text,rev_semantic_orient,bad_rev_before,bad_rev_after,class)
}

df_dataset<-data.frame(t(sapply(mylist,c)))
names(df_dataset)<-c("app_price","app_score","rev_title_len","rev_body_len","rev_pos_ascend","rev_pos_descend","avg_cosine_similarity_title","avg_cosine_similarity_text","avg_levenshtein_dist_title","avg_levenshtein_dist_text","numeric_title_ratio","numeric_text_ratio","avg_num_ratio","cap_words_ratio","num_cap_letters_ratio","rev_rating","stdev_revApp_rating","avg_words_freq_title","avg_words_freq_text","num_unique_words_title","num_unique_words_text","unique_words_to_words_title_ratio","unique_words_to_words_text_ratio","stdev_num_words_title_text","stdev_num_unique_words_title_text","stdev_length_title_text","levenshtein_title_text","cosine_sim_title_text","stdev_avg_lev_dist_title_text","stdev_avg_cosine_sim_title_text","first_rev","only_rev","brand_names_in_title","brand_names_in_text","rev_semantic_orient","bad_rev_before","bad_rev_after","class")

## Subtituting NAs & Inf with 0's
for(x in seq(1,ncol(df_dataset))){
  df_dataset[!is.finite(df_dataset[,x]),x]<-0 
}

write.csv(x = df_dataset,file = "5000_ready.csv",row.names = FALSE,col.names = TRUE)