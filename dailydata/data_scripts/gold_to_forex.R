# adds rows where necessary to fill missing spots in gold dataframe
# essentially want to match rows in forex dataframe. Using Bid.Average

diff <- nrow(forex) - nrow(gold.filter)
print(diff)

pall_idx <- 1
for(i in 1:nrow(forex)) {
    f <- forex[i, ]
    p <- gold.filter[pall_idx, ]
    if(f$Date != p$Date) {
        # create new row
        price <- 0
        if(pall_idx > 1) {
            price <- gold.filter[pall_idx,]$Bid.Average + gold.filter[pall_idx-1,]$Bid.Average
            price <- price / 2
        } else {
            price <- gold.filter[pall_idx,]$Bid.Average
        }
        date <- f$Date
        r <- c(date, price)
        
        # add to dataframe
        gold.filter[seq(pall_idx + 1, nrow(gold.filter)+1), ] <- gold.filter[seq(pall_idx, nrow(gold.filter)), ]
        gold.filter[pall_idx, ]$Date <- date
        gold.filter[pall_idx, ]$Bid.Average <- price
    }
    pall_idx <- pall_idx + 1
}