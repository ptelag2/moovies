from flask import Flask, request, abort, jsonify, render_template
import os
import sqlalchemy
from yaml import load, Loader

def init_connect_engine():
    if os.environ.get('GAE_ENV') != 'standard':
        variables = load(open("app.yaml"), Loader=Loader)
        env_variables = variables['env_variables']
        for var in env_variables:
            os.environ[var] = env_variables[var]
            pool = sqlalchemy.create_engine(
            sqlalchemy.engine.url.URL(
            drivername="mysql+pymysql",
            username=os.environ.get('MYSQL_USER'), #username
            password=os.environ.get('MYSQL_PASSWORD'), #user password
            database=os.environ.get('MYSQL_DB'), #database name
            host=os.environ.get('MYSQL_HOST') #ip
            )
        )
    return pool

GET = 'GET'
PUT = 'PUT'
POST = 'POST'
DELETE = 'DELETE'

app = Flask(__name__)

@app.route('/')
def homepage():
    return render_template('index.html')

@app.route('/movies/', methods=[GET, PUT, POST, DELETE])
def moviepage():
    fake_movie = [{'MovieId': 3532, 'Title': 'My Moovie', 'Runtime': 215,
                  'Publication_Year': 2022, 'Genre': 'Adult', 'Language': 'English'}]
    movie_id = request.args.get('id', default = -1, type = int)
    if movie_id != -1:
        return render_template('movies.html', movie_infos=fake_movie)
    
    recommand = request.args.get('recommand', default = False, type = bool)
    if recommand:
        return render_template('movies.html', movie_infos=fake_movie+fake_movie+fake_movie)
    
    abort(404)

@app.route('/actors/', methods=[GET, PUT, POST, DELETE])
def actorpage():
    fake_actor = [{'ActorId': 53314, 'Actor_Name': 'My Actor', 'Birth_Year': 2077,
                   'Most_Known_Titles': 'Aha'}]
    actor_id = request.args.get('id', default = -1, type = int)
    if actor_id != -1:
        return render_template('actors.html', actor_infos=fake_actor)
    
    recommand = request.args.get('recommand', default = False, type = bool)
    if recommand:
        return render_template('actors.html', actor_infos=fake_actor+fake_actor+fake_actor)
    
    abort(404)

@app.route('/directors/', methods=[GET, PUT, POST, DELETE])
def directorpage():
    fake_director = [{'DirectorId': 321685, 'Director_name': 'My Director', 'Birth_Year': 1344,
                      'Award': None}]
    director_id = request.args.get('id', default = -1, type = int)
    if director_id != -1:
        return render_template('directors.html', director_infos=fake_director)
    
    recommand = request.args.get('recommand', default = False, type = bool)
    if recommand:
        return render_template('directors.html', director_infos=fake_director+fake_director)
    
    abort(404)

@app.route('/reviews/', methods=[GET, PUT, POST, DELETE])
def reviewpage():
    fake_review = [{'ReviewId': 5644564, 'UserId': 654684768, 'MovieId': 659,
                      'Comment': 'I like this movie', 'Rating':5}]
    movie_id = request.args.get('movie_id', default = -1, type = int)
    if movie_id != -1:
        return render_template('review.html', review_infos=fake_review+fake_review)
    
    abort(404)

if __name__ == '__main__':
    app.run(port=5000, debug=True)
    '''
    import model.database as mydb
    print('start')
    db_conn = init_connect_engine().connect()
    mydb.test(db_conn)
    db_conn.close()
    print('end')
    '''

