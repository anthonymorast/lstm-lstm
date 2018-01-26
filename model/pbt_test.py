from errors import *
from data_handler import *
from lstm import *
import time
from pbt_lstm import *


def train_individual(trainx, trainy, testx, testy, output):
    lstm = MyLSTM(trainx.shape[1], 1, [300 for _ in range(10)], trainy.shape[1],
        epochs=100, batch_size=100, fit_verbose=0)
    lstm.train(trainx, trainy)
    yhat = lstm.predict(testx)
    error = mse(testy, yhat)

    # output will be map between hyperparams and error
    out = str(error) + ':1, 300, 100'
    output.append(out)


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

    start = time.time()
    pbt = PBT(trainx, trainy, testx, testy, threshold=10)
    params = pbt.train()
    print(params[0], params[1])
    print("Time Elapsed (seconds): " + str(time.time() - start))

    # start = time.time()
    # output = []
    # """ Works """
    # for k in range(0, 50):
    #     print("Iteration " + str(k) + " out of 50, time elapsed " +
    #           str(time.time() - start) + " seconds.")
    #     train_individual(trainx, trainy, testx, testy, output)
    # print("Time Elapsed (seconds): " + str(time.time() - start))
    # print(output)
    # exit()
