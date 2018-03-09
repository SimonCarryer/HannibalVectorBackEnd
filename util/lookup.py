import numpy as np
from sklearn.metrics.pairwise import cosine_similarity


class bidict(dict):
    def __init__(self, *args, **kwargs):
        super(bidict, self).__init__(*args, **kwargs)
        self.inverse = {}
        for key, value in self.items():
             self.inverse[value] = key

class MovieGetter:
    def __init__(self, movie_to_matrix_dic, matrix):
        movie_to_matrix_dic.index = range(len(movie_to_matrix_dic))
        self.movie_to_matrix_dic = bidict(movie_to_matrix_dic.IMDbId.to_dict())
        self.matrix = matrix

    def get(self, imdb_id):
        index = self.movie_to_matrix_dic.inverse[imdb_id]
        return self.matrix[index].reshape(1, -1)
    
    def get_closest(self, movie1, movie2, imdb_1, imdb_2):
        best_movie = movie1 + movie2
        print('Got some values %s %s' % (imdb_1, imdb_2))
        best_list = [i for i in np.argsort(cosine_similarity(best_movie, self.matrix))[0][::-1] if self.movie_to_matrix_dic[i] not in [imdb_1, imdb_2]][:10]

        return self.movie_to_matrix_dic[best_list[0]]
