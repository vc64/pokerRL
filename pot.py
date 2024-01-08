from collections import defaultdict

class Pot:
    def __init__(self, maxWinnings = {}):
        self.bets = {} # playerID : total bet in current round
        self.maxWinnings = defaultdict(lambda:0, {}) # playerID : max eligible winnings
        # self.allInPlayers = {} # playerID : allInBet
        self.totals = defaultdict(lambda:0, {}) # playerID : total bet in pot
        # self.amounts = amounts # dict: playerID -> (currRoundBet, totalSettledBets)
        # self.sidePot = None
        # self.allInPlayer = -1
        # self.hasAllInThisRound = False
        # self.isCurrentPot = True
    
    # goal: a Pot should only contain the players and amounts relevant to that pot
    # resulting side pot of an existing pot will only contain the excess from the previous pot
    # the side pot also only needs to know about the players with the excess
    # since an AllIn could occur any time during a round, it may be easier to have update to sidepot during advanceRound
    # need to also accoutn for multiple AllIns in one round, not quite sure

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
        
        self.bets = {}

    def addToPot(self, playerID, amount, isAllIn = False):
        # if not self.isCurrentPot:
        #     self.sidePot.addToPot(playerID, amount, isAllIn)
        # else:
        self.bets[playerID] = amount
        # self.maxWinnings[]
        # if isAllIn:
        #     # self.hasAllInThisRound = True
        #     self.allInPlayers[playerID] = amount
        #     self.maxWinnings[playerID] = (amount, self.amounts[playerID][1])
    

    #TODO
    # need to fix splitpot so it doesnt just let everyone make money, also refactor code
    # should not allow folding from start
    # need to actually modify balance when bets are made, which means somehow handling case 
        # where someone bets more than everyone else so they should get refunded
    # actually implement a game loop
    # debug :(
    # work on bot eventually


    def splitPot(self, tieredWinnerIDs):
        outputSplit = {}
        for winnerIDs in tieredWinnerIDs:
            if len(winnerIDs) > 1:
                playerWinnings = sorted(self.maxWinnings.items(), key=lambda x : x[1])
                # print(playerWinnings)
                winnerCount = len(winnerIDs)
                currWin = 0
                prevMaxWin = 0
                playerSplit = {}
                maxWinnerTotal = max([self.totals[playerID] for playerID in winnerIDs])
                for playerID, maxWin in playerWinnings:
                    if playerID in winnerIDs:
                        if maxWin != prevMaxWin:
                            currWin += round((maxWin - prevMaxWin) / winnerCount, 1)
                        playerSplit[playerID] = currWin - self.totals[playerID]
                        winnerCount -= 1
                        prevMaxWin = maxWin
                    else:
                        playerSplit[playerID] = -min(self.totals[playerID], maxWinnerTotal)
                
                if sum([playerSplit[x] for x in playerSplit]) != 0:
                    raise Exception("Pot split incorrectly.")
                outputSplit.update(playerSplit)
            else:
                currPlayerID = winnerIDs[0]
                outputSplit[currPlayerID] = self.maxWinnings[currPlayerID]
        return outputSplit
        # if self.sidePot != None:
        #     playerWinnings = self.sidePot.splitPot(winnerIDs)
        
        # # not the best approach, can "create" money, but will adhere to one decimal place
        # perWinnerEarning = round(sum([x[1] for x in self.amounts.values()]) / len(winnerIDs), 1) 
        # for playerID in winnerIDs:
        #     playerWinnings[playerID] += perWinnerEarning
            



        # active = []
        # numActive = 0
        # for player in self.players:
        #     if player.isActive():
        #         active.append(player)
        #         numActive += 1
        
        # for player in active:
        #     pass # win money




