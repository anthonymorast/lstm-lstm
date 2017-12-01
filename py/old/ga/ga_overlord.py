from deap_ga import *
import os
import matplotlib.pyplot as plt

def plot_data(data, start_dt, end_dt):
	plt.plot([i for i in range(0, len(data))], data)
	plt.ylabel('Price')
	plt.xlabel('Days ['+ start_dt + ' - ' + end_dt + ']')
	plt.show()


data = DataClass()
start_dt = '1999-01-01'
timeframe = 90 #days

# num days = num_rows
num_days = len(data.getDataDict())
iters = int(num_days/timeframe)  # number of full <timeframe> days
last_days = (num_days - (timeframe*iters))-1 # count of last days 


# get data for full <timeframe> days 
headers = data.getFormattedHeaders()
for i in range(0, iters):
	run_dict = dict()
	for head in headers:
		run_dict[head] = []

	s_dt = datetime.datetime.strptime(start_dt, '%Y-%m-%d')
	while s_dt.weekday() >= 5:
		s_dt += datetime.timedelta(days=1)
	start_dt = s_dt.strftime('%Y-%m-%d')
	run_data, end_dt = data.getListOfPricesInRange(start_dt, 90)

	# rows to cols
	for row in run_data:
		for j in range(0, len(row)):
			run_dict[headers[j]].append(row[j])

	# run GA
	dir_ = './' + start_dt + '-' + end_dt
	if not os.path.exists(dir_):
		os.mkdir(dir_)
	for head in headers:		
		_data = run_dict[head]	
		outputFileName = dir_ + '/' + head + '.dat'
		pngfilename = dir_ + '/' + head + '.png'
		print("Processing " + head + " iter " + str(i))
		ga = ForexGA(_data, pngfilename, outputFileName, number_gens=100000, ind_size=timeframe, verbose=True, 
					 start_cash=(float(_data[0]) * 1.10)*100000, threshold=0.25)
		ga.create_and_run()

	t_dt = datetime.datetime.strptime(end_dt, '%Y-%m-%d')
	start_dt = (t_dt + datetime.timedelta(days=1)).strftime('%Y-%m-%d')


run_dict = dict()
for i in headers:
	run_dict[i] = []

# get data for last days 
run_data, end_dt = data.getListOfPricesInRange(start_dt, last_days)

# rows to cols
for row in run_data:
	for i in range(0, len(row)):
		run_dict[headers[i]].append(row[i])

dir_ = './' + start_dt + '-' + end_dt
if not os.path.exists(dir_):
	os.mkdir(dir_)
for head in headers:		
	_data = run_dict[head]	
	outputFileName = dir_ + head + '.dat'
	pngfilename = dir_ + head + '.png'
	ga = ForexGA(_data, pngfilename, outputFileName, number_gens=100000, ind_size=last_days, verbose=True,
				 start_cash=(float(_data[0]) * 1.10)*100000, threshold=0.25)
	ga.create_and_run()

