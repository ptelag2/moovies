from flask import Flask, request, abort, render_template, make_response
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
        msg = mydb.upload_movie(request.form['id'], request.form, db_conn)
        return render_template('message.html', msg=msg)

    method = request.args.get('_method', default=None, type=str)
    if method == UPDATE:
        # no need to do anything
        return render_template('post_movie.html', movie_info={'MovieId': -1})

    movie_id = request.args.get('id', default=-1, type=int)
    if movie_id != -1:
        if method == DELETE:
            # delete movie with movie_id
            msg = mydb.delete_movie(movie_id, db_conn)
            return render_template('message.html', msg=msg)
        movie_info = mydb.get_movie_info(movie_id, db_conn)
        if method == EDIT:
            # no need to do anything
            return render_template('post_movie.html', movie_info=movie_info)
        return render_template('movies.html', movie_infos = [movie_info])
    recommand = request.args.get('recommand', default = False, type = bool)
    if recommand:
        # place for your advanced query
        rec_movies = mydb.get_movie_recommand1(db_conn)
        rec_movies += mydb.get_movie_recommand2(db_conn)
        return render_template('movies.html', movie_infos=rec_movies)
    
    key_word = request.args.get('key_word', default=None, type=str)
    if key_word:
        found_movies = mydb.get_movie_key_word(key_word, db_conn)
        # result for movies containing the key words
        if len(found_movies) < 1:
            return render_template('message.html', msg=f'We cannot find any movies with the name {key_word}')
        return render_template('movies.html', movie_infos=found_movies)
    
    abort(404)

@app.route('/actors/', methods=[GET, POST])
def actorpage():
    if request.method == "POST":
        msg = mydb.upload_actor(request.form['id'], request.form, db_conn)
        return render_template('message.html', msg=msg)

    method = request.args.get('_method', default=None, type=str)
    if method == UPDATE:
        return render_template('post_actor.html', actor_info={'ActorId': -1})

    actor_id = request.args.get('id', default=-1, type=int)
    if actor_id != -1:
        if method == DELETE:
            msg = mydb.delete_actor(actor_id, db_conn)
            return render_template('message.html', msg=msg)
        actor_info = mydb.get_actor_info(actor_id, db_conn)
        if method == EDIT:
            return render_template('post_actor.html', actor_info=actor_info)
        return render_template('actors.html', actor_infos = [actor_info])
    
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
        msg = mydb.upload_director(request.form['id'], request.form, db_conn)
        return render_template('message.html', msg=msg)
    method = request.args.get('_method', default=None, type=str)
    if method == UPDATE:
        return render_template('post_director.html', director_info={'DirectorId': -1})

    director_id = request.args.get('id', default=-1, type=int)
    if director_id != -1:
        if method == DELETE:
            msg = mydb.delete_director(director_id, db_conn)
            return render_template('message.html', msg=msg)
        dict_info = mydb.get_director_info(director_id, db_conn)
        if method == EDIT:
            return render_template('post_director.html', director_info= dict_info)
        return render_template('directors.html', director_infos=[dict_info])

    recommand = request.args.get('recommand', default=False, type=bool)
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
        if request.authorization and mydb.authenticate(request.authorization.username, request.authorization.password):
            user_id = mydb.get_user_id(request.authorization.username)
            msg = mydb.upload_review(request.form['review_id'], user_id, request.form, db_conn)
            return render_template('message.html', msg=msg)
        return make_response('Could not verify!', 401, {'WWW-Authenticate':'Basic realm="Login Required"'})
    method = request.args.get('_method', default=None, type=str)

    movie_id = request.args.get('movie_id', default=-1, type = int)
    review_id = request.args.get('review_id', default=-1, type = int)
    if movie_id != -1 or review_id != -1:
        if method == DELETE:
            msg = mydb.delete_review(review_id, db_conn)
            return render_template('message.html', msg=msg)
        review_info = mydb.get_review_info(review_id, db_conn)
        review_info_all = mydb.get_all_reviews(movie_id, db_conn)
        if method == EDIT:
            return render_template('post_review.html', review_info=review_info)
        return render_template('reviews.html', MovieId=movie_id, review_infos=review_info_all, allow_comment=True)
    
    key_word = request.args.get('key_word', default=None, type=str)
    if key_word:
        found_reviews = mydb.get_review_key_word(key_word, db_conn)
        if len(found_reviews) < 1:
            return render_template('message.html', msg=f'We cannot find any reviews with the {key_word}')
        return render_template('reviews.html', review_infos=found_reviews, allow_comment=False)

    abort(404)

@app.route('/votes/')
def votepage():
    if request.authorization and mydb.authenticate(request.authorization.username, request.authorization.password):
        user_id = mydb.get_user_id(request.authorization.username)
        review_id = request.args.get('review_id', default=-1, type = int)
        if review_id == -1:
            abort(404)
        return render_template('message.html', msg=f'Get vote on review {review_id} made by {user_id}')
    return make_response('Could not verify!', 401, {'WWW-Authenticate':'Basic realm="Login Required"'})

if __name__ == '__main__':
    app.run(port=5000, debug=True)
