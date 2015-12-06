import urllib2
import xml.etree.ElementTree as xml
import os.path as systemfile
import math
import time

compassList = "N NNE NW ENE E ESE SE SSE S SSW SW WSW W WNW NW NNW"
compassDict = {}
compassTmpval = 0
for i in compassList.split(" "):
    compassDict[i] = compassTmpval
    compassTmpval += 22.5

metoffice_api_key = "6b57d1a1-0fc0-40dc-ae66-950b3ec03c4f"

site_list_url = "http://datapoint.metoffice.gov.uk/public/data/val/wxfcs/all/xml/sitelist?res=daily&key=" + metoffice_api_key
weather_url = "http://datapoint.metoffice.gov.uk/public/data/val/wxfcs/all/xml/%s?res=3hourly&key=" + metoffice_api_key

weather_site_filename = 'weather_sites.xml'

cache_expiry = 15 * 60  # 15 minutes

# Format of weather_cache => {id : (xml, expiry)}
weather_cache = {}


def get_nearest_weather_site(sites, lat=0.0, lon=0.0):
    site_distances = {}

    for site in sites:
        id = int(site.get('id'))
        site_lat = float(site.get('latitude'))
        site_lon = float(site.get('longitude'))

        distance = haversine(site_lon, site_lat, lon, lat)
        site_distances[id] = distance

    return min(site_distances.items(), key=lambda x: x[1])[0]  # finding the least value and then returning the key


def haversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance between two points
    on the earth (specified in decimal degrees)

    Found from stackoverflow
    """
    # convert decimal degrees to radians
    lon1, lat1, lon2, lat2 = map(math.radians, [lon1, lat1, lon2, lat2])

    # haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    c = 2 * math.asin(math.sqrt(a))
    r = 6371  # Radius of earth in kilometers. Use 3956 for miles
    return c * r


def get_weather_sites_online():
    req = urllib2.Request(site_list_url)
    response = urllib2.urlopen(req)
    site_list_xml = response.read()

    root = xml.fromstring(site_list_xml)

    f = open(weather_site_filename, 'w')
    f.write(xml.tostring(root))
    f.close()


def get_weather_sites():
    if not systemfile.exists(weather_site_filename):  # if a local copy of weather sites not available then download
        get_weather_sites_online()

    with open(weather_site_filename, "r") as sites:
        sites_xml = sites.read()

    return xml.fromstring(sites_xml)


def cache_weather(site_id, weather_data):
    weather_cache[site_id] = (weather_data, round(time.time()) + cache_expiry)


def get_weather(lat, lon, hour_offset):
    required_minute = (int(time.strftime("%H")) + hour_offset) * 60
    sites = get_weather_sites()
    site_id = get_nearest_weather_site(sites, lat, lon)

    weather_data = None

    # if the data is in cache and it hasn't expired, then show the cached data otherwise fetch from internet
    if (site_id in weather_cache) and (weather_cache[site_id][1] > time.time()):
        print "Cached weather data"
        weather_data = xml.fromstring(weather_cache[site_id][0])
    else:
        print "New weather data"
        req = urllib2.Request(weather_url % site_id)
        response = urllib2.urlopen(req)
        weather_xml = xml.fromstring(response.read())

        weather_data_sets = weather_xml[1][0][0][:]

        for data in reversed(weather_data_sets):
            if abs(int(data.text)) >= required_minute:
                weather_data = data

        cache_weather(site_id, xml.tostring(weather_data))  # cache the new data for future

    if weather_data is None:
        return None  # something went terribly wrong

    # all the data from met office
    temp = weather_data.get('T')
    wind_direction = compassDict[weather_data.get('D')]
    wind_speed = weather_data.get('S')
    relative_humidity = weather_data.get('H')
    precipitation_prob = weather_data.get('Pp')

    #print "weather = " + precipitation_prob, relative_humidity, temp, wind_direction, wind_speed

    return float(precipitation_prob), float(relative_humidity), float(temp), float(wind_direction), float(
        wind_speed) * 0.44704
