import math
import urllib2
import xml.etree.ElementTree as ET


#https://developer.here.com/rest-apis/documentation/traffic/topics_v6.1/example-flow.html
app_id = "tip09eTk3MPc1vqGNztA"
app_code = "Z8z1Sd_gX-4MvRacAgihqw"

def getTrafficData(coordX, coordY):
    z = 19
    (x_tile, y_tile) = calculateTile(coordX, coordY, 19)
    url = formURL(int(x_tile), int(y_tile), z)
    print url
    req = urllib2.Request(url)
    response = urllib2.urlopen(req)
    traffic_xml = response.read()
    #print traffic_xml

    # Getting the root of the XML data
    root = ET.fromstring(traffic_xml)

    rw = root[0][0]
    cf = rw[0][0][1]
    print cf.attrib
    jf = float(cf.get('JF'))

    print rw
    print jf.__str__()



def calculateTile(lat=0.0, lon=0.0, z=1):
    lat_rad = lat * math.pi / 180.0
    n = 2 ** z
    x_tile = n * ((lon + 180.0) / 360.0)
    y_tile = n * (1 - (math.log(math.tan(lat_rad) + 1 / math.cos(lat_rad)) / math.pi)) / 2

    return x_tile, y_tile


def formURL(x,y,z):
    url = "http://traffic.cit.api.here.com/traffic/6.1/flow/xml/" \
      + str(z) + "/" + str(int(x)) + "/" + str(int(y)) + "?app_id=" + app_id + "&app_code=" + app_code

    return url


lat = 51.5263248  # float(raw_input("lat"))
lon = -0.1355824  # float(raw_input("lon"))
getTrafficData(lat, lon)
