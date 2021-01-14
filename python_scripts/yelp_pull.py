from yelp.client import Client
from yelp.oauth1_authenticator import Oauth1Authenticator

auth = Oauth1Authenticator(
    consumer_key=YoSLC-Eyjyj5BPG6ZX-0OUA,
    consumer_secret=ko6RY2I1CD1hPgDT2jCI0w0vn48,
    token=0uzdrsOdbua5Ysq0fGYxOHebYPl7YAf5,
    token_secret=raCdl7sc6d5b-FzHUQ-agDZ5C78
)
client = Client(auth)

params = {'category_filter': 'hotels', 'radius_filter': 5000}

hash5 = []
#counts = []
for line in open('/Users/chrisholloway/database/VA_lat_lon_pop.csv','rU'):
	parts = line.split(',')
	lat, lon = float(parts[0]), float(parts[1])
	hash5.append(geohash.encode(lat,lon,precision=5))


	#geo_hotels = client.search_by_coordinates(lat,lon, **params)
	#counts.append(len(geo_hotels.businesses))
	#for hotel in range(len(geo_hotels.businesses)):


