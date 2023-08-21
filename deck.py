from card import Card
import random

class Deck:
    def __init__(self):
        self.cards = []
    
    def shuffle(self):
        random.shuffle(self.cards)

    def resetDeck(self):
        for suit in ["diamonds", "clubs", "hearts", "spades"]:
            for val in range(1,13):
                self.cards.append(Card(suit, val))
    
    def dealCard(self):
        return self.cards.pop()

    def dealCards(self, n):
        return [self.dealCard() for i in range(n)]
    
    def cardCount(self):
        return len(self.cards)
   
