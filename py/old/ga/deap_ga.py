'''
	A GA with the intention of maximizing the money that can be made by choosing to 
	Buy, Hold, or Sell on any given day. The data is broken into 90 day chunks. 

	Choices:
		0 - Buy
		1 - Sell
		2 - Hold

	REF:
		- https://en.wikipedia.org/wiki/Crossover_(genetic_algorithm)
		- https://en.wikipedia.org/wiki/Mutation_(genetic_algorithm)
		- http://deap.gel.ulaval.ca/doc/dev/api/tools.html#deap.tools.cxTwoPoint
		- https://github.com/DEAP/notebooks/blob/master/OneMax.ipynb
'''

import random
from deap import base, creator, tools, algorithms
from data import *
import numpy as np
import matplotlib.pyplot as plt


'''
	price_data - data from the csv file for some time period
	plot_name - output name of the file save, include dir path and extension
	outname - output of the optimal solution, include dir path and extension
	number_gens - number of generations to run for 
	pop_size - number of individuals in a population
	lot_size - # of shares we're purchasing, standard lot is 100,000
	trade_fee - a fee to penalize overtrading
	start_cash - starting cash, need to have some money to buy shares
	ind_size - essentially number of days, number of decision an individual can make
	verbose - True --> see GA output, False --> don't see output
	threshold - max iters to run without change before breaking
'''
class ForexGA(object):
	def __init__(self, price_data, plot_name, outname, number_gens=15000, pop_size=50, 
				 lot_size=100000, trade_fee=30, start_cash=150000, ind_size=90, verbose=True,
				 threshold=0.0):
		self.LOT = lot_size
		self.TRADE_FEE = trade_fee
		self.pop_size = pop_size
		self.price_data = price_data
		self.ngen = number_gens
		self.start_cash = start_cash
		self.verbose = verbose
		self.filename = plot_name
		self.output = outname
		self.ind_size = len(price_data)
		self.threshold = threshold

	# GA
	def maximize(self, individual):
		cash = self.start_cash
		shares = 0 
	
		idx = 0
		for i in range(0, len(individual)):
			decision = individual[i]
			price = float(self.price_data[idx])
			if decision == 0:
				# buy if we have enough cash 
				if cash >= (self.LOT * price):
					cash -= self.LOT * price
					shares += self.LOT
					cash -= self.TRADE_FEE
				else:
					individual[i] = 2
			elif decision == 1:
				# sell if we have enough shares
				if shares >= self.LOT:
					cash += self.LOT * price
					shares -= self.LOT
					cash -= self.TRADE_FEE
				else:
					individual[i] = 2
			# else --> hold, do nothing
			idx += 1

		# get profit
		cash = cash - self.start_cash
		return (cash,)

	def create(self):
		creator.create("FitnessMax", base.Fitness, weights=(1.0,))
		creator.create("Individual", list, fitness=creator.FitnessMax)

		self.toolbox = base.Toolbox()
		self.toolbox.register("attr_bool", random.randint, 0, 2)
		self.toolbox.register("individual", tools.initRepeat, creator.Individual, 
								self.toolbox.attr_bool, n=self.ind_size)
		self.toolbox.register("population", tools.initRepeat, list, self.toolbox.individual)

		self.toolbox.register("evaluate", self.maximize)
		self.toolbox.register("mate", tools.cxUniform, indpb=0.5) # 0.5 ==> half from first half from second
		self.toolbox.register("mutate", tools.mutUniformInt, low=0, up=2, indpb=0.1)
		self.toolbox.register("select", tools.selTournament, tournsize=3)


	def run(self):
		pop = self.toolbox.population(n=self.pop_size)
		hof = tools.HallOfFame(1)
		stats = tools.Statistics(lambda ind: ind.fitness.values)
		stats.register("avg", np.mean)
		stats.register("min", np.min)
		stats.register("max", np.max)
		pop, log = algorithms.eaSimple(pop, self.toolbox, cxpb=0.5, mutpb=0.2, ngen=self.ngen, 
										stats=stats, halloffame=hof, verbose=self.verbose, 
										threshold=self.threshold)

		print('Best individual is: %s\nWith fitness: %s' % (hof[0], hof[0].fitness))
		with open(self.output, 'w') as outfile:
			outfile.write('ind=%s\nfitness=%s\n' % (hof[0], hof[0].fitness))
		print(self.output, self.filename)
		gen, avg, min_, max_ = log.select("gen", "avg", "min", "max")
		plt.figure(1)
		plt.plot(gen, avg, label="average")
		plt.plot(gen, min_, label="minimum")
		plt.plot(gen, max_, label="maximum")
		plt.xlabel('Generation')
		plt.ylabel('Fitness')
		plt.legend(loc="lower right")
		plt.savefig(str(self.filename))
		plt.close()


	def create_and_run(self):
		self.create()
		self.run()
