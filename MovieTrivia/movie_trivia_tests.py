from movie_trivia import *
import unittest

class TestMovies(unittest.TestCase):

    movie_DB = {}
    ratings_DB = {}

    def setUp(self):
        self.movie_DB = create_movie_DB('my_test_actors.txt')
        self.ratings_DB = create_ratings_DB('my_ratings.csv')
        
    # ========= Utility functions ===========
    def test_insert_actor_info(self):
        insert_actor_info('Audrey Hepburn', set(['Roman Holiday', 'Sabrina']), self.movie_DB)
        condition1 = (self.movie_DB['Audrey Hepburn'] == set(['Roman Holiday', 'Sabrina']))
        self.assertTrue(condition1, 'insert new actor fail')

        insert_actor_info('Brad Pitt', set(['Test4', 'Test5']), self.movie_DB)
        condition2 = (self.movie_DB['Brad Pitt'] == set(['Sleepers', 'Troy', 'Test', 'Test2', 'Test4', 'Test5']))
        self.assertTrue(condition2, 'add movie to existing actor fail')

    def test_insert_rating(self):
        insert_rating('Test4', (2,3), self.ratings_DB)
        condition1 = (self.ratings_DB['Test4'] == (2,3))
        self.assertTrue(condition1, 'insert rating fail')
        
        insert_rating('Test3', (4,5), self.ratings_DB)
        condition2 = (self.ratings_DB['Test3'] == (4,5))
        self.assertTrue(condition2, 'replace rating fail')

    def test_delete_movie(self):
        delete_movie('Test', self.movie_DB, self.ratings_DB)
        condition1 = False
        condition2 = False
        #condition1 is True if the movie is still in the movie database
        for actor in self.movie_DB:
            if 'Test' in self.movie_DB[actor]:
                condition1 = True
        #condition2 is True if the movie is still in the ratings database        
        if 'Test' in self.ratings_DB.keys():
            condition2 = True          
        self.assertFalse((condition1 or condition2), 'delete_movie fail')
        
    def test_select_where_actor_is(self):
        movieList1 = select_where_actor_is('Brad Pitt', self.movie_DB)
        self.assertEqual(set(movieList1), set(['Sleepers', 'Troy', 'Test', 'Test2']), 'select where actor is fail 1')

        movieList2 = select_where_actor_is('Johnny Depp', self.movie_DB)
        self.assertEqual(movieList2, ['Test3'], 'select where actor is fail 2')
    
    def test_select_where_movie_is(self):
        actorList1 = select_where_movie_is('Test', self.movie_DB)
        self.assertEqual(set(actorList1), set(['Brad Pitt', 'Tom Hanks']), 'select where movie is fail 1')

        actorList2 = select_where_movie_is('Test4', self.movie_DB)
        self.assertEqual(actorList2, [], 'select where movie is fail 2')

 
    def test_select_where_rating_is(self):
        movieList1 = select_where_rating_is(85, '>', False, self.ratings_DB)
        self.assertEqual(set(movieList1), set(['Apollo 13', 'Test', 'Test2']), 'select where rating is fail 1')

        movieList2 = select_where_rating_is(55, '<', True, self.ratings_DB)
        self.assertEqual(set(movieList2), set(['Troy', 'Test3']), 'select where rating is fail 2')

        movieList3 = select_where_rating_is(74, '=', True, self.ratings_DB)
        self.assertEqual(movieList3, ['Sleepers'], 'select where rating is fail 3')
        
    # ========= User questions ===========
    def test_get_co_actors(self):
        actorList = get_co_actors('Brad Pitt', self.movie_DB)
        self.assertEqual(actorList, ['Tom Hanks', 'Kevin Bacon'], 'get co actors fail')

    def test_get_common_movie(self):
        commonMovies = get_common_movie('Brad Pitt', 'Tom Hanks', self.movie_DB)
        self.assertEqual(commonMovies, ['Test'], 'get common movie fail')

    def test_critics_darling(self):
        darlingList = critics_darling(self.movie_DB, self.ratings_DB)
        self.assertEqual(darlingList, ['Tom Hanks'], 'critics_darling fail')

    def test_audience_darling(self):
        darlingList = audience_darling(self.movie_DB, self.ratings_DB)
        self.assertEqual(darlingList, ['Kevin Bacon'], 'audience_darling fail')

    def test_good_movies(self):
        goodMovies = good_movies(self.ratings_DB)
        self.assertEqual(goodMovies, set(['Apollo 13', 'Test']), 'good Movies fail')

    def test_get_common_actors(self):
        commonActors = get_common_actors('Troy', 'Test', self.movie_DB)
        self.assertEqual(commonActors, ['Brad Pitt'], 'get common actors fail')

    def test_get_bacon(self):
        baconNumber = get_bacon('Kevin Bacon', self.movie_DB)
        self.assertEqual(baconNumber, '0', 'Kevin Bacon fail')

        baconNumber = get_bacon('Brad Pitt', self.movie_DB)
        self.assertEqual(baconNumber, '1', 'Brad Pitt fail')

        baconNumber = get_bacon('Johnny Depp', self.movie_DB)
        self.assertEqual(baconNumber, 'inf', 'no connection fail')

# ========= additional functions ===========        
    def test_name_converter(self):
        changed1 = name_converter('c. b. murray')
        self.assertEqual(changed1, 'C. B. Murray', 'fails to capitalize actor names')
        
        changed2 = name_converter("you've got mail")
        self.assertEqual(changed2, "You've Got Mail", 'fails to capitalize movie names')
        
    def test_rating_range_judgement(self):
        judge1 = rating_range_judgement('abc')
        self.assertFalse(judge1, 'rating range judgement fail')

        judge2 = rating_range_judgement('101')
        self.assertFalse(judge2, 'out of range judgement fail')

        
unittest.main()
