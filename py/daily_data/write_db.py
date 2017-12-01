import sqlite3
import sys
import os
import struct 
import calendar
import time

def usage():
	print('\nUSAGE:')
	print('\tpython write_db.py <.daily file>')
	print('\tOR')
	print('\tpython write_db.py * (or list of files)\n')

def check_args(argv):
	if len(argv) < 2:
		usage()
		return False
	return True


if __name__ == '__main__':
	if not check_args(sys.argv):
		exit(0)

	files = []
	for i in range(1, len(sys.argv)):
		if sys.argv[i].endswith('.daily'):
			files.append(sys.argv[i])
	
	if len(files) == 0:
		print('No daily files input')
		exit(0)

	conn = sqlite3.connect('daily_data.db')
	cursor = conn.cursor()
	for filename in files:
		f = open(filename, 'rb')
		filesize = os.path.getsize(filename)
		iters = filesize / 16
		ticker = filename[0:6]
		print("Processing: " + ticker)

		i = 0
		while i < iters:
			i += 1
			b = f.read(16)
			values = struct.unpack('Qff', b)
			t = time.gmtime(values[0]/1000)
			ask = values[1]
			bid = values[2]
			ast = time.asctime(t)
			sql = "INSERT INTO DAILY VALUES ('" + ticker + "', '" + ast + "', " + str(bid) + ", " + str(ask) + ");"
			cursor.execute(sql)
		conn.commit()
	conn.close()
