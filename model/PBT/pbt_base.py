from errors import *
from data_handler import *
from lstm import *
import time
from pbt_proc_single import *
import multiprocessing
import os
import subprocess

"""
    best.dat format:
        best error
        # hidden layer
        hidden layer sizes
        # epochs
        previous best
        threshold count
"""


if __name__ == '__main__':
    random.seed(time.time)
    filename = './model/PBT/best.dat'

    # dh = DataHandler('../dailydata/forex/EURUSD.csv')
    # dh = DataHandler('./Sunspots.csv')
    dh = DataHandler('./model/mackey.csv')
    dh.timeSeriesToSupervised()
    dh.splitData(500, len(dh.tsdata) - 500, 0)

    train, test, out = dh.getDataSets()

    trainx, trainy = train[:, 1], train[:, 3]
    testx, testy = test[:, 1], test[:, 3]
    trainy = trainy.reshape(trainy.shape[0], 1)
    trainx = trainx.reshape(trainx.shape[0], 1)
    testx = testx.reshape(testx.shape[0], 1)
    trainx = trainx.reshape((trainx.shape[0], 1, trainx.shape[1]))
    testx = testx.reshape((testx.shape[0], 1, testx.shape[1]))

    start = time.time()
    # pbt = PBT(trainx, trainy, testx, testy, threshold=10)
    # params = pbt.train()

    # read data from previous run, if exists. Otherwise initalize.
    best = []
    threshold_count = 0
    prevBest = 9999999
    if os.path.isfile(filename):
        f = open(filename)
        bestError = float(f.readline())
        num_hidden_layers = int(f.readline())
        layer_sizes = f.readline().split(',')
        layer_sizes = layer_sizes[:-1]
        layer_sizes = [int(i) for i in layer_sizes]
        epochs = int(f.readline())
        f.readline()
        threshold_count = int(f.readline())
        best = [bestError, [num_hidden_layers, layer_sizes, epochs]]
        prevBest = bestError
    else:
        threshold_count = 0
        best = [9999999, [1, [1,2], 1], []]
        prevBest = best[0]
    if threshold_count >= 25:   #threshold
        print("Threshold count reached.")
        exit(0)

    # create new best file
    p = multiprocessing.Process(target=run, args=(trainx, trainy, testx, testy, best, mse, 10))
    p.start()
    p.join()

    with open(filename, 'r') as f:
        bestLine = f.readline()
        if float(prevBest) == float(bestLine):
            threshold_count = threshold_count + 1
        else:
            threshold_count = 0
        f.close()

    with open(filename, 'a') as f:
        f.write(str(prevBest) + '\n')
        f.write(str(threshold_count) + '\n')
        f.close()

    print("Time Elapsed (seconds): " + str(time.time() - start))
    subprocess.Popen(['python', './model/PBT/pbt_base.py'])
    exit(0)
