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
    global outx, outy, error_func
    y_hat_v = model[0][0].predict(outx)
    y_hat_e = model[1][0].predict(outx)
    y_hat = y_hat_e + y_hat_v
    # if self.error_measure == 'mse':
    return error_func(outy, y_hat[:,0])


def step(model):
    """
        Trains the model using its built in train method.
    """
    global trainx, trainy, testx, testy
    print('\tTraining model with hyperparams: ', model[0][1], ' and ', model[1][1])
    model[0][0].train(trainx, trainy)
    yhat = model[0][0].predict(testx)
    errors = testy - yhat[:,0]
    errors = errors.reshape(errors.shape[0], 1)
    model[1][0].train(testx, errors)


def explore(index):
    """
        Get new weights for population member
    """
    global models
    models[index] = [getLSTM(), getLSTM()]


def exploit(index, best):
    """
        Set the hyperparams and apply a mutation.
    """
    global models, trainx, trainy
    # best Format: MSE, hyperparams, weights
    hyperparams_base = copy.deepcopy(best[1])
    hyperparams_err = copy.deepcopy(best[2])

    # Mutate
    hyperparams_base[0] = hyperparams_base[0] + random.randint(-2, 2)
    for i in range(0, hyperparams_base[0]):
        if i < len(hyperparams_base[1]):
            hyperparams_base[1][i] = hyperparams_base[1][i] + random.randint(-10, 10)
        else:
            hyperparams_base[1].append(random.randint(2, 50))
        if hyperparams_base[1][i] <= 0:
            hyperparams_base[1][i] = random.randint(2, 50)
        if len(hyperparams_base[1]) > hyperparams_base[0]:
            hyperparams_base[1] = hyperparams_base[1][:hyperparams_base[0]]
    hyperparams_base[2] = hyperparams_base[2] + random.randint(-15, 15)
    if hyperparams_base[2] < 50:
        hyperparams_base[2] = 50

    hyperparams_err[0] = hyperparams_err[0] + random.randint(-2, 2)
    for i in range(0, hyperparams_err[0]):
        if i < len(hyperparams_err[1]):
            hyperparams_err[1][i] = hyperparams_err[1][i] + random.randint(-10, 10)
        else:
            hyperparams_err[1].append(random.randint(2, 50))
        if hyperparams_err[1][i] <= 0:
            hyperparams_err[1][i] = random.randint(2, 50)
        if len(hyperparams_err[1]) > hyperparams_err[0]:
            hyperparams_err[1] = hyperparams_err[1][:hyperparams_err[0]]
    hyperparams_err[2] = hyperparams_err[2] + random.randint(-15, 15)
    if hyperparams_err[2] < 50:
        hyperparams_err[2] = 50

    models[index] = [[MyLSTM(trainx.shape[1], hyperparams_base[0], hyperparams_base[1],
                  trainy.shape[1], epochs=hyperparams_base[2], fit_verbose=0, batch_size=100),
                  hyperparams_base],
                  [MyLSTM(trainx.shape[1], hyperparams_err[0], hyperparams_err[1],
                    trainy.shape[1], epochs=hyperparams_err[2], fit_verbose=0, batch_size=100),
                    hyperparams_err]]

def train():
    """
        Run a single generation.
    """
    global population_size, models, best
    # Create the population
    for _ in range(0, population_size):
        models.append([getLSTM(), getLSTM()])

    # Format: MSE, hyperparams, weights
    errors = []
    for j in range(0, len(models)):
        print("\tTraining member " + str(j) + " out of " + str(population_size))
        model = models[j]
        step(model)
        error = eval(model)
        if error < best[0]:
            print("New best error: " + str(error) + ", hyperparams_base=",
                  model[0][1], ', hyperparams_err=', model[1][1])
            best = [error, model[0][1], model[1][1]]
        errors.append(error)
        # TODO: make better decisions
        if random.randint(0, 100) % 2 == 0:
            explore(j)
        else:
            exploit(j, best)

    return best


def run(train_x, train_y, test_x, test_y, out_x, out_y, bst, error_fun, pop_size=10):
    global models, trainx, trainy, testx, testy, population_size, error_func, best, outx, outy
    # Format: [model, [num_hidden_layers, hidden_layer_sizes, epochs]]
    models = []
    trainx = train_x
    trainy = train_y
    testx = test_x
    testy = test_y
    outx = out_x
    outy = out_y
    population_size=pop_size
    error_func = error_fun
    best = bst
    print(best[1])
    random.seed(time.time())
    best = train()
    print(best[1])
    if best[0] >= bst[0]:
        best[0] = bst[0]
        best[1] = bst[1]
        best[2] = bst[2]
    with open('PBT/best.dat', 'w+') as f:
        f.write(str(best[0]) + '\n')

        f.write(str(best[1][0]) + '\n')
        for i in best[1][1]:
            f.write(str(i) + ',')
        f.write('\n' + str(best[1][2]) + '\n')

        f.write(str(best[2][0]) + '\n')
        for i in best[2][1]:
            f.write(str(i) + ',')
        f.write('\n' + str(best[2][2]) + '\n')
        f.close()
