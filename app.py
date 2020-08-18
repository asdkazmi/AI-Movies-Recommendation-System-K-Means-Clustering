# -*- coding: utf-8 -*-

from flask import Flask
from flask_restful import Resource, Api
from Modules.userRequestedFor import userRequestedFor
from Modules.dataEngineering import dataEngineering
from Modules.loadRequirements import loadRequirements
from Modules.kmeansModel import kmeansModel

app = Flask(__name__)
api = Api(app)


class GetMoviesForUser(Resource):
    def get(self, user_id):
        if int(user_id) is user_id:
            users_data = dataEngineering().loadUsersData()
            if users_data[0]:
                return userRequestedFor(user_id, users_data[1]['users_data'], making_recommendations = True).recommendMostFavouriteMovies(), 200
            else:
                return users_data
class trainModel(Resource):
    def put(self):
        kmeans = kmeansModel()
        trained_data = kmeans.run_model()
        if trained_data[0]:
            if kmeans.saveClusterMoviesDataset(trained_data[1]['clusters_movies_df'])[0] and kmeans.saveUsersClusters(trained_data[1]['users_cluster'])[0]:
                return [True, 'Training completed and saved successfully'], 201

api.add_resource(trainModel, '/training')
api.add_resource(GetMoviesForUser, '/<int:user_id>')
app.run(port=2000)