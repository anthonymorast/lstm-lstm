import random
import time
from errors import *
from lstm import *

"""
    TODO:
        Generalize
            - add model.set_hyperparams(...) as a requirement which will create a
              new model with these params.
            -
        Improve
            - better explore/exploit decisions (follow paper more closely)

"""


class PBT(object):
    """
        Population based training class as in:

        Population Based Training of Neural Networks (2017)

        Jaderberg, Max and Dalibard, Valentin and Osindero,
        Simon and Czarnecki, Wojciech M and Donahue, Jeff and Razavi,
        Ali and Vinyals, Oriol and Green, Tim and Dunning,
        Iain and Simonyan, Karen and others

        This implementation is not parallel due to Tensorflow... Should be
        extended for use on network machine (# threads = # GPUs)
    """
    def __init__(self, trainx, trainy, testx, testy, \
                 max_iters=1000, population_size=10, threshold=50,
                 error_measure='mse'):
        """
            Initializes the PBT class. The 'model' parameter must
            have train, predict, get_weights, and set_weigthts methods.
            'Train' should train the model and 'predict' should return
            y_hat values to be compared to actual values.

            max_iters: maximum number of models trained
            population_size: number of members in population
            threshold: number of iters without change in best params
            error_measure: not implemented
        """
        # self.model = model
        # Format: [model, [num_hidden_layers, hidden_layer_sizes, epochs]]
        self.models = []
        self.trainx = trainx
        self.trainy = trainy
        self.testx = testx
        self.testy = testy
        self.max_iters = max_iters
        self.population_size=population_size
        self.threshold = threshold
        self.error_measure = error_measure

        random.seed(time.time())


    def train(self):
        """
            Executes PBT.
        """
        # Create the population
        for _ in range(0, self.population_size):
            self.models.append(self.getLSTM())

        # Format: MSE, hyperparams, weights
        best = [9999999, [1, [1,2], 1], []]
        prevBest = best[0]
        threshold_count = 0
        for i in range(0, self.max_iters):
            print("Iteration: " + str(i) + ", Best Error: " + str(best[0]) +
                  ", Unchanged Count: " + str(threshold_count))
            if threshold_count >= self.threshold:
                break
            elif prevBest == best[0]:
                threshold_count = threshold_count + 1
            elif prevBest != best[0]:
                threshold_count = 0
                prevBest = best[0]

            errors = []
            for j in range(0, len(self.models)):
                print("\tTraining member " + str(j) + " out of " + str(self.population_size))
                model = self.models[j]
                self.step(model)
                error = self.eval(model)
                if error < best[0]:
                    print("New best error: " + str(error) + ", hyperparams=",model[1])
                    best = [error, model[1], model[0].get_weights()]
                errors.append(error)
                # TODO: make better decisions
                if random.randint(0, 100) % 2 == 0:
                    self.explore(j)
                else:
                    self.exploit(j, best)

        return best


    def getLSTM(self):
        """
            Creates a population member.
        """
        hidden_layers = random.randint(2, 15)
        layer_sizes = []
        for _ in range(0, hidden_layers):
            layer_sizes.append(random.randint(2, 50))
        hyperparams = [hidden_layers, layer_sizes, random.randint(50, 250)]
        return [MyLSTM(self.trainx.shape[1], hyperparams[0], hyperparams[1],
                      self.trainy.shape[1], epochs=hyperparams[2], fit_verbose=0,
                      batch_size=100), hyperparams]


    def eval(self, model):
        """
            Gets preditions from the model and measures the error for model
            goodness.
        """
        y_hat = model[0].predict(self.testx)
        # if self.error_measure == 'mse':
        return mse(self.testy, y_hat)


    def step(self, model):
        """
            Trains the model using its built in train method.
        """
        model[0].train(self.trainx, self.trainy)


    def explore(self, index):
        """
            Get new weights for population member
        """
        self.models[index] = self.getLSTM()


    def exploit(self, index, best):
        """
            Set the weights and hyperparams and apply a mutation.
        """
        # best Format: MSE, hyperparams, weights
        hyperparams = best[1]

        # Mutate
        hyperparams[0] = hyperparams[0] + random.randint(-2, 2)
        for i in range(0, hyperparams[0]):
            if i < len(hyperparams[1]):
                hyperparams[1][i] = hyperparams[1][i] + random.randint(-10, 10)
            else:
                hyperparams[1].append(random.randint(2, 50))
            if hyperparams[1][i] <= 0:
                hyperparams[1][i] = random.randint(2, 50)
        hyperparams[2] = hyperparams[2] + random.randint(-15, 15)
        if hyperparams[2] < 50:
            hyperparams[2] = 50

        self.models[index] = [MyLSTM(self.trainx.shape[1], hyperparams[0], hyperparams[1],
                      self.trainy.shape[1], epochs=hyperparams[2], fit_verbose=0, batch_size=100),
                      hyperparams]
