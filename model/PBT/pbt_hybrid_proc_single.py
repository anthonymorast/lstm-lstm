from lstm import *
import sys
import random
import time
import copy

def getLSTM():
    """
        Creates a population member.
    """
    global trainx, trainy
    hidden_layers = random.randint(2, 15)
    layer_sizes = []
    for _ in range(0, hidden_layers):
        layer_sizes.append(random.randint(2, 50))
    hyperparams = [hidden_layers, layer_sizes, random.randint(50, 250)]
    return [MyLSTM(trainx.shape[1], hyperparams[0], hyperparams[1],
                  trainy.shape[1], epochs=hyperparams[2], fit_verbose=0,
                  batch_size=100), hyperparams]


def eval(model):
    """
        Gets preditions from the model and measures the error for model
        goodness.
    """
    global testx, testy, error_func, L1

    y_hat_v = L1.predict(testx)
    y_hat_e = model[0].predict(testx)
    y_hat = y_hat_v + y_hat_e

    return error_func(testy, y_hat[:,0])


def step(model):
    """
        Trains the model using its built in train method.
    """
    global trainx, trainy
    print('\tTraining model with hyperparams: ', model[1])
    model[0].train(trainx, trainy)


def explore(index):
    """
        Get new weights for population member
    """
    global models
    models[index] = getLSTM()


def exploit(index, best):
    """
        Set the weights and hyperparams and apply a mutation.
    """
    global models, trainx, trainy
    # best Format: MSE, hyperparams, weights
    hyperparams = copy.deepcopy(best[1])

    # Mutate
    hyperparams[0] = hyperparams[0] + random.randint(-2, 2)
    for i in range(0, hyperparams[0]):
        if i < len(hyperparams[1]):
            hyperparams[1][i] = hyperparams[1][i] + random.randint(-10, 10)
        else:
            hyperparams[1].append(random.randint(2, 50))
        if hyperparams[1][i] <= 0:
            hyperparams[1][i] = random.randint(2, 50)
        if len(hyperparams[1]) > hyperparams[0]:
            hyperparams[1] = hyperparams[1][:hyperparams[0]]
    hyperparams[2] = hyperparams[2] + random.randint(-15, 15)
    if hyperparams[2] < 50:
        hyperparams[2] = 50

    models[index] = [MyLSTM(trainx.shape[1], hyperparams[0], hyperparams[1],
                  trainy.shape[1], epochs=hyperparams[2], fit_verbose=0, batch_size=100),
                  hyperparams]

def train():
    """
        Run a single generation.
    """
    global population_size, models, best
    # Create the population
    for _ in range(0, population_size):
        models.append(getLSTM())

    # Format: MSE, hyperparams, weights
    errors = []
    for j in range(0, len(models)):
        print("\tTraining member " + str(j) + " out of " + str(population_size))
        model = models[j]
        step(model)
        error = eval(model)
        if error < best[0]:
            print("New best error: " + str(error) + ", hyperparams=", model[1])
            best = [error, model[1], model[0].get_weights()]
        errors.append(error)
        # TODO: make better decisions
        if random.randint(0, 100) % 2 == 0:
            explore(j)
        else:
            exploit(j, best)

    return best


def run(train_x, train_y, test_x, test_y, outx, outy, bst, error_fun, pop_size=10):
    global models, trainx, trainy, testx, testy, population_size, error_func, best, L1
    # Format: [model, [num_hidden_layers, hidden_layer_sizes, epochs]]
    models = []

    base = MyLSTM(train_x.shape[1], 3, [50 for _ in range(3)],
                   train_y.shape[1], epochs=235, batch_size=100, fit_verbose=0)
    base.train(train_x, train_y)
    yhat = base.predict(test_x)
    error = test_y - yhat[:, 0]
    mse_b = error_fun(test_y, yhat)
    e_trainx = test_x
    e_trainy = error.reshape(error.shape[0], 1)

    trainx = e_trainx
    trainy = e_trainy
    testx = outx
    testy = outy
    population_size=pop_size
    error_func = error_fun
    best = bst
    L1 = base

    random.seed(time.time())
    best = train()
    print(best[1])
    if best[0] >= bst[0]:
        best[0] = bst[0]
        best[1] = bst[1]
    with open('PBT/best.dat', 'w+') as f:
        f.write(str(best[0]) + '\n')
        f.write(str(best[1][0]) + '\n')
        for i in best[1][1]:
            f.write(str(i) + ',')
        f.write('\n' + str(best[1][2]) + '\n')
        f.close()
