import math


class Tile:
    def __init__(self, start_x=0.0, start_y=0.0, end_x=0.0, end_y=0.0, key=-1):
        self.key = key
        self.start_x = start_x
        self.start_y = start_y
        self.end_x = end_x
        self.end_y = end_y

    def __str__(self):
        return str(self.start_x) + "," + str(self.start_y) + "; " + \
               str(self.end_x) + "," + str(self.end_y) + "\n"

    def kml(self):
        kml = "<Polygon><outerBoundaryIs><LinearRing><coordinates>" + \
            str(self.start_y) + "," + str(self.start_x) + ",0" + " " + \
            str(self.end_y) + "," + str(self.start_x) + ",0" + " " + \
            str(self.end_y) + "," + str(self.end_x) + ",0" + " " + \
            str(self.start_y) + "," + str(self.end_x) + ",0" + \
            "</coordinates></LinearRing></outerBoundaryIs></Polygon>"

        return kml

    def includes(self, x, y):
        smallest_x = min(self.start_x, self.end_x)
        smallest_y = min(self.start_y, self.end_y)
        largest_x = max(self.start_x, self.end_x)
        largest_y = max(self.start_y, self.end_y)

        return (smallest_x <= x < largest_x) and (smallest_y <= y < largest_y)


def fragment_tile(big_tile, step_x, step_y):
    """
    Creates tiles
    :param big_tile: the tile that needs to be broken up
    :param step_x: the height (x) of smaller tile
    :param step_y: the width (y) of smaller tile
    :type big_tile: Tile
    :type step_x: float
    :type step_y: float
    :return: array of smaller Tiles

    NOTE: The order of tiles may be random
    """
    smaller_tiles = []

    smallest_x = min(big_tile.start_x, big_tile.end_x)
    smallest_y = min(big_tile.start_y, big_tile.end_y)
    largest_x = max(big_tile.start_x, big_tile.end_x)
    largest_y = max(big_tile.start_y, big_tile.end_y)

    current_x = smallest_x
    key = 0
    while (current_x + step_x) <= largest_x:
        current_y = smallest_y

        while (current_y + step_y) <= largest_y:
            tile = Tile(current_x, current_y, current_x + step_x, current_y + step_y, key)
            smaller_tiles.append(tile)
            current_y += step_y
            key += 1
            # print str(tile)

        current_x += step_x

    return smaller_tiles


def m_to_lat(distance):
    one_lat = 110.574 * (10 ** 3)  # meters
    latitude = distance / one_lat
    return latitude


def m_to_lon(distance, latitude):
    one_lon = 111.320 * math.cos(latitude) * (10 ** 3)  # meters
    longitude = distance / one_lon
    return longitude
