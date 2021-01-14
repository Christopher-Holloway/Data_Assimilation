from __future__ import print_function
import sqlite3
import pandas as pd

from sklearn.naive_bayes import GaussianNB
from sklearn.cross_validation import  cross_val_score
from sklearn.cross_validation import  cross_val_predict
from sklearn.preprocessing import StandardScaler
from scipy.sparse import coo_matrix
from sklearn.utils import resample

#Connect to database and load dataset
conn = sqlite3.connect('rockstar_02.db', isolation_level='DEFERRED')
dataframe = pd.read_sql_query("SELECT * FROM boxes", conn)
dataset = dataframe.values

#Build Contingency Matrix
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


gnb = GaussianNB()
scores = cross_val_score(gnb, X, Y, cv=10)
print("Running Gaussian Naive Bayes classification model")
print("mean: {:.3f} (std: {:.3f})".format(scores.mean(),
                                          scores.std()),
                                          end="\n\n" )

y_pred = cross_val_predict(gnb, X, Y, cv=10)
cm = contingency_matrix(y_pred)

conn.close()