# add missing Oil rows as average bettween the two days

diff <- nrow(forex) - nrow(oil_dates)
print(diff)

if (diff > 0) {
    # append 3 rows since forex goes to 11/30 and oil goes to 11/27, grabbed real prices online
    oil_dates[nrow(oil_dates) + 1, ]$Day <- as.Date("11/28/2017", format="%m/%d/%Y")
    oil_dates[nrow(oil_dates), ]$Cushing.OK.WTI.Spot.Price.FOB.Dollars.per.Barrel <- 57.99
    
    oil_dates[nrow(oil_dates) + 1, ]$Day <- as.Date("11/29/2017", format="%m/%d/%Y")
    oil_dates[nrow(oil_dates), ]$Cushing.OK.WTI.Spot.Price.FOB.Dollars.per.Barrel <- 57.30
    
    oil_dates[nrow(oil_dates) + 1, ]$Day <- as.Date("11/30/2017", format="%m/%d/%Y")
    oil_dates[nrow(oil_dates), ]$Cushing.OK.WTI.Spot.Price.FOB.Dollars.per.Barrel <- 57.40
}

oil_idx <- 1
for(i in 1:nrow(forex)) {
    f <- forex[i, ]
    o <- oil_dates[oil_idx, ]
    if(f$Date != o$Day) {
        # create new row
        price <- 0
        if(oil_idx > 1) {
            price <- oil_dates[oil_idx,]$Cushing.OK.WTI.Spot.Price.FOB.Dollars.per.Barrel +
                    oil_dates[oil_idx-1,]$Cushing.OK.WTI.Spot.Price.FOB.Dollars.per.Barrel
            price <- price / 2
        } else {
            price <- oil_dates[oil_idx,]$Cushing.OK.WTI.Spot.Price.FOB.Dollars.per.Barrel
        }
        date <- f$Date
        r <- c(date, price)
        
        # add to dataframe
        oil_dates[seq(oil_idx + 1, nrow(oil_dates)+1), ] <- oil_dates[seq(oil_idx, nrow(oil_dates)), ]
        oil_dates[oil_idx, ]$Day <- date
        oil_dates[oil_idx, ]$Cushing.OK.WTI.Spot.Price.FOB.Dollars.per.Barrel <- price
    }
    oil_idx <- oil_idx + 1
}
