# -*- coding: utf-8 -*-
"""
Created on Tue Aug 18 16:55:45 2020

@author: asdka
"""

class loadRequirements:
    def loadLiabraries(self):
        print('loadRequirements -> loadLiabraries: Please wait while loading liabraries...')
        import pandas as pd
        print('Pandas version: ', pd.__version__)
        
        import numpy as np
        print('NumPy version: ', np.__version__)
        
        import matplotlib
        print('Matplotlib version: ', matplotlib.__version__)
        
        from matplotlib import pyplot as plt
        
        import sklearn
        print('Scikit-Learn version: ', sklearn.__version__)
        
        from sklearn.feature_extraction.text import CountVectorizer
        
        from sklearn.cluster import KMeans
        
        
        import pickle
        print('Pickle version: ', pickle.format_version)
        
        import sys
        print('Sys version: ', sys.version[0:5])
        
        from sys import exc_info
        
        import ast
        print('loadRequirements -> loadLiabraries: All liabraries loaded successfully.')