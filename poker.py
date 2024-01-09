from table import Deck, Board
from card import Card, Hand
from player import CardPlayer, HumanPlayer
from bot import BotPlayer
from pot import Pot

import random
from itertools import combinations
import math

import os, platform
def clear():
   if platform.system() == 'Windows':
      os.system('cls')
   else:
      os.system('clear')

class Move:
    """General class to allow Player to make a Move based on game info."""
    def __init__(self, game, playerID = -1):
        self.playerID = playerID
        self.game = game

    def isValid(self):
        pass

class PokerMove(Move):
    def __init__(self, game, playerID: int):
        super().__init__(game, playerID)
        self.action = ""
        self.amount = -1
        self.isSet = False
        self.gameInfo = {
            "boardCards": self.game.boardCards, 
            "validMoveActions": self.game.getValidMoveActions(self.playerID),
            "lastNotableMove": self.game.lastNotableMove,
            "potTotal": self.game.pot.getTotal()
        }
        self.isValid = lambda : self.game.validMoveFunc(self.playerID)(self.action, self.amount)
        self.minBet = self.game.minBetFunc()
    
    def setMove(self, action: str, amount = 0) -> bool:
        """Sets attributes to match specified move if valid. Returns whether set or not."""
        if self.isSet:
            raise Exception("Move already set.")
        self.action = action
        if action in ["Call", "Check", "Fold"]:
            amount = 0
        self.amount = amount
        self.isSet = self.isValid()
        if self.isSet:
            self.game.update(self)
        else:
            print("Invalid move: please try again.")
        return self.isSet
    
    def __str__(self):
        return f"{self.action} {self.amount}"

# class GameObs:
#     """Observable-like class for Game"""
#     def __init__(self, funcs: list, ids = []):
#         if (len(ids) != len(funcs)):
#             ids = list(range(len(funcs)))
#         self.playerFuncs = {}
#         for i in range(len(funcs)):
#             self.subscribe(funcs[i], ids[i])
    
#     def subscribe(self, playerFunc, playerID: int):
#         self.playerFuncs[playerID] = playerFunc
    
#     def update(self, orderedIDs, gameObj, moveObj):
#         for p in orderedIDs:
#             moveObj.setPlayer(p)
#             self.playerFuncs[p](gameObj, moveObj) # pass in game state in some format -> likely as game object

class Game:
    """Represents a game."""
    def __init__(self, players = list, moves = list):
        self.players = dict(enumerate(players))
        self.ids = list(range(len(players)))
        # self.obs = GameObs([p.makeMove for p in players], self.ids)
        self.moveActions = moves
    
    def start(self):
        """Start the game. Will block until game ends."""
        pass

    def getValidMoveActions(self):
        """Return list of valid move actions for specific player."""
        pass

    def isValidMove(self):
        """Check if specified move is valid."""
        pass

    # def generateMove(self):
    #     """Return a move object for the game."""
    #     pass

    def update(self, move: Move):
        """Update game with given move."""
        pass


class CardGame(Game):
    """Represents a card game (has a deck)."""
    def __init__(self, players = list, moves = list):
        super().__init__(players, moves)
        self.deck = Deck()
        self.deck.shuffle()

