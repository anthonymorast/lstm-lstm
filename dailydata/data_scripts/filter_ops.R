##
## Below are the operations performed to read and filter the data to contain the
## same rows as the forex data frame. This example uses silver and applies to PERTH
## datasets.
##

# silver <- read.csv("commodities/PERTH-SLVR_USD_D.csv")
# silver.filter <- silver[silver$Date %in% forex$Date, ]
# plot(silver$Bid.Average)
# silver$Date <- as.Date(silver$Date, format="%Y-%m-%d")
# silver.filter <- silver.filter[, -8]
# silver.filter <- silver[silver$Date %in% forex$Date, ]
# silver.filter2 <- silver.filter
#
# after this we run the <var>_to_forex.R scripts

### PLOTTING (using gold now)
# plot(gold.filter$Bid.Average, forex$EUR.USD, col="blue", xlab="Gold Prices (Avg. Bid)", 
#      ylab="EUR/USD", main="Gold Prices (USD) vs. EUR/USD")
#
# cor(gold.filter$Bid.Average, forex$EUR.USD)
# gold.lm <- lm(forex$EUR.USD~gold.filter$Bid.Average)
# abline(gold.lm, col="green", lwd=2)
#
# Finally write a new CSV with the (good) filtered data
# write.csv(silver.filter, "commodities/real_silver.csv")