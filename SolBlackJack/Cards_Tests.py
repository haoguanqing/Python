from Cards import *
import unittest

class TestCard(unittest.TestCase):

     def setUp(self):
          self.card1 = Card('11', 's')
          self.card2 = Card(11, 'D')
          self.card3 = Card('j', 'c')
          self.card4 = Card('J', 'H')
          
          self.deck = Deck()
          
     # tests for Card()
     def test_Card_init(self):
          '''tests the __init__ func in Card()'''
          # raises error if not in range
          self.assertRaises(ValueError, Card, '14', 's')
          self.assertRaises(ValueError, Card, 0, 's')
          self.assertRaises(ValueError, Card, 'x', 's')
          self.assertRaises(ValueError, Card, '12', 'x')
          
          # reasonable integers(1~13) and strings(such as '1', 'j', 'J') should all be acceptable for card rank
          self.assertEqual('11', self.card1.r, 'Card.r failed')
          self.assertEqual(11, self.card2.r, 'Card.r failed')
          self.assertEqual('j', self.card3.r, 'Card.r failed')
          self.assertEqual('H', self.card4.s, 'Card.s failed')

     def test_Card_str(self):
          '''tests the __str__ func in Card()'''
          self.assertEqual('JS', str(self.card1), 'Card __str__ failed')
          self.assertEqual('JD', str(self.card2), 'Card __str__ failed')
          self.assertEqual('JC', str(self.card3), 'Card __str__ failed')
          self.assertEqual('JH', str(self.card4), 'Card __str__ failed')
          
     def test_get_rank(self):
          '''tests the get_rank func in Card()'''
          self.assertEqual(11, self.card1.get_rank(), 'get_rank failed')
          self.assertEqual(11, self.card2.get_rank(), 'get_rank failed')
          self.assertEqual(11, self.card3.get_rank(), 'get_rank failed')
          self.assertEqual(11, self.card4.get_rank(), 'get_rank failed')

     def test_get_suit(self):
          '''tests the get_suit func in Card()'''
          self.assertEqual('S', self.card1.get_suit(), 'get_suit failed')
          self.assertEqual('D', self.card2.get_suit(), 'get_suit failed')

          
     # tests for Deck()
     def test_Deck_init(self):
          '''tests the __init__ func in Deck()'''
          actDeck = self.deck.get_deck()
          expDeck = []
          for s in ['S', 'C', 'H', 'D']:
               for r in xrange(1,14):
                    expDeck.append(Card(r, s))
          for index in xrange(0,len(actDeck)):
               self.assertEqual(expDeck[index].get_rank(), actDeck[index].get_rank())
               self.assertEqual(expDeck[index].get_suit(), actDeck[index].get_suit())

     def test_Deck_str(self):
          '''tests the __str__ func in Deck() '''
          expStr = 'The deck is:\n'
          for suit in ['S', 'C', 'H', 'D']:
               for rank in xrange(1,14):
                    expStr += (str(Card(rank, suit)) + '\n')
          self.assertEqual(expStr, str(Deck()))

     def test_deal(self):
          '''tests the deal func in Deck()'''
          topCard1 = self.deck.deal()
          self.assertEqual('KD', str(topCard1))
          topCard2 = self.deck.deal()
          self.assertEqual('QD', str(topCard2))
          
     def test_get_deck(self):
          '''tests the get_deck func in Deck()
          compares the string form of every card in deck list to the corresponding card in expected list'''
          actDeck = self.deck.get_deck()
          expDeck = []
          for s in ['S', 'C', 'H', 'D']:
               for r in xrange(1,14):
                    expDeck.append(Card(r, s))
          for index in xrange(0,len(actDeck)):
               self.assertEqual(str(expDeck[index]), str(actDeck[index]))

unittest.main()
