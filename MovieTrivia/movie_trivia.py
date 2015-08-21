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
        if actor not in movieInfo.keys():
            movieInfo[actor] = set([])
        movies = actorAndMovies[1:]
        cleaned_movies = []
        for movie in movies:
            cleaned_movies.append(movie.strip())
        movieInfo[actor] =  movieInfo.get(actor).union(set(cleaned_movies))

    f.close()
    return movieInfo

def create_ratings_DB(ratings_file):
    '''make a dictionary from the rotten tomatoes csv file'''
    scores_dict = {}
    with open(ratings_file, 'r') as csvfile:
        reader = csv.reader(csvfile)
        reader.next()
        for row in reader:
            scores_dict[row[0]] = [row[1], row[2]]
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
            if is_critic == True and int(ratings_DB[movie][0]) > targeted_rating:
                movieList.append(movie)
            elif is_critic == False and int(ratings_DB[movie][1]) > targeted_rating:
                movieList.append(movie)
            else:
                pass
        elif comparison == '<':
            if is_critic == True and int(ratings_DB[movie][0]) < targeted_rating:
                movieList.append(movie)
            elif is_critic == False and int(ratings_DB[movie][1]) < targeted_rating:
                movieList.append(movie)
            else:
                pass
        elif comparison == '=':
            if is_critic == True and int(ratings_DB[movie][0]) == targeted_rating:
                movieList.append(movie)
            elif is_critic == False and int(ratings_DB[movie][1]) == targeted_rating:
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
        ratingSum = 0
        count = 0
        for movie in movie_DB[actor]:
            if movie in ratings_DB.keys():
                ratingSum += int(ratings_DB[movie][0])
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
            if movie in ratings_DB.keys():
                ratingSum += int(ratings_DB[movie][1])
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
    secondList = movie_DB.keys()
    length = len(secondList)
    secondList.remove('Kevin Bacon')
    firstList = ['Kevin Bacon']
    while (actor not in firstList) and (baconNumber < length):
        baconNumber += 1
        actorList = []
        for actor1 in firstList:
            for actor2 in secondList:
                if get_common_movie(actor1, actor2, movie_DB) != []:
                    actorList.append(actor2)
                    secondList.remove(actor2)
        firstList = actorList
    if baconNumber == length:
        return 'inf'
    else:
        return str(baconNumber)

# ========= additional functions ===========
def name_converter(string):
    # capitalize every word in the string
    string = capwords(string)
    return string
    
def rating_range_judgement(string):
    # see if the ratings entered are numbers between 0~100
    judgeNum = True
    judgeRange = True
    stringLen = len(string)           
    i = 0
    for i in range(stringLen):
        if string[i] not in ['1','2','3','4','5','6','7','8','9','0']:
            judgeNum = False
    if judgeNum == True:
        if (int(string) not in range(101)):
            judgeRange = False
    return (judgeNum and judgeRange)


