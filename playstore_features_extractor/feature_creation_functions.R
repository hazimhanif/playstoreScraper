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



