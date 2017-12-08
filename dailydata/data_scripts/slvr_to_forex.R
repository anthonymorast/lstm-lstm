# adds rows where necessary to fill missing spots in silver dataframe
# essentially want to match rows in forex dataframe. Using Bid.Average

diff <- nrow(forex) - nrow(silver.filter)
print(diff)

pall_idx <- 1
for(i in 1:nrow(forex)) {
    f <- forex[i, ]
    p <- silver.filter[pall_idx, ]
    if(f$Date != p$Date) {
        # create new row
        price <- 0
        if(pall_idx > 1) {
            price <- silver.filter[pall_idx,]$Bid.Average + silver.filter[pall_idx-1,]$Bid.Average
            price <- price / 2
        } else {
            price <- silver.filter[pall_idx,]$Bid.Average
        }
        date <- f$Date
        r <- c(date, price)
        
        # add to dataframe
        silver.filter[seq(pall_idx + 1, nrow(silver.filter)+1), ] <- silver.filter[seq(pall_idx, nrow(silver.filter)), ]
        silver.filter[pall_idx, ]$Date <- date
        silver.filter[pall_idx, ]$Bid.Average <- price
    }
    pall_idx <- pall_idx + 1
}