# ========= Main function =========== 
def main():
    movie_DB = create_movie_DB('movies.txt')
    ratings_DB = create_ratings_DB('moviescores.csv')

    menu = '''
=========== MAIN MENU OF MOVIE TRIVIA ===========
1. Given an actor's name, find all the actors with whom he/she has acted
2. Find out the movies in which both actors are present
3. Actor(s) with the highest avg critic rating score
4. Actor(s) with the highest avg audience rating score
5. Good movies(both critic and audience scores above 85)
6. Find all the actors that acted in a pair of movies
7. Get an actor's Bacon number

8.  Update actor/movies info
9.  Update movie/ratings info
10. Delete all the info that corresponds to a movie
11. View the list of all movies an actor acted in
12. View the list of actors that acted in a movie
13. Movie filter
14. Quit

What would you like to do? '''

    shouldContinue = ''
    menuSelection = ''
    while shouldContinue != 'n':
        menuSelection = raw_input(menu)
        
        while menuSelection not in ['1','2','3','4','5','6','7','8','9','10','11','12','13','14']:
             menuSelection = raw_input('Error! Please enter a number between 1 and 14: ')
             
        if menuSelection == '1':
            actor = raw_input("\n1. Given an actor's name, find all the actors with whom he/she has acted\nActor's name: ")
            actor = name_converter(actor)
            if actor not in movie_DB.keys():
                print 'Sorry,', actor, 'is not in our database.'
            else:
                movieList = get_co_actors(actor, movie_DB)
                print "The movie", actor, "has acted in are listed as below:"
                for movie in movieList:
                    print ' ',movie
            shouldContinue = raw_input('continue? (y/n) ')

        elif menuSelection == '2':
            actor1 = raw_input("\n2. Find out the movies in which both actors are present\nActor1's name: ")
            actor2 = raw_input("Actor2's name: ")
            actor1 = name_converter(actor1)
            actor2 = name_converter(actor2)
            if actor1 not in movie_DB.keys():
                print 'Sorry,', actor1, 'is not in our database.'
            elif actor2 not in movie_DB.keys():
                print 'Sorry,', actor2, 'is not in our database.'
            else:
                movieList = get_common_movie(actor1, actor2, movie_DB)
                if movieList != []:
                    print "Their common movies are listed as below:"
                    for movie in movieList:
                        print ' ',movie
                else:
                    print "They have no common movie"
            shouldContinue = raw_input('continue? (y/n) ')
            
        elif menuSelection == '3':
            actorList = critics_darling(movie_DB, ratings_DB)
            print "\n3. Actor(s) with the highest avg critic rating score:"
            for actor in actorList:
                    print ' ',actor            
            shouldContinue = raw_input('continue? (y/n) ')
            
        elif menuSelection == '4':
            actorList = audience_darling(movie_DB, ratings_DB)
            print "\n4. Actor(s) with the highest avg audience rating score:"
            for actor in actorList:
                    print ' ',actor    
            shouldContinue = raw_input('continue? (y/n) ')
            
        elif menuSelection == '5':
            movieList = good_movies(ratings_DB)
            print "\n5. Good movies (both critic and audience scores above 85) are listed as below:"
            for movie in movieList:
                    print ' ',movie
            shouldContinue = raw_input('continue? (y/n) ')
            
        elif menuSelection == '6':
            movie1 = raw_input("\n6. Find all the actors that acted in a pair of movies\nMovie1 name: ")
            movie2 = raw_input("Movie2 name: ")
            movie1 = name_converter(movie1)
            movie2 = name_converter(movie2)
            exist1 = False
            exist2 = False
            for actor in movie_DB.keys():
                for movie in movie_DB[actor]:
                    if movie1 == name_converter(movie):
                        movie1 = movie
                        exist2 = True
                    if movie2 == name_converter(movie):
                        movie2 = movie
                        exist2 = True                    
            if exist1 == False:
                print 'Sorry,', movie1, 'is not in our database.'
            elif exist2 == False:
                print 'Sorry,', movie2, 'is not in our database.'
            else:
                actorList = get_common_actors(movie1, movie2, movie_DB)
                print "Their common movies are listed as below:"
                for actor in actorList:
                    print ' ',actor
            shouldContinue = raw_input('continue? (y/n) ')
            
        elif menuSelection == '7':
            actor = raw_input("\n7. Get an actor's Bacon number\nActor's name: ")
            actor = name_converter(actor)
            if actor not in movie_DB.keys():
                print 'Sorry,', actor, 'is not in our database.'
            else:
                baconNumber = get_bacon(actor, movie_DB)
                print str(actor)+"'s Bacon number is", baconNumber
            shouldContinue = raw_input('continue? (y/n) ')
 
        # update actor/movies to movie_DB
        elif menuSelection == '8':
            actor = raw_input("\n8. Update actor/movies info\nActor's name: ")
            actor = name_converter(actor)
            movies = set([])
            newMovie = raw_input('New movie: ')
            newMovie = name_converter(newMovie)
            movies.add(newMovie)
            while newMovie != '<>':
                newMovie = raw_input("Other new movies(enter '<>' to stop): ")
                newMovie = name_converter(newMovie)
                movies.add(newMovie)
            insert_actor_info(actor, movies , movie_DB)
            shouldContinue = raw_input('continue? (y/n) ')

        # update movie/ratings to ratings_DB
        elif menuSelection == '9':
            newMovie = raw_input("\n9. Update movie/ratings info\nMovie name: ")
            newMovie = name_converter(newMovie)
            for actor in movie_DB.keys():
                for movie in movie_DB[actor]:
                    if newMovie == name_converter(movie):
                        newMovie = movie
                        
            criRating = raw_input('Critics rating score for the movie: ')
            criJudge = rating_range_judgement(criRating)
            while criJudge == False:
                criRating = raw_input("Please enter a score between 0~100: ")
                criJudge = rating_range_judgement(criRating)
                
            audRating = raw_input('Audience rating score for the movie: ')
            audJudge = rating_range_judgement(audRating)
            while audJudge == False:
                audRating = raw_input("Please enter a score between 0~100: ")
                audJudge = rating_range_judgement(audRating)

            ratings = [criRating, audRating]
            insert_rating(newMovie, ratings, ratings_DB)
            shouldContinue = raw_input('continue? (y/n) ')

        elif menuSelection == '10':
            delMovie = raw_input("\n10. Delete all the info that corresponds to a movie\nMovie name: ")
            delMovie = name_converter(delMovie)
            exist = False
            for actor in movie_DB.keys():
                for movie in movie_DB[actor]:
                    if delMovie == name_converter(movie):
                        delMovie = movie
                        exist = True
            if exist == True:
                delete_movie(delMovie, movie_DB, ratings_DB)
            else:
                print "Sorry,", delMovie, "doesn't exist in our database."
            shouldContinue = raw_input('continue? (y/n) ')

        elif menuSelection == '11':
            #11. View the list of all movies an actor acted in
            actor = raw_input("\n11. View the list of all movies an actor acted in\nActor's name: ")
            actor = name_converter(actor)
            if actor not in movie_DB.keys():
                print 'Sorry,', actor, 'is not in our database.'
            else:
                movieList = select_where_actor_is(actor, movie_DB)
                print actor, "has acted in these movies:"
                for movie in movieList:
                    print ' ', movie
            shouldContinue = raw_input('continue? (y/n) ')

        elif menuSelection == '12':
            movie = raw_input("\n12. View the list of actors that acted in a movie\nMovie name: ")
            movie = name_converter(movie)
            exist = False
            for actor in movie_DB.keys():
                for movies in movie_DB[actor]:
                    if movie == name_converter(movies):
                        movie = movies
                        exist = True
            if exist:
                actorList = select_where_movie_is(movie, movie_DB)
                print "The actors acted in", movie, "are listed as below:"
                for actor in actorList:
                    print ' ',actor
            else:
                print 'Sorry,', movie, 'is not in our database.'
            shouldContinue = raw_input('continue? (y/n) ')

        elif menuSelection == '13':
            print "\n13. Movie filter"
            CriOrAud = raw_input("Do you want to use critic scores(enter 'c') or audience scores(enter 'a')? ")
            judge1 = (CriOrAud == 'c') or (CriOrAud == 'a')
            while judge1 == False:
                CriOrAud = raw_input("Please enter 'c' for critic scores or 'a' for audience scores: ")
                judge1 = (CriOrAud == 'c') or (CriOrAud == 'a')
            isCritic = CriOrAud == 'c'
                                 
            targetRating = raw_input("Please enter the targeted rating score(0~100): ")
            judge2 = rating_range_judgement(targetRating)
            while judge2 == False:
                targetRating = raw_input("Please enter a score between 0~100): ")
                judge2 = rating_range_judgement(targetRating)
                
            comparison = raw_input("Want the scores to be higher than('>'), lower than('<'), or equal to('=') your target score: ")
            judge3 = comparison in ['>', '<', '=']
            while judge3 == False:
                comparison = raw_input("Please enter '>', '<', or '=': ")
                judge3 = comparison in ['>', '<', '=']

            targetRating = int(targetRating)
            movieList = select_where_rating_is(targetRating, comparison, isCritic, ratings_DB)
            print 'Movies with scores', comparison, targetRating, 'are listed as below:'
            for movie in movieList:
                print ' ', movie 
            shouldContinue = raw_input('continue? (y/n) ')

        else:
            shouldContinue = 'n'

    
if __name__ == '__main__':
    main()
