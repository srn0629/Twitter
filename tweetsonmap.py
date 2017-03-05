#Savanna Nagorski
#TGIS 501
#March 3, 2016
#Search Tweets from Twitter, place them on a Leaflet map

from TwitterSearch import *
import folium
import webbrowser
import os
import time
from geopy import geocoders
from geopy.exc import GeocoderTimedOut

#Define geocoding functions
def geo(location):     
	g = geocoders.Nominatim()     
	loc = g.geocode(location)     
	return (loc.latitude), (loc.longitude)

#Define our map location and settings
while True:
	where = raw_input("Where do you want a map of? Please include city, state and/or country!")
	try:
		map2 = folium.Map(location=geo(where), tiles='Stamen Toner', zoom_start=8)
	except AttributeError:
		print "Please try again with a real place!"
	else:
		break

#Let's begin defining the Tweets we want to search for
try:     
	tso = TwitterSearchOrder() 				#Create a TwitterSearchOrder objec  
	tso.set_keywords(['University of Washington Tacoma']) 	#Let's define all words we would like to have a look for
	tso.set_language('en')					#Searches only tweets in English
	tso.set_include_entities(False) 			#Don't include all that entity information
   #Object creation with secret token - get your at https://apps.twitter.com/ and create a new app  
	ts = TwitterSearch(
    	consumer_key = 'ENTER YOUR CONSUMER KEY HERE',         
    	consumer_secret = 'ENTER YOUR CONSUMER SECRET HERE',         
    	access_token = 'ENTER YOUR ACCESS TOKEN HERE',         
    	access_token_secret = 'ENTER YOUR ACCESS TOKEN SECRET HERE'      
    )
    #This is where the fun actually starts - iterate through tweets to find location data  
	for tweet in ts.search_tweets_iterable(tso):         
		USER = tweet['user']['screen_name']		#Use for defining and printing tweets
		TWEET = tweet['text']
		tweets = USER +" tweeted: "+ TWEET
		if tweet['place'] is not None:
			#Allow the geocoder to rest
			time.sleep(.1)
			(lat, lng) = geo(tweet['place']['full_name'])             
			print ( '@%s tweeted: %s' % ( USER, TWEET ) ) + 'And they said it from (' + str(lat) +', ' +str(lng)+')'
			#Modified marker for pins on the map
			folium.Marker(location =geo(tweet['place']['full_name']) , popup= tweets, icon=folium.Icon(color = 'purple')).add_to(map2)
		else:             
			pass
		
except AttributeError:
	pass

except TwitterSearchException as e				#Take care of all those ugly errors if there are some     
	print(e)

#Save map and open in web browser
map2.save('F:\UWT MS GT\TGIS_501\Lab_6\map2.html')
webbrowser.open('file://'+os.path.realpath('map2.html'))

print "There you have it!"
