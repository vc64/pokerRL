class Player:
    def __init__(self, name, isBot=False, botObj=None):
        self.money = 1000
        self.wins = 0
        self.losses = 0
        self.name = name
        self.hand = []
        self.isBot = isBot
        self.bot = botObj
        self.bet = 0
        self.expect = 0
        self.isActive = False

    def getMoney(self):
        return self.money
    
    def getRatio(self):
        return self.wins / self.losses
    
    def getWins(self):
        return self.wins
    
    def getLosses(self):
        return self.losses
    
    def getName(self):
        return self.name
    
    def isActive(self):
        return self.isActive

    def setActive(self, state):
        self.isActive = state

    def setHand(self, cards):
        self.hand = cards

    def setExpect(self, amount):
        self.expect = amount
    
    def winMoney(self, amount):
        self.money += amount
    
    def currBet(self):
        return self.bet

    
    def getBet(self, community, actions):
        bet = 0
        if self.isBot:
            bet = self.bot.getAction(self.money, self.openBet, self.hand, community, actions)
        else:
            self.viewMoney()
            bet = int(input("Please enter bet (cannot exceed current balance): "))
        
        self.bet = bet
        return bet
    
    def bet(self, amount):
        if self.getMoney() <= amount:
            self.money -= amount
            return True
        else:
            self.money = 0
            return False

    def getHand(self):
        return self.hand

    def viewHand(self):
        print(self.name + "'s hand: " + ", ".join(self.hand))

    def viewMoney(self):
        print("Balance: $" + str(self.getMoney))