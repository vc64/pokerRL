from player import CardPlayer

class BotPlayer(CardPlayer):
    def __init__(self, name, score):
        super().__init__(name, score)

    def getAction(self, money, openBet, hand, community, actions):
        prob = getProb(hand)
    
    def getProb(hand):
        pass

    
