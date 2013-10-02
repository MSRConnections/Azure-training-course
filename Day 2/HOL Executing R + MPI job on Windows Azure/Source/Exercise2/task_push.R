
# Initialize MPI
library("Rmpi")

# Notice we just say "give us all the slaves you've got."
mpi.spawn.Rslaves()

if (mpi.comm.size() < 2) {
    print("More slave processes are required.")
    mpi.quit()
    }

.Last <- function(){
    if (is.loaded("mpi_initialize")){
        if (mpi.comm.size(1) > 0){
            print("Please use mpi.close.Rslaves() to close slaves.")
            mpi.close.Rslaves()
        }
        print("Please use mpi.quit() to quit R")
        .Call("mpi_finalize")
    }
}

# Function the slaves will call to perform a validation on the
# fold equal to their slave number.
# Assumes: thedata,fold,foldNumber,p
foldslave <- function() {
    # Get a task 
    task <- mpi.recv.Robj(mpi.any.source(),mpi.any.tag()) 
    task_info <- mpi.get.sourcetag() 
    tag <- task_info[2] 

    # While task is not a "done" message. Note the use of the tag to indicate 
    # the type of message
    while (tag != 2) {
        # Perform the task.  
        foldNumber <- task$foldNumber

        rss <- double(p)
        for (i in 1:p) {
            # produce a linear model on the first i variables on training data
            templm <- lm(y~.,data=thedata[fold!=foldNumber,1:(i+1)])

            # produce predicted data from test data
            yhat <- predict(templm,newdata=thedata[fold==foldNumber,1:(i+1)])

            # get rss of yhat-y
            localrssresult <- sum((yhat-thedata[fold==foldNumber,1])^2)
            rss[i] <- localrssresult
            }

        # Construct and send message back to master
        result <- list(result=rss,foldNumber=foldNumber)
        mpi.send.Robj(result,0,1)

        # Get a task 
        task <- mpi.recv.Robj(mpi.any.source(),mpi.any.tag()) 
        task_info <- mpi.get.sourcetag() 
        tag <- task_info[2] 
        }

    junk <- 0
    mpi.send.Robj(junk,0,2)
    }

# We're in the parent.  
# first make some data
n <- 1000	# number of obs
p <- 30		# number of variables

# Create data as a set of n samples of p independent variables,
# make a "random" beta with higher weights in the front.
# Generate y's as y = beta*x + random
x <- matrix(rnorm(n*p),n,p)
beta <- c(rnorm(p/2,0,5),rnorm(p/2,0,.25))
y <- x %*% beta + rnorm(n,0,20)
thedata <- data.frame(y=y,x=x)

fold <- rep(1:10,length=n)
fold <- sample(fold)

summary(lm(y~x))

# Now, send the data to the slaves
mpi.bcast.Robj2slave(thedata)
mpi.bcast.Robj2slave(fold)
mpi.bcast.Robj2slave(p)

# Send the function to the slaves
mpi.bcast.Robj2slave(foldslave)

# Call the function in all the slaves to get them ready to
# undertake tasks
mpi.bcast.cmd(foldslave())


# Create task list
tasks <- vector('list')
for (i in 1:10) {
    tasks[[i]] <- list(foldNumber=i)
    }

# Make the round-robin list for slaves
n_slaves <- mpi.comm.size()-1
slave_ids <- rep(1:n_slaves, length=length(tasks))

# Send tasks
for (i in 1:length(tasks)) {
    slave_id <- slave_ids[i]
    mpi.send.Robj(tasks[[i]],slave_id,1)
    }

# Collect results
rssresult <- matrix(0,p,10)
for (i in 1:length(tasks)) {
    message <- mpi.recv.Robj(mpi.any.source(),mpi.any.tag())
    foldNumber <- message$foldNumber
    results    <- message$result
    rssresult[,foldNumber] <- results
    }

# Perform closing handshake
for (i in 1:n_slaves) {
    junk <- 0
    mpi.send.Robj(junk,i,2)
    }

for (i in 1:n_slaves) {
    mpi.recv.Robj(mpi.any.source(),2)
    }

# plot the results
plot(apply(rssresult,1,mean))

mpi.close.Rslaves()
mpi.quit(save="no")

