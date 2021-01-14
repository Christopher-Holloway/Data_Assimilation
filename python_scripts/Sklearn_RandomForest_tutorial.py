from __future__ import print_function
import sqlite3
import pandas as pd


import os
import subprocess

from time import time
from operator import itemgetter
from scipy.stats import randint

import numpy as np
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import AdaBoostClassifier
from sklearn.tree import export_graphviz
from sklearn.grid_search import GridSearchCV
from sklearn.grid_search import RandomizedSearchCV
from sklearn.cross_validation import  cross_val_score
from sklearn.cross_validation import  cross_val_predict
from sklearn.preprocessing import StandardScaler
from scipy.sparse import coo_matrix
from sklearn.utils import resample


#Connect to database and load dataset
conn = sqlite3.connect('rockstar_02.db', isolation_level='DEFERRED')
dataframe = pd.read_sql_query("SELECT * FROM boxes", conn)
dataset = dataframe.values

"""Split dataset into input(X) and output(Y) variables,
where the first 9 columns are removed since they are identifiers and
population_count0, and the Y (hotel existance) variable is classified
by 1 if it exists in a particular geohash otherwise it is classified by 0
"""

X = dataset[:,10:-3].astype(float)
#X = StandardScaler().fit_transform(X)
Y = [0]*len(X)
for sample in range(len(X)):
  if dataset[sample,-1] > 0:
    Y[sample] += 1
X_sparse = coo_matrix(X)
X, X_sparse,  Y= resample(X, X_sparse, Y, random_state=0)
"""Build sklearn baseline decision tree, with known seed to ensure reproducibility

Parameters:
criterion = function to measure the quality of a split -> default = 'gini'
splitter = strategy used to choose the split at each node -> default = 'best'
max_features = nummber of features to consider when looking for best split -> default = None
max_depth = maxiumum depth of tree -> default = None
min_samples_split = minimum number of samples required to split an internal node -> default = 2
min_samples_leaf = minimum number of samples required to be at a leaf node -> default = 1
min_weight_fraction_leaf = minimum weighted fraction of the input samples required to be at a leaf node -> default = 0
max_leaf_nodes = grow a tree with max_leaf_nodes in best-first fashion -> default = None
class_weight = 
random_state = seed used by the random number generator -> default = None
presort = presort the data to speed up the finding of best splits in fitting -> default = False
"""

#Build sklearn decision tree using random grid search
def report(grid_scores, n_top=3):
    """Report top n_top parameters settings, default n_top=3.

    Args
    ----
    grid_scores -- output from grid or random search
    n_top -- how many to report, of top models

    Returns
    -------
    top_params -- [dict] top parameter settings found in
                  search
    """
    top_scores = sorted(grid_scores,
                        key=itemgetter(1),
                        reverse=True)[:n_top]
    for i, score in enumerate(top_scores):
        print("Model with rank: {0}".format(i + 1))
        print(("Mean validation score: "
               "{0:.3f} (std: {1:.3f})").format(
               score.mean_validation_score,
               np.std(score.cv_validation_scores)))
        print("Parameters: {0}".format(score.parameters))
        print("")

    return top_scores[0].parameters

def run_gridsearch(X, y, clf, param_grid, cv=5):
    """Run a grid search for best Decision Tree parameters.

    Args
    ----
    X -- features
    y -- targets (classes)
    cf -- scikit-learn Decision Tree
    param_grid -- [dict] parameter settings to test
    cv -- fold of cross-validation, default 5

    Returns
    -------
    top_params -- [dict] from report()
    """
    grid_search = GridSearchCV(clf,
                               param_grid=param_grid,
                               cv=cv)
    start = time()
    grid_search.fit(X, y)

    print(("\nGridSearchCV took {:.2f} "
           "seconds for {:d} candidate "
           "parameter settings.").format(time() - start,
                len(grid_search.grid_scores_)))

    top_params = report(grid_search.grid_scores_, 3)
    return  top_params

def run_randomsearch(X, y, clf, para_dist, cv=5,
                     n_iter_search=20):
    """Run a random search for best Decision Tree parameters.

    Args
    ----
    X -- features
    y -- targets (classes)
    cf -- scikit-learn Decision Tree
    param_dist -- [dict] list, distributions of parameters
                  to sample
    cv -- fold of cross-validation, default 5
    n_iter_search -- number of random parameter sets to try,
                     default 20.

    Returns
    -------
    top_params -- [dict] from report()
    """
    random_search = RandomizedSearchCV(clf,
                        param_distributions=param_dist,
                        n_iter=n_iter_search)

    start = time()
    random_search.fit(X, y)
    print(("\nRandomizedSearchCV took {:.2f} seconds "
           "for {:d} candidates parameter "
           "settings.").format((time() - start),
                               n_iter_search))

    top_params = report(random_search.grid_scores_, 3)
    return  top_params

