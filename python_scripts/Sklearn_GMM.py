from __future__ import print_function
import sqlite3
import pandas as pd
from sklearn import mixture
import geohash
import heatmap

conn = sqlite3.connect('/Users/chrisholloway/work/geonames/US/rockstar_02.db', isolation_level='DEFERRED')
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

clf = mixture.GMM(n_components=6, covariance_type='full', random_state=7)
clusters = clf.fit(X)
cluster_means = clusters.means_
print(cluster_means)
cluster_predict = clusters.predict(X)

#lons = dataset[:,3]
#lats = dataset[:,2]
#pts = zip(lons,lats)
lons = []
lats = []
for i in range(len(cluster_predict)):
	if cluster_predict[i] == 5:
		lons.append(dataset[i,3])
		lats.append(dataset[i,2])

pts = zip(lons,lats)
hm = heatmap.Heatmap()
hm.heatmap(pts,dotsize=10,opacity=255, scheme='omg')
hm.saveKML("cluster5.kml")
#with open('/Users/chrisholloway/test/geohash2kml-master/cluster.csv','w') as f:
#	for i in range(len(cluster_predict)):
#		f.write('%s,%s\n' % (geohash[i],cluster_predict[i]))
#f.close()