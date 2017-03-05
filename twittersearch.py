#Savanna Nagorski
#TGIS 501
#Februar 29, 2016
#Search Twitter with Keyword, collect location data, create shapefile of location data in points

from TwitterSearch import *
from geopy import geocoders
import arcpy
from arcpy import env
env.workspace = '.../FILEPATH'
arcpy.env.overwriteOutput = True
fc = ".../FILE.shp"

#Create new feature class for your garden points, declare: outpath, name, type, optionals and spatial reference
arcpy.CreateFeatureclass_management(env.workspace, 'FILE.shp', "POINT", "", "", "", "WGS 1984")

fieldLength = 100

# Execute AddField twice for two new fields
arcpy.AddField_management(gardenfc, 'USER', "TEXT", "", "", fieldLength)
arcpy.AddField_management(gardenfc, 'TWEET', "TEXT", "", "", fieldLength)
cursor = arcpy.da.InsertCursor(gardenfc, ["SHAPE@", 'USER', 'TWEET'])		#insert cursor into Shape field of garden points

#define geocoding functions
def geo(location):     
	g = geocoders.Nominatim()     
	loc = g.geocode(location)     
	return float(loc.latitude), float(loc.longitude)	#Make location data readable in ArcGIS

#Let's beging searching Tweets
try:     
	tso = TwitterSearchOrder() 		#Create a TwitterSearchOrder object     
	tso.set_keywords(['University of Washington Tacoma']) #Let's define all words we would like to have a look for
	tso.set_language('en')			#Searches only tweets in English
	tso.set_include_entities(False)		#Don't include all that entity information
    
    #Object creation with secret token     
	ts = TwitterSearch(
    	consumer_key = 'YOUR CONSUMER KEY HERE',         
    	consumer_secret = 'YOUR CONSUMER SECRET HERE',         
    	access_token = 'YOUR ACCESS TOKEN HERE',         
    	access_token_secret = 'YOUR ACCESS TOKEN SECRET HERE'      
    )
    
     #This is where the fun actually starts - iterate through tweets to find location data
	for tweet in ts.search_tweets_iterable(tso):         
		USER = tweet['user']['screen_name']  #Use for fields while inserting row
		TWEET = tweet['text']  

		if tweet['place'] is not None:             
			(lat, lng) = geo(tweet['place']['full_name'])             
			print ( '@%s tweeted: %s' % ( USER, TWEET ) ) + 'And they said it from (' + str(lat) +', ' +str(lng)+')'

			gpoint = arcpy.Point(lng,lat)			#Create points in ArcGIS
			cursor.insertRow([gpoint, USER, TWEET]) 	#Add new point data	
	
		else:             
			pass
except TwitterSearchException as e: 		#Take care of all those ugly errors if there are some     
	print(e)

del cursor
