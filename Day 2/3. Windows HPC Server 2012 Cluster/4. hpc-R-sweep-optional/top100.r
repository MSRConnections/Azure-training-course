library(plyr)

args <- commandArgs(trailingOnly = TRUE)
taskId <- as.integer(args[1])

fname <- sprintf("chunk%d.csv", taskId)
bnames <- read.csv(fname, stringsAsFactors = FALSE)

bnames <- ddply(bnames, c("sex", "year"), transform, rank = rank(-percent, ties.method = "first"))
top100 <- subset(bnames, rank <= 100)

write.csv(top100, fname, row.names=FALSE)
