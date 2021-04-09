from flask import Flask, request, abort, jsonify, render_template

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
    movie_id = request.args.get('movie_id', default = -1, type = int)
    if movie_id != -1:
        return {'status': 'OK'}
    
    abort(404)

if __name__ == '__main__':
    app.run(port=5000, debug=True)

