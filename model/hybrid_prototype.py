from matplotlib import pyplot
from math import *
from pandas import DataFrame
import random
from lstm import *
from errors import *

from data_handler import *


if __name__ == "__main__":
    train_size = 1000
    test_size = 3000

    dh = DataHandler("../dailydata/forex/EURUSD.csv")
    # dh = DataHandler("./Sunspots.csv")

    # Creates 2 new columns that are lagged by 1. These columns are
    # the 'features'.
    dh.timeSeriesToSupervised()
    test_size = len(dh.tsdata) - train_size
    dh.splitData(test_size, train_size, len(dh.tsdata) - train_size - test_size)
    train, test, out = dh.getDataSets()

    trainx, trainy = train[:, 1], train[:, 3]
    trainy = trainy.reshape(trainy.shape[0], 1)
    trainx = trainx.reshape(trainx.shape[0], 1)
    trainx = trainx.reshape((trainx.shape[0], 1, trainx.shape[1]))

    testx, testy = test[:, 1], test[:, 3]
    testx = testx.reshape(testx.shape[0], 1)
    testx = testx.reshape((testx.shape[0], 1, testx.shape[1]))

    print("Training Base Model...")
    base = MyLSTM(trainx.shape[1], 4, [27, 35, 3, 45], trainy.shape[1],
                  epochs=750, batch_size=100, fit_verbose=0)
    base.train(trainx, trainy)

    yhat = base.predict(trainx)
    errors = trainy[:, 0] - yhat[:, 0]
    errors = errors.reshape(errors.shape[0], 1)

    print("Training Error Model...")
    error = MyLSTM(trainx.shape[1], 1, [43], errors.shape[1], epochs=720,
                   batch_size=100, fit_verbose=0)
    error.train(trainx, errors)

    yhat_e = error.predict(testx)
    yhat_v = base.predict(testx)
    yhat = yhat_v + yhat_e

    print("MSE Single: ", mse(testy, yhat_v))
    print("MSE Hybrid: ", mse(testy, yhat))
