from collections import defaultdict

class Pot:
    def __init__(self, maxWinnings = {}):
        self.bets = {} # playerID : total bet in current round
        self.maxWinnings = defaultdict(lambda:0, {}) # playerID : max eligible winnings
        self.blind = 0
        self.totals = defaultdict(lambda:0, {}) # playerID : total bet in pot
    
    # goal: a Pot should only contain the players and amounts relevant to that pot
    # resulting side pot of an existing pot will only contain the excess from the previous pot
    # the side pot also only needs to know about the players with the excess
    # since an AllIn could occur any time during a round, it may be easier to have update to sidepot during advanceRound
    # need to also accoutn for multiple AllIns in one round, not quite sure

    def getTotal(self):
        return sum(self.totals.values()) + sum(self.bets.values()) + self.blind

    def advanceTurn(self):
        sortedBets = sorted(self.bets.items(), key=lambda x : x[1])
        numBets = len(self.bets)
        prevBet = 0
        prevWinnings = 0
        currTotal = 0
        i = 0
        for playerID, roundBet in sortedBets:
            if prevBet != roundBet:
                prevWinnings = (numBets - i) * roundBet + currTotal
            self.maxWinnings[playerID] += prevWinnings
            prevBet = roundBet
            currTotal += roundBet
            self.totals[playerID] += roundBet
            i += 1
        
        turnBets = self.bets
        self.bets = {}
        return turnBets
    
    def addBlind(self, amount):
        self.blind += amount

    def addToPot(self, playerID, amount, isAllIn = False):
        self.bets[playerID] = amount

    def splitPot(self, tieredWinnerIDs):
        outputSplit = {}
        prevTotal = 0
        for winnerIDs in tieredWinnerIDs:
            playerWinnings = sorted(self.maxWinnings.items(), key=lambda x : x[1])
            winnerCount = len(winnerIDs)
            currWin = 0
            prevMaxWin = 0
            playerSplit = {}
            currTotal = 0
            for playerID, maxWin in playerWinnings:
                maxWin += self.blind
                if winnerCount > 0 and playerID in winnerIDs:
                    if maxWin != prevMaxWin and maxWin > prevTotal:
                        currWin += (maxWin - prevMaxWin - prevTotal) / winnerCount
                    currTotal += currWin
                    playerSplit[playerID] = round(currWin, 1)
                    winnerCount -= 1
                    prevMaxWin = max(0, maxWin - prevTotal)
            prevTotal += currTotal
            outputSplit.update(playerSplit)
        return outputSplit




