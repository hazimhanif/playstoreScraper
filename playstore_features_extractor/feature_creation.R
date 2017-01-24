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
print("Removing all punctuations..")
for(x in seq(1,nrow(dataset))){
  dataset[x,"revTitle"]<- gsub(dataset[x,"revTitle"],pattern = "[[:punct:]]",replacement = "")
  dataset[x,"revText"]<- gsub(dataset[x,"revText"],pattern = "[[:punct:]]",replacement = "")
}


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


##Features Extraction
app_price<-obs$appPrice
app_score<-obs$appScore
rev_title_len<-len(obs$revTitle)
rev_body_len<-len(obs$revText)
rev_pos_ascend<-func_rev_pos_ascend(obs)
rev_pos_descend<-func_rev_pos_descend(obs)
first_rev<-func_first_rev
only_rev<-func_only_rev

