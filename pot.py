class Pot:
    def __init__(self, amount, players):
        self.players = players
        self.amount = amount
    
    def splitPot(self):
        active = []
        for player in players:
            if player.isActive():
                active.append(player)
        
        numActive = len(active)
        for player in active:
            player.winMoney(self.amount / numActive)

