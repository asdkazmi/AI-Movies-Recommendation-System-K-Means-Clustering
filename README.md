# AI-Movies-Recommendation-System-K-Means-Clustering
This is repository for a project of AI movies recommendation system based on k-means clustering algorithm with Flask-RESTFUL APIs. An associated article is published on medium, read it here
[AI Movies Recommendation System Based on K-Means Clustering Algorithm](https://medium.com/@asdkazmi/ai-movies-recommendation-system-with-clustering-based-k-means-algorithm-f04467e02fcd)

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
3. kmeansModel
4. saveLoadFiles
5. userRequestedFor
#### 1. dataEngineering
Import it as `from Modules.dataEngineering import dataEngineering`
dataEngineering is a class which will be used to prepare data for k-means clustering model
create instance of dataEngineering as
```
YOUR_VAR_NAME = dataEngineering()
```
##### Attributes:
- **users** -> Default: None | It will be a list of users IDs in descending order.
- **users_movies_list** -> Default: None | It will be list of strings where each string will contain user movies separated by comma ",".
##### Methods:
- `loadUsersData(from_loc)`
  - Arguments:
    - `from_loc` -> Default: './Prepairing Data/From Data/filtered_ratings.csv' | Must be a string with valid location of data _csv_ file. _csv_ file format must be following
      
      _csv_ file format -> Number of Rows: Any | Columns: `['userId', 'movieId']` where `'userId'` column should contain IDs of users and `'movieId'` column should contain ID of movie which user has added into his favorite OR has watched OR any other type on which you want to make recommendations. `'userId'` column could contain multiple entries of same ID.
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
  - Attribute Updates: `users`, `users_movies_list`
  - Associated Method: `loadUsersData(from_loc)`
  - Return: _Nothing_
- `prepSparseMatrix(from_loc)`: 
  - Arguments: 
    - `from_loc` -> It will be used with associated method `moviesListForUsers(from_loc)`. It is required only if attribute **users_movies_list** not updated and still `None`. See `loadUsersData(from_loc)` method docs for further detail on `from_loc` argument.
  - Attribute Updates: _No_
  - Associated Method: `moviesListForUsers(from_loc)` -> If attribute **users_movies_list** is `None`.
  - Return: Python `list` of length 2.
    - Index 0: 
      - `True`: If method runs successfully.
    - Index 1:
      - `dict` with following format 
        ```
        {'sparse_matrix': It will be a sparse matrix (NumPy Array) with dimensions `(Number of Users, Number of Movies)` with value `1` if users has movie in its list, otherwise `0`,
         'feature_names': It will be an array containing all movies IDs in the same order as the columns in **sparseMatrix**}
        ```
- `showSparseMatrix(sparseMatrix, feature_names, users)`: 
  - Arguments:
    - `sparseMatrix` -> A sparse matrix obtained from `prepSparseMatrix(from_loc)` method.
    - `feature_names` -> An array of feature names obtained from `prepSparseMatrix(from_loc)` method.
    - `users` -> An array of users IDs saved in **users** attribute if not `None`.
  - Attribute Updates: _False_
  - Associated Method: _No_
  - Return: Panda DataFrame with presentation of sparse matrix containing indexes with users IDs and columns with movies IDs.
