#create the databases
from string import capwords
import csv

def create_movie_DB(actor_file):
    '''Create a dictionary keyed on actors from a text file'''
    f = open(actor_file)
    movieInfo = {}
    for line in f:
        line = line.rstrip().lstrip()
        actorAndMovies = line.split(',')
        actor = actorAndMovies[0]
        movies = [x.lstrip().rstrip() for x in actorAndMovies[1:]]
        movieInfo[actor] = set(movies)
    f.close()
    return movieInfo

def create_ratings_DB(ratings_file):
    '''make a dictionary from the rotten tomatoes csv file'''
    scores_dict = {}
    with open(ratings_file, 'r') as csvfile:
        reader = csv.reader(csvfile)
        reader.next()
        for row in reader:
            scores_dict[row[0]] = (eval(row[1]), eval(row[2]))
    return scores_dict

# ========= Utility functions ===========
def insert_actor_info(actor, movies, movie_DB):
    '''update the movie_DB.
    If the actor already exists, add the new movies to his/her movie set.'''
    if actor in movie_DB.keys():
        newMovies = movie_DB[actor]
        newMovies.update(movies)
        movie_DB[actor] = newMovies
    else:
        movie_DB[actor] = movies

def insert_rating(movie, ratings, ratings_DB):
    '''update the ratings_DB.
    If the movie exists, replace its ratings with the new ones.'''
    ratings_DB[movie] = ratings

def delete_movie(movie, movie_DB, ratings_DB):
    '''delete all information that corresponds to this movie.'''
    for actor in movie_DB.keys():
        if movie in movie_DB[actor]:
            newMovies = movie_DB[actor]
            newMovies.remove(movie)
            movie_DB[actor] = newMovies
    for element in ratings_DB.keys():
        if movie == element:
            del ratings_DB[movie]

def select_where_actor_is(actorName, movie_DB):
    '''given an actor, return the list of all movies'''
    return list(movie_DB[actorName])

def select_where_movie_is(movieName, movie_DB):
    '''given a movie, return the list of all actors'''
    actorList = []
    for actor in movie_DB.keys():
        if movieName in movie_DB[actor]:
            actorList.append(actor)
    return actorList


def select_where_rating_is(targeted_rating, comparison, is_critic, ratings_DB):
    '''returns a list of movies that satisfy certain conditions'''
    movieList = []
    for movie in ratings_DB.keys():
        if comparison == '>':
            if is_critic == True and ratings_DB[movie][0] > targeted_rating:
                movieList.append(movie)
            elif is_critic == False and ratings_DB[movie][1] > targeted_rating:
                movieList.append(movie)
            else:
                pass
        elif comparison == '<':
            if is_critic == True and ratings_DB[movie][0] < targeted_rating:
                movieList.append(movie)
            elif is_critic == False and ratings_DB[movie][1] < targeted_rating:
                movieList.append(movie)
            else:
                pass
        elif comparison == '=':
            if is_critic == True and ratings_DB[movie][0] == targeted_rating:
                movieList.append(movie)
            elif is_critic == False and ratings_DB[movie][1] == targeted_rating:
                movieList.append(movie)
            else:
                pass
    return movieList

# ========= User questions ===========
def get_co_actors(actorName, movie_DB):
    '''returns list of all actors that the actor has ever worked with in any movie'''
    movieList = list(movie_DB[actorName])
    actorList = []
    for actor in movie_DB.keys():
        for movie in movie_DB[actor]:
            if movie in movieList:
                actorList.append(actor)
    actorList = list(set(actorList))
    actorList.remove(actorName)
    return actorList

def get_common_movie(actor1, actor2, movie_DB):
    movies1 = movie_DB[actor1]
    movies2 = movie_DB[actor2]
    commonMovies = list(movies1.intersection(movies2))
    return commonMovies

def critics_darling(movie_DB, ratings_DB):
    '''find the actors with the highest avg ratings, as per the critics.'''
    #first make a dictionary for actors and their avg ratings
    actorRating = {}
    for actor in movie_DB.keys():
        ratingSum= 0
        count = 0
        for movie in movie_DB[actor]:
            ratingSum += ratings_DB[movie][0]
            count += 1
        avgRating = ratingSum / count
        actorRating[actor] = avgRating
    #then make a list of the darlings    
    topRating = max(actorRating.values())
    darlingList = []
    for actor in actorRating:
        if actorRating[actor] == topRating:
            darlingList.append(actor)
    return darlingList

def audience_darling(movie_DB, ratings_DB):
    '''find the actors with the highest avg ratings, as per the audience.'''
    #first create a dictionary for actors and their movies' avg ratings
    actorRating = {}
    for actor in movie_DB.keys():
        ratingSum= 0
        count = 0
        for movie in movie_DB[actor]:
            ratingSum += ratings_DB[movie][1]
            count += 1
        avgRating = ratingSum / count
        actorRating[actor] = avgRating
    #then make a list of the darlings
    topRating = max(actorRating.values())
    darlingList = []
    for actor in actorRating:
        if actorRating[actor] == topRating:
            darlingList.append(actor)
    return darlingList

def good_movies(ratings_DB):
    '''returns the set of movies that both critics and the audience have rated above 85'''
    criGoodMovies = set(select_where_rating_is(84, '>', True, ratings_DB))
    audGoodMovies = set(select_where_rating_is(84, '>', False, ratings_DB))
    goodMovies = criGoodMovies.intersection(audGoodMovies)
    return goodMovies

def get_common_actors(movie1, movie2, movie_DB):
    '''return a list of actors who acted in both movies
    first create two sets with actors who acted in each movie
    then intersect two sets to get the list'''
    commonActors = []
    for actor in movie_DB.keys():
        if (movie1 in movie_DB[actor]) and (movie2 in movie_DB[actor]):
            commonActors.append(actor)
    return commonActors

def get_bacon(actor, movie_DB):
    '''get the bacon number'''
    baconNumber = 0
    fullList = movie_DB.keys()
    length = len(fullList)
    fullList.remove('Kevin Bacon')
    actorList = ['Kevin Bacon']
    while (actor not in actorList) and (baconNumber < length):
        baconNumber += 1
        actorList2 = []
        for actor1 in actorList:
            for actor2 in fullList:
                if get_common_movie(actor1, actor2, movie_DB) != []:
                    actorList2.append(actor2)
                    fullList.remove(actor2)
        actorList = actorList2
    if baconNumber == length:
        return 'no connection'
    else:
        return baconNumber

def name_converter(string):
    string = capwords(string)
    return string
        

# ========= Main function =========== 
def main():
    movie_DB = create_movie_DB('my_test_actors.txt')
    ratings_DB = create_ratings_DB('my_ratings.csv')

    # ask if user wants to add new actor/movies to movie_DB
    insertActorInfo = raw_input('Add new actor/movies?(y/n) ')
    newMovie = ''
    while insertActorInfo != 'n' and newMovie != 'done':
        if insertActorInfo == 'y':
            actor = raw_input('actor/actress\'s name:')
            movies = set([])
            newMovie = raw_input('new movie(type done to stop):')
            while newMovie != 'done':
                movies.add(newMovie)
                newMovie = raw_input('other new movies(type done to stop):')
            insert_actor_info(actor, movies , movie_DB)
            print movie_DB
        else:
            insertActorInfo = raw_input('Add new actor/movies?(y/n) ')

    insert_rating('wtf', (5, 666), ratings_DB)
    print ratings_DB
    print movie_DB.keys()

    print select_where_rating_is(85, '>', False, ratings_DB)
    print movie_DB['Brad Pitt']
    
if __name__ == '__main__':
    main()