class Poker(CardGame):
    def __init__(self, players=list):
        super().__init__(players, ["Check", "Bet", "Raise", "Call", "Fold"])
        self.boardCards = []
        self.lastNotableMove: PokerMove = None
        self.pot = Pot()
        self.playersInRound = 0
        self.allInCount = 0
        self.isActive = False

    def start(self):
        """Start the game. Will block until game ends."""
        self.isActive = True
        self.deck.resetDeck()
        self.deck.shuffle()

        for playerID in self.ids:
            self.players[playerID].inGame = True
        
        random.shuffle(self.ids) # ..., D, SB, BB,

        while sum([self.players[playerID].inGame for playerID in self.ids]) > 1:
            self.playRound()
            print(f"Balances: {', '.join([f'{self.players[playerID].name}: {self.players[playerID].score}' for playerID in self.ids])}")
            input("Press enter to continue the game.")

        # for playerID in self.ids:
        #     currPlayer = self.players[playerID]
        #     currPlayer.addToHand(self.deck.dealCards(2))
        #     currPlayer.makeMove(self, PokerMove(self, playerID, self.validMoveFunc(playerID)))

        # self.obs.update(self.ids, self, PokerMove())

        # flop
        # print("flop")
        # self.boardCards.append(self.deck.dealCards(3))
        # self.obs.update(self.ids, self)

        # # turn
        # print("turn")
        # self.boardCards.append(self.deck.dealCards())
        # self.obs.update(self.ids, self)

        # # river
        # print("flop")
        # self.boardCards.append(self.deck.dealCards())
        # self.obs.update(self.ids, self)

        # showdown
    
    def playRound(self):
        self.ids.append(self.ids.pop(0))
        self.pot = Pot()
        self.allInCount = 0
        self.boardCards = []

        for playerID in self.ids:
            if self.players[playerID].inGame:
                self.players[playerID].resetPlayer()
                self.playersInRound += 1

        # pre-flop
        print("pre-flop")
        self.pot.addBlind(0.5)
        self.players[self.ids[-2]].updateScore(-0.5)
        self.pot.addBlind(1)
        self.players[self.ids[-1]].updateScore(-1)
        self.pot.advanceTurn()
        self.turn("Pre-flop")

        # flop
        self.turn("Flop")

        # turn
        self.turn("Turn")

        # river
        self.turn("River")

        self.endRound()
    
    def endRound(self):
        if self.playersInRound <= 1:
            tieredPlayers = [[playerID for playerID in self.ids if self.players[playerID].inRound]]
        else:
            sortedPlayers = sorted([(self.getBestHandVal(playerID), playerID) for playerID in self.ids 
                                if self.players[playerID].inRound], reverse=True)
            prevHandVal = -1
            tieredPlayers = []
            for handVal, playerID in sortedPlayers:
                if prevHandVal != handVal:
                    tieredPlayers.append([])
                tieredPlayers[-1].append(playerID)
        
        for playerID, winAmount in self.pot.splitPot(tieredPlayers).items():
            # print(winAmount)
            self.players[playerID].updateScore(winAmount)
            print(f"{self.players[playerID].name} won {winAmount} bb")
        
        # for playerID in self.ids:
        #     print(f"{self.players[playerID].name} {self.players[playerID].score} bb")
        self.playersInRound = 0
    
    def turn(self, turnName: str):
        turnDict = {"Pre-flop": (2,0), "Flop": (0,3), "Turn": (0,1), "River": (0,1)}

        if not (turnName in turnDict.keys()):
            raise Exception("Invalid turn name.")
        
        handCards, boardCards = turnDict[turnName] 
        for i in range(len(self.ids)):
            if self.players[self.ids[i]].inRound:
                self.players[self.ids[i]].addToHand(self.deck.dealCards(handCards))
        self.boardCards += list(self.deck.dealCards(boardCards))
        print(f"===== {turnName} =====")
        print(f"Board: {self.boardCards}")
        if self.playersInRound - self.allInCount <= 1:
            return

        index = 0
        currPlayerID = self.ids[index]
        currPlayer = self.players[currPlayerID]
        while currPlayer.inRound:
            clear()
            # if self.lastNotableMove != None:
                # print(self.lastNotableMove.action, self.lastNotableMove.amount, self.lastNotableMove.playerID)
                # print(currPlayerID, currPlayer.currBet)
            print(f"===== {turnName} =====")
            print(f"Board: {self.boardCards}")
            if self.playersInRound == 1 or (self.lastNotableMove != None and self.lastNotableMove.playerID == currPlayerID 
                and self.lastNotableMove.amount == currPlayer.currBet):
                break
            currPlayer.makeMove(PokerMove(self, currPlayerID))

            # update variables for next player
            index = (index + 1) % len(self.ids)
            currPlayerID = self.ids[index]
            currPlayer = self.players[currPlayerID]
        
        # signal end of turn to pot and subtract turn bets from players
        for playerID, betAmount in self.pot.advanceTurn().items():
            self.players[playerID].updateScore(-betAmount)
            self.players[playerID].currBet = 0
        
        # reset for next turn
        self.lastNotableMove = None
        # if self.playersInRound == 1:
        #     self.endRound()

    def getValidMoveActions(self, playerID):
        """Return list of valid move actions for specific player."""
        possibleMoves = []
        if self.lastNotableMove == None or self.lastNotableMove.action == "Check":
            possibleMoves = ["Check", "Bet"]
        else:
            if self.lastNotableMove.action in ["Bet", "Raise"]:
                possibleMoves = [] if self.lastNotableMove.playerID == playerID else ["Call"]
                if self.players[playerID].score > self.lastNotableMove.amount:
                    possibleMoves.append("Raise")
            elif self.lastNotableMove.action == "Call":
                possibleMoves = ["Call"]
            possibleMoves.append("Fold")
        return possibleMoves

    def validMoveFunc(self, playerID: int):
        """Return function for move validation for specified player"""
        def isValid(action: str, amount: int):
            if amount == self.players[playerID].score and action == "Raise" and amount > self.lastNotableMove.amount:
                return True
            return (action in self.getValidMoveActions(playerID) and amount <= self.players[playerID].score 
                    and amount >= self.minBetFunc()(action))
        return isValid
    
    def minBetFunc(self):
        def minBet(action: str):
            if action == "Raise":
                return self.lastNotableMove.amount * 2
            elif action == "Bet":
                return 1
            else:
                return -1
        return minBet

    # def generateMove(self):
    #     return PokerMove(self, )

    def update(self, move: PokerMove):
        """Update game with given move. Should only be called after move is validated."""
        currPlayer = self.players[move.playerID]
        currPlayer.inRound = move.action != "Fold"
        self.playersInRound -= move.action == "Fold" # or (not currPlayer.isAllIn and move.amount == currPlayer.score)     
        currPlayer.isAllIn = move.amount == currPlayer.score

        if move.action == "Check" and (self.lastNotableMove == None or self.lastNotableMove.action != "Check"):
            self.lastNotableMove = move
        elif move.action in ["Bet", "Raise"]:
            if move.action == "Raise" and currPlayer.score == move.amount and move.amount <= self.minBetFunc()("Raise"):
                allInMove = PokerMove(self, move.playerID)
                allInMove.action = "Call"
                allInMove.amount = move.amount
                allInMove.isSet = True
                self.lastNotableMove = allInMove
            else:
                self.lastNotableMove = move
        elif move.action == "Call":
            if self.lastNotableMove.amount > currPlayer.score:
                currPlayer.isAllIn = True
            move.amount = min(self.lastNotableMove.amount, currPlayer.score)
        
        self.allInCount += currPlayer.isAllIn
        self.pot.addToPot(move.playerID, move.amount)
        self.players[move.playerID].currBet = move.amount
        print(f"Player {currPlayer.name}: {move.action}{' '+str(move.amount) if move.action in ['Bet', 'Call', 'Raise'] else ''}")
    
    def getBestHandVal(self, playerID):
        return max([Hand(handCards).getHandValue() for handCards in combinations(self.boardCards + self.players[playerID].cards, 5)])

