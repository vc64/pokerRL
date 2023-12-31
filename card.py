from enum import Enum, unique
from functools import total_ordering
from itertools import combinations, chain
from collections import defaultdict
import math

Suits = Enum("Suits", {"d": "Diamonds", "c": "Clubs", "h": "Hearts", "s": "Spades"})
Vals = Enum("Values", {"Ace(low)": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5, "Six": 6, "Seven": 7, "Eight": 8, 
                       "Nine": 9, "Ten": 10, "Jack": 11, "Queen": 12, "King": 13, "Ace": 14})

# suits = ["Diamonds", "Clubs", "Hearts", "Spades"]
# values = {1: "Ace", 2: "Two", 3: "Three", 4: "Four", 5: "Five", 6: "Six", 7: "Seven", 
#           8: "Eight", 9: "Nine", 10: "Ten", 11: "Jack", 12: "Queen", 13: "King"}

class Card:
    def __init__(self, suit, number):
        # either will throw error if provided suit/number is invalid
        if (len(suit) > 1):
            suit = suit[0].lower()
        self._suit = Suits[suit].name
        self._number = Vals(number).value

    #try to avoid using these getters unless necessary (i.e. for sorting list of cards)
    def getSuit(self):
        return self._suit
    
    def getValue(self):
        return self._number
        
    def isVal(self, value):
        return self._number == value
    
    def isSuit(self, suit):
        return self._suit == suit
    
    def hexVal(self):
        return hex(self._number)

    def __str__(self):
        return Vals(self._number).name + " of " + Suits[self._suit].value
    
    # 0 if not equal, 1 if equal
    def compareSuits(self, otherCard):
        return self._suit == otherCard._suit

    # -1 if less than, 0 if equal, 1 if greater than
    def compareVals(self, otherCard):
        return -1 if self._number < otherCard._number else 0 if self._number == otherCard._number else 1


@total_ordering #functools - fills in remaining comparators
class Hand:
    def __init__(self, cards: tuple):
        if len(cards) != 5:
            raise Exception("Invalid number of cards for a hand.")
        
        self.cards = cards
        self.hex = 0
        self.suitFreqs = defaultdict(lambda:0, {})
        self.valFreqs = defaultdict(lambda:0, {})
        self._orderCards()
        self.handVal = self._handValue()
    
    def _orderCards(self):
        valGroups = defaultdict(lambda:[], {})
        for card in self.cards:
            self.suitFreqs[card.getSuit()] += 1
            self.valFreqs[card.getValue()] += 1
            valGroups[card.getValue()].append(card)

        sortedCardGroups = sorted(valGroups.values(), key=lambda x : [len(x), x[0].getValue()], reverse = True)
        self.cards = tuple(chain.from_iterable(sortedCardGroups)) #join together list of lists into one list

        # calculate hand hex value
        for card in self.cards:
            self.hex *= 16
            self.hex += card.getValue()

    def _handValue(self):
        def isOneAway(a, b, isAscending = True):
            return a - b == -1 + (2 * isAscending)
        
        # check if given list of cards is a straight (must have > 1 card)
        def isStraight(cards):
            assert(len(cards) > 1)
            initialDiff = cards[0].getValue() - cards[1].getValue()
            isNext = lambda index : isOneAway(self.cards[index].getValue(), self.cards[index+1].getValue(), isAscending = initialDiff > 0)
            return all([isNext(i) for i in range(len(self.cards)-1)])
        
        # return a boolean tuple with booleans for four/three/two/twopair of a kind
        def sameVals():
            out = [False, False, False, False]
            for freq in self.valFreqs.values():
                if freq == 2 and out[2]:
                    out[3] = True
                if freq <= 4 and freq >= 2:
                    out[freq * -1 + 4] = True
            return out
        
        handScore = 0

        royal = all([self.cards[i].getValue() == range(14, 14 - len(self.cards), -1)[i] for i in range(len(self.cards))])
        straight = isStraight(self.cards) or (self.cards[0].isVal(14) and isStraight(self.cards[1:] + (Card("s",1),)))
        flush = len(self.suitFreqs.values()) == 1
        fourKind, threeKind, pair, twoPair = sameVals()

        if royal and flush:
            handScore = 9
        elif straight and flush:
            handScore = 8
        elif fourKind:
            handScore = 7
        elif threeKind and pair:
            handScore = 6
        elif flush:
            handScore = 5
        elif straight:
            handScore = 4
        elif threeKind:
            handScore = 3
        elif twoPair:
            handScore = 2
        elif pair:
            handScore = 1
        else:
            handScore = 0

        return handScore * 1000000 + self.hex

    def getHandValue(self):
        return self.handVal

    def _validateOperand(op: object) -> None:
        if not callable(getattr(op, "_getHandValue")):
            raise Exception("Invalid operand for comparison with Hand object.")

    # compare hand values
    def __lt__(self, __value: object) -> bool:
        self._isValidOperand(__value)
        return self.getHandValue() < __value.getHandValue()
    
    # will not compare equality of hand, only hand values
    def __eq__(self, __value: object) -> bool:
        self._isValidOperand(__value)
        return self.getHandValue() == __value.getHandValue()
    
    def __str__(self):
        return ", ".join([str(x) for x in self.cards])