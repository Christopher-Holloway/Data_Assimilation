import sqlite3
import pandas as pd

#Connect to database and load dataset
conn = sqlite3.connect('rockstar_02.db', isolation_level='DEFERRED')
dataframe = pd.read_sql_query("SELECT * FROM boxes", conn)

# minimum = dataframe.groupby('admin2').min()
# minimum = minimum.values
# minimum = minimum[:,8:]

#maximum = dataframe.groupby('admin2').max()
#maximum = maximum.values
#maximum = maximum[:,8:]

#mean = dataframe.groupby('admin2').mean().fillna(dataframe.groupby('admin2').last())
mean = dataframe.groupby('admin2').mean()
mean = mean.values
mean = mean[:,3:]

std = dataframe.groupby('admin2').std()
std = std.values
std = std[:,3:]
admin2=dataframe.admin2.unique()

#cursor = conn.cursor()
#cursor.execute('''CREATE TABLE Minimums (twitter_count0 numeric,
#	twitter_ratio0 numeric, population_count0 numeric, population_smooth_count0 numeric, cellphonetower_count0 numeric, 
#	cellphonetower_ratio0 numeric, airport_distance numeric, cellphonetower_distance numeric, starbucks_distance numeric,
#	cemetery_distance numeric, cemetery_count0 numeric, med_cent_count0 numeric, med_cent_distance numeric, farm_count0 numeric,
#	farm_distance numeric, prison_count0 numeric, prison_distance numeric, restaraunt_count0 numeric, restaraunt_distance numeric,
#	stadium_count0 numeric, stadium_distance numeric, parks_count0 numeric, parks_distance numeric, office_building_distance numeric,
#	office_building_count0 numeric, hospital_distance numeric, hospital_count0 numeric, gold_course_distance numeric, gold_course_count0 numeric,
#	motorway_link_distance numeric, motorway_link_count0 numeric, turnk_link_distance numeric, trunk_link_count0 numeric, 
#	primary_link_distance numeric, primary_link_count0 numeric, secondary_link_distance numeric, secondary_link_count0 numeric, 
#	university_distance numeric, beach_distance numeric, hotel_count0 numeric, test_hotel_count0 numeric, yelp_hotel_count0 numeric)''')
#conn.commit()
#cursor.executemany('''insert into Minimums values (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)''',map(tuple,minimum.tolist()))
#conn.commit()

#cursor = conn.cursor()
#cursor.execute('''CREATE TABLE Maximums (twitter_count0 numeric,
#	twitter_ratio0 numeric, population_count0 numeric, population_smooth_count0 numeric, cellphonetower_count0 numeric, 
#	cellphonetower_ratio0 numeric, airport_distance numeric, cellphonetower_distance numeric, starbucks_distance numeric,
#	cemetery_distance numeric, cemetery_count0 numeric, med_cent_count0 numeric, med_cent_distance numeric, farm_count0 numeric,
#	farm_distance numeric, prison_count0 numeric, prison_distance numeric, restaraunt_count0 numeric, restaraunt_distance numeric,
#	stadium_count0 numeric, stadium_distance numeric, parks_count0 numeric, parks_distance numeric, office_building_distance numeric,
#	office_building_count0 numeric, hospital_distance numeric, hospital_count0 numeric, gold_course_distance numeric, gold_course_count0 numeric,
#	motorway_link_distance numeric, motorway_link_count0 numeric, turnk_link_distance numeric, trunk_link_count0 numeric, 
#	primary_link_distance numeric, primary_link_count0 numeric, secondary_link_distance numeric, secondary_link_count0 numeric, 
#	university_distance numeric, beach_distance numeric, hotel_count0 numeric, test_hotel_count0 numeric, yelp_hotel_count0 numeric)''')
#conn.commit()
#cursor.executemany('''insert into Maximums values (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)''',map(tuple,maximum.tolist()))
#conn.commit()

cursor = conn.cursor()
#cursor.execute('''CREATE TABLE Means (twitter_count0 numeric,
#	twitter_ratio0 numeric, population_count0 numeric, population_smooth_count0 numeric, cellphonetower_count0 numeric, 
#	cellphonetower_ratio0 numeric, airport_distance numeric, cellphonetower_distance numeric, starbucks_distance numeric,
#	cemetery_distance numeric, cemetery_count0 numeric, med_cent_count0 numeric, med_cent_distance numeric, farm_count0 numeric,
#	farm_distance numeric, prison_count0 numeric, prison_distance numeric, restaraunt_count0 numeric, restaraunt_distance numeric,
#	stadium_count0 numeric, stadium_distance numeric, parks_count0 numeric, parks_distance numeric, office_building_distance numeric,
#	office_building_count0 numeric, hospital_distance numeric, hospital_count0 numeric, gold_course_distance numeric, gold_course_count0 numeric,
#	motorway_link_distance numeric, motorway_link_count0 numeric, turnk_link_distance numeric, trunk_link_count0 numeric, 
#	primary_link_distance numeric, primary_link_count0 numeric, secondary_link_distance numeric, secondary_link_count0 numeric, 
#	university_distance numeric, beach_distance numeric, hotel_count0 numeric, test_hotel_count0 numeric, yelp_hotel_count0 numeric)''')
#conn.commit()
#cursor.executemany('''insert into Means values (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)''',map(tuple,mean.tolist()))
#conn.commit()

cursor = conn.cursor()
cursor.execute('''CREATE TABLE StdDevs (twitter_count0 numeric,
	twitter_ratio0 numeric, population_count0 numeric, population_smooth_count0 numeric, cellphonetower_count0 numeric, 
	cellphonetower_ratio0 numeric, airport_distance numeric, cellphonetower_distance numeric, starbucks_distance numeric,
	cemetery_distance numeric, cemetery_count0 numeric, med_cent_count0 numeric, med_cent_distance numeric, farm_count0 numeric,
	farm_distance numeric, prison_count0 numeric, prison_distance numeric, restaraunt_count0 numeric, restaraunt_distance numeric,
	stadium_count0 numeric, stadium_distance numeric, parks_count0 numeric, parks_distance numeric, office_building_distance numeric,
	office_building_count0 numeric, hospital_distance numeric, hospital_count0 numeric, gold_course_distance numeric, gold_course_count0 numeric,
	motorway_link_distance numeric, motorway_link_count0 numeric, turnk_link_distance numeric, trunk_link_count0 numeric, 
	primary_link_distance numeric, primary_link_count0 numeric, secondary_link_distance numeric, secondary_link_count0 numeric, 
	university_distance numeric, beach_distance numeric, hotel_count0 numeric, test_hotel_count0 numeric, yelp_hotel_count0 numeric)''')
conn.commit()
cursor.executemany('''insert into StdDevs values (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)''',map(tuple,std.tolist()))
conn.commit()

cursor.close()
conn.close()