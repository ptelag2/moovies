'''This Program handles all SQL query to the database.'''

def actor_query_recommand1():
    return """
            Select Actor_Name, Birth_Year, Most_Known_Titles, avg(mr.Rating) as AvgRating
            From Actors as a Natural Join Acted_in Natural Join Movies as m Join MovieRating as mr on m.MovieId = mr.MovieId
            Group BY ActorId
            Having count(m.MovieId) >= 2
            Order By AvgRating Desc, Director_name
            Limit 15;
           """

def query_key_word(query_name, key_words):
    keys = key_words.split(' ')
    match = ''
    for key in keys:
        match += f"{query_name} LIKE '%{key}%' and "
    
    # remove the last and
    return match[:-5]

def actor_query_key_word(key_words):
    match = query_key_word('Actor_Name', key_words)
    return f"""
            Select Actor_Name, Birth_Year, Most_Known_Titles
            From Actors
            Where {match}
            Limit 15;
            """

def director_query_recommand1():
    return f"""
            SELECT Director_name as name, Count(Title) as movie_count
            FROM (Directors d LEFT JOIN Directed_by db ON d.DirectorId = db.DirectorId) LEFT JOIN Movies m ON db.MovieId = m.MovieId
            WHERE d.Birth_Year < 1970 and d.Birth_Year > 1950
            GROUP BY Director_name
            
            UNION
            
            SELECT Director_name as name, Count(Title) as movie_count
            FROM (Directors d LEFT JOIN Directed_by db ON d.DirectorId = db.DirectorId) LEFT JOIN Movies m ON db.MovieId = m.MovieId
            WHERE m.Publication_Year > 1990 and m.Publication_Year < 2000
            GROUP BY Director_name
            
            LIMIT 15;
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
    print(type(name))
    print(name)
    print("name")
    birth_year = director_dict['birth_year']
    death_year = director_dict['death_year']
    return f"""
            INSERT INTO Directors(DirectorId, Director_name, Birth_Year, Death_Year)
            Values ({new_director_id}, "{name}", {birth_year}, {death_year});
            """
print(actor_query_key_word('scott huang'))