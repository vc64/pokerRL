# from poker import Poker
from card import Card

class CardPlayer:
    def __init__(self, name: str, score: int):
        self.score = score
        self.wins = 0
        self.losses = 0
        self.name = name
        self.cards = []
        self.inGame = False
        self.inRound = False

    def makeMove(self, game):
        pass
    
    def addToHand(self, cards):
        for card in cards:
            self.cards.append(card)
    


    # def getMoney(self):
    #     return self.money
    
    # def getRatio(self):
    #     return self.wins / self.losses
    
    # def getWins(self):
    #     return self.wins
    
    # def getLosses(self):
    #     return self.losses
    
    # def getName(self):
    #     return self.name
    
    # def isActive(self):
    #     return self.isActive

    # def setActive(self, state):
    #     self.isActive = state

    # def setHand(self, cards):
    #     self.hand = cards

    # def setExpect(self, amount):
    #     self.expect = amount
    
    # def winMoney(self, amount):
    #     self.money += amount
    
    # def currBet(self):
    #     return self.bet

    
    # def getBet(self, community, actions):
    #     bet = 0
    #     if self.isBot:
    #         bet = self.bot.getAction(self.money, self.openBet, self.hand, community, actions)
    #     else:
    #         self.viewMoney()
    #         bet = int(input("Please enter bet (cannot exceed current balance): "))
        
    #     self.bet = bet
    #     return bet
    
    # def bet(self, amount):
    #     if self.getMoney() <= amount:
    #         self.money -= amount
    #         return True
    #     else:
    #         self.money = 0
    #         return False

    # def getHand(self):
    #     return self.hand

    # def viewHand(self):
    #     print(self.name + "'s hand: " + ", ".join(self.hand))

    # def viewMoney(self):
    #     print("Balance: $" + str(self.getMoney))


class HumanPlayer(CardPlayer):
    def __init__(self, name, score):
        super().__init__(name, score)
        self.currBet = 0
    
    def makeMove(self, game, moveObj):
        validMoveActions = game.getValidMoveActions()

        print(f"{self.name}'s turn. Hand: {self.cards}") 
        print(f"Board: {game.boardCards}")
        print(f"Balance: {self.score}")
        print(f"Valid actions: {'  '.join([f'({i+1}) {validMoveActions[i]}' for i in range(len(validMoveActions))])}")

        madeValidMove = False
        while not madeValidMove:
            moveActionNum = input("Please select an action by their corresponding number: ")
            while not (moveActionNum.isnumeric() and 1 <= int(moveActionNum) and int(moveActionNum) <= len(validMoveActions)):
                moveActionNum = input("Invalid action. Please choose a valid action: ")
            moveAction = validMoveActions[int(moveActionNum-1)]
            moveAmount = 0
            if moveAction in ["Bet", "Raise"]:
                moveAmount = input(f"Please specify amount for {moveAction} (positive integers only): ")
                while not moveAmount.isnumeric():
                    moveAmount = input(f"Invalid amount. Please specify amount for {moveAction} (positive integers only): ")
            madeValidMove = moveObj.setMove(moveAction, moveAmount)
        self.currBet = moveAmount
    
    def updateScore(self, val):
        self.score += val