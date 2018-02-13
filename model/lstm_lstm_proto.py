from matplotlib import pyplot
from math import *
from pandas import DataFrame
import random
from lstm import *
from errors import *

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

    dh = DataHandler("../dailydata/forex/EURUSD.csv")

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

    # not bad
    # base = MyLSTM(trainx.shape[1], 1, [50 for _ in range(3)], trainy.shape[1], epochs=200, batch_size=100)
    # base = MyLSTM(trainx.shape[1], 1, [250 for _ in range(3)], trainy.shape[1], epochs=100, batch_size=100)
    # # good: base = MyLSTM(trainx.shape[1], 1, [250 for _ in range(10)], trainy.shape[1], epochs=100, batch_size=100)
    # # baseline: base = MyLSTM(trainx.shape[1], 1, [300 for _ in range(10)], trainy.shape[1], epochs=100, batch_size=100)
    # PBT: model is too strong, makes worse hybrid (need weak nonlinearities)
    base = MyLSTM(trainx.shape[1], 7,
                  [8,38,46,31,49,14,14],
                  trainy.shape[1], epochs=235, batch_size=100)
    base = MyLSTM(trainx.shape[1], 2, [35 for _ in range(2)],
                   trainy.shape[1], epochs=100, batch_size=200, fit_verbose=2)
    print("\n\nTraining Base Model...")
    base.train(trainx, trainy)

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

    # not bad
    # error = MyLSTM(e_trainx.shape[1], 50, [50 for _ in range(50)], e_trainy.shape[1], epochs=200, batch_size=100)
    # good: error = MyLSTM(e_trainx.shape[1], 3, [50 for _ in range(10)], e_trainy.shape[1], epochs=150, batch_size=100)
    error = MyLSTM(e_trainx.shape[1], 6, [8,29,10,36,41,3],
                   e_trainy.shape[1], epochs=213, batch_size=150)
    error = MyLSTM(e_trainx.shape[1], 2, [17, 10], e_trainy.shape[1], epochs=242, batch_size=100)
    # error = MyLSTM(e_trainx.shape[1], 3, [50 for _ in range(10)], e_trainy.shape[1], epochs=100, batch_size=100)
    print("\n\nTraining Error Model...")
    error.train(e_trainx, e_trainy)

    # with both models trained, pass in out_x to each prediction
    yhat_v = base.predict(outx)
    yhat_e = error.predict(outx)
    mse_v = mse(outy, yhat_v)

    yhat_ve = yhat_v + yhat_e
    mse_ve = mse(outy, yhat_ve)

    yhat_vr = yhat_v.copy()
    for i in range(len(yhat_vr)):
        yhat_vr[i] += random.uniform(-.2, .2)
    mse_vr = mse(outy, yhat_vr)

    yhat_range = yhat_v.copy()
    for i in range(len(yhat_range)):
        yhat_range[i] += random.uniform(-ma, ma)
    mse_range = mse(outy, yhat_range)

    # for i in range(len(outx)):
    # print("eurusd:", outy[i], ", naive prediction:", yhat_v[i, 0], ", hybrid prediction:", yhat_ve[i,0])
    print("\n\nSingle model MAE:\t\t", mse_v, "\nHybrid MAE:\t\t\t", mse_ve, "\nRandom Error Added MAE:\t\t", mse_vr,
          "\nMinMax Range Random MAE:\t", mse_range)

    pyplot.title("LSTM-LSTM vs. LSTM vs. Actual")
    pyplot.plot(outy, 'bs', label='actual')
    pyplot.plot(yhat_v, 'r^', label='single lstm')
    pyplot.plot(yhat_ve, 'go', label='hybrid')
    pyplot.ylabel("EUR/USD Exchange Rate")
    pyplot.xlabel("Time (Days Since 6/23/2004)")
    pyplot.legend()
    # pyplot.show()
