import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sys import exc_info

# -*- coding: utf-8 -*-
class dataEngineering:
    def __init__(self):
        self.users = None
        self.users_movies_list = None
        self.sparseMatrix = None
        self.feature_names = None
    # A method which will load users data for us which we were prepaired and saved into local
    # The data was already in proper format. If anyone using any database, then he/she can edit this method to load data
    # into pandas DataFrame in the same format as we were described earlier.
    def loadUsersData(self):
        try:
            print('dataEngineering -> loadUsersData: Loading users data...')
            users_data = pd.read_csv('./Prepairing Data/From Data/filtered_ratings.csv')
            # users_data = a dataframe of users favourite movies or users watched movies
            users = np.unique(users_data['userId'])
            # users = a list of users IDs in descending order
        except:
            err = 'Error: {0}, {1}'.format(exc_info()[0], exc_info()[1])
            print('Error while loading users data: ', err)
            return [False, err]
        else:
            print('dataEngineering -> loadUsersData: Users data loaded.')
            return [True, 
                    {'users_data': users_data, 
                     'users_list': users}]
    # define a method which will create a list containing string of movies list for each user with users IDs in descending order
    def moviesListForUsers(self):
        load_users_data = self.loadUsersData()
        if load_users_data[0]:
            users_data = load_users_data[1]['users_data']
            self.users = load_users_data[1]['users_list']
            self.users_movies_list = []
            print('dataEngineering -> moviesListForUsers: Prepairing movies list for each user...')
            for user in self.users:
                self.users_movies_list.append(str(list(users_data[users_data['userId'] == user]['movieId'])).split('[')[1].split(']')[0])
            print('dataEngineering -> moviesListForUsers: Prepaired movies list')
        else:
            print('dataEngineering -> moviesListForUsers: Error in loading users data: ', load_users_data[1])
    # define a method to prepair a sparse matrix of each user against favourite movies list
    def prepSparseMatrix(self):
        # list_of_str = A list, which contain strings of users favourite movies separate by comma ",".
        # It will return us sparse matrix and feature names on which sparse matrix is defined 
        # i.e. name of movies in the same order as the column of sparse matrix
        if self.users_movies_list is None:
            print('dataEngineering -> prepSparseMatrix: Movies list is not perpaired.')
            self.moviesListForUsers()
        print('dataEngineering -> prepSparseMatrix: Prepairing sparse matrix...')
        cv = CountVectorizer(token_pattern = r'[^\,\ ]+', lowercase = False)
        sparseMatrix = cv.fit_transform(self.users_movies_list)
        print('dataEngineering -> prepSparseMatrix: Sparse matrix prepaired.')
        return [True, 
                {'sparse_matrix': sparseMatrix.toarray(), 
                'feature_names': cv.get_feature_names()}]
    # define a method to show sparse matrix in dataframe for presentation
    def showSparseMatrix(self, sparseMatrix, feature_names, users):
        return pd.DataFrame(sparseMatrix, index = users, columns = feature_names)