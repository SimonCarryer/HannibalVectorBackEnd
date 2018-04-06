from flask import Flask, jsonify, request
from util.process_pickle import load_compressed_pickled_object
from util.lookup import MovieGetter, MovieSearcher
from util.validation import MovieInputValidator, SearchInputValidator

print('starting app')

print('gonna download the matrix')
matrix = load_compressed_pickled_object("https://s3.amazonaws.com/hannibal-vector/hanibalVectorModel-09-03-2018.gz")
print('got a matrix with shape %d, %d' % matrix.shape)

print('gonna download the movie_dataframe')
movie_dataframe = load_compressed_pickled_object("https://s3.amazonaws.com/hannibal-vector/hanibalVectorIndex-09-03-2018.gz")
print('got a movie_dataframe')

movie_getter = MovieGetter(movie_dataframe, matrix)
movie_searcher = MovieSearcher(movie_dataframe)
movie_validator =  MovieInputValidator(list(movie_dataframe.IMDbId))
search_validator = SearchInputValidator()

app = Flask(__name__)

@app.route('/movies')
def api_root():
    if not search_validator.validate(request):
        return jsonify(search_validator.errors()), 400
    query = request.args.get('query')
    return jsonify(movie_searcher.search(query))

@app.route('/add')
def addmovie():
    if not movie_validator.validate(request):
        return jsonify(movie_validator.errors()), 400
    imdb_id_1 = request.args.get('movie_imdb_1')
    imdb_id_2 = request.args.get('movie_imdb_2')
    movie1 = movie_getter.get(imdb_id_1)
    movie2 = movie_getter.get(imdb_id_2)
    best_movie = movie1 + movie2
    closest = movie_getter.get_closest(best_movie, imdb_id_1, imdb_id_2)
    return jsonify(closest), 200

@app.route('/subtract')
def subtractmovie():
    if not movie_validator.validate(request):
        return jsonify(movie_validator.errors()), 400
    imdb_id_1 = request.args.get('movie_imdb_1')
    imdb_id_2 = request.args.get('movie_imdb_2')
    movie1 = movie_getter.get(imdb_id_1)
    movie2 = movie_getter.get(imdb_id_2)
    best_movie = movie1 - movie2
    closest = movie_getter.get_closest(best_movie, imdb_id_1, imdb_id_2)
    return jsonify(closest), 200

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
    return response

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug = False)
