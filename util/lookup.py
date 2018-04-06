import numpy as np
from sklearn.metrics.pairwise import cosine_similarity


class bidict(dict):
    def __init__(self, *args, **kwargs):
        super(bidict, self).__init__(*args, **kwargs)
        self.inverse = {}
        for key, value in self.items():
             self.inverse[value] = key

class MovieGetter:
    def __init__(self, movie_dataframe, matrix):
        movie_dataframe.index = range(len(movie_dataframe))
        self.movie_to_matrix_dic = bidict(movie_dataframe.IMDbId.to_dict())
        self.matrix = matrix

    def get(self, imdb_id):
        index = self.movie_to_matrix_dic.inverse[imdb_id]
        return self.matrix[index].reshape(1, -1)
    
    def get_closest(self, movie, imdb_1, imdb_2):
        print('Got some values %s %s' % (imdb_1, imdb_2))
        closest_movie = [i for i in np.argsort(cosine_similarity(movie, self.matrix))[0][::-1] if self.movie_to_matrix_dic[i] not in [imdb_1, imdb_2]][:10]
        return self.movie_to_matrix_dic[closest_movie[0]]	

class MovieSearcher:
    def __init__(self, movie_dataframe):        
        movie_dataframe.index = range(len(movie_dataframe))
        self.dataframe = movie_dataframe

    def search(self, search_string):
        matches = self.dataframe[self.dataframe.title.str.lower().str.contains(search_string.lower())]
        return [i for i in matches.to_dict('index').values()]