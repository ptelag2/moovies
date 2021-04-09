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
    fake_movie = [{'MovieId': 3532, 'Title': 'My Moovie', 'Runtime': 215, 'Publication_Year': 2022, 'Genre': 'Adult', 'Language': 'English'}]
    movie_id = request.args.get('id', default = -1, type = int)
    if movie_id != -1:
        return render_template('movies.html', movie_infos=fake_movie)
    
    recommand = request.args.get('recommand', default = False, type = bool)
    if recommand:
        return render_template('movies.html', movie_infos=fake_movie+fake_movie+fake_movie)
    
    abort(404)

@app.route('/actors/', methods=[GET, PUT, POST, DELETE])
def actorpage():
    actor_id = request.args.get('id', default = -1, type = int)
    if actor_id != -1:
        fake_actor = [{'ActorId': 3532, 'Actor_Name': 'John Smith', 'Birth_Year': 1982, 'Death_Year': 0, 'Most_Known_Titles': 'tt10'}]
        return render_template('actors.html', actors_info=fake_actor)
    
    recommand = request.args.get('recommand', default = False, type = bool)
    if recommand:
        return render_template('actors.html', actors_info=fake_actor)
        
    abort(404)

@app.route('/directors/', methods=[GET, PUT, POST, DELETE])
def directorpage():
    director_id = request.args.get('id', default = -1, type = int)
    if director_id != -1:
        return {'status': 'OK'}
    
    recommand = request.args.get('recommand', default = False, type = bool)
    if recommand:
        return {'status': 'OK'}
    
    abort(404)

@app.route('/reviews/', methods=[GET, PUT, POST, DELETE])
def reviewpage():
    movie_id = request.args.get('movie_id', default = -1, type = int)
    if movie_id != -1:
        return {'status': 'OK'}
    
    abort(404)

if __name__ == '__main__':
    app.run(port=5000, debug=True)

