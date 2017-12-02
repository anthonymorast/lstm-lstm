import tensorflow as tf
from matplotlib import pyplot
from keras.models import Sequential
from keras.layers import Dense, LSTM
from math import *
from pandas import DataFrame
import random

from data_handler import * 


def getDifferenceStats(seriesData):
	obs = len(seriesData)
	diff = []
	seriesData = [float(i) for i in seriesData]
	for i in range(1, obs):
		diff.append(seriesData[i] - seriesData[i-1])
	return min(diff), max(diff), sum(diff)/len(diff)


if __name__ == "__main__":
	train_size = 1000
	test_size = 2000

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

	trainx = trainx.reshape(trainx.shape[0], 1)
	testx = testx.reshape(testx.shape[0], 1)
	outx = outx.reshape(outx.shape[0], 1)
	trainx = trainx.reshape((trainx.shape[0], 1, trainx.shape[1]))
	testx = testx.reshape((testx.shape[0], 1, testx.shape[1]))
	outx = outx.reshape((outx.shape[0], 1, outx.shape[1]))
	
	lstm_v = Sequential()
	lstm_v.add(LSTM(50, input_shape=(trainx.shape[1], trainx.shape[2])))
	lstm_v.add(Dense(1))
	lstm_v.compile(loss='mean_squared_error', optimizer='adam')
	# history = lstm_v.fit(trainx, trainy, epochs=25, batch_size=100, validation_data=(testx, testy), verbose=2, shuffle=False)
	print("\n\nTraining Series Model...")
	history = lstm_v.fit(trainx, trainy, epochs=25, batch_size=100, verbose=2, shuffle=False)

	# get error data and train error lstm
	yhat = lstm_v.predict(testx)
	error = testy-yhat[:, 0]
	mse = sum(error**2) / len(yhat)

	# error = output (y) for each input (series value)
	e_trainx = testx
	e_trainy = error
	
	lstm_e = Sequential()
	lstm_e.add(LSTM(50, input_shape=(e_trainx.shape[1], e_trainx.shape[2])))
	lstm_e.add(Dense(1))
	lstm_e.compile(loss='mean_squared_error', optimizer='adam')
	print("\n\nTraining Error Model...")
	history_e = lstm_e.fit(e_trainx, e_trainy, epochs=25, batch_size = 100, verbose=2, shuffle=False)


	# with both models trained, pass in out_x to each prediction
	yhat_v = lstm_v.predict(outx)
	yhat_e = lstm_e.predict(outx)

	error_v = outy - yhat_v[:, 0]	# get error of just the series lstm
	mse_v = sum(error_v**2) / len(error_v)

	yhat_ve = yhat_v + yhat_e
	error_ve = outy - yhat_ve[:, 0]
	mse_ve = sum(error_ve**2) / len(error_ve)

	yhat_vr = yhat_v.copy()
	for i in range(len(yhat_vr)):
		yhat_vr[i] += random.uniform(-.2, .2)
	error_vr = outy - yhat_vr[:, 0]
	mse_vr = sum(error_vr**2) / len(error_vr)

	yhat_range = yhat_v.copy()
	for i in range(len(yhat_range)):
		yhat_range[i] += random.uniform(-ma, ma)
	error_range = outy - yhat_range[:,0]
	mse_range = sum(error_range**2) / len(error_range)

	#for i in range(len(outx)):
	#	print("eurusd:", outy[i], ", naive prediction:", yhat_v[i, 0], ", hybrid prediction:", yhat_ve[i,0])
	print("\n\nSingle model MSE:\t\t", mse_v, "\nHybrid MSE:\t\t\t", mse_ve, "\nRandom Error Added MSE:\t\t", mse_vr, "\nMinMax Range Random MSE:\t", mse_range)
