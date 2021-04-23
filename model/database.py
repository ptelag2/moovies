'''This program is responsible load and format query result.'''

import model.query as q

def get_result(query, db_connection):
    '''Make a query and get the response from the sql database.

    Arguments:
        query: The query msg.
        db_connection: Database connection.
    Returns:
        The response from the database in a list.
    '''

    results = db_connection.execute(query)
    return results

'''
You should implement your backend code here and in model.py.
Look at the example use of model.database in app.py to debug.
I will soon write some documentation in app.py to specify some expected behavior of each call.
'''

'''Get, return a list of dict'''
def get_actor_recommand1(db_connection):
    results = get_result(q.actor_query_recommand1(), db_connection)
    l = []
    for result in results:
        d = {}
        d['ActorId'] = result[0]
        d['Actor_Name'] = result[1]
        d['Birth_Year'] = result[2]
        d['Death_Year'] = result[3]
        l.append(d)
    return l

def get_actor_key_word(key_word, db_connection):
    query = q.actor_query_key_word(key_word)
    print(query)
    results = get_result(query, db_connection)
    print(results)
    l = []
    for result in results:
        d = {}
        d['ActorId'] = result[0]
        d['Actor_Name'] = result[1]
        d['Birth_Year'] = result[2]
        d['Death_Year'] = result[3]
        l.append(d)
    return l

def get_director_recommand1(db_connection):
    results = get_result(q.director_query_recommand1(), db_connection)
    l = []
    for result in results:
        d = {}
        d['DirectorId'] = result[0]
        d['Director_name'] = result[1]
        d['Birth_Year'] = result[2]
        d['Death_Year'] = result[3]
        l.append(d)
    return l

def get_director_key_word(key_word, db_connection):
    query = q.director_query_key_word(key_word)
    results = get_result(query, db_connection)
    print(results)
    l = []
    for result in results:
        d = {}
        d['DirectorId'] = result[0]
        d['Director_name'] = result[1]
        d['Birth_Year'] = result[2]
        d['Death_Year'] = result[3]
        l.append(d)
    return l

def get_movie_recommand1(db_connection):
    results = get_result(q.movie_query_recommand1(), db_connection)
    l = []
    for result in results:
        d = {}
        d['MovieId'] = result[0]
        d['Title'] = result[1]
        d['Genre'] = result[2]
        d['Language'] = result[3]
        d['Publication_Year'] = result[4]
        d['Runtime'] = result[5]
        l.append(d)
    return l

def get_movie_recommand2(db_connection):
    results = get_result(q.movie_query_recommand2(), db_connection)
    l = []
    for result in results:
        d = {}
        d['MovieId'] = result[0]
        d['Title'] = result[1]
        d['Genre'] = result[2]
        d['Language'] = result[3]
        d['Publication_Year'] = result[4]
        d['Runtime'] = result[5]
        l.append(d)
    return l

def get_movie_key_word(key_word, db_connection):
    query = q.movie_query_key_word(key_word)
    results = get_result(query, db_connection)
    l = []
    for result in results:
        d = {}
        d['MovieId'] = result[0]
        d['Title'] = result[1]
        d['Genre'] = result[2]
        d['Language'] = result[3]
        d['Publication_Year'] = result[4]
        d['Runtime'] = result[5]
        l.append(d)
    return l

def get_review_key_word(key_word, db_connection):
    query = q.review_query_key_word(key_word)
    results = get_result(query, db_connection)
    print(results)
    l = []
    for result in results:
        d = {}
        d['Comment'] = result[3]
        d['Rating'] = result[4]
        d['MovieId'] = result[2]
        d['ReviewId'] = result[0]
        d['UserId'] = result[1]
        l.append(d)
    return l

'''Delete, return a msg whether delete succeeded'''
def delete_actor(actor_id, db_connection):
    try:
        db_connection.execute(q.delete_actor_query_recommand1(actor_id))
        return 'Actor deleted :('
    except Exception: 
        return 'Unable to delete the actor'

def delete_director(director_id, db_connection):
    try:
        db_connection.execute(q.delete_director_query_recommand1(director_id))
        return 'Director deleted :('
    except Exception: 
        return 'Unable to delete the director'

