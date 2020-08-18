# -*- coding: utf-8 -*-

from sys import exc_info
from Modules.saveLoadFiles import saveLoadFiles

class userRequestedFor:
    def __init__(self, user_id, users_data, making_recommendations = False):
        self.users_data = users_data.copy()
        self.user_id = user_id
        if making_recommendations:
            # Find User Cluster
            users_cluster = saveLoadFiles().loadUsersClusters()
            self.user_cluster = int(users_cluster[users_cluster['userId'] == self.user_id]['Cluster'])
            # Load User Cluster Movies Dataframe
            self.movies_list = saveLoadFiles().loadClusterMoviesDataset()
            self.cluster_movies = self.movies_list[self.user_cluster] # dataframe
            self.cluster_movies_list = list(self.cluster_movies['movieId']) # list
    def getMyMovies(self):
        return list(self.users_data[self.users_data['userId'] == self.user_id]['movieId'])
    def updatedFavouriteMoviesList(self, new_movie_Id):
        if new_movie_Id in self.cluster_movies_list:
            self.cluster_movies.loc[self.cluster_movies['movieId'] == new_movie_Id, 'Count'] += 1
        else:
            self.cluster_movies = self.cluster_movies.append([{'movieId':new_movie_Id, 'Count': 1}], ignore_index=True)
        self.cluster_movies.sort_values(by = ['Count'], ascending = False, inplace= True)
        self.movies_list[self.user_cluster] = self.cluster_movies
        saveLoadFiles().saveClusterMoviesDataset(self.movies_list)

    def recommendMostFavouriteMovies(self):
        try:
            user_movies = self.getMyMovies()
            cluster_movies_list = self.cluster_movies_list.copy()
            for user_movie in user_movies:
                if user_movie in cluster_movies_list:
                    cluster_movies_list.remove(user_movie)
            return [True, cluster_movies_list]
        except KeyError:
            err = "User history does not exist"
            print('userRequestedFor -> recommendMostFavouriteMovies: ', err)
            return [False, err]
        except:
            err = 'Error: {0}, {1}'.format(exc_info()[0], exc_info()[1])
            print('userRequestedFor -> recommendMostFavouriteMovies: ', err)
            return [False, err]