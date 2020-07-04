setwd("~/GitHub/UOW-CSCI992-Spring-2019-Team-B/src/ml")

# https://stackoverflow.com/questions/26237688/rmse-root-mean-square-deviation-calculation-in-r
#
rmse = function(predictions, targets){ 
  return(sqrt(mean((predictions - targets) ** 2))) 
}


train_list = c('train-003.csv', 'train-004.csv',
               'train-005.csv', 'train-006.csv', 'train-007.csv')

for(train in train_list) {
  print('------------------')
  print(train)
  
  df <- read.csv(train)
  print(levels(as.factor(df$y)))
  
  right <- 0
  wrong <- 0
  for (r in 1:nrow(df)) {
    if (df$sirna[r] == df$y[r]) {
      print(r)
      print(df$sirna[r])
      right <- right + 1
    } else {
      wrong <- wrong + 1
    }
  }
  
  score <- right / nrow(df)
  trainng_error <- wrong / nrow(df)
  
  print(score)
  print(trainng_error)
  
  print(rmse(df$sirna, df$y))
}


df_d <- data.frame("epoch" = c(100, 200, 500, 1000, 3000), "rmse" = c(461.1742, 420.6447, 400.2201, 362.269, 315.4277))
head(df_d)

plot(df_d, xlab="epoches", ylab="RMSE")
lines(df_d)
