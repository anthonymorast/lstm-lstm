import urllib2
import datetime
import csv

### PYTHON2 
##	Gets data from a forex trading site. Can only get daily high, low, and close data which should be good enough.
# 	Can get data from 1/1/1999 until present day, start the day before just in case. Needed to get these one at a time
#		since their bulk grab just gives summaries.
#	Change Submit=<> to: 
#		Get%20Weekly%20Stats for weekly stats
#		Get%20Monthly%20Stats for monthly stats
# 	Change the date range as necessary
# 	Can change CLOSE_<#> to HIGH_<#> or LOW_<#> where # ranges from 1-13 as follows:
#		1 - EUR/USD
#		2 - USD/JPY
#		3 - USD/CHF
#		4 - GBP/USD
#		5 - USD/CAD
#		6 - EUR/GBP
#		7 - EUR/JPY
#		8 - EUR/CHF
#		9 - AUD/USD
#		10 - GBP/JPY
#		11 - CHF/JPY
#		12 - GBP/CHF
#		13 - NZD/USD
#
# 	A few less than Gain Capital but not too bad. 
###
url = 'http://global-view.com/forex-trading-tools/forex-history/exchange_csv_report.html?<stat>_<id>=ON&start_date=<start>&stop_date=<stop>&Submit=<type>'

# STATS
CLOSE = 'CLOSE'
HIGH = 'HIGH'
LOW = 'LOW'

# TYPES
DAILY = "Get%20Daily%20Stats"
MONTHLY = "Get%20Monthly%20Stats"
WEEKLY = "Get%20Weekly%20Stats"

# Get current date (get data up until today)
now = datetime.datetime.now()
stop_date = str(now.strftime('%m/%d/%Y'))

start_date = '1/1/1999' # start of data collection 
id_start = 1
id_end = 13


# Get Data
t_url = 'http://global-view.com/forex-trading-tools/forex-history/exchange_csv_report.html?CLOSE_13=ON&start_date=1/1/1999&stop_date=06/05/2017&Submit=Get%20Daily%20Stats'
run_id = id_start
dates = []
col_heads = ['Date']
values = []
while run_id <= id_end:
	run_url = url.replace('<stat>', CLOSE)
	run_url = run_url.replace('<start>', start_date)
	run_url = run_url.replace('<id>', str(run_id))
	run_url = run_url.replace('<stop>', stop_date)
	run_url = run_url.replace('<type>', DAILY)

	print(run_url)	
	response = urllib2.urlopen(run_url)
	data=response.read()
	data = data.split('\r\n')
	data = data[7:]
	
	col_heads.append(data[0].split(',')[1])
	data = data[1:]
	if run_id == 1:
		for dat in data:
			if len(dat) > 0:
				dates.append(dat.split(',')[0])

	run_vals = []
	for dat in data:
		if len(dat) > 0:
			run_vals.append(dat.split(',')[1])

	values.append(run_vals)
	run_id += 1


# Print CSV
rows = []
for idx in range(0, len(dates)):
	row = [dates[idx]]
	for val_list in values:
		row.append(val_list[idx])
	rows.append(row)

with open('daily_close.csv', 'wb') as csvfile:
	writer = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
	writer.writerow(col_heads)
	for row in rows:
		writer.writerow(row)	
