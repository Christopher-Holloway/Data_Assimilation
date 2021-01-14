import geohash
import collections
import sqlite3
import time

#global variables
#'with great power comes great responsibility' Uncle Ben, spiderman
geohash_count = {}
counter = 0 
conn = sqlite3.connect('rockstar_02.db', isolation_level='DEFERRED')
cursor = conn.cursor()

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
	admin1, lat, lon, tag = parts[10], float(parts[4]), float(parts[5]), parts[7]
	if admin1 == 'VA' and tag == 'REST':
		geo5= (geohash.encode(lat,lon,precision=5))
		print lat, lon, geo5, tag
		geohash_count[geo5] = geohash_count.get(geo5,0) + 1

for geohash_key, count_value in geohash_count.items():
	print "geo5, population count: %s\t%s" %(geohash_key, count_value)
	#this next line updates individual rows of the database
	cursor.execute('UPDATE boxes set restaurant_count0=? where geohash=?',(count_value, geohash_key))
#this next line commits all values to the database
conn.commit()