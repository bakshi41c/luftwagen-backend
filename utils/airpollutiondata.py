import urllib2
import urllib
import lxml.html as Scraper
import os.path

pageSourceList = [
    "CO",
    "COm",
    "NO2",
    "NO2m",
    "NO",
    "NOm",
    "NOX",
    "NOXm",
    "O3",
    "O3m",
    "PM10",
    "DUST",
    "PM25",
    "FINE",
    "SO2",
    "SO2m",
    "BENZ",
    "BENZm",
    "BP",
    "RAIN",
    "RHUM",
    "SOLR",
    "TMP",
    "WDIR",
    "WSPD"]
list = dict()
baseUrl = "http://www.londonair.org.uk/london/asp/dataspecies.asp?species="


def get_common_sets():
    for i in pageSourceList:
        response = urllib2.urlopen(baseUrl + i)
        page_source = response.read()

        doc = Scraper.fromstring(page_source)
        elements = doc.xpath('//*[@id="site1"]/option')
        del elements[0]
        codes = map(lambda x: x.get('value'), elements)
        list[i] = codes
        print i + ": " + codes.__str__()

    print list


def download_historic_data():

    download_link = "http://www.londonair.org.uk/london/asp/downloadsite.asp?site=###CODE###&species1=NOXm&species2=&species3=&species4=&species5=&species6=&start=1-jan-2008&end=31-dec-2015&res=6&period=hourly&units=ugm3"
    response = urllib2.urlopen("http://www.londonair.org.uk/london/asp/datadownload.asp")
    page_source = response.read()

    doc = Scraper.fromstring(page_source)
    elements = doc.xpath('//*[@id="species1"]/option')
    codes = map(lambda x: x.get('value'), elements)

    for code in codes:
        if code is not None and not os.path.isfile(code + ".csv"):
            print "Downloading... " + code
            urllib.urlretrieve(download_link.replace("###CODE###", code), code + ".csv")
        else:
            print "Already Exists"

    '''
    for element in elements:
        print element.get('value');
        print "\n";
    '''
