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

print(actor_query_key_word('scott huang'))