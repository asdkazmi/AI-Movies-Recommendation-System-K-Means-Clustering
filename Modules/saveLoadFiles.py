# -*- coding: utf-8 -*-

import pickle
from sys import exc_info

class saveLoadFiles:
    def save(self, filename, data):
        try:
            print('saveLoadFiles -> save: Trying to save \"' + filename + '.pkl\" file...')
            file = open('datasets/' + filename + '.pkl', 'wb')
            pickle.dump(data, file)
        except:
            err = 'Error: {0}, {1}'.format(exc_info()[0], exc_info()[1])
            print('saveLoadFiles -> save: ', err)
            file.close()
            return [False, err]
        else:
            file.close()
            print('saveLoadFiles -> save: File \"' + filename + '.pkl\" saved successfully.')
            return [True]
    def load(self, filename):
        try:
            print('saveLoadFiles -> load: Trying to load \"' + filename + '.pkl\" file...')
            file = open('datasets/' + filename + '.pkl', 'rb')
        except:
            err = 'Error: {0}, {1}'.format(exc_info()[0], exc_info()[1])
            print(err)
            file.close()
            return [False, err]
        else:
            data = pickle.load(file)
            file.close()
            print('saveLoadFiles -> load: File \"' + filename + '.pkl\" loaded successfully.')
            return data
    def loadClusterMoviesDataset(self):
        return self.load('clusters_movies_dataset')
    def saveClusterMoviesDataset(self, data):
        return self.save('clusters_movies_dataset', data)
    def loadUsersClusters(self):
        return self.load('users_clusters')
    def saveUsersClusters(self, data):
        return self.save('users_clusters', data)