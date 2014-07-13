library(plyr)

args <- commandArgs(trailingOnly = TRUE)
nTasks <- as.integer(args[1])

top100 <- read.csv("chunk1.csv", stringsAsFactors = FALSE)
for(i in 2:nTasks) {
	fname <- sprintf("chunk%d.csv", i)
	tpart <- read.csv(fname, stringsAsFactors = FALSE)
	top100 <- rbind(top100, tpart)
}

top100s <- ddply(top100, c("sex", "year"), summarise, tot = sum(percent))

library(ggplot2)
qplot(year, tot, data = top100s, colour = sex, geom = "line", ylim = c(0, 1))
ggsave("bname-top100.png", width = 4, height = 3)