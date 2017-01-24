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




