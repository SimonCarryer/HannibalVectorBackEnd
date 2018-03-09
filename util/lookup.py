import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

class bidict(dict):
    def __init__(self, *args, **kwargs):
        super(bidict, self).__init__(*args, **kwargs)
        self.inverse = {}
        for key, value in self.items():
            self.inverse.setdefault(value,[]).append(key) 

    def __setitem__(self, key, value):
        if key in self:
            self.inverse[self[key]].remove(key) 
        super(bidict, self).__setitem__(key, value)
        self.inverse.setdefault(value,[]).append(key)        

    def __delitem__(self, key):
        self.inverse.setdefault(self[key],[]).remove(key)
        if self[key] in self.inverse and not self.inverse[self[key]]: 
            del self.inverse[self[key]]
        super(bidict, self).__delitem__(key)

class MovieGetter:
    def __init__(self, movie_to_matrix_dic, matrix):
        self.movie_to_matrix_dic = bidict(movie_to_matrix_dic)
        self.matrix = matrix

    def get(self, imdb_id):
        index = self.movie_to_matrix_dic[imdb_id]
        return self.matrix[index]
    
    def get_closest(self, movie1, movie2, imdb_1, imdb_2):
        best_movie = movie1 + movie2
        print('Got some values %d %d %d %d' % movie1, movie2, imdb_1, imdb_2)
        best_list = [i for i in np.argsort(cosine_similarity(best_movie, self.matrix))[0][::-1] if self.movie_to_matrix_dic.inverse[i] not in [imdb_1, imdb_2]][:10]

        movie_title = self.movie_to_matrix_dic[best_list]
        return movie_title
