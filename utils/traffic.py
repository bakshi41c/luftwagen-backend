import math
import urllib2
import xml.etree.ElementTree as xml
import time

# https://developer.here.com/rest-apis/documentation/traffic/topics_v6.1/example-flow.html

app_id = "tip09eTk3MPc1vqGNztA"
app_code = "Z8z1Sd_gX-4MvRacAgihqw"

cache_expiry = 15  # 15 minutes

# format for traffic_cache= {quadkey: (value, expiry)}
traffic_cache = {}


def cache_traffic(quadkey, traffic_data):
    traffic_cache[quadkey] = (traffic_data, round(time.time()) + cache_expiry)


def get_traffic_data(coord_x, coord_y):
    z = 19
    (x_tile, y_tile) = calculate_tile(coord_x, coord_y, z)
    quadkey = tile2quadkey(x_tile, y_tile, z)

    traffic_data = None

    if (quadkey in traffic_cache) and (traffic_cache[quadkey][1] > time.time()):
        print ("Cached")
        traffic_data = xml.fromstring(traffic_cache[quadkey][0])
    else:
        print ("New")
        url = form_url(quadkey)
        print url
        req = urllib2.Request(url)
        response = urllib2.urlopen(req)
        traffic_xml = response.read()

        # Getting the root of the XML data
        root = xml.fromstring(traffic_xml)
        roadway = root[0][0]
        traffic_data = roadway[0][0][1]
        cache_traffic(quadkey, xml.tostring(traffic_data))

    if traffic_data is None:
        return 1.0  # return the lowest value in case of error

    jf = float(traffic_data.get('JF'))
    return jf


def calculate_tile(lat=0.0, lon=0.0, z=1):
    lat_rad = lat * math.pi / 180.0
    n = 2 ** z
    x_tile = n * ((lon + 180.0) / 360.0)
    y_tile = n * (1 - (math.log(math.tan(lat_rad) + 1 / math.cos(lat_rad)) / math.pi)) / 2

    return int(x_tile), int(y_tile)


def tile2quadkey(x_tile, y_tile, z):
    quadKey = ""
    for i in range(z, 0, -1):
        digit = 0
        mask = 1 << (i - 1)
        if (x_tile & mask) is not 0:
            digit += 1

        if (y_tile & mask) is not 0:
            digit += 2

        quadKey += str(digit)

    return quadKey


def form_url(quadkey):
    url = "http://traffic.cit.api.here.com/traffic/6.1/flow.xml" \
          + "?quadkey=" + quadkey + "&app_id=" + app_id + "&app_code=" + app_code
    return url


# How to use
lat = 51.5263248
lon = -0.1355824

print get_traffic_data(lat, lon)
