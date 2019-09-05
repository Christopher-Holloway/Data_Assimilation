import pymapia as PyMapia  
import geohash
import time



for line in open('VA_lat_lon_centroid.csv'):
	line = line.strip()
	parts = line.split(',')
	lat, lon = float(parts[0]), float(parts[1])
	session = PyMapia.PyMapia("5CF5C382-654FAFA-4B2C501B-5B04BABB-60055776-793FC26A-A4CC3ADE-692F0E90")
	place = session.search_place('', lat, lon, category = ['50'], distance = 3000.0)

	count = place['found']
	hash5 = geohash.encode(lat,lon, precision = 5)
	print hash5, count


