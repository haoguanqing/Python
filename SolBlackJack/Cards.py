import random

class Card():
    
    def __init__(self, r, s):
        #r is the rank, s is suit
        self.r = r   #int or str, number or letter all acceptable
        self.s = s   #str
        if str(r) not in ['1','2','3','4','5','6','7','8','9','10','11','12','13','j','q','k','J','Q','K']:
            raise ValueError('card rank out of range')
        if str(s) not in ['s','S','c','C','h','H','d','D']:
            raise ValueError('card suit error')

    def __str__(self):
        rank = ''
        if self.r in ['j','q','k']:
            rank = self.r.upper()
        elif str(self.r) == '11':
            rank = 'J'
        elif str(self.r) == '12':
            rank = 'Q'
        elif str(self.r) == '13':
            rank = 'K'
        else:
            rank = str(self.r)
        suit = self.s.upper()
        return rank + suit

    def get_rank(self):
        if self.r == 'j' or self.r == 'J':
            rank = 11
        elif self.r == 'q' or self.r == 'Q':
            rank = 12
        elif self.r == 'k' or self.r == 'K':
            rank = 13
        else:
            rank = int(self.r)
        return rank

    def get_suit(self):
        return self.s.upper()

class Deck():
    '''Denote a deck to play cards with'''
    
    def __init__(self):
        '''Initialize deck as a list of all 52 cards:
           13 cards in each of 4 suits'''
        self.__deck = []
        for suit in ['S', 'C', 'H', 'D']:
            for rank in xrange(1,14):
                self.__deck.append(Card(rank, suit))

    def shuffle(self):
        '''Shuffle the deck'''
        random.shuffle(self.__deck)

    def deal(self):
        '''get the last card in the deck
        simulates a pile of cards and getting the top one'''
        return self.__deck.pop(-1)

    def get_deck(self):
        return self.__deck
    
    def __str__(self):
        '''Represent the whole deck as a string for printing'''
        printInfo = "The deck is:\n"
        for card in self.__deck:
            printInfo += str(card)
            printInfo += '\n'
        return printInfo
