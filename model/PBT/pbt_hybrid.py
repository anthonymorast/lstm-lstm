from errors import *
from data_handler import *
from lstm import *
import time
from pbt_lstm import *
from pbt_proc_hybrid import *
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
    best_file = 'PBT/best.dat'
    random.seed(time.time)

    dh = DataHandler('../dailydata/forex/EURUSD.csv')
    dh.timeSeriesToSupervised()
    dh.splitData(1000, 1000, len(dh.tsdata) - 2000)

    train, test, out = dh.getDataSets()

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

    start = time.time()
    # pbt = PBT(trainx, trainy, testx, testy, threshold=10)
    # params = pbt.train()

    # read data from previous run, if exists. Otherwise initalize.
    best = []
    threshold_count = 0
    prevBest = 9999999
    if os.path.isfile(best_file):
        f = open(best_file)
        bestError = float(f.readline())
        num_hidden_layers_base = int(f.readline())
        layer_sizes_base = f.readline().split(',')
        layer_sizes_base = layer_sizes_base[:-1]
        layer_sizes_base = [int(i) for i in layer_sizes_base]
        epochs_base = int(f.readline())
        num_hidden_layers_err = int(f.readline())
        layer_sizes_err = f.readline().split(',')
        layer_sizes_err = layer_sizes_err[:-1]
        layer_sizes_err = [int(i) for i in layer_sizes_err]
        epochs_err = int(f.readline())
        threshold_count = int(f.readline())
        best = [bestError, [num_hidden_layers_base, layer_sizes_base, epochs_base],
                [num_hidden_layers_err, layer_sizes_err, epochs_err]]
        prevBest = bestError
    else:
        threshold_count = 0
        best = [9999999, [1, [1,2], 1], [1, [1,2], 1]]
        prevBest = best[0]
    if threshold_count >= 50:   #threshold
        print("Threshold count reached.")
        exit(0)

    # create new best file
    p = multiprocessing.Process(target=run, args=(trainx, trainy, testx, testy,
                                                  outx, outy, best, mse, 10))
    p.start()
    p.join()

    with open(best_file, 'r') as f:
        bestLine = f.readline()
        if float(prevBest) == float(bestLine):
            threshold_count = threshold_count + 1
        else:
            threshold_count = 0
        f.close()

    with open(best_file, 'a') as f:
        f.write(str(threshold_count) + '\n')
        f.close()

    print("Time Elapsed (seconds): " + str(time.time() - start))
    subprocess.Popen(['python', 'PBT/pbt_hybrid.py'])
    exit(0)