def contingency_matrix(y_pred):
    TPt = 0
    TPf = 0
    FPt = 0
    FPf = 0
    for i in range(len(Y)):
      if Y[i] == 1 and y_pred[i] == 1:
        TPt += 1
      if Y[i] == 0 and y_pred[i] == 0:
        TPf += 1
      if Y[i] == 0 and y_pred[i] == 1:
        FPt += 1
      if Y[i] == 1 and y_pred[i] == 0:
        FPf += 1

    print("Number of mislabeled points out of a total %d points : %d"  % (X.shape[0],(Y != y_pred).sum()))
    print("Number of Recall(TPt) %d out of %d, percent = %f" % (TPt, sum(Y), float(TPt)/sum(Y)))
    print("Number of Recall(TPf) %d out of %d, percent = %f" % (TPf, (len(Y)-sum(Y)), float(TPf)/(len(Y)-sum(Y))))
    print("Number of FPt %d out of %d, percent = %f" % (FPt, (len(Y)-sum(Y)), float(FPt)/(len(Y)-sum(Y))))
    print("Number of FPf %d out of %d, percent = %f" % (FPf, sum(Y), float(FPf)/sum(Y)))

print("\n\n-- Testing default parameters...")
clf = RandomForestClassifier(class_weight='balanced', random_state=7) 
default = cross_val_score(clf, X_sparse, Y, cv=10)
print("mean: {:.3f} (std: {:.3f})".format(default.mean(),
                                          default.std()),
                                          end="\n\n" )
y_pred = cross_val_predict(clf, X_sparse, Y, cv=10)
cm_default = contingency_matrix(y_pred)

param_grid = {'criterion': ['gini','entropy'],
				'min_samples_split': [2,10,20],
				'random_state': [7],
				'max_depth': [None,3,4,5,10],
				'min_samples_leaf': [1,5,10],
				'max_leaf_nodes': [None, 5,10,15],
        'class_weight':['balanced']
        }

dt = RandomForestClassifier()
ts_gs = run_gridsearch(X_sparse, Y, dt, param_grid, cv=10)

print("\n-- Best Parameters:")
for k, v in ts_gs.items():
    print("parameters: {:<20s} setting: {}".format(k, v))

print("\n\n-- Testing best parameters [Grid]...")
dt_ts_gs = RandomForestClassifier(**ts_gs)
scores = cross_val_score(dt_ts_gs, X_sparse, Y, cv=10)
print("mean: {:.3f} (std: {:.3f})".format(scores.mean(),
                                          scores.std()),
                                          end="\n\n" )

y_pred_gs = cross_val_predict(dt_ts_gs, X_sparse, Y, cv=10)
cm_gs = contingency_matrix(y_pred_gs)

print("-- Random Parameter Search via 10-fold CV")

# dict of parameter list/distributions to sample
param_dist = {"criterion": ["gini", "entropy"],
              "min_samples_split": randint(1, 20),
              "max_depth": randint(2, 20),
              "min_samples_leaf": randint(1, 20),
              "max_leaf_nodes": randint(2, 20),
              "random_state": [7],
              "class_weight": ['balanced']
              }

dt = RandomForestClassifier()
ts_rs = run_randomsearch(X_sparse, Y, dt, param_dist, cv=10,
                         n_iter_search=300)

print("\n-- Best Parameters:")
for k, v in ts_rs.items():
    print("parameters: {:<20s} setting: {}".format(k, v))

# test the retuned best parameters
print("\n\n-- Testing best parameters [Random]...")
dt_ts_rs = RandomForestClassifier(**ts_rs)
scores = cross_val_score(dt_ts_rs, X_sparse, Y, cv=10)
print("mean: {:.3f} (std: {:.3f})".format(scores.mean(),
                                          scores.std()),
                                          end="\n\n" )

y_pred_rs = cross_val_predict(dt_ts_rs, X_sparse, Y, cv=10)
cm_rs = contingency_matrix(y_pred_rs)

conn.close()