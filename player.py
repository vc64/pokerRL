class CardPlayer:
    def __init__(self, name: str, score: int, minScore: int):
        self.score = score
        self.minScore = minScore
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

    def updateScore(self, val):
        self.score += val
        self.inGame = self.score >= self.minScore


class PokerPlayer(CardPlayer):
    def __init__(self, name: str, score: int):
        super().__init__(name, score, 1)
        self.isAllIn = False
    
    def resetPlayer(self):
        self.cards = []
        self.isAllIn = False
        self.inRound = True
    
    # def getRatio(self):
    #     return self.wins / self.losses
    
    # def getWins(self):
    #     return self.wins
    
    # def getLosses(self):
    #     return self.losses
    

class HumanPlayer(PokerPlayer):
    def __init__(self, name, score: int):
        super().__init__(name, score)
        self.currBet = 0
    
    def makeMove(self, moveObj):
        validMoveActions = moveObj.gameInfo["validMoveActions"]

        print(f"{self.name}'s turn. Hand: {self.cards}")
        print(f"Balance: {self.score - self.currBet}   Pot: {moveObj.gameInfo['potTotal']}   Current bet: {self.currBet}   Bet to meet: {moveObj.gameInfo['lastNotableMove']}")
        print(f"Valid actions: {'  '.join([f'({i+1}) {validMoveActions[i]}' for i in range(len(validMoveActions))])}")

        madeValidMove = False
        while not madeValidMove:
            moveActionNum = input("Please select an action by their corresponding number: ")
            while not (moveActionNum.isnumeric() and 1 <= int(moveActionNum) and int(moveActionNum) <= len(validMoveActions)):
                moveActionNum = input("Invalid action. Please choose a valid action: ")
            moveAction = validMoveActions[int(moveActionNum)-1]
            moveAmount = 0
            if moveAction in ["Bet", "Raise"]:
                moveAmount = input(f"Please specify amount for {moveAction} (at least {moveObj.minBet(moveAction)}): ")
                while not moveAmount.replace(".","",1).isnumeric():
                    moveAmount = input(f"Invalid amount. Please specify amount for {moveAction} (positive integers only): ")
            madeValidMove = moveObj.setMove(moveAction, round(float(moveAmount), 1))
        print()