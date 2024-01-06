class Pot:
    def __init__(self, amounts = {}):
        self.amounts = amounts # dict: playerID -> (currRoundBet, totalSettledBets)
        self.sidePot = None
        self.allInPlayer = -1
        self.isCurrentPot = True
    
    def advanceRound(self):
        for p in self.amounts.keys():
            self.amounts[p][1] += self.amounts[p][0]
            self.amounts[p][0] = 0
        if self.sidePot != None:
            self.isCurrentPot = False

    def addToPot(self, playerID, amount, isAllIn = False):
        if not self.isCurrentPot:
            self.sidePot.addToPot(playerID, amount, isAllIn)
        else: 
            if isAllIn:
                self.allInPlayer = playerID
                self.sidePot = Pot({x: self.amounts[x] for x in self.amounts if x != playerID})
            self.amounts[playerID] = (amount, self.amounts[playerID][1])
    
    def splitPot(self, winnerIDs):
        active = []
        numActive = 0
        for player in self.players:
            if player.isActive():
                active.append(player)
                numActive += 1
        
        for player in active:
            pass # win money




