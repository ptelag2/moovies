from flask import Flask, request, abort, jsonify, render_template
import os
import sqlalchemy
from yaml import load, Loader
import model.database as mydb

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

# Initialize Google GCP databyse connection    
db_conn = init_connect_engine().connect()


GET = 'GET'
PUT = 'PUT'
POST = 'POST'
DELETE = 'DELETE'
EDIT = 'EDIT'
UPDATE = 'UPDATE'

app = Flask(__name__)

@app.route('/')
def homepage():
    return render_template('index.html')

@app.route('/movies/', methods=[GET, POST])
def moviepage():
    ''' This function handles the route /movies/ which accepts GET and POST calls.
    The POST call deals with uploading information of a new or existing movie.
    If the movie does not exist in the database,
    the uploaded json should contain movie_id = -1,
    you should insert a new movie with a generated id into the movies table.
    Otherwise, write the uploaded json into the existing attribute.


    '''
    if request.method == "POST":
        print(request.form['title']) # get example data
        return render_template('message.html', msg='post to movies')

    method = request.args.get('_method', default=None, type=str)
    if method == UPDATE:
        # no need to do anything
        return render_template('post_movie.html', movie_info={'MovieId': -1})

    fake_movie = [{'MovieId': 3532, 'Title': 'My Moovie', 'Runtime': 215,
                  'Publication_Year': 2022, 'Genre': 'Adult', 'Language': 'English'}]

    movie_id = request.args.get('id', default = -1, type = int)
    if movie_id != -1:
        if method == DELETE:
            # delete movie with movie_id
            return render_template('message.html', msg='movie deleted :(')
        if method == EDIT:
            # no need to do anything
            return render_template('post_movie.html', movie_info=fake_movie[0])
        return render_template('movies.html', movie_infos=fake_movie)
    
    recommand = request.args.get('recommand', default = False, type = bool)
    if recommand:
        # place for your advanced query
        rec_list = fake_movie+fake_movie+fake_movie
        return render_template('movies.html', movie_infos=rec_list)
    
    key_word = request.args.get('key_word', default=None, type=str)
    if key_word:
        # result for movies containing the key words
        search_result = fake_movie+fake_movie+fake_movie
        return render_template('movies.html', movie_infos=search_result)
    
    abort(404)

@app.route('/actors/', methods=[GET, POST])
def actorpage():
    if request.method == "POST":
        print(request.form['actor_name']) # get example data
        return render_template('message.html', msg='post to actors')
    method = request.args.get('_method', default=None, type=str)
    if method == UPDATE:
        return render_template('post_actor.html', actor_info={'ActorId': -1})

    fake_actor = [{'ActorId': 53314, 'Actor_Name': 'My Actor', 'Birth_Year': 2077,
                   'Most_Known_Titles': 'Aha'}]
    actor_id = request.args.get('id', default=-1, type=int)
    if actor_id != -1:
        if method == DELETE:
            return {'status': 'OK', 'delete': 'works'}
        if method == EDIT:
            return render_template('post_actor.html', actor_info=fake_actor[0])
        return render_template('actors.html', actor_infos=fake_actor)
    
    recommand = request.args.get('recommand', default=False, type=bool)
    if recommand:
        rec_actors = mydb.get_actor_recommand1(db_conn)
        return render_template('actors.html', actor_infos=rec_actors)
    
    key_word = request.args.get('key_word', default=None, type=str)
    if key_word:
        found_actors = mydb.get_actor_key_word(key_word, db_conn)
        if len(found_actors) < 1:
            return render_template('message.html', msg=f'We cannot find any actors with the name {key_word}')
        return render_template('actors.html', actor_infos=found_actors)
    
    abort(404)

@app.route('/directors/', methods=[GET, POST])
def directorpage():
    if request.method == "POST":
        print(request.form['director_name']) # get example data
        d = request.form # assign request_form as dictionary
        print("line 122")
        print(request.form['id'])
        mydb.upload_director(request.form['id'], d, db_conn)
        print("line 124")
        return render_template('message.html', msg='post to directors')
    method = request.args.get('_method', default=None, type=str)
    if method == UPDATE:
        return render_template('post_director.html', director_info={'DirectorId': -1})

    fake_director = [{'DirectorId': 321685, 'Director_name': 'My Director', 'Birth_Year': 1344,
                      'Death_Year': 0}]
    director_id = request.args.get('id', default = -1, type = int)
    if director_id != -1:
        if method == DELETE:
            mydb.delete_director(director_id, db_conn)
            return render_template('message.html', msg='deleted from directors')
        if method == EDIT:
            dict_info = mydb.get_director_info(director_id, db_conn)
            return render_template('post_director.html', director_info= dict_info)
    
    recommand = request.args.get('recommand', default = False, type = bool)
    if recommand:
        rec_directors = mydb.get_director_recommand1(db_conn)
        return render_template('directors.html', director_infos=rec_directors)

    key_word = request.args.get('key_word', default=None, type=str)
    if key_word:
        found_directors = mydb.get_director_key_word(key_word, db_conn)
        if len(found_directors) < 1:
            return render_template('message.html', msg=f'We cannot find any directors with the name {key_word}')
        return render_template('directors.html', director_infos=found_directors)
    
    abort(404)

@app.route('/reviews/', methods=[GET, POST])
def reviewpage():
    if request.method == "POST":
        print(request.form['comment']) # get example data
        return render_template('message.html', msg='post to reviews')
    method = request.args.get('_method', default=None, type=str)
    fake_review = [{'ReviewId': 5644564, 'UserId': 654684768, 'MovieId': 659,
                      'Comment': 'I like this movie', 'Rating':5}]
    movie_id = request.args.get('movie_id', default = -1, type = int)
    review_id = request.args.get('review_id', default = -1, type = int)
    if movie_id != -1 or review_id != -1:
        if method == DELETE:
            return {'status': 'OK', 'delete': 'works'}
        if method == EDIT:
            return render_template('post_review.html', review_info=fake_review[0])
        return render_template('reviews.html', review_infos=fake_review+fake_review, allow_comment=True)
    
    key_word = request.args.get('key_word', default=None, type=str)
    if key_word:
        return render_template('reviews.html', review_infos=fake_review+fake_review, allow_comment=False)

    abort(404)

if __name__ == '__main__':
    # app.run(port=5000, debug=True)
    '''
    # Example use of model.database
    import model.database as mydb
    print('start')
    db_conn = init_connect_engine().connect()
    mydb.test(db_conn)
    db_conn.close()
    print('end')
    '''
    print('start')
    # mydb.upload_director(-1, db_conn)
    print('end')
