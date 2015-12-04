import math
import overpy
from routers import Google

def getPolutionPoints(LTx,LTy,RBx,RBy):
    # LT = Left top corner, and RB = right bottom corner
    #todo implement this fuction
    return {
        'status':'Under construction',
        'LTx':LTx,
        'LTy':LTy,
        'RBx':RBx,
        'RBy':RBy
    }


def getWaysAroundPoint(lat,long):
    api = overpy.Overpass()
    result = api.query("way[highway](%f,%f,%f,%f);out;"%(lat-.05,long-.1,lat+.05,long+.1))
    print result
    print result.nodes
    print result.ways
    for way in result.ways:
        print way.get_nodes(resolve_missing=True)


"""
Idea taken form http://stackoverflow.com/questions/8487893/generate-all-the-points-on-the-circumference-of-a-circle
"""
def PointsInCircum(lat, long,r,n=10):
    return [(math.sin(2*math.pi/n*x)*r+lat,math.cos(2*math.pi/n*x)*r+long) for x in xrange(0,n+1)]

def getRandomDirections(lat,long,distance):
    google = Google()
    cs = PointsInCircum(lat,long,distance/2)
    routes = [route for routes in
        [google.route("%f,%f"%(lat,long),"%f,%f"%(lat,long),waypoints=["%f,%f"%c]) for c in cs] for route in routes]
    return routes

def getRandomDirectionsAtoB(Alat,Along,Blat,Blong):
    google = Google()
    cs = [["%f,%f"%((Alat+Blat)/2+(i/60.0),(Along+Blong)/2+(j/60.0))] for i in xrange(-1,2) for j in xrange(-1,2)]
    cs.append([])
    routes = [route for routes in
        [google.route("%f,%f"%(Alat,Along),"%f,%f"%(Blat,Blong),waypoints=c) for c in cs] for route in routes]
    return routes

def addPollutionLeveltoRoutes(routes):
    for route in routes:
        route['pollution'] = 0
        for i in xrange(0,len(route['coords']),10): #todo change the 'magic' number (10)

           route['pollution'] += calculatePollution(route['coords'][i])

def bestThreeRoutes(routes):
    return sorted(routes,compareRoutes)[:3]

def compareRoutes(x,y):
    return cmp(x['pollution'],y['pollution'])

def calculatePollution(point):
    #todo implement, this shoud be avarage between the traffic data and pollution data
    return 1