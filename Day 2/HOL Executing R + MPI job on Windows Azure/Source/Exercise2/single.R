# first make some data
n <- 1000       # number of obs
p <- 30         # number of variables
                                                                                
x <- matrix(rnorm(n*p),n,p)
beta <- c(rnorm(p/2,0,5),rnorm(p/2,0,.25))
y <- x %*% beta + rnorm(n,0,20)
thedata <- data.frame(y=y,x=x)
                                                                                
summary(lm(y~x))
                                                                                
fold <- rep(1:10,length=n)
fold <- sample(fold)
                                                                                
rssresult <- matrix(0,p,10)
for (j in 1:10)
    for (i in 1:p) {
        templm <- lm(y~.,data=thedata[fold!=j,1:(i+1)])
        yhat <- predict(templm,newdata=thedata[fold==j,1:(i+1)])
        rssresult[i,j] <- sum((yhat-y[fold==j])^2)
        }
                                                                                
# this plot shows cross-validated residual sum of squares versus the model
# number.  As expected, the most important thing is including the first p/2
# of the predictors.
                                                                                
plot(apply(rssresult,1,mean))
