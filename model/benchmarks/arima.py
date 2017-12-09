from statsmodels.tsa.arima_model import ARIMA 
from matplotlib import pyplot
import pandas as pd

from data_handler import *


class Arima(object):
	def __init__(self, data, p, d, q, ddates):

		# p, d, q = 3, 1, 2 recommended by auto.arima in R
		self.model = ARIMA(data, [p, d, q], freq=ddates)

	def fit(self):
		self.model_fit = self.model.fit(disp=0)
		self.model_fit.summary()
		return self.model_fit

	def get_residuals(self):
		return self.model_fit.resid

	def predict(data):
		i = 0




if __name__ == "__main__":
	train_size = 1000
	test_size = 10

	dh = DataHandler("../../dailydata/forex/EURUSD.csv")
	data = dh.data.values[:, 1]

	train, test, out_of_sample = data[:train_size], data[train_size:(train_size+test_size)], data[(train_size+test_size):]
	hist = [x for x in train]

	#pd.tools.plotting.autocorrelation_plot(trainx)
	#pyplot.show()

	arima = Arima(train, 5, 1, 0, 'D')
	arima.fit()	
	errors = pd.DataFrame(arima.get_residuals())
	#pyplot.plot(errors)
	#pyplot.show()

	predictions = []
	for i in range(len(test)):
		model = Arima(hist, 5, 1, 0, 'D')
		fit = model.fit()
		output = fit.forecast()
		yhat = output[0]
		predictions.append(yhat)
		obs = test[i]
		hist.append(obs)
		print('predicted: %f\texpected: %f\tdiff: %f' % (yhat, obs, abs(yhat-obs)))

	mse = 0
	for i in range(len(predictions)):
		mse = mse + ((test[i] - predictions[i])**2)
	mse /= len(predictions)
	print(mse)
