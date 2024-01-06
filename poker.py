from table import Deck, Board
from card import Card, Hand
from player import CardPlayer, HumanPlayer
from bot import BotPlayer

import random
from itertools import combinations
import math

class Move:
    """General class to allow Player to make a Move based on game info."""
    def __init__(self, game, playerID = -1,):
        self.playerID = playerID
        self.game = game

    def isValid(self):
        pass

class PokerMove(Move):
    def __init__(self, playerID: int, isValid):
        super().__init__(playerID)
        self.action = ""
        self.amount = -1
        self.isSet = False
        self.validMoveActions = self.game.getValidMoveActions(self.playerID)
        self.isValid = lambda : self.game.validMoveFunc(self.playerID)(self.action, self.amount)
        self.minBet = self.minBetFunc(self.playerID)
    
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
        return self.isSet

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

    def generateMove(self):
        """Return a move object for the game."""
        pass

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

    def start(self):
        """Start the game. Will block until game ends."""
        self.deck.resetDeck()
        self.deck.shuffle()

        random.shuffle(self.ids) # ..., D, SB, BB,

        # pre-flop
        print("pre-flop")
        self.players[self.ids[-2]]
        for playerID in self.ids:
            currPlayer = self.players[playerID]
            currPlayer.addToHand(self.deck.dealCards(2))
            currPlayer.makeMove(self, PokerMove(self, playerID, self.validMoveFunc(playerID)))

        # self.obs.update(self.ids, self, PokerMove())

        # flop
        print("flop")
        self.boardCards.append(self.deck.dealCards(3))
        self.obs.update(self.ids, self)

        # turn
        print("turn")
        self.boardCards.append(self.deck.dealCards())
        self.obs.update(self.ids, self)

        # river
        print("flop")
        self.boardCards.append(self.deck.dealCards())
        self.obs.update(self.ids, self)

        # showdown
    
    def turn(self, handCards: int, boardCards: int):
        index = 0
        currPlayerID = self.ids[index]
        currPlayer = self.players[currPlayerID]
        while currPlayer.inRound:
            if handCards > 0:
                currPlayer.addToHand(self.deck.dealCards(handCards))
            elif boardCards > 0:
                self.boardCards.append(self.deck.dealCards(boardCards))
            currPlayer.makeMove(self, PokerMove(currPlayerID, self.validMoveFunc(currPlayerID)))
            
            # update variables for next player
            index = (index + 1) % len(self.ids)
            currPlayerID = self.ids[index]
            currPlayer = self.players[currPlayerID]

    def getValidMoveActions(self, playerID):
        """Return list of valid move actions for specific player."""
        possibleMoves = []
        if self.lastNotableMove.action == "Check":
            possibleMoves = self.moveActions
        # elif self.lastNotableMove.action == "Call":
        #     possibleMoves = []
        elif self.lastNotableMove.action in ["Bet", "Raise"] and self.lastNotableMove.playerID == playerID:
            possibleMoves = [] if self.lastNotableMove.playerID == playerID else ["Call", "Raise", "Fold"]
        else:
            possibleMoves = ["Fold"]
        return possibleMoves

    def validMoveFunc(self, playerID: int):
        """Return function for move validation for specified player"""
        def isValid(action: str, amount: int):
            return (action in self.getValidMoveActions(playerID) and amount <= self.players[playerID].score 
                    and amount >= self.minBetFunc(playerID)(action))
        return isValid
    
    def minBetFunc(self, playerID: int):
        def minBet(action: str):
            if action == "Raise":
                return self.lastNotableMove.amount * 2
            elif action == "Bet":
                return 1
            else:
                return -1
        return minBet

    def generateMove(self):
        return PokerMove(self.getValidMoveActions(), self.isValidMove)

    def update(self, move: PokerMove):
        """Update game with given move."""
        currPlayer = self.players[move.playerID]
        
        print(f"Player {currPlayer.name}: {move.action} {move.amount}")
        pass





# class Game:
#     def __init__(self, players=[]):
#         self.deck = Deck()
#         self.players = players
#         self.pot = []
#         self.ante = 1
#         self.roundNum = 1
#         self.dealer = 0
#         self.SB = 5
#         self.BB = 10
#         self.community = []

#     def addPlayer(self, player):
#         self.players.append(player)
    
#     def next(self, playerNum):
#         return (playerNum + 1) % len(self.players)
    
#     #will loop forever if none active
#     def nextActive(self, playerNum):
#         while not self.players[next(playerNum)].isActive():
#             playerNum = self.next(playerNum)
#         return self.next(playerNum)

#     def reset(self):
#         self.deck.resetDeck()
#         self.deck.shuffle()
#         self.pot = {}
#         for i in range(len(self.players)):
#             if self.players[i].getMoney() <= 0:
#                 if i != self.dealer:
#                     self.dealer -= 1
#                 del self.players[i]
        
#         if self.roundNum == 1:
#             self.dealer = random.randint(0,len(self.players))
#         else:
#             self.dealer = next(self.dealer)
        
#     def bettingPrehand(self):
#         self.ante = self.roundNum * 2
#         for i in range(len(self.players)):
#             if i == self.next(self.dealer):
#                 self.players[i].bet(self.SB)
#             elif i == self.next(self.next(self.dealer)):
#                 self.players[i].bet(self.BB)
#             else:
#                 self.players[i].bet(self.ante)