def main():
    # players = [Player("arnold"), Player("bom"), Player("cork"), Player("probaldo", True, Bot())]
    # poker = Game(players = players)
    # poker.reset()

    # poker.community = poker.deck.dealCards(5)
    # # poker.community = [Card("hearts", 12), Card("clubs", 10), Card("spades", 11), Card("diamonds", 13), Card("hearts", 9)]
    # bestHand = poker.handValue(poker.deck.dealCards(2))
    # # bestHand = poker.handValue([])
    # print([str(x) for x in bestHand[0]], bestHand[1])

    # testHand = Hand((Card("hearts", 12), Card("clubs", 10), Card("spades", 11), Card("diamonds", 13), Card("hearts", 9)))

    # hands = []

    # for x in range(100):
    #     deck = Deck()
    #     deck.shuffle()
    #     for i in range(10):
    #         hands.append(Hand(deck.dealCards(5)))
    
    # hands.sort(key = lambda x: x.getHandValue(), reverse = True)
    
    # for i in range(10): 
    #     print(f"{i+1}: {hands[i]} \t | {hands[i].getHandValue():,}")
    
    g = Poker([HumanPlayer("Vervov",100), HumanPlayer("Violet",100)])
    g.start()
    # p = Pot()
    # print("betting round 1")
    # bets = enumerate([100, 150, 50, 150])
    # for x, betAmount in bets:
    #     # betAmount = (x % 2) * 50 + 100
    #     print(x, betAmount)
    #     p.addToPot(x,betAmount)
    # p.addToPot(0,200)
    # p.addToPot(1,200)
    # # p.addToPot(3, 0)
    # # p.addToPot(3,200)
    # p.advanceTurn()

    # print("betting round 2")
    # bets = [(0,100),(1,200)]
    # for x, betAmount in bets:
    #     # betAmount = (x % 2) * 50 + 100
    #     print(x, betAmount)
    #     p.addToPot(x,betAmount)
    # p.advanceTurn()
    # print("splitting")
    # for a,b in p.splitPot([[0,2,3],[1]]).items():
    #     print(a, b)
    
    #2

    # testHand2 = Hand((Card("hearts", 12), Card("clubs", 9), Card("spades", 12), Card("diamonds", 13), Card("hearts", 9)))
    
    
    # print(testHand2.getHandValue())
    

    # poker.bettingPrehand()
    # poker.dealHands()
    # poker.betting()
    # poker.dealComm(1)
    # poker.betting()
    # poker.dealComm(2)
    # poker.betting()
    # poker.dealComm(3)
    # poker.betting()
    # poker.results()
    

if __name__ == '__main__':
    main()