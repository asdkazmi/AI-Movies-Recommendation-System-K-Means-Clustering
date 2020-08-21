# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sys import exc_info
from Modules.saveLoadFiles import saveLoadFiles
from Modules.dataEngineering import dataEngineering
from Modules.userRequestedFor import userRequestedFor

class kmeansModel(KMeans, saveLoadFiles):
    def __init__(self):
        KMeans.__init__(self)
        # Setting of k-means model
        self.n_clusters=15
        self.init = 'k-means++'
        self.max_iter = 300
        self.n_init = 10
        self.random_state = 0
        # Other attributes
        self.users_cluster = None
        self.clusters_movies_df = None
    def clustersMovies(self, users_cluster, users_data):
        clusters = list(users_cluster['Cluster'])
        each_cluster_movies = list()
        for i in range(len(np.unique(clusters))):
            users_list = list(users_cluster[users_cluster['Cluster'] == i]['userId'])
            users_movies_list = list()
            for user in users_list:    
                users_movies_list.extend(list(users_data[users_data['userId'] == user]['movieId']))
            users_movies_counts = list()
            users_movies_counts.extend([[movie, users_movies_list.count(movie)] for movie in np.unique(users_movies_list)])
            each_cluster_movies.append(pd.DataFrame(users_movies_counts, columns=['movieId', 'Count']).sort_values(by = ['Count'], ascending = False).reset_index(drop=True))
        return each_cluster_movies

    def fixClusters(self, clusters_movies_dataframes, users_cluster_dataframe, users_data, smallest_cluster_size = 11):
        # clusters_movies_dataframes: will be a list which will contain each dataframes of each cluster movies
        # users_cluster_dataframe: will be a dataframe which contain users IDs and their cluster no.
        # smallest_cluster_size: is a smallest cluster size which we want for a cluster to not remove
        print('kmeansModel -> fixClusters: Fixing started...')
        each_cluster_movies = clusters_movies_dataframes.copy()
        users_cluster = users_cluster_dataframe.copy()
        # Let convert dataframe in each_cluster_movies to list with containing only movies IDs
        each_cluster_movies_list = [list(df['movieId']) for df in each_cluster_movies]
        # First we will prepair a list which containt lists of users in each cluster -> [[Cluster 0 Users], [Cluster 1 Users], ... ,[Cluster N Users]] 
        usersInClusters = list()
        total_clusters = len(each_cluster_movies)
        for i in range(total_clusters):
            usersInClusters.append(list(users_cluster[users_cluster['Cluster'] == i]['userId']))
        uncategorizedUsers = list()
        i = 0
        # Now we will remove small clusters and put their users into another list named "uncategorizedUsers"
        # Also when we will remove a cluster, then we have also bring back cluster numbers of users which comes after deleting cluster
        # E.g. if we have deleted cluster 4 then their will be users whose clusters will be 5,6,7,..,N. So, we'll bring back those users cluster number to 4,5,6,...,N-1.
        for j in range(total_clusters):
            if len(usersInClusters[i]) < smallest_cluster_size:
                uncategorizedUsers.extend(usersInClusters[i])
                usersInClusters.pop(i)
                each_cluster_movies.pop(i)
                each_cluster_movies_list.pop(i)
                users_cluster.loc[users_cluster['Cluster'] > i, 'Cluster'] -= 1
                i -= 1
            i += 1
        for user in uncategorizedUsers:
            elemProbability = list()
            user_movies = userRequestedFor(user, users_data).getMyMovies()
#             if len(user_movies) == 0:
#                 print(user)
            user_missed_movies = list()
            for movies_list in each_cluster_movies_list:
                count = 0
                missed_movies = list()
                for movie in user_movies:
                    if movie in movies_list:
                        count += 1
                    else:
                        missed_movies.append(movie)
                elemProbability.append(count / len(user_movies))
                user_missed_movies.append(missed_movies)
            user_new_cluster = np.array(elemProbability).argmax()
            users_cluster.loc[users_cluster['userId'] == user, 'Cluster'] = user_new_cluster
            if len(user_missed_movies[user_new_cluster]) > 0:
                each_cluster_movies[user_new_cluster] = each_cluster_movies[user_new_cluster].append([{'movieId': new_movie, 'Count': 1} for new_movie in user_missed_movies[user_new_cluster]], ignore_index = True)
        print('kmeansModel -> fixClusters: Fixing completed.')
        return each_cluster_movies, users_cluster
    
    def run_model(self, sparseMatrix = None, fix_clusters = True, smallest_cluster = 6):
        try:
            if sparseMatrix is None:
                print('kmeansModel -> run_model: Sparse matrix was not given in model, prepairing sparse matrix...')
                sparseMatrix = dataEngineering().prepSparseMatrix()[1]['sparse_matrix']
        except:
            err = 'Error: {0}, {1}'.format(exc_info()[0], exc_info()[1])
            print('kmeansModel -> run_model: Error while running k-means model: ',err)
            return [False, err]
        print('kmeansModel -> run_model: Fitting and predicting k-means model...')
        # fitting and predicting k-means model
        clusters = self.fit_predict(sparseMatrix)
        print('kmeansModel -> run_model: Model fitting and predictions are completed.')
        load_users_data = dataEngineering().loadUsersData()
        if load_users_data[0]:
            users = load_users_data[1]['users_list']
            users_data = load_users_data[1]['users_data']
            self.users_cluster = pd.DataFrame(np.concatenate((users.reshape(-1,1), clusters.reshape(-1,1)), axis = 1), columns = ['userId', 'Cluster'])
            self.clusters_movies_df = self.clustersMovies(self.users_cluster, users_data)
            if fix_clusters:
                print('kmeansModel -> run_model: Fixing small clusters less than', smallest_cluster, 'size.')
                self.clusters_movies_df, self.users_cluster = self.fixClusters(self.clusters_movies_df, self.users_cluster, users_data, smallest_cluster_size = smallest_cluster)
            print('kmeansModel -> run_model: Predictions completed and users clusters DataFrame prepaired.')
            return [True, 
                    {'users_cluster': self.users_cluster,
                    'clusters_movies_df': self.clusters_movies_df}]
        else:
            print('kmeansModel -> run_model: Error in loading users data inside k-means: ', load_users_data[1])
            return [False, load_users_data[1]]
    def saveFiles(self):
        print('KMeans -> saveFiles: Trying to save files...')
        if self.clusters_movies_df is None and self.users_cluster is None:
            err = 'Model is not trained yet, please call run_model(...) method to train it first.'
            print('KMeans -> saveFiles: ', err)
            return [False, err]
        else:
            save_movies = self.saveClusterMoviesDataset(self.clusters_movies_df)
            save_clusters = self.saveUsersClusters(self.users_cluster)
            if save_movies[0] and save_clusters[0]:
                success_msg = 'File Saved Successfully.'
                print('KMeans -> saveFiles: ', success_msg)
                return [True, success_msg]
            else:
                err = list()
                if not save_movies[0]:
                    err.append(['Error in Saving Movies Dataset', save_movies[1]])
                if not save_clusters[0]:
                    err.append(['Error in Saving Clusters Dataset', save_clusters[1]])
                print('KMeans -> saveFiles: ', err)
                return [False, err]