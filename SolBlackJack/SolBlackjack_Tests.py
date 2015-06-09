from SolBlackjack import *
import unittest

class test_SolBlackjack(unittest.TestCase):

    def setUp(self):
        self.deal = Card('4','h')
        
        self.row1 = [Card(13,'D'), Card('7', 'H'), Card(2, 'D'), Card(6, 'S'), Card(1, 'H')]
        self.row2 = [Card('j','d'), Card(9, 's'), Card('Q','H'), Card(4, 'C'), Card(10,'D')]
        self.row3 = [Card(10,'d'), Card(5, 'S'), Card(6, 'C')]
        self.row4 = [Card(4, 'S'), Card('k', 's'), Card(5, 'C')]
        self.table1 = {'row1': self.row1, 'row2': self.row2, 'row3': self.row3, 'row4': self.row4}

        self.row5 = ['1','2','3','4','5']
        self.row6 = ['6','7','8','9','10']
        self.row7 = ['11','12','13']
        self.row8 = ['14','15','16']
        self.table2 = {'row1':self.row5, 'row2':self.row6, 'row3':self.row7, 'row4':self.row8}
        
        self.discard = ['17','18','19','20']
        
        #variables for the class 'BalckJack'
        self.blackjack = BlackJack()

    def test_combineList(self):
        lst = combineList(self.deal, self.table1, self.discard)
        lst2 = [self.deal] + self.row1 + self.row2 + self.row3 + self.row4 + self.discard
        self.assertEqual(lst2, lst, 'combine list fail')

    def test_splitList(self):
        lst = []
        for x in range(0,21):
            lst.append(str(x))
        table, discard = splitList(lst)
        self.assertEqual(self.table2, table)
        self.assertEqual(self.discard, discard)

    def test_isAce(self):
        is_ace1 = isAce(self.row1)
        is_ace2 = isAce(self.row2)
        self.assertTrue(is_ace1)
        self.assertFalse(is_ace2)

    def test_scoreRow(self):
        score1 = scoreRow([Card(13,'D'), Card(1,'H')])
        score2 = scoreRow([Card(8,'D'), Card(1,'H'), Card(3,'S')])
        score3 = scoreRow(self.row1)
        self.assertEqual(10, score1)
        self.assertEqual(1, score2)
        self.assertEqual(0, score3)

    def test_scoreTable(self):
        self.assertEqual(33, scoreTable(self.table1))

## TA said it's not necessary to write unittests for io related functions
##    
##    def test_safeRead(self):
##        '''tests by using a file name that does not exist
##        the func should create a new file and store 0 as highest score
##        finally it should return 0'''
##        fileName = 'highScoreTest.txt'
##        highScore = safeRead(fileName)
##        self.assertEqual(0, highScore)
##
##    def test_isHighScore(self):
##        '''create another list'''
##        fileName = 'highScoreTest2.txt'
##        isHighScore(21, fileName)
##        highScore1 = safeRead(fileName)
##        self.assertEqual(21, highScore1)
##        
##        isHighScore(10, fileName)
##        highScore2 = safeRead(fileName)
##        self.assertEqual(21, highScore2)


    # tests the func in class 'BlackJack()'
    def test_BlackJack_init(self):
        '''tests the __init__ func in BlackJack()'''
        self.assertEqual(str(Deck()), str(self.blackjack.deck))
        
        availableList = [str(x) for x in xrange(1,21)]
        self.assertEqual(availableList, self.blackjack.availableList)
        
        # we need a new table here because '01' is different from '1'
        # i.e. this table is different from self.table2
        row1 = ['01', '02', '03', '04', '05']
        row2 = ['06', '07', '08', '09', '10']
        row3 = ['11', '12', '13']
        row4 = ['14', '15', '16']
        table = {'row1':row1, 'row2':row2, 'row3':row3, 'row4':row4}
        self.assertEqual(table, self.blackjack.table)
        
        self.assertEqual(self.discard, self.blackjack.discard)

    def test_checkErrorMove(self):
        judge1 = self.blackjack.checkErrorMove('12')
        self.assertTrue(judge1, 'checkErrorMove')

        judge2 = self.blackjack.checkErrorMove('0')
        self.assertFalse(judge2, 'checkErrorMove')

        judge3 = self.blackjack.checkErrorMove('abc')
        self.assertFalse(judge3, 'checkErrorMove')

    def test_processUserMove(self):
        move = '1'
        deal = Card(3,'s')
        self.blackjack.processUserMove(move, deal)
        insertCard = self.blackjack.table['row1'][0]
        self.assertEqual(insertCard.get_rank(), 3)
        self.assertEqual(insertCard.get_suit(), 'S')

## acceptUserMove() just simply calls the previous two functions
## thus we don't need to test it

## play() calls a lot of functions, which are all tested above, and returns nothing
## thus we don't need to test it

unittest.main()



