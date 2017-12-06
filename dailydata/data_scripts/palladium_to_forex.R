# adds rows where necessary to fill missing spots in palladium dataframe
# essentially want to match rows in forex dataframe. Using Bid.Average

diff <- nrow(forex) - nrow(pall.filter)
print(diff)

pall_idx <- 1
for(i in 1:nrow(forex)) {
    f <- forex[i, ]
    p <- pall.filter[pall_idx, ]
    if(f$Date != p$Date) {
        # create new row
        price <- 0
        if(pall_idx > 1) {
            price <- pall.filter[pall_idx,]$Bid.Average + pall.filter[pall_idx-1,]$Bid.Average
            price <- price / 2
        } else {
            price <- pall.filter[pall_idx,]$Bid.Average
        }
        date <- f$Date
        r <- c(date, price)
        
        # add to dataframe
        pall.filter[seq(pall_idx + 1, nrow(pall.filter)+1), ] <- pall.filter[seq(pall_idx, nrow(pall.filter)), ]
        pall.filter[pall_idx, ]$Date <- date
        pall.filter[pall_idx, ]$Bid.Average <- price
    }
    pall_idx <- pall_idx + 1
}