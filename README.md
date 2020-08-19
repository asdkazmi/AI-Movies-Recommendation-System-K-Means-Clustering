# AI-Movies-Recommendation-System-K-Means-Clustering
This is repository for a project of AI movies recommendation system based on k-means clustering algorithm with Flask-RESTFUL APIs. An associated article is published on medium, read it here
[AI Movies Recommendation System Based on K-Means Clustering Algorithm](https://medium.com/@asdkazmi/ai-movies-recommendation-system-with-clustering-based-k-means-algorithm-f04467e02fcd). You can also download Jupyter Notebook **AI Movies Recommendation System Based on K-Means Clustering Algorithm** from this repositry for the understanding of this whole project completely with step by step instructions and tutorials. This Python Notebook is similar as Medium article.

## Documentation
In this section, the complete documentation is given to use model and it's different APIs. This model is very flexible with a lot of APIs and analysis methods on datasets. This project can work both with csv files and databases. It built default with csv file with format of MovieLens dataset but it is described that how to use it with other sources. 
### Required Libraries
Following libraries of Python are needed to be installed in your working environment
```
Pandas version:  0.25.1
NumPy version:  1.16.5
Matplotlib version:  3.1.1
Scikit-Learn version:  0.21.3
Pickle version:  4.0
Sys version:  3.7.7
```
### Modules
Different modules are designed and their APIs are discussed as follows
1. dataEngineering
2. elbowMethod
3. saveLoadFiles
4. kmeansModel
5. userRequestedFor
#### 1. dataEngineering
Import it as `from Modules.dataEngineering import dataEngineering`

**Purpose**: dataEngineering is a class which will be used to prepare data for k-means clustering model

Create instance of dataEngineering as
```
YOUR_VAR_NAME = dataEngineering()
```
- Arguments: _No_
##### Attributes:
- **users** -> Default: None | It will be a list of users IDs in descending order.
- **users_movies_list** -> Default: None | It will be list of strings where each string will contain user movies separated by comma ",".
##### Methods:
- `loadUsersData(from_loc)`
  - Arguments:
    - `from_loc` -> Default: './Prepairing Data/From Data/filtered_ratings.csv' | Must be a string with valid location of data _csv_ file. _csv_ file format must be following
      
      _csv_ file format -> Number of Rows: Any | Columns: `['userId', 'movieId']` where `'userId'` column should contain IDs of users and `'movieId'` column should contain ID of movie which user has added into his favorite OR has watched OR any other type on which you want to make recommendations. `'userId'` column could contain multiple entries of same ID.
  - Purpose: It will be used to load users data from location and create list of users IDs in users data.
  - Attribute Updates: _False_
  - Associated Method: _No_
  - Return: Python `list` of length 2.
    - Index 0: 
      - `True`: If data loaded successfully.
      - `False`: If any error arise.
    - Index 1:
      - If index 0 `True` then `dict` with following format 
        ```
        {'users_data': A Pandas DataFrame containing data loaded from from_loc,
         'users_list': A list of users IDs in descending order extracted from users_data}
        ```
      - If index 0 `False` then `str` containing error information.
  - **Note**: If you're using any other way to load data, then it is recommended to edit this method to get your data and return in the same format as described above in the **_csv_ file format**. Please write your code inside the indicated area.
- `moviesListForUsers(from_loc)`: 
  - Arguments:
    - `from_loc` -> It will be used with associated method `loadUsersData(from_loc)`. See `loadUsersData(from_loc)` method docs for further detail on `from_loc` argument. 
  - Purpose: It will be used to create a list of strings containing IDs of movies of each user (obtained from users data) separated by comma ",". The order of list will be same as list of users obtained from `loadUsersData` which is in descending order.
  - Attribute Updates: `users`, `users_movies_list`
  - Associated Method: `loadUsersData(from_loc)`
  - Return: _None_
- `prepSparseMatrix(from_loc)`: 
  - Arguments: 
    - `from_loc` -> It will be used with associated method `moviesListForUsers(from_loc)`. It is required only if attribute **users_movies_list** not updated and still `None`. See `loadUsersData(from_loc)` method docs for further detail on `from_loc` argument.
  - Purpose: It will create a sparse matrix (NumPy Array) with dimensions `(Number of Users, Number of Movies)` with value `1` if users has movie in its list, otherwise `0`
  - Attribute Updates: _False_
  - Associated Method: `moviesListForUsers(from_loc)` -> If attribute **users_movies_list** is `None`.
  - Return: Python `list` of length 2.
    - Index 0: 
      - `True`: If method runs successfully.
    - Index 1:
      - `dict` with following format 
        ```
        {'sparse_matrix': Required sparse matrix as described in purpose,
         'feature_names': It will be an array containing all movies IDs in the same order as the columns in **sparseMatrix**}
        ```
- `showSparseMatrix(sparseMatrix, feature_names, users)`: 
  - Arguments:
    - `sparseMatrix` -> A sparse matrix obtained from `prepSparseMatrix(from_loc)` method.
    - `feature_names` -> An array of feature names obtained from `prepSparseMatrix(from_loc)` method.
    - `users` -> An array of users IDs saved in **users** attribute if not `None`.
  - Attribute Updates: _False_
  - Associated Method: _None_
  - Return: Panda DataFrame with presentation of sparse matrix containing indexes with users IDs and columns with movies IDs.

#### 2. elbowMethod
Import it as `from Modules.elbowMethod import elbowMethod`

**Purpose**: It will be used to analyze the optimal number of clusters for k-means algorithm. It will not run with app but can be used by individual for only analysis purpose.

Create instance of elbowMethod as
```
YOUR_VAR_NAME = elbowMethod(sparseMatrix)
``` 
- Arguments:
  - `sparseMatrix`: A sparse matrix obtained from `dataEngineering` module method `prepSparseMatrix()`.
##### Attributes:
- **sparseMatrix** -> Default: A sparse matrix given by argument `sparseMatrix`
- **wcss** -> Default: `list()` | A list which will contain WCSS values obtained from k-means algorithm.
- **differences** -> Default: `list()` | A list which will contain difference between each two consective WCSS values.
##### Methods:
- `run(init, upto, max_iterations = 300)`: 
  - Arguments:
    - `init` -> Default: None | Initial number of clusters.
    - `upto` -> Default: None | Final number of clusters.
    - `max_iterations` - > Default: 300 | It can be any +ve int to set KMeans iterations during clustering.
  - Purpose: It will calculate WCSS values and their difference between _init_ to _upto_ numbers of clusters.
  - Attribute Updates: `sparseMatrix`, `wcss` and `differences`
  - Associated Method: _None_
  - Return: _None_
- `showPlot(boundary = 500, upto_cluster = None)`: 
  - Arguments:
    - `boundary` - > Default: 500 | A boundary which you want to set for minimum WCSS value.
    - `upto_cluster` -> Default: None | To show plot upto specific cluster numbers e.g. if `upto_cluster = 10` then it will return plot for clusters 1-10 only.
  - Purpose: It will show plots of elbow method and differences of WCSS to analyze cluster numbers.
  - Attribute Updates: _False_
  - Associated Method: _None_
  - Return: Matplotlib plots.
#### 3. saveLoadFiles
Import it as `from Modules.saveLoadFiles import saveLoadFiles`

**Purpose**: To save and load files to local by using `pickle` library.

Create instance of saveLoadFiles as
```
YOUR_VAR_NAME = saveLoadFiles()
```
- Arguments: _None_
##### Attributes: 
_None_
##### Methods:
- `save(filename, data)`: 
  - Arguments:
    - `filename` - > Default: None | A string containing pickle filename (no need to write _pkl_ extension at the end) in which you want to write data inside the directory `~/datasets/`
    - `data` -> Default: None | The data which you want to save inside filename.
  - Purpose: It will be used to save or write data in the pkl file.
  - Attribute Updates: _False_
  - Associated Method: _False_
  - Return: A `list` containing following
    - `[True]`: If file saved successfully
    - `[False, err]`: If file not saved, then return `False` and a string `err` containing error information.
- `load(filename)`: 
  - Arguments:
    - `filename` - > Default: None | A string containing pickle filename (no need to write _pkl_ extension at the end) which you want to load from the directory `~/datasets/`
  - Purpose: It will be used to load or read data in the pkl file.
  - Attribute Updates: _False_
  - Associated Method: _False_
  - Return: It will return following:
    - `data`: if file loaded or read successfully then it will return data from the source filename
    - `[False, err]`: If file not loaded, then return `False` and a string `err` containing error information.
- `saveClusterMoviesDataset(data)`: 
  - Arguments:
    - `data` - > Default: None | A data which you want to save in the location `~/datasets/clusters_movies_dataset.pkl`.
  - Purpose: It will save data in the location `~/datasets/clusters_movies_dataset.pkl`. It is designed to save list of clusters movies dataframes.
  - Attribute Updates: _None_
  - Associated Method: `save(filename)`
  - Return: A `list` containing following
    - `[True]`: If file saved successfully
    - `[False, err]`: If file not saved, then return `False` and a string `err` containing error information.
- `loadClusterMoviesDataset()`: 
  - Arguments: _None_
  - Purpose: It will load data from location `~/datasets/clusters_movies_dataset.pkl`. It is designed to load list of clusters movies dataframes.
  - Attribute Updates: _None_
  - Associated Method: `load(filename)`
  - Return: It will return following:
    - `data`: if file loaded or read successfully then it will return data from the source filename
    - `[False, err]`: If file not loaded, then return `False` and a string `err` containing error information.
- `saveUsersClusters(data)`: 
  - Arguments:
    - `data` - > Default: None | A data which you want to save in the location `~/datasets/users_clusters.pkl`.
  - Purpose: It will save data in the location `~/datasets/users_clusters.pkl`. It is designed to save dataframe of users clusters.
  - Attribute Updates: _None_
  - Associated Method: `save(filename)`
  - Return: A `list` containing following
    - `[True]`: If file saved successfully
    - `[False, err]`: If file not saved, then return `False` and a string `err` containing error information.
- `loadUsersClusters()`: 
  - Arguments: _None_
  - Purpose: It will load data from location `~/datasets/users_clusters.pkl`. It is designed to load dataframe of users clusters.
  - Attribute Updates: _None_
  - Associated Method: `load(filename)`
  - Return: It will return following:
    - `data`: if file loaded or read successfully then it will return data from the source filename
    - `[False, err]`: If file not loaded, then return `False` and a string `err` containing error information.
#### 4. kmeansModel
Import it as `from Modules.kmeansModel import kmeansModel`

**Purpose**: It will be used to make clusters of users, clusters movies lists, methods to fix small clusters.
**Inherits**: This method inherits `KMeans` and `saveLoadFiles` classes. So, it inhertis all the properties of `KMeans` algorithm of `sklearn` library and `saveLoadFiles` module.

Create instance of kmeansModel as
```
YOUR_VAR_NAME = kmeansModel()
```
- Arguments: _None_
##### Attributes:
- **It inherits all the attributes of `KMeans` class/object of `sklearn`**.
- **users_cluster** -> Default: None | It will be a pandas DataFrame of users clusters with structure `(Rows: The number of Users, Columns: ['userId', 'Cluster'])`.
- **clusters_movies_df** -> Default: None | It will be a list containing panda DataFrames of each cluster movies list with following structure `[dataframe_of_cluster_1, dataframe_of_cluster_2, ..., dataframe_of_cluster_N]` where each cluster DataFrame will be of following structure `(Rows: The number of movies in cluster, Columns: ['movieId', 'Counts'])` where `Counts` is the value telling the number of users in the clusters who has particular movie in their list.
##### Methods:
**It inherits all the methods of `saveLoadFiles`**
- `clustersMovies(users_cluster, users_data)`: 
  - Arguments:
    - `users_cluster` - > Default: None | A panda DataFrame containing users clusters as described in **Attributes**.
    - `users_data` - > Default: None | A panda DataFrame containing users data as described in following -> Module: `dataEngineering` -> Method: `loadUsersData(from_loc)` -> Arguments: `from_loc` -> csv file format.
  - Purpose: It will be used to prepare a list of panda DataFrames containing each cluster movies as structure described in **Attributes** -> **clusters_movies_df**.
  - Attribute Updates: _None_
  - Associated Method: _None_
  - Return: A list of panda DataFrames containing each cluster movies with structure described in **Attributes** -> **clusters_movies_df**
- `fixClusters(clusters_movies_dataframes, users_cluster_dataframe, users_data, smallest_cluster_size = 11)`: 
  - Arguments:
    - `clusters_movies_dataframes` - > Default: None | A panda DataFrame obtained from `clustersMovies` method.
    - `users_cluster_dataframe` - > Default: None | A panda DataFrame with structure and information as described in **Attributes** -> **users_cluster**.
    - `users_data` - > Default: None | A panda DataFrame of users detail. For structure see -> Module: `dataEngineering` -> Method: `loadUsersData(from_loc)` -> Arguments: `from_loc` -> csv file format.
    - `smallest_cluster_size` - > Default: 11 | An `int` value indicating the smallest cluster size. See below _Purpose_
  - Purpose: It will be used to fix small clusters whose sizes are less than `smallest_cluster_size`. The small clusters will be deleted and the users belonging to those clusters will be shifted to others clusters which containing more relevant data with highest probability and users with more similar taste of them. Also the cluster in which users will be shifted will also updated with small clusters users records.
  - Attribute Updates: _None_
  - Associated Method: `getMyMovies() from userRequestedFor`: `userRequestedFor` is a module, read docs below in section 5.
  - Return: A `tuple` containing following:
    - Updated and fixed `clusters_movies_dataframes`
    - Updated and fixed `users_cluster_dataframe`
- `run_model(sparseMatrix = None, fix_clusters = True, smallest_cluster = 6)`: 
  - Arguments:
    - `sparseMatrix` - > Default: None | A sparse matrix which can be obtained from `dataEngineering().prepSparseMatrix()`. See `dataEngineering` module
      **Note**: If not given, then it will calculate byself by using default location of `from_loc`. If you're using a different type data source to load model, then run it yourself.
    - `fix_clusters` - > Default: True | `fixClusters` method will be called if _True_ or _Default_ to fix small clusters which are not enough for making recommendation.
    - `smallest_cluster` - > Default: 6 | Needed only if `fix_clusters` is _True_. The smallest cluster size which we want.
  - Purpose: It is the K-Means model which will run to make users clusters and each cluster movies collections based on matrix provided in `sparseMatrix`. This method will call itself `loadUsersData() from dataEngineering` to load users data as given in method `loadUsersData()`.
  - Attribute Updates: `users_cluster` and `clusters_movies_df`.
  - Associated Method: `clustersMovies`, `fixClusters`, `prepSparseMatrix() from dataEngineering` and `loadUsersData() from dataEngineering`.
  - Return: A `list` of length 2
    - Index 0:
      _True_: If run successfully
      _False: If any error arise.
    - Index 1:
      If Index 0 is _True_: A `dict` with following format 
      ```
      {'users_cluster': users_cluster, 'clusters_movies_df': clusters_movies_df}
      ```
      If Index 0 is _False_: A `str` containing error information.
- `saveFiles`: 
  - Arguments: _None_
  - Purpose: To save training data after call of `run_model` into files at default locations provided in `saveLoadFiles` module.
  - Attribute Updates: _None_
  - Associated Method: `saveClusterMoviesDataset(data)` and `saveUsersClusters(data)`
  - Return: A `list` of length 2
    - Index 0:
      _True_: If files saved successfully.
      _False_: Else
    - Index 1:
      A `str` containing information of success or error.
