import shapefile
import geohash
import collections
import sqlite3


conn = sqlite3.connect('rockstar_02.db', isolation_level='DEFERRED')
cursor = conn.cursor()

sf = shapefile.Reader('/Users/chrisholloway/Downloads/virginia-latest-free.shp/gis.osm.roads_free_1.shp')
shaperec = sf.shapeRecords()
motorway_hash=[]
for rec in range(len(shaperec)):
	if 'motorway_link' in shaperec[rec].record[2]:
		 motorway_hash.append(geohash.encode(shaperec[rec].shape.points[0][1],shaperec[rec].shape.points[0][0], precision=5))


motorway_hash_count = collections.Counter(motorway_hash)
for geohash_key, count_value in motorway_hash_count.items():
	print "geo5, motorway_hash_count count: %s\t%s" %(geohash_key, count_value)
	#this next line updates individual rows of the database
	cursor.execute('UPDATE boxes set motorway_link_count0=? where geohash=?',(count_value, geohash_key))

#this next line commits all values to the database
conn.commit()