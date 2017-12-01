'''
	Reads the daily data from the CSV and stores it in a Python dictionary.
'''
import csv
import datetime


class DataClass(object):
	def __init__(self):
		self.data_dict = dict()
		with open('./data/daily_close.csv', 'r') as csvfile:
			reader = csv.reader(csvfile)
			for row in reader:
				k = row[0]
				v = row[1:]
				self.data_dict[k] = v

	def getDataDict(self):
		return self.data_dict

	def getHeaders(self):
		return self.data_dict['Date']

	def getFormattedHeaders(self):
		headers = self.data_dict['Date']
		for i in range(0, len(headers)):
			head = headers[i]
			head = head[:7]
			head = head.replace('/', '.')
			headers[i] = head
		return headers

	'''
		Breaks the data dictionary into a chunk of values from start_date to start_date + count days
	'''
	def getRangeOfDates(self, start_date, count):
		ret_dict = dict()
		date = datetime.datetime.strptime(start_date, "%Y-%m-%d")
		idx_add = 0
		for _ in range(0, count):
			it_date = date + datetime.timedelta(days=idx_add)
			it_date = it_date.strftime("%Y-%m-%d")
			
			found = False
			value = []
			while not found:
				try:
					value = self.data_dict[it_date]
					found = True
				except KeyError:
					idx_add += 1
					it_date = date + datetime.timedelta(days=idx_add)
					it_date = it_date.strftime("%Y-%m-%d")
			ret_dict[it_date] = value 
			idx_add += 1

		return ret_dict, it_date
	
	def getListOfPricesInRange(self, start_date, count):
		ret_list = []	
		date = datetime.datetime.strptime(start_date, "%Y-%m-%d")
		idx_add = 0
		for _ in range(0, count):
			it_date = date + datetime.timedelta(days=idx_add)
			while it_date.weekday() >= 5:
				idx_add += 1
				it_date = date + datetime.timedelta(days=idx_add)

			it_date = it_date.strftime("%Y-%m-%d")
			
			ret_list.append(self.data_dict[it_date])
			idx_add += 1
		return ret_list, it_date

