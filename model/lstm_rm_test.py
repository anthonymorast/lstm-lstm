from errors import *
from data_handler import *
from lstm import *
import time
from pbt_lstm import *


if __name__ == '__main__':
    random.seed(time.time)

    dh = DataHandler('../dailydata/forex/EURUSD.csv')
    dh.timeSeriesToSupervised()
    dh.splitData(1000, 1000, len(dh.tsdata) - 2000)

    train, test, out = dh.getDataSets()

    trainx, trainy = train[:, 1], train[:, 3]
    testx, testy = test[:, 1], test[:, 3]
    trainy = trainy.reshape(trainy.shape[0], 1)
    trainx = trainx.reshape(trainx.shape[0], 1)
    testx = testx.reshape(testx.shape[0], 1)
    trainx = trainx.reshape((trainx.shape[0], 1, trainx.shape[1]))
    testx = testx.reshape((testx.shape[0], 1, testx.shape[1]))

    lstm = MyLSTM(trainx.shape[1], 8, [41,81,21,27,48,66,65,55],
                  trainy.shape[1], epochs=500, fit_verbose=2,
                  batch_size=100)
    lstm.train(trainx, trainy)
    y_hat = lstm.predict(testx)
    print(mse(testy, y_hat))
 # New best error: 0.0628555460035, hyperparams= [3, [35, 29, 2], 167]
 # New best error: 0.00824273261169, hyperparams= [13, [33, 40, 24, 9, 19, 36, 39, 3, 45, 14, 24, 18, 32], 229]
