from errors import *
from data_handler import *
from lstm import *
from threading import Thread
from multiprocessing import Queue
import random
import copy
import time


def train_individual(trainx, trainy, testx, testy, output):
    lstm = MyLSTM(trainx.shape[1], 1, [300 for _ in range(10)], \
                  trainy.shape[1], epochs=100, batch_size=100)
    lstm.train(trainx, trainy)
    yhat = lstm.predict(testx)
    error = mse(testy, yhat)

    # output will be map between hyperparams and error
    out = str(error) + ':1, 300, 100'
    output.put(out)


if __name__ == '__main__':
    """
        Need to make this into a class that accepts hyper params for the GA and
        runs any model that has a .train and .predict method
    """
    random.seed(time.time)
    output = Queue()

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

    """ Works """
    for k in range(0, 10):
        train_individual(trainx, trainy, testx, testy, output)
    print(output)

    """
        Seems to be an issue with running these in parallel on the GPU. Can't
        seem to allocate enough memory. About 3 or 4 out of 12 will actually be
        run while the rest error.

        Maybe try threading? -- Also didn't work

        The Keras GitHub seems to imply this can't be done.
    """
    # cpu_count = multiprocessing.cpu_count()
    # cpu_count = 4
    # processes = [multiprocessing.Process(target=train_individual, args=(trainx, trainy, testx, testy, output))\
    #              for _ in range(cpu_count)]
    # for p in processes:
    #     p.start()
    # for p in processes:
    #     p.join()
    #
    # for q in iter(output.get, None):
    #     print(q)
