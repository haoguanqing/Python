from Cards import *

def combineList(deal, table, discard):
    '''create a list with index 0 being the deal card, 1~16 being the table and 17~20 being the discard pile'''
    lst = [deal]
    for row in table:
        lst += table[row]
    lst += discard
    return lst

def splitList(lst):
    '''Conversely, split the list combined above back into table and discard.
    These two functions make the program a lot easier to put the new card in either table or discard,
    since you don't need to distinguish between different rows'''
    table = {}
    table['row1'] = lst[1:6]
    table['row2'] = lst[6:11]
    table['row3'] = lst[11:14]
    table['row4'] = lst[14:17]
    discard = lst[17:21]
    return table, discard

def isAce(lst):
    '''see if there is any Ace in a row/column. return boolean'''
    is_ace = False
    for card in lst:
        if card.get_rank() == 1:
            is_ace = True
    return is_ace

def scoreRow(lst):
    '''scores a single row or column'''
    sum_row = 0
    for card in lst:
        value = card.get_rank()
        if value > 10:
            value = 10
        sum_row += value
    #score the Aces
    is_ace = isAce(lst)
    if sum_row +10 < 22 and is_ace:
        sum_row += 10
    #return the scores
    if sum_row == 21:
        if len(lst) == 2:
            return 10
        else:
            return 7
    elif 16 < sum_row < 21:
        return sum_row - 15
    elif sum_row <= 16:
        return 1
    else:
        return 0

def scoreTable(table):
    '''sums up the points scored in each row and column to get the final point'''
    lst1 = table['row1']
    lst2 = table['row2']
    lst3 = table['row3']
    lst4 = table['row4']
    lst5 = [lst1[0], lst2[0]]
    lst6 = [lst1[1], lst2[1], lst3[0], lst4[0]]
    lst7 = [lst1[2], lst2[2], lst3[1], lst4[1]]
    lst8 = [lst1[3], lst2[3], lst3[2], lst4[2]]
    lst9 = [lst1[4], lst2[4]]
    score_table = (scoreRow(lst1) + scoreRow(lst2)
    + scoreRow(lst3) + scoreRow(lst4) + scoreRow(lst5)
    + scoreRow(lst6) + scoreRow(lst7) + scoreRow(lst8) + scoreRow(lst9))
    return score_table

def safeRead(fileName):
    '''safely opens the file and returns the highest score as an integer
    if file doesn't exist, create a new file with highest score being 0'''
    try:
        f = open(fileName, 'r')
    except IOError, e:
        f = open(fileName, 'w')
        f.write('0')
        f.close
    finally:
        f = open(fileName, 'r')
        highScore = f.read()
        f.close()
        return int(highScore)

def isHighScore(finalScore, fileName):
    '''if a new record is made, the func saves the score and prints a message
    otherwise, just shows what is the highest score'''
    highScore = safeRead(fileName)
    f = open(fileName, 'w')
    if finalScore > highScore:
        highScore = finalScore
        print 'Congratulations! New record!'
    else:
        print 'The highest score is', highScore
    f.write(str(highScore))
    f.close()
    

def display(deal, table, discard):
    '''prints the cards with a decent UI'''
    lst = combineList(deal, table, discard)

    for i in xrange(0,len(lst)):
        if len(str(lst[i])) == 2:
            lst[i] = str(lst[i])+'|'
        else:
            lst[i] = str(lst[i])           
    print '''
DEAL:      | TABLE:
 __        |  __  __  __  __  __ 
|'''+lst[0]+'''       | |'''+lst[1]+'''|'''+lst[2]+'''|'''+lst[3]+'''|'''+lst[4]+'''|'''+lst[5]+'''
|__|       | |__||__||__||__||__|
           |  __  __  __  __  __ 
DISCARD:   | |'''+lst[6]+'''|'''+lst[7]+'''|'''+lst[8]+'''|'''+lst[9]+'''|'''+lst[10]+'''
 __  __    | |__||__||__||__||__|
|'''+lst[17]+'''|'''+lst[18]+'''   |      __  __  __ 
|__||__|   |     |'''+lst[11]+'''|'''+lst[12]+'''|'''+lst[13]+'''
 __  __    |     |__||__||__|
|'''+lst[19]+'''|'''+lst[20]+'''   |      __  __  __ 
|__||__|   |     |'''+lst[14]+'''|'''+lst[15]+'''|'''+lst[16]+'''
           |     |__||__||__|
___________|______________________
'''

    
class BlackJack():

    def __init__(self):
        '''initialize the table and discard pile
        also, create a list which stores the indices of available spots left'''
        self.deck = Deck()
        self.availableList = []
        for i in xrange(1,21):
            self.availableList.append(str(i))
        row1 = ['01', '02', '03', '04', '05']
        row2 = ['06', '07', '08', '09', '10']
        row3 = ['11', '12', '13']
        row4 = ['14', '15', '16']
        self.table = {'row1':row1, 'row2':row2, 'row3':row3, 'row4':row4}
        self.discard = ['17', '18', '19', '20']


    def checkErrorMove(self, move):
        '''if the input is invalid, return False'''
        if move not in self.availableList:
            return False
        return True

    def processUserMove(self, move, deal):
        '''place the card in table/discard
        and remove the corresponding index from availableList'''
        index = int(move)
        self.availableList.remove(move)
        lst = combineList(deal, self.table, self.discard)
        lst.remove(lst[index])
        lst.insert(index, deal)
        self.table, self.discard = splitList(lst)

    def acceptUserMove(self, move, deal):
        '''calls the previous 2 functions'''
        while self.checkErrorMove(move) == False:
            move = raw_input('select an available number to place your card: ')
            self.checkErrorMove(move)
        self.processUserMove(move, deal)

    def play(self):
        '''play the game in following steps:
        (deal card, check availiability, place card)*n and score the table'''
        #display('NA', self.table, self.discard)
        print "Welcome to SolBlackJack Game!\nH->Heart S->Spade D->Diamond C->Club"
        self.deck.shuffle()
        #if the table are not fully filled, loop to play
        while self.availableList != [] and int(self.availableList[0])<17:
            deal = self.deck.deal()
            display(deal, self.table, self.discard)
            move = raw_input('Where would you place the card? ')
            self.acceptUserMove(move, deal)
        #scores the table
        display('NA', self.table, self.discard)
        finalScore = scoreTable(self.table)
        print "=======================\nYour final score is "+ str(finalScore)
        isHighScore(finalScore, 'highScore.txt')
        
    def _str_(self):
        print 'Zhou and Guanqing'
        
def main():
    '''play the game and ask whether the user wants to restart'''
    restartGame = 'y'
    while restartGame != 'n':
        if restartGame != 'y':
            restartGame = raw_input('Restart the game? y/n ')
        else:
            bj_solitaire = BlackJack()
            bj_solitaire.play()
            restartGame = raw_input('Restart the game? y/n ')


if __name__ == "__main__": main()





