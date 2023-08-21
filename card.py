from enum import Enum, unique

suits = ["Diamonds", "Clubs", "Hearts", "Spades"]
values = {1: "Ace", 2: "Two", 3: "Three", 4: "Four", 5: "Five", 6: "Six", 7: "Seven", 
          8: "Eight", 9: "Nine", 10: "Ten", 11: "Jack", 12: "Queen", 13: "King"}

class Card:
    def __init__(self, suit, number):
        self.suit = suit
        self.number = number
    
    def sameSuit(self, other):
        return self.suit == other.suit
    
    def sameNum(self, other):
        return self.number == other.number
    
    def getSuit(self):
        return self.suit
    
    def getVal(self):
        return self.number
    
    def numStr(val):
        try:
            return values[val]
        
        except:
            print("error: not a valid card value")
            return -1

    def __str__(self):
        return Card.numStr(self.number) + " of " + self.suit


