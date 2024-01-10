from card import Card, Suits, Vals
import random

class Deck:
    def __init__(self):
        self.resetDeck()
    
    def shuffle(self):
        random.shuffle(self.cards) # maybe replace with fisher yates later on

    def resetDeck(self):
        self.cards = []
        for suit in Suits:
            for val in Vals:
                if (val.name != "Ace(low)"):
                    self.cards.append(Card(suit.value, val.value))
    
    # deal n cards, with default being 1
    def dealCards(self, n = 1):
        return tuple(self.cards.pop() for i in range(n))
    
    def cardCount(self):
        return len(self.cards)
