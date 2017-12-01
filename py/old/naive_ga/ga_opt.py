########## LIBRARIES
import pandas as pd
import matplotlib.pyplot as plt
import sys
import random

from population import * 
from organism import *

########## END LIBRARIES

########## GLOBALS
tickerData = None

# Actions
NOTHING = 0
BUY = 1
SELL = 2

brokerFee = 5.00 # penalty for excessive trading
lot = 100000 # standard lot - primary
# add in later
minilot = 10000
microlot = 1000
nanlot = 100
roundShares = 0

fitness = []
population = []
threshold = 10000000 # when we stop making >= $5 per pop, stop
optimalSolution = []
populationSize = 100

########## END GLOBALS

# GA:
#   Initialize population with random selections for each row 
#   Keep common decision between 'good' parents, set others to -1 (re-decide)
#   Mutate some children (try 1 child derived from parent, 1 that's mutated after derivation (keep pop size the same)) 

########## FUNCTIONS
def plotOptimal():
    xplt = tickerData.plot(title="EURUSD Data")
    xplt.set_xlabel("Days (From 1/1/1998 - 4/28/2017)")
    xplt.set_ylabel("Price")

    # ms=markersize=size of point(s)
    # optimalSolution[i] = [action, day(index in tickerData df)] (get Data/Price from day index)
    #   tickerData.iloc[1] <- gives second row, p.iloc[1][{'Date', 0}] gives second row, first column
    for i in range(0, len(optimalSolution)):
        price = tickerData.iloc[i][1]

        if optimalSolution[i] == NOTHING:
            continue
        elif optimalSolution[i] == BUY:
            xplt.plot(i, price, 'g^', ms=2)
        else:
            xplt.plot(i, price, 'r^', ms=2)

    plt.show()

def printFile():
    with open('optimal.solution.dat', 'w') as f:
        for point in optimalSolution:
            f.write('1') # f.write(Date, Action, Price)

def mutate():
    global population
    #mutate

def recombination():
    global population
    oldpop = population
    population = []
    # initial - each member crossover next member
    for i in range(0, len(oldpop)-1):
        o = organism()
        p1 = oldpop[i]
        p2 = oldpop[i+1]
        x = p1.getActions()
        y = p2.getActions()
        # first half of actions from parent 1, second half from parent 2
        actions = [x[:int(len(x)/2)], y[int(len(x)/2):]]
        actions = [item for sublist in actions for item in sublist]
        o.setActions(actions)
        population.append(o)
    
    # special case last index with first index
    o = organism()
    p1 = oldpop[populationSize-1]
    p2 = oldpop[0]
    x = p1.getActions()
    y = p2.getActions()
    # first half of actions from parent 1, second half from parent 2
    actions = [x[:int(len(x)/2)], y[int(len(x)/2):]]
    actions = [item for sublist in actions for item in sublist]
    o.setActions(actions)
    population.append(o)


    # here we need to iterate the new actions for the members of the population
    # and find the new cash/fees 
    for mem in population:
        for i in range(0, len(mem.getActions())):
            action = mem.getActions()[i]
            price = tickerData.iloc[i][1]
            if action == SELL:
                mem.sellShares(brokerFee, roundShares, tickerData.iloc[i][1])
            elif action == BUY:
                mem.buyShares(brokerFee, roundShares, tickerData.iloc[i][1])
    

def normalizeFit():
    fits = []
    for org in population:
        fits.append(org.getCash())
    
    # make all > 0
    newFits = []
    for fit in fits:
        fit += abs(min(fits))
        newFits.append(fit)
    
    for i in range(0, populationSize):
        population[i].setCash(newFits[i])

def calcFit():
    # fit_i = cash - fees = profits
    for org in population:
        org.setCash(org.getCash() - org.getTotalFees())

def getBestFit():
    best = -1
    for org in population:
        if org.getCash() > best:
            best = org.getCash()
    return best

def popInit():
    global population
    print("Initializing population of " + str(populationSize) + " organisms.")
    for i in range(0, populationSize):
        #print("\tCreating organism " + str(i+1) + " out of " + str(populationSize) + "...")
        actions = []
        o = organism()
        days = len(tickerData)
        for j in range(0, days):
            #print("\t\tDay " + str(j) + " out of " + str(days) + ".")
            actions.append(-1)
            action = random.randint(0, 2)
            actions[j] = action

            if action == SELL and o.getTotalShares() < roundShares:
                actions[j] = NOTHING
            elif action == SELL and o.getTotalShares() > roundShares:
                o.sellShares(brokerFee, roundShares, tickerData.iloc[j][1])
            elif action == BUY:
                o.buyShares(brokerFee, roundShares, tickerData.iloc[j][1])

        o.setActions(actions)
        population.append(o)

def runGA():
    global optimalSolution
    """
    " TO TRY:
    "   Find rates of convergence (fit decresing < threshold)
    "   Try with crossover, mutation, selection (not sure real name), and combos of the three
    "   Try breeding all with most fit
    "   ... 
    """
    popInit()
    calcFit()
    normalizeFit()

    best = getBestFit()
    prevBest = 0
    while abs(best - prevBest) > threshold:
        prevBest = best 
        recombination()
        # create mutation parameter -- if best < prevBest increase number of mutations
        mutate()
        calcFit()
        # only really need this method if trimming population 
        #   p_i = f_i/sum(f_i) - probability of staying in the population 
        #       !! NO NEGATIVE PROBS !!
        normalizeFit()
        best = getBestFit()
        print("Previous Best: " + str(prevBest) + "\tBest: " + str(best))
    
    for org in population:
        if org.getCash() == best:
            optimalSolution = org.getActions()
            break
    
    plotOptimal()

########## END FUNCTIONS

########## MAIN
def main():
    global tickerData, roundShares
    if len(sys.argv) != 2:
        print('Usage: python3 ga_opt.py <filename>.csv')
        return
    
    # read tick data 
    tickerData = pd.read_csv(sys.argv[1])
    roundShares = lot
    runGA()


if __name__ == '__main__':
    main()
