from directions import routers
import itertools
import polycomp

"""
This is a subclass of Google router used in the directions package
"""


class Google(routers.Google):

    def _query_params(self, waypoints):
        origin = waypoints[0]
        destination = waypoints[-1]
        vias = waypoints[1:-1]
        # This assumes you're not running Python on a device with a location
        # sensor.
        payload = {
            'origin': self._convert_coordinate(origin, t=None),
            'destination': self._convert_coordinate(destination, t=None),
            'sensor': 'false',
            'units': 'metric',
            'mode': 'walking',
        }
        if vias:
            payload['waypoints'] = '|'.join(self._convert_coordinate(v)
                                            for v in vias)
        return payload

    def format_output(self, data):
        routes = []
        for r in data['routes']:
            duration = sum(leg['duration']['value'] for leg in r['legs'])
            distance = sum(leg['distance']['value'] for leg in r['legs'])

            latlons = []
            # Legs are the spans of the route between waypoints desired. If
            # there are no waypoints, there will only be 1 leg
            for leg in r['legs']:
                for step in leg['steps']:
                    latlons.append(
                        polycomp.decompress(step['polyline']['points']))

            # latlons is a list of list of lat/lon coordinate pairs. The end
            # point of each list is the same as the first point of the next
            # list. Get rid of the duplicates
            lines = [x[:-1] for x in latlons]
            lines.append([latlons[-1][-1]])  # Add the very last point
            points = itertools.chain(*lines)

            coords = [tuple(c) for c in points]
            route = {"coords": coords,"distance":distance,"duration":duration}
            routes.append(route)

        return routes