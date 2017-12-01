"""
" Cash will start at 0
" Organisms can end up with 0 cash at the end of the timeframe (leverage)
" Cash will increase/decrease by shares*price
" Checks in ga_opt.py to determine if organism has enough shares to sell
" Rules:
"   Can't sell until we buy
"   Shares are worthless at the end of the timeframe
"   Will always sell one lot (or micro, mini, nano lot)
"""
class organism:
    actions = []
    totalFees = 0.00
    totalShares = 0
    cash = 0

    NOTHING = 0
    BUY = 1
    SELL = 2

    def __init__(self):
        i = 0
    
    """
    " Increase the total number shares by 'shares' and adds the trading fee
    """
    def buyShares(self, fee, shares, price):
        self.totalShares = self.totalShares + shares
        self.totalFees = self.totalFees + fee
        self.cash = self.cash - (price * shares)

    """
    " Decrement the total number of shares and add to total fees
    """
    def sellShares(self, fee, shares, price):
        self.totalShares = self.totalShares - shares
        self.totalFees = self.totalFees + fee
        self.cash = self.cash + (price * shares)

    def getTotalShares(self):
        return self.totalShares
    
    def getTotalFees(self):
        return self.totalFees

    def getCash(self):
        return self.cash
    
    def setCash(self, cash):
        self.cash = cash

    """
    " Sets this organisms actions to the 'actions' list of values 0-2
    """
    def setActions(self, actions):
        self.actions = actions

    """
    " Gets the action taken on day number 'day'.
    """
    def getActions(self):
        return self.actions

    """
    " Iterates this organisms actions and sets the total shares and fees
    """
    def setSharesAndFees(self, shares, fee, price):
        for action in self.actions:
            if action == NOTHING:
                pass
            elif action == BUY:
                self.buyShares(shares, fee, price)
            else:
                self.sellShares(shares, fee)
