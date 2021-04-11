'''This Program handles all SQL query to the database.'''

''' Queries all key_words '''
def query_key_word(query_name, key_words):
    keys = key_words.split(' ')
    match = ''
    for key in keys:
        key = '%%'+key+'%%'
        match += "{0} LIKE \"{1}\" and ".format(query_name, key)
    
    # remove the last and
    return match[:-5]

''' Actor Functions '''
def actor_query_recommand1():
    return """
            Select Actor_Name, Birth_Year, avg(mr.Rating) as AvgRating
            From Actors as a Natural Join Acted_in Natural Join Movies as m Join MovieRating as mr on m.MovieId = mr.MovieId
            Group BY ActorId
            Having count(m.MovieId) >= 2
            Order By AvgRating Desc, Actor_Name
            Limit 15;
           """

def actor_query_key_word(key_words):
    match = query_key_word('Actor_Name', key_words)
    return f"""
            Select Actor_Name, Birth_Year
            From Actors
            Where {match}
            Limit 15;
            """

''' Director Functions'''
def director_query_recommand1():
    return f"""
            SELECT d.DirectorId, Director_name as name, Birth_Year, Death_Year, Count(Title) as movie_count
            FROM (Directors d LEFT JOIN Directed_by db ON d.DirectorId = db.DirectorId) LEFT JOIN Movies m ON db.MovieId = m.MovieId
            WHERE d.Birth_Year < 1970 and d.Birth_Year > 1950
            GROUP BY d.DirectorId
            
            UNION
            
            SELECT d.DirectorId, Director_name as name, Birth_Year, Death_Year, Count(Title) as movie_count
            FROM (Directors d LEFT JOIN Directed_by db ON d.DirectorId = db.DirectorId) LEFT JOIN Movies m ON db.MovieId = m.MovieId
            WHERE m.Publication_Year > 1990 and m.Publication_Year < 2000
            GROUP BY d.DirectorId
            
            LIMIT 15;
            """
def director_query_key_word(key_words):
    match = query_key_word('Director_name', key_words)
    return f"""
            Select *
            From Directors
            Where {match}
            Limit 15;
            """
def delete_director_query_recommand1(director_id):
    return f"""
            DELETE FROM Directors
            WHERE {director_id} = DirectorId;
            """

def get_max_DirectorId():
    return f"""
            SELECT MAX(DirectorId)
            FROM Directors;
            """

def insert_DirectorId(new_director_id, director_dict):
    name = director_dict['director_name']
    birth_year = director_dict['birth_year']
    death_year = director_dict['death_year']
    return f"""
            INSERT INTO Directors(DirectorId, Director_name, Birth_Year, Death_Year)
            Values ({new_director_id}, "{name}", {birth_year}, {death_year});
            """

def update_DirectorId(director_id, director_dict):
    name = director_dict['director_name']
    birth_year = director_dict['birth_year']
    death_year = director_dict['death_year']
    return f"""
            UPDATE Directors
            SET Director_name = "{name}", Birth_Year = {birth_year}, Death_Year = {death_year}
            Where DirectorId = {director_id};
            """ 

def get_director_info(director_id):
    return f"""
            Select *
            From Directors
            Where DirectorId = {director_id};
            """

''' Movie Functions '''
def movie_query_recommand1():
    return f"""
            (Select m.MovieId, m.Title, m.Genre, m.Language, m.Publication_Year, m.Runtime, avg(r.Rating) as rating
            From Movies m Left Join Reviews r ON m.MovieId = r.MovieId
            Where (m.Publication_Year > 2000 and m.Publication_Year < 2010)
            Group By m.MovieId, m.Title, m.Genre, m.Language, m.Publication_Year, m.Runtime
            Having rating > 8.0
            Order By rating DESC)

            UNION

            (Select m.MovieId, m.Title, m.Genre, m.Language, m.Publication_Year, m.Runtime, avg(r.Rating) as rating
            From Movies m Left Join Reviews r ON m.MovieId = r.MovieId
            Where m.Title like "A%%"
            Group By m.MovieId, m.Title, m.Genre, m.Language, m.Publication_Year, m.Runtime
            Having rating > 8.0
            Order By rating DESC)
            Limit 15;
            """

def movie_query_recommand2():
    return f"""
            SELECT DISTINCT M.MovieId,M.Title, M.Genre, M.Language, M.Publication_Year, M.Runtime, count(A.ActorId)
            From (Movies M LEFT JOIN Acted_in I ON M.MovieId = I.MovieId) LEFT JOIN Actors A ON
            I.ActorId = A.ActorId
            WHERE A.Death_Year <> 0 and A.Birth_Year > 1920 and A.Death_Year < 1980 and A.Most_Known_Titles NOT Between "tt0045103" and "tt0046103"
            Group By M.MovieId, Birth_Year
            ORDER BY count(A.ActorId) DESC
            LIMIT 15;
            """

def movie_query_key_word(key_words):
    match = query_key_word('Title', key_words)
    return f"""
            Select *
            From Movies
            Where {match}
            Limit 15;
            """

def delete_movie_query_recommand1(MovieId):
    return f"""
            DELETE FROM Movies
            WHERE {MovieId} = MovieId;
            """

def get_max_MovieId():
    return f"""
            SELECT MAX(MovieId)
            FROM Movies;
            """

def insert_MovieId(new_movie_id, movie_dict):
    title = movie_dict['title']
    genre = movie_dict['genre']
    language = movie_dict['language']
    pub_year = movie_dict['pub_year']
    run_time = movie_dict['runtime']
    return f"""
            INSERT INTO Movies(MovieId, Title, Genre, Language, Publication_Year, Runtime)
            Values ({new_movie_id}, "{title}", "{genre}", "{language}", {pub_year}, {run_time});
            """

def update_MovieId(movie_id, movie_dict):
    title = movie_dict['title']
    genre = movie_dict['genre']
    language = movie_dict['language']
    pub_year = movie_dict['pub_year']
    run_time = movie_dict['runtime']
    return f"""
            UPDATE Movies
            SET Title = "{title}", Genre = "{genre}", Language = "{language}", Publication_Year = {pub_year}, Runtime = {run_time}
            Where MovieId = {movie_id};
            """ 

def get_movie_info(movie_id):
    return f"""
            Select *
            From Movies
            Where MovieId = {movie_id};
            """