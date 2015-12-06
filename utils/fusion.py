import os
import urllib
import urllib2
import requests
import json
import tiles
import datetime
import pollution

# ********************
# !!! ATTENTION !!!**
# ********************
# Replace these *** values with actual values
# Ask Shubham if unsure


fusion_table_id = "1uscrBV4D6yxUcHkz7qVU6nCjSTmSo_qxTERxNQXC"  # "1pHZ_F-xDRFU0omNrpu-SdLoVYOm0Fm5CPDdSsbab"
client_id = "670715399306-hahi5146oiap2fpqrm890n61h9v6110r.apps.googleusercontent.com"
client_secret = "aKinU0Qp-H7T6cWX0LdREO_z"
server_key = "AIzaSyAXOf2VLCgafuEmBGsfinlzsxCzl0_AX_o"
access_token = "ya29.QgIUEES8ny9_gArEWGe-fckY5cYsLuE2cJMyBBJvACN9yDL-0ua2qiwVKydEPtU0Jxq8"
refresh_token = "1/pZaFoWgijy3i30LRUsAlH4wkFJRBzho3HwdBk_6JI4k"

url = "https://www.googleapis.com/upload/fusiontables/v2/tables/" + fusion_table_id + \
      "/replace?uploadType=media&isStrict=true&key=" + server_key

delete_url = "https://www.googleapis.com/fusiontables/v2/query?sql=delete+from+" + \
             fusion_table_id + "&key={" + server_key + "}"


def update_table(filename):
    with open(filename) as f:
        if is_accesscode_valid() is False:
            refresh_access_token()

        print access_token

        # Re-upload all rows
        resp = requests.post(url, data=f, headers=get_upload_header())


def is_accesscode_valid():
    check_url = "https://www.googleapis.com/oauth2/v1/tokeninfo?access_token={" + access_token + "}"
    resp = requests.get(check_url)

    if "error" in str(resp.content):
        return False
    else:
        return True


def get_upload_header():
    header = {
        'Content-Type': 'application/octet-stream',
        'Authorization': "Bearer " + access_token,
    }
    return header


def get_delete_header():
    header = {
        'Authorization': "Bearer " + access_token,
        'Content-Length': '0',
    }
    return header


def refresh_access_token():
    data = urllib.urlencode({
        'client_id': client_id,
        'client_secret': client_secret,
        'refresh_token': refresh_token,
        'grant_type': 'refresh_token'})

    request = urllib2.Request(
        url='https://accounts.google.com/o/oauth2/token',
        data=data)
    request_open = urllib2.urlopen(request)
    response = request_open.read()
    request_open.close()
    tokens = json.loads(response)

    global access_token
    access_token = tokens['access_token']


def main():
    london_x1 = 51.700559
    london_y1 = -0.497709

    london_x2 = 51.308527
    london_y2 = 0.246893

    # try 50
    big_tile = tiles.Tile(london_x1, london_y1, london_x2, london_y2)
    smaller_tiles = tiles.fragment_tile(big_tile, tiles.m_to_lat(200), tiles.m_to_lon(200 / 3, london_x1))
    # print smaller_tiles

    filename = 'fusion.csv'

    with open(filename, 'w') as f:
        i = 0
        sum = 0
        for tile in smaller_tiles:
            pollution_value = 1.0
            if i % 5 == 0:
                pollution_value = pollution.get_pollution_value(tile.start_x, tile.start_y, 0)
                sum = 0
            else:
                pollution_value = sum / (i % 10)

            line = "\"" + tile.kml() + "\"" + ", " + str(pollution_value) + "\n"
            f.write(line)
            i += 1
            sum += pollution_value
            print "Progress: " + str(i) + "/" + str(len(smaller_tiles))

    success = False
    tries = 0
    while success is not True or tries < 3:
        tries += 1
        try:
            print "Try no:" + str(tries) + " to update table"
            update_table(filename)

        except Exception:
            print "Failed to update table"

    if success:
        print "Last fusion update: " + str(datetime.datetime.now())

main()
