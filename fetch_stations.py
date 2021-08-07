from requests import get
import json
from pprint import pprint

from math import radians, cos, sin, asin, sqrt

#DEFINE YOUR LATITUDE AND LONGITUDE
my_lat = float(input("Enter Latitude (degrees): ")) #40.2288699
my_lon = float(input("Enter Longitude (degrees): ")) #-8.4863146

url_stations = 'https://apex.oracle.com/pls/apex/raspberrypi/weatherstation/getallstations'
stations = get(url_stations).json()['items']
#pprint(stations)
url_weather0 = 'https://apex.oracle.com/pls/apex/raspberrypi/weatherstation/getlatestmeasurements/'


#FIND DISTANCE FROM MY LOCATION TO WEATHER STATIONS
def haversine(lon1, lat1, lon2, lat2):
    #convert degrees to radians
    lon1 = radians(lon1)
    lat1 = radians(lat1)
    lon2 = radians(lon2)
    lat2 = radians(lat2)

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    distance = 2 * asin(sqrt(a)) * 6371 #6371 is the radius of the Earth

    return distance

#FIND CLOSEST WEATHER STATIONS
def find_closest():
    closest_station = 0
    closest_station2 = 0
    smallest = 99999
    for st in stations:
        station_lon = st['weather_stn_long']
        station_lat = st['weather_stn_lat']
        dist = haversine(my_lon, my_lat, station_lon, station_lat)
        if dist < smallest:
            smallest = dist
            closest_station3 = closest_station2
            closest_station2 = closest_station
            closest_station = st['weather_stn_id']
    return [closest_station, closest_station2, closest_station3]

#FIND CLOSEST WEATHER DATA - IF NOT THE CLOSEST, THE 2ND OR 3RD
closest_stn = find_closest()
weather1 = url_weather0 + str(closest_stn[0])
weather2 = url_weather0 + str(closest_stn[1])
weather3 = url_weather0 + str(closest_stn[2])
my_weather1 = get(weather1).json()['items']
my_weather2 = get(weather2).json()['items']
my_weather3 = get(weather3).json()['items']
if not my_weather1:
    if not my_weather2:
        pprint(my_weather3)
    else:
        pprint(my_weather2)
elif (not my_weather2 and not my_weather3):
    pprint(my_weather1)    
