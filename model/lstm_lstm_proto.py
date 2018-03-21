from matplotlib import pyplot
from math import *
from pandas import DataFrame
import random
from lstm import *
from errors import *
import os

from data_handler import *


def getDifferenceStats(seriesData):
    obs = len(seriesData)
    diff = []
    seriesData = [float(i) for i in seriesData]
    for i in range(1, obs):
        diff.append(seriesData[i] - seriesData[i - 1])
    return min(diff), max(diff), sum(diff) / len(diff)


if __name__ == "__main__":
    train_size = 1000
    test_size = 1000

    # dh = DataHandler("../dailydata/forex/EURUSD.csv")
    dh = DataHandler("./model/Sunspots.csv")

    # Creates 2 new columns that are lagged by 1. These columns are
    # the 'features'.
    dh.timeSeriesToSupervised()

    tsvalues = dh.tsdata.values
    mi, ma, avg = getDifferenceStats(tsvalues[:, 3])

    train = tsvalues[:train_size, :]  # used to train lstm
    test = tsvalues[train_size:(train_size + test_size), :]  # get errors for error lstm
    out = tsvalues[(train_size + test_size):, :]  # predict these values with both lstm's
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


    base = MyLSTM(trainx.shape[1], 4,
                  [27, 25, 3, 45],
                  trainy.shape[1], epochs=756, batch_size=100)

    error_model = MyLSTM(testx.shape[1], 1, [43], testx.shape[1], epochs=728, batch_size=100)

    if os.path.isfile('base_weights.h5') and os.path.isfile('error_weights.h5'):
        base.load_model_weights('base_weights.h5')
        error_model.load_model_weights('error_weights.h5')
    else:
        print("\n\nTraining Base Model...")
        base.train(trainx, trainy)
        base.save_model_weights('base_weights.h5')

        # get error data and train error lstm
        yhat = base.predict(testx)
        error = testy - yhat[:, 0]
        mse_b = mse(testy, yhat)

        pyplot.title("Single LSTM Residuals")
        # pyplot.plot(yhat, error, 'bs', label="residuals") # no clue which we want
        pyplot.plot(error, 'bs', label="residuals")
        pyplot.legend()
        # pyplot.show()

        # error = output (y) for each input (series value)
        e_trainx = testx
        e_trainy = error.reshape(error.shape[0], 1)

        print("\n\nTraining Error Model...")
        error_model.train(e_trainx, e_trainy)
        error_model.save_model_weights('error_weights.h5')

    # works...
    for i in range(0, 100):
        smpl = outx[i]
        smpl = smpl.reshape(1, 1, 1)
        print(base.predict(smpl))

    # with both models trained, pass in out_x to each prediction
    yhat_v = base.predict(outx[:100, :, :])
    yhat_e = error_model.predict(outx[:100, :, :])
    mse_v = mse(outy[:100], yhat_v)
    for i in range(len(yhat_v)):
        print(yhat_v[i], outy[i])

    yhat_ve = yhat_v + yhat_e
    mse_ve = mse(outy[:100], yhat_ve)

    yhat_vr = yhat_v.copy()
    for i in range(len(yhat_vr)):
        yhat_vr[i] += random.uniform(-.2, .2)
    mse_vr = mse(outy[:100], yhat_vr)

    yhat_range = yhat_v.copy()
    for i in range(len(yhat_range)):
        yhat_range[i] += random.uniform(-ma, ma)
    mse_range = mse(outy[:100], yhat_range)

    # for i in range(len(outx)):
    # print("eurusd:", outy[i], ", naive prediction:", yhat_v[i, 0], ", hybrid prediction:", yhat_ve[i,0])
    print("\n\nSingle model MAE:\t\t", mse_v, "\nHybrid MAE:\t\t\t", mse_ve, "\nRandom Error Added MAE:\t\t", mse_vr,
          "\nMinMax Range Random MAE:\t", mse_range)

    pyplot.title("LSTM-LSTM vs. LSTM vs. Actual")
    pyplot.plot(outy[:100], 'bs', label='actual')
    pyplot.plot(yhat_v, 'r^', label='single lstm') # TODO: plot with best single
    pyplot.plot(yhat_ve, 'go', label='hybrid')
    pyplot.ylabel("EUR/USD Exchange Rate")
    pyplot.xlabel("Time (Days Since 6/23/2004)")
    pyplot.legend()
    # pyplot.show()
