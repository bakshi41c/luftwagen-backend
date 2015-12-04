from time import sleep
import urllib
import urllib2
import requests, json

#********************
# !!! ATTENTION !!!**
#********************
# Repalce these *** values with actual values
# Ask Shubham if unsure
fusion_table_id = "1pHZ_F-xDRFU0omNrpu-SdLoVYOm0Fm5CPDdSsbab"
client_id = "***.apps.googleusercontent.com"
client_secret = "***"
server_key = "***"
access_token = "***"
refresh_token = "***"

url = "https://www.googleapis.com/upload/fusiontables/v2/tables/" + fusion_table_id + \
      "/replace?uploadType=media&isStrict=true&key=" + server_key

delete_url = "https://www.googleapis.com/fusiontables/v2/query?sql=delete+from+" + \
             fusion_table_id + "&key={" + server_key + "}"

print url


def update_table(filename):
    with open(filename) as f:
        valid = is_accesscode_valid()
        if not valid:
            print "access code invalid, refreshing..."
            refresh_access_token()

        print access_token

        # Re-upload all rows
        resp = requests.post(url, data=f, headers=get_upload_header())
        print resp.content


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