#         # get ante from players
    
#     def dealHands(self):
#         for player in self.players:
#             if player.isActive():
#                 player.setHand(self.deck.dealCards(2))
    
#     def dealComm(self, roundNum):
#         if roundNum == 1:
#             self.community = self.deck.dealCards(3)
#         elif roundNum == 2 or roundNum == 3:
#             self.community.append(self.deck.dealCard())

#     def handValue(self, hand):
#         bestHand = self.community
#         bestVal = 0
#         # bestVal = '0'
#         for group in combinations(hand + self.community, 5):
#             suitFreq = {}
#             valFreq = {}
#             small = group[0].getVal()
#             large = group[0].getVal()
#             royalNums = True
#             for card in group:
#                 royalNums = royalNums and (card.getVal() == 1 or card.getVal() >= 10)

#                 if card.getVal() < small:
#                     small = card.getVal()
#                 if card.getVal() > large:
#                     large = card.getVal()

#                 try:
#                     valFreq[card.getVal()] += 1
#                 except:
#                     valFreq[card.getVal()] = 1
                
#                 try:
#                     suitFreq[card.getSuit()] += 1
#                 except:
#                     suitFreq[card.getSuit()] = 1
            
#             flush = False
#             straight = False
#             quad = False
#             triple = False
#             twoPair = False
#             pair = False

#             flush = len(suitFreq) == 1
#             for val, freq in valFreq.items():
#                 quad = quad or freq == 4
#                 triple = triple or freq == 3
#                 twoPair = twoPair or (pair and freq == 2)
#                 pair = pair or freq == 2
            
#             unique = not pair and not twoPair and not triple and not quad
#             straight = unique and (large - small) == 4
            
#             # values = [royalNums and unique, straight and flush, quad, triple and pair, 
#             #           flush, straight, triple, twoPair, pair, True]

#             # binVal = ''.join(['1' if x else '0' for x in values])
#             # if binVal > bestVal:
#             #     bestVal = binVal
#             #     bestHand = group

#             handVal = 0
#             if royalNums and unique:
#                 handVal = 10
#             elif straight and flush:
#                 handVal = 9
#             elif quad:
#                 handVal = 8
#             elif triple and pair:
#                 handVal = 7
#             elif flush:
#                 handVal = 6
#             elif straight: 
#                 handVal = 5
#             elif triple:
#                 handVal = 4
#             elif twoPair:
#                 handVal = 3
#             elif pair:
#                 handVal = 2
#             else:
#                 handVal = 1
            
#             if bestVal < handVal:
#                 bestVal = handVal
#                 bestHand = group

#         return bestHand, bestVal
        # print(int(bestVal, 2))
        # return bestHand, math.floor(math.log(int(bestVal, 2), 2))

    # -1 if handB > handA, 1 if handA > handB, 0 if tied    
    # def tiebreak(handA, handB, handVal):
    #     if handVal == 10:

    #     elif handVal == 9:

    #     elif handVal == 8:
            

    # def betting(self):
    #     self.openBet = 0
    #     playerNum = self.nextActive(self.dealer)
    #     actions = []
    #     betNum = 1
    #     currBet = 0
    #     while betNum <= len(self.players) or self.openBet != self.players[playerNum].currBet():
    #         if betNum == 1:
    #             actions = ["Bet", "Check", "Fold"]
    #         elif self.openBet == 0:
    #             actions = ["Call", "Check", "Fold", "Raise"]
    #         else:
    #             actions = ["Call", "Fold", "Raise"]
    #         currBet = self.players[playerNum].getBet(self.community, actions)
    #         if currBet >= self.openBet:
    #             self.openBet = currBet
    #         playerNum = self.nextActive(playerNum)
    #         betNum += 1
        

    #     roundPot = 0
    #     roundActive = 0
    #     for player in self.players:
    #         roundPot += player.currBet()
    #         if player.currBet() != 0:
    #             roundActive += 1
        
    #     for player in self.players:
    #         if player.isActive():
    #             if player.currBet() < self.openBet:
    #                 player.setExpect(player.currBet() * roundActive)
    #             else:
    #                 player.setExpect(self.pot + roundPot)
        
    #     self.pot += roundPot
    
    # def results(self):
    #     maxVal = 0
    #     maxHand = None
    #     winner = None
    #     for player in self.players:
    #         currHand, currVal = self.handValue(player.getHand())
    #         if currVal > maxVal:
    #             maxVal = currVal
    #             maxHand = currHand
    #             winner = player
    #         elif currVal == maxVal:
    #             result = tiebreak(maxHand, currHand, currVal)
    #             if result < 0:
    #                 maxHand = currHand
    #             elif result == 0:

    #             else:

                
    #     pass


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

    hands = []

    for x in range(100):
        deck = Deck()
        deck.shuffle()
        for i in range(10):
            hands.append(Hand(deck.dealCards(5)))
    
    hands.sort(key = lambda x: x.getHandValue(), reverse = True)
    
    for i in range(10): 
        print(f"{i+1}: {hands[i]} \t | {hands[i].getHandValue():,}")
    
    g = Poker([HumanPlayer("Vervov",100)])
    g.start()
    
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