from statsmodels.tsa.arima_model import ARIMA, ARIMAResults
from statsmodels.base.model import Results
from matplotlib import pyplot
import pandas as pd

from data_handler import *
from errors import *


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
	test_size = 1000

	# dh = DataHandler("../dailydata/forex/EURUSD.csv")
	dh = DataHandler("./Sunspots.csv")
	data = dh.data.values[:, 1]

	train, test, out_of_sample = data[:train_size], data[train_size:(train_size+test_size)], data[(train_size+test_size):]
	hist = [x for x in test]

	#pd.tools.plotting.autocorrelation_plot(trainx)
	#pyplot.show()

	# arima = Arima(train, 5, 1, 0, 'D')
	# arima.fit()
	# errors = pd.DataFrame(arima.get_residuals())
	#pyplot.plot(errors)
	#pyplot.show()

	predictions = []
	model = ARIMA(hist, order=(1, 0, 2))
	results = model.fit(disp=0)
	for i in range(len(out_of_sample)):
		model = ARIMA(hist, order=(1, 0, 2))
		fit = model.fit(disp=0)
		output = fit.forecast()
		yhat = output[0]
		predictions.append(yhat)
		obs = out_of_sample[i]
		hist.append(obs)
		del hist[0]
		print(i, len(hist))
		# print('predicted: %f\texpected: %f\tdiff: %f' % (yhat, obs, abs(yhat-obs)))

	print(mse(out_of_sample, predictions))

	pyplot.title("ARIMA vs. Actual")
	pyplot.plot(out_of_sample, 'bs', label='actual')
	# pyplot.plot(yhat_v, 'r^', label='single lstm')
	pyplot.plot(predictions, 'go', label='hybrid')
	pyplot.ylabel("Sunspots")
	pyplot.xlabel("Time")
	pyplot.legend()
	# pyplot.show()
