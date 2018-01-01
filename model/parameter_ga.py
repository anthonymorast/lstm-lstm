## GA to find optimal parameters.
# Population = base/error number hidden layers, layer width, and epochs (6 'bits')
# Cost = MSE

import random
from deap import base, creator, tools, algorithms
from lstm import *
import numpy as np
import matplotlib.pyplot as plt


class ParameterGA(object):
    # pass cost func in here to make generic
    def __init__(self, output_filename, train_x, train_y, test_x, test_y, out_x, out_y,
                 number_gens=15000, pop_size=100, ind_size=6):
        # pop_size == number of population members, ind_size = things we are guessing at
        self.output_filename = output_filename
        self.number_gens = number_gens
        self.pop_size = pop_size
        self.ind_size = ind_size
        self.testx = test_x
        self.testy = test_y
        self.trainx = train_x
        self.trainy = train_y
        self.outy = out_y
        self.outx = out_x
        self.track = 0

    def create(self):
        # since the ind params are cycles, 3 each
        isize = int(self.ind_size / 3)

        creator.create("FitnessMax", base.Fitness, weights=(1.0,))
        creator.create("Individual", list, fitness=creator.FitnessMax)

        self.toolbox = base.Toolbox()
        self.toolbox.register("attr_epochs", random.randint, 1, 100)
        self.toolbox.register("attr_layers", random.randint, 1, 20)
        self.toolbox.register("attr_layer_size", random.randint, 1, 50)
        self.toolbox.register("individual", tools.initCycle, creator.Individual,
                              (self.toolbox.attr_layers, self.toolbox.attr_layer_size, self.toolbox.attr_epochs),
                              n=isize)
        self.toolbox.register("population", tools.initRepeat, list, self.toolbox.individual)
        self.toolbox.register("evaluate", self.cost)
        self.toolbox.register("mate", tools.cxUniform, indpb=0.5)  # 1/2 from first parent, 1/2 from second
        self.toolbox.register("mutate", tools.mutUniformInt, low=0, up=2, indpb=0.1)
        self.toolbox.register("select", tools.selTournament, tournsize=3)

    def run(self):
        pop = self.toolbox.population(n=self.pop_size)
        hof = tools.HallOfFame(1)
        stats = tools.Statistics(lambda ind: ind.fitness.values)
        stats.register("avg", np.mean)
        stats.register("max", np.max)
        stats.register("min", np.min)
        pop, log = algorithms.eaSimple(pop, self.toolbox, cxpb=0.5, mutpb=0.2, ngen=self.number_gens,
                                       stats=stats, halloffame=hof, verbose=True)
        print('Best Individual is %s\nWith fitness%s' % (hof[0], hof[0].fitness))

    def create_and_run(self):
        self.create()
        self.run()

    def cost(self, ind):
        print(ind)

        vlayers, vlayersize, vepochs = ind[0], ind[1], ind[2]
        elayers, elayersize, eepochs = ind[3], ind[4], ind[5]

        if vlayers == 0:
            vlayers = 1;
        if vlayersize == 0:
            vlayersize = 1
        if vepochs == 0:
            vepochs = 1
        if elayers == 0:
            elayers = 1;
        if elayersize == 0:
            elayersize = 1
        if eepochs == 0:
            eepochs = 1

        print('building and fitting base model', self.track, 'out of', self.number_gens, '...')
        base = MyLSTM(self.trainx.shape[1], vlayers, [vlayersize for _ in range(vlayers)], self.trainy.shape[1],
                      epochs=vepochs, batch_size=100, fit_verbose=0)
        base.train(self.trainx, self.trainy)

        yhat = base.predict(self.testx)
        e = self.testy - yhat[:, 0]

        e_trainx = self.testx
        e_trainy = e.reshape(e.shape[0], 1)

        print('building and fitting error model', self.track, 'out of', self.number_gens, '...')
        error = MyLSTM(e_trainx.shape[1], elayers, [elayersize for _ in range(elayers)], e_trainy.shape[1],
                       epochs=eepochs, batch_size=100, fit_verbose=0)
        error.train(e_trainx, e_trainy)

        # out of sample predictions
        yhat_v = base.predict(self.outx)
        yhat_e = error.predict(self.outx)

        yhat_ve = yhat_v + yhat_e
        error_ve = self.outy - yhat_ve[:, 0]
        mse = sum(error_ve ** 2) / len(error_ve)

        # maximization problem....
        self.track += 1
        return (1 / mse,)
