import geohash
import collections
import sqlite3
import time

#global variables
#'with great power comes great responsibility' Uncle Ben, spiderman
geoname_count = {}
hotelbase_count={}
counter = 0 
#conn = sqlite3.connect('rockstar_02.db', isolation_level='DEFERRED')
#cursor = conn.cursor()

for line in open('US.txt','rU'):
	counter += 1
	#if counter > 1:
	#		print line
	#	break
	line = line.strip()
	parts = line.split('\t')
	if len(parts)< 17:
		#ignore lines with less than 17 elements
		continue
	title, admin1, lat, lon, tag = parts[1], parts[10], float(parts[4]), float(parts[5]), parts[7]
	if admin1 == 'VA' and tag == 'BCH':
		geo5= (geohash.encode(lat,lon,precision=5))
		print parts
		print lat, lon, geo5, tag
		geoname_count[geo5] = geoname_count.get(geo5,0) + 1

for geohash_key, count_value in geoname_count.items():
	print "geo5, population count: %s\t%s" %(geohash_key, count_value)
	#this next line updates individual rows of the database
	#cursor.execute('UPDATE boxes set road_jct_count0=? where geohash=?',(count_value, geohash_key))
#this next line commits all values to the database
#conn.commit()