"""
This program loads a bunch of cellphone towers into memory and then 
populates a database of distances from geohash5 centroids to their nearest corresponding
cellphone tower.

"""
from geoindex import GeoGridIndex, GeoPoint
import sqlite3
import time
import shapefile

MINIMUM_DISTANCE = 50.0

class DistanceCalculator(object):
	def __init__(self):
		self.geo_index = GeoGridIndex(precision=3)
		self.conn = sqlite3.connect('rockstar_02.db',isolation_level="DEFERRED")
		self.conn.text_factory = str
		self.cursor = self.conn.cursor()
		self.debug = False

	def load_index(self, input=None):
		"""
		Load all of the geolocated cemetery towers into memory,
		inside of our geo_index variable
		"""
		print 'Loading locations of interest into internal spatial index.'
		input_counter = 0
		sf = shapefile.Reader('/Users/chrisholloway/Downloads/virginia-latest-free.shp/gis.osm.roads_free_1.shp')
		shaperec = sf.shapeRecords()
		motorway_hash=[]
		for rec in range(len(shaperec)):
			if 'motorway_link' in shaperec[rec].record[2]:
				lat = shaperec[rec].shape.points[0][1]
				lon = shaperec[rec].shape.points[0][0]
				self.geo_index.add_point(GeoPoint(lat,lon))
				input_counter +=1
		print 'Done loading index of motorway_links (added %s values)' %(input_counter)

	def enumerate_all_distances(self, admin1=None):
		"""
		Walk the geohash5 centroids,
		calculate the distance to the nearest tower for each one,
		and write the distance value to the database.
		"""
		#Walk the geohash5 centroids,
		c = self.cursor
		c.execute('SELECT geohash, centroid_lat, centroid_lon from boxes where admin1=?',(admin1,))
		geohashes_plus_coords = []
		for row in c.fetchall():
			geo5_item, lat, lon = row
			geohashes_plus_coords.append([geo5_item, lat, lon])
			#print geo5_item
		#print 'Those are the geohashes'
		progress_counter = 0
		for geo5, lat, lon in geohashes_plus_coords:
			progress_counter +=1
			if progress_counter % 50 == 0:
				print 'Processed %s records.' %(progress_counter)
			if self.debug == True:
				print '--------'
				print 'geohash of interest:',geo5, lat, lon
			#calculate the distance to the nearest tower for each one,
			temp_geo_point = GeoPoint(lat,lon)
			values = self.geo_index.get_nearest_points(temp_geo_point, 50.0, 'km')
			#print values
			minimum_distance = MINIMUM_DISTANCE
			for value in values:
				the_point, the_distance = value
				if the_distance < minimum_distance:
					minimum_distance = the_distance

			#and write the distance value to the database.
			c.execute('UPDATE boxes set motorway_link_distance=? where geohash=?',(minimum_distance,geo5))
		self.conn.commit()
		print 'Finished updating distance from geo5 centroids to input data'



def main():
	"""
	Instantiate a DistanceCalculator object,
	load tower locations into a spatial index using https://github.com/gusdan/geoindex
	enumerate all geohash5, and compute the nearest tower distance for each one
	then store the results
	"""
	distance_calc = DistanceCalculator()
	input_file = '/Users/chrisholloway/Downloads/virginia-latest-free.shp/gis.osm.roads_free_1.shp'
	distance_calc.load_index(input=input_file)
	distance_calc.enumerate_all_distances(admin1='Virginia')


if __name__ == '__main__':
	main()
