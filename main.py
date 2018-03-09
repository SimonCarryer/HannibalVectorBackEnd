from flask import Flask, jsonify, request
from util.process_pickle import load_compressed_pickled_object
from util.lookup import MovieGetter

print('starting app')

print('gonna download the matrix')
matrix = load_compressed_pickled_object("https://s3.amazonaws.com/hannibal-vector/hanibalVectorModel-09-03-2018.gz")
print('got a matrix with shape %d, %d' % matrix.shape)

print('gonna download the movie_to_matrix_dic')
movie_to_matrix_dic = load_compressed_pickled_object("https://s3.amazonaws.com/hannibal-vector/hanibalVectorIndex-09-03-2018.gz")
print('got a movie_to_matrix_dic')

movie_getter = MovieGetter(movie_to_matrix_dic, matrix)

app = Flask(__name__)

@app.route('/movies')
def api_root():
    return jsonify(["Matt and Deans amazing adventures (1990)",
    "Why did Jenny fall asleep (1990)", "Pulp Fiction (1994)"])

@app.route('/add')
def addmovie():
    imdb_id_1 = request.args.get('movie_imdb_1')
    imdb_id_2 = request.args.get('movie_imdb_2')
    movie1 = movie_getter.get(imdb_id_1)
    movie2 = movie_getter.get(imdb_id_2)
    closest = movie_getter.get_closest(movie1, movie2, imdb_id_1, imdb_id_2)
    return jsonify(closest)

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
    return response

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug = False)
