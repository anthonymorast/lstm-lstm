import time
import struct
import calendar
import sys
import os


'''
	Dump the data from the binary data files.

	This will be used as some inputs to the NN. Will probably want 
	to return 
'''
def dump_data(filename):
	f = open(filename, 'rb')
	fileSize = os.path.getsize(filename)
	print(fileSize)	

	# read 16 bytes (sizeof(data_rec.h))
	b = f.read(16)
	
	# first 8 bytes = time, second = ask price, third = bid price
	# unpacks bytes into list of values (Qff are formats found here 
	# https://docs.python.org/3.6/library/struct.html#format-characters)
	values = struct.unpack('Qff', b)
	print(values)
	t = time.asctime(time.gmtime(values[0]/1000))
	print('Time: ' + str(t) + '\task: ' + str(values[1]) + '\tbid: ' + str(values[2]))

'''
	Dump the optimal solutions from a *.optimal binary file.
	
	Use this to get the optimal trading decisions for a given day/hour/minute/second
	or whatever. This will be the y values. The ticker passed to this function is the
	one for which we're trying to predict trading decisions. 
'''
def dump_optimal(filename):
	f = open(filename, 'rb')
	filesize = os.path.getsize(filename)	

	# read 9 bytes (time + bool)
	b = f.read(9)
	
	# unpack into time and trading decision
	values = struct.unpack('Q?', b)
	t = time.asctime(time.gmtime(values[0]))
	print('Date: ' + str(t) + '\tChoice: ' + str(values[1]))
	

def get_daily_price(filename):
	ret_list = []
	f = open(filename, 'rb')
	filesize = os.path.getsize(filename)
	iters = filesize / 16

	i = 0
	while i < iters:
		i += 1
		b = f.read(16)
		values = struct.unpack('Qff', b)
		t = time.gmtime(values[0]/1000)
		start_tm = t
		curr_day = t.tm_mday
		total_ask = values[1]
		total_bid = values[2]
		count = 1
		# values[1] = ask, values[2] = bid
		while t.tm_mday == curr_day and i < iters:
			b = f.read(16)
			values = struct.unpack('Qff', b)
			t = time.gmtime(values[0]/1000)
			i += 1
			count += 1
			total_ask += values[1]
			total_bid += values[2]
		ask = total_ask/count
		bid = total_bid/count
		secs_to_minus = start_tm.tm_hour*60*60 + start_tm.tm_min*60 + start_tm.tm_sec
		dt = (calendar.timegm(start_tm) - secs_to_minus) * 1000
		nt = time.gmtime(dt/1000)
#		print('Date (Old): ' + str(time.asctime(start_tm)) + '\t(New) Date: ' + str(time.asctime(nt)) + '\tAvg ask: ' + str(ask) + '\tAvg bid: ' + str(bid))
		ret_list.append([dt, ask, bid])
	
	return ret_list


'''
	Main function.
'''
if __name__ == '__main__':
	if len(sys.argv) < 2:
		print('usage: data_file')
		exit(0)

	tickers = []
	ticker_files = []
	for i in range(1, len(sys.argv)):
		ticker_files.append(sys.argv[i])
		tickers.append(sys.argv[i][-6:])

	for i in range(0, len(ticker_files)):
		print("Processing: " + tickers[i])
		daily = get_daily_price(ticker_files[i])
		with open(tickers[i] + '.daily', 'wb') as out:
			for day in daily:
				# int seems to cast to 64 bits....
				# print(day[0], int(day[0]))
				out.write(struct.pack('Qff', int(day[0]), float(day[1]), float(day[2])))
