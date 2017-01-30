func_rev_pos_ascend<-function(obs){
  temp<-dataset[dataset$appId==obs$appId,]
  temp<-temp[order(temp$revDate,decreasing = FALSE),]
  which(temp[temp$appId==obs$appId,]$id==obs$id)
}

func_rev_pos_descend<-function(obs){
  temp<-dataset[dataset$appId==obs$appId,]
  temp<-temp[order(temp$revDate,decreasing = TRUE),]
  which(temp[temp$appId==obs$appId,]$id==obs$id)
}

func_first_rev<-function(obs){
  temp<-dataset[which(dataset$appId==obs$appId & dataset$revAuthor==obs$revAuthor),]
  temp<-temp[order(temp$revDate,decreasing = FALSE),]
  if(which(temp$id==obs$id)==1)
  {1}else{0}
}

func_only_rev<-function(obs){
  temp<-dataset[which(dataset$appId==obs$appId & dataset$revAuthor==obs$revAuthor),]
  if(nrow(temp)==1)
  {1}else{0}
}

func_avg_cosine_similarity_title<-function(obs){
  temp<-dataset[dataset$appId==obs$appId,]
  tempList<-c()
  for(x in seq(1,nrow(temp))){
    tempList<-c(tempList,stringdist(obs$revTitle,dataset[x,"revTitle"], method ="cosine"))
  }
  mean(tempList)
}

func_avg_cosine_similarity_text<-function(obs){
  temp<-dataset[dataset$appId==obs$appId,]
  tempList<-c()
  for(x in seq(1,nrow(temp))){
    tempList<-c(tempList,stringdist(obs$revText,dataset[x,"revText"], method ="cosine"))
  }
  mean(tempList)
}

func_avg_levenshtein_dist_title<-function(obs){
  temp<-dataset[dataset$appId==obs$appId,]
  tempList<-c()
  for(x in seq(1,nrow(temp))){
    tempList<-c(tempList,stringdist(obs$revTitle,dataset[x,"revTitle"], method ="lv"))
  }
  mean(tempList)
}

func_avg_levenshtein_dist_text<-function(obs){
  temp<-dataset[dataset$appId==obs$appId,]
  tempList<-c()
  for(x in seq(1,nrow(temp))){
    tempList<-c(tempList,stringdist(obs$revText,dataset[x,"revText"], method ="lv"))
  }
  mean(tempList)
}

func_brand_names_in_title<-function(obs){
  if(grep(tolower(obs$revTitle),pattern = tolower(obs$appTitle))==1){
    1
  }else{
    0
  }
}

func_brand_names_in_text<-function(obs){
  if(grep(tolower(obs$revText),pattern = tolower(obs$appTitle))==1){
    1
  }else{
    0
  }
}

func_bad_rev_before<-function(obs){
  temp<-dataset[dataset$appId==obs$appId,]
  temp<-temp[order(temp$revDate,decreasing = FALSE),]
  x<-which(temp[temp$appId==obs$appId,]$id==obs$id)
  if(temp[x-1,"label_sentiment"]=="negative"){1}else{0}
}

func_bad_rev_after<-function(obs){
  temp<-dataset[dataset$appId==obs$appId,]
  temp<-temp[order(temp$revDate,decreasing = FALSE),]
  x<-which(temp[temp$appId==obs$appId,]$id==obs$id)
  if(temp[x+1,"label_sentiment"]=="negative"){1}else{0}
}

func_avg_words_freq_title<-function(obs){
  temp<-gsub(obs$revTitle,pattern = "[[:punct:]]",replacement = "")
  temp<-strsplit(temp," ")
  temp<-table(temp)
  mean(temp)
}

func_avg_words_freq_text<-function(obs){
  temp<-gsub(obs$revText,pattern = "[[:punct:]]",replacement = "")
  temp<-strsplit(temp," ")
  temp<-table(temp)
  mean(temp)
}

func_num_unique_words_title<-function(obs){
  temp<-gsub(obs$revTitle,pattern = "[[:punct:]]",replacement = "")
  temp<-strsplit(temp," ")
  temp<-table(temp)
  length(temp)
}

func_num_unique_words_text<-function(obs){
  temp<-gsub(obs$revText,pattern = "[[:punct:]]",replacement = "")
  temp<-strsplit(temp," ")
  temp<-table(temp)
  length(temp)
}

func_unique_words_to_words_title_ratio<-function(obs){
  temp<-gsub(obs$revTitle,pattern = "[[:punct:]]",replacement = "")
  temp<-strsplit(temp," ")
  temp1<-table(temp)
  length(temp1)/length(unlist(temp))
}

func_unique_words_to_words_text_ratio<-function(obs){
  temp<-gsub(obs$revText,pattern = "[[:punct:]]",replacement = "")
  temp<-strsplit(temp," ")
  temp1<-table(temp)
  length(temp1)/length(unlist(temp))
}

func_stdev_num_words_title_text<-function(obs){
  temp<-gsub(obs$revTitle,pattern = "[[:punct:]]",replacement = "")
  temp<-strsplit(temp," ")
  temp1<-gsub(obs$revText,pattern = "[[:punct:]]",replacement = "")
  temp1<-strsplit(temp," ")
  sd(c(length(unlist(temp)),length(unlist(temp1))))
}