def delete_movie(movie_id, db_connection):
    try:
        db_connection.execute(q.delete_movie_query_recommand1(movie_id))
        return 'Movie deleted :('
    except Exception: 
        return 'Unable to delete the movie'

def delete_review(review_id, db_connection):
    try:
        db_connection.execute(q.delete_review_query_recommand1(review_id))
        return 'Review deleted :('
    except Exception: 
        return 'Unable to delete the review'
    

'''Upload (both Put and Post), return a msg whether upload succeeded'''
def upload_actor(actor_id, actor_dict, db_connection):
    actor_id = int(actor_id)
    if actor_id < 0: # insert a new actor
        max_id = db_connection.execute(q.get_max_actor_id())
        new_id = -1
        for data in max_id:
            new_id = 1 + data[0]
        db_connection.execute(q.insert_actor(new_id, actor_dict))
        return actor_dict['actor_name'] + ' has been added to the database.'
    # update actor
    db_connection.execute(q.update_actor(actor_id, actor_dict))
    return 'Information updated'

def upload_director(director_id, director_dict, db_connection):
    director_id = int(director_id)
    if director_id < 0: # insert a new director
        max_id = db_connection.execute(q.get_max_director_id())
        new_id = -1
        for data in max_id:
            new_id = 1 + data[0]
        db_connection.execute(q.insert_director(new_id, director_dict))
        return director_dict['director_name'] + ' has been added to the database.'
    # update director
    db_connection.execute(q.update_director(director_id, director_dict))
    return 'Information updated'

def upload_movie(movie_id, movie_dict, db_connection):
    movie_id = int(movie_id)
    if movie_id < 0: # insert a new movie
        max_id = db_connection.execute(q.get_max_movie_id())
        new_id = -1
        for data in max_id:
            new_id = 1 + data[0]
        db_connection.execute(q.insert_movie(new_id, movie_dict))
        return movie_dict['title'] + ' has been added to the database'
    # update movie
    db_connection.execute(q.update_movie(movie_id, movie_dict))
    return 'Information updated'

def upload_review(review_id, user_id, review_dict, db_connection):
    review_id = int(review_id)
    if review_id < 0: # insert a new review
        max_id = db_connection.execute(q.get_max_review_id())
        new_id = -1
        for data in max_id:
            new_id = 1 + data[0]
        db_connection.execute(q.insert_review(new_id, user_id, review_dict))
        return "Your review has been posted."
    # update review
    db_connection.execute(q.update_review(review_id, review_dict))
    return 'Information updated'

'''Get Info'''
def get_actor_info(actor_id, db_connection):
    results = db_connection.execute(q.get_actor_info(actor_id))
    d = {}
    for result in results:
        d['ActorId'] = result[0]
        d['Actor_Name'] = result[1]
        d['Birth_Year'] = result[2]
        d['Death_Year'] = result[3]
        break
    return d

def get_director_info(director_id, db_connection):
    results = db_connection.execute(q.get_director_info(director_id))
    d = {}
    for result in results:
        d['DirectorId'] = result[0]
        d['Director_name'] = result[1]
        d['Birth_Year'] = result[2]
        d['Death_Year'] = result[3]
        break
    return d

def get_movie_info(movie_id, db_connection):
    results = db_connection.execute(q.get_movie_info(movie_id))
    d = {}
    for result in results:
        d['MovieId'] = result[0]
        d['Title'] = result[1]
        d['Genre'] = result[2]
        d['Language'] = result[3]
        d['Publication_Year'] = result[4]
        d['Runtime'] = result[5]
        break
    return d

def get_review_info(review_id, db_connection):
    results = db_connection.execute(q.get_review_info(review_id))
    d = {}
    for result in results:
        d['Comment'] = result[3]
        d['Rating'] = result[4]
        d['MovieId'] = result[2]
        d['ReviewId'] = result[0]
        d['UserId'] = result[1]
        break
    return d

def get_all_reviews(movie_id, db_connection):
    all_results = db_connection.execute(q.get_all_review_info(movie_id))
    l = []
    for result in all_results:
        d = {}
        d['Comment'] = result[3]
        d['Rating'] = result[4]
        d['MovieId'] = result[2]
        d['ReviewId'] = result[0]
        d['UserId'] = result[1]
        l.append(d)
    return l

'''Authentification.'''
def authenticate(username, password):
    return True

def get_user_id(username):
    return 2