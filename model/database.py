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
        d['Actor_Name'] = result[0]
        d['Birth_Year'] = result[1]
        d['Most_Known_Titles'] = result[2]
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
        d['Actor_Name'] = result[0]
        d['Birth_Year'] = result[1]
        d['Most_Known_Titles'] = result[2]
        l.append(d)
    return l

def get_director_recommand1(db_connection):
    results = db_connection.execute(q.director_query_recommand1())
    return results

def get_director_key_word(db_connection):
    pass

def get_movie_recommand1(db_connection):
    pass

def get_movie_key_word(db_connection):
    pass

def get_review_key_word(db_connection):
    pass

'''Delete, return a msg whether delete succeeded'''
def delete_actor(actor_id, db_connection):
    pass

def delete_director(director_id, db_connection):
    results = db_connection.execute(q.delete_director_query_recommand1(director_id))
    return results

def delete_movie(movie_id, db_connection):
    pass

def delete_review(review_id, db_connection):
    pass

'''Upload (both Put and Post), return a msg whether upload succeeded'''
def upload_actor(actor_id, db_connection):
    if actor_id < 0: # insert a new actor
        pass
    pass

def upload_director(director_id, director_dict, db_connection):
    print(director_id)
    director_id = int(director_id)
    if director_id < 0: # insert a new director
        max_id = db_connection.execute(q.get_max_DirectorId())
        new_id = -1
        # print(type(max_id))
        for data in max_id:
            new_id = 1 + data[0]
        result = db_connection.execute(q.insert_DirectorId(new_id, director_dict))
        return director_dict['director_name'] + " has been added to the Directors table with Director ID " + str(new_id)
    # update director
    if director_id >= 0:
        result = db_connection.execute(q.update_DirectorId(director_id, director_dict))
        return result
    pass

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
    

def upload_movie(movie_id, db_connection):
    if movie_id < 0: # insert a new movie
        pass
    pass

def upload_review(review_id, db_connection):
    if review_id < 0: # insert a new review
        pass
    pass
