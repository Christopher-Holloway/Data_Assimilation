import csv
import geohash
import collections

### Open csv file with twitter data

tweets = [] #Create empty list to store tweets
with open('geo_tweets_2013_04_15.csv','rb') as file:
	reader = csv.reader(file)
	next(reader,None) #Remove header
	for row in reader:
		tweets.append(row) #Place tweets into list


### Create empty lists to place lat and lon from tweets

lats = []
lons = []

### Grab lat and lon data from the tweets

for row in range(len(tweets)):
	if tweets[row][2] and tweets[row][3]: #Skip tweets without lat and lon data
		lats.append(tweets[row][2])
		lons.append(tweets[row][3])

### Create new lists for lat and lon data as float points, and create list to store geohashes

lats_fin = []
lons_fin = []
geocode = []
parent_geocode = []

### Change lat and lons from string into float data since geohash needs floats

for row in range(len(lons)):
	lats_fin.append(float(lats[row]))
	lons_fin.append(float(lons[row]))

### Create geohashes with precision 5

for row in range(len(lons_fin)):
	geocode.append(geohash.encode(lats_fin[row], lons_fin[row], precision=5))
	parent_geocode.append(geohash.encode(lats_fin[row], lons_fin[row], precision=4))

### Sort and find unique geohashes and store in a dict

#sorted_codes=sorted(geocode)
#counts=collections.Counter(sorted_codes)

parent_count = collections.Counter(parent_geocode)
count = collections.Counter(geocode)

#with open('twitter_geohash5_perc.txt','w') as f:
#	for key in sorted(parent_count.keys()):
#		for k in sorted(count.keys()):	
#			if k.startswith(key):
#				f.write('%s	%s\n' % (k, float(count[k])/parent_count[key]))

#parent_count = [(k,v) for k,v in parent_count.iteritems()]
#count = [(k,v) for k,v in count.iteritems()]
#parent_count = sorted(parent_count)
#count = sorted(count)

#with open('twitter_geohash5_counts.txt', 'w') as f:
#	for key, value in count.items():
#		f.write('%s	%s\n' % (key,value))

with open('twitter_geohash4_counts.txt', 'w') as f:
	for key, value in parent_count.items():
		f.write('%s	%s\n' % (key,value))




#keywords = []
#
#with open('twitter_geohash4_counts.txt','r') as list_file:
#	for line in list_file:
#		if line.strip():
#			keywords.append(line.split('\t')[0])
#
#test=[]
#with open('twitter_geohash5_counts.txt','r') as master_file:
#	with open('test_twitter_counts.txt', 'w') as search_results:
#		for line in master_file:
#			#print "line", line
#			test.append(line.split('\t')[0])
#			print "test", test
#			#if set(line.split('\t')[:-1]) & keywords:
#			#	search_results.write(line)
#			#	print "line",line







#test = []
#testt = []
#for key in sorted(counts.keys()):
#	test.append(counts[key])
#	testt.append(key)

### Write geohashes and counts into a file

#with open('twitter_geohash_counts.txt', 'w') as f:
#	for key, value in counts.items():
#		f.write('%s	%s\n' % (key,value))
#f.close()

#twit=[]
#with open('twitter_geohash_counts.txt','r') as r:
#	reader = csv.reader(r, delimiter='\t')
#	for row in reader:
#			twit.append(row)
#
#mini = []
#with open('minneapolis_counts.txt','rb') as f:
#	reader = csv.reader(f, delimiter='\t')
#	for row in reader:
#			mini.append(row)
#
#print "mini", mini
#
#mini_hashs=[]
#for row in range(len(mini)):
#	mini_hashs.append(mini[row][0])
#
#result = [x for x in counts.keys() if x[0] in mini_hashs]
#print "result", result

























