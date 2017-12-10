from data_handler import *
from parameter_ga import *


def getDifferenceStats(seriesData):
	obs = len(seriesData)
	diff = []
	seriesData = [float(i) for i in seriesData]
	for i in range(1, obs):
		diff.append(seriesData[i] - seriesData[i-1])
	return min(diff), max(diff), sum(diff)/len(diff)


if __name__ == "__main__":
	train_size = 1000
	test_size = 1000

	dh = DataHandler("../dailydata/forex/EURUSD.csv")

	# Creates 2 new columns that are lagged by 1. These columns are
	# the 'features'.
	dh.timeSeriesToSupervised()
	dh.tsdata.columns = ['DATE_LAG', 'TICKER_LAG', 'DATE', 'TICKER']

	tsvalues = dh.tsdata.values
	mi, ma, avg = getDifferenceStats(tsvalues[:, 3])

	train = tsvalues[:train_size, :]						# used to train lstm
	test = tsvalues[train_size:(train_size+test_size), :]	# get errors for error lstm
	out = tsvalues[(train_size+test_size):, :]				# predict these values with both lstm's
															# compare lstm_v rmse with lstm_v + lstm_e prediction rsme

	outx, outy = out[:, 1], out[:, 3]

	trainx, trainy = train[:, 1], train[:, 3]
	testx, testy = test[:, 1], test[:, 3]

	testy_dates = test[:, 2]

	# vec->2d
	trainy = trainy.reshape(trainy.shape[0], 1)
	trainx = trainx.reshape(trainx.shape[0], 1)
	testx = testx.reshape(testx.shape[0], 1)
	outx = outx.reshape(outx.shape[0], 1)
	trainx = trainx.reshape((trainx.shape[0], 1, trainx.shape[1]))
	testx = testx.reshape((testx.shape[0], 1, testx.shape[1]))
	outx = outx.reshape((outx.shape[0], 1, outx.shape[1]))

	ga = ParameterGA(None, trainx, trainy, testx, testy, outx, outy, number_gens=25, pop_size=10, ind_size=6)
	ga.create_and_run()	
