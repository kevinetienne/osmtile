import math
import os
import urllib2

MAP_URL = "http://ojw.dev.openstreetmap.org/StaticMap/" + \
        "?lat=%(lat)s&lon=%(lon)s&z=%(zoom)s&mode=Location&show=1"

class DownloadMap(object):
    def __init__(self, map_name=None, upload_to=None):

        self.map_name = map_name
        self.upload_to = upload_to

    def set_boundaries(self, left, bottom, right, top):
        """
        TODO given boundaries calculate lat lon
        """
        self.left, self.bottom, self.right, self.top = \
                left, bottom, right, top

    def set_center(self, lat, lon, zoom):
        """
        sets lat, lon and zoom
        """
        self.lat, self.lon, self.zoom = lat, lon, zoom

    def download(self):
        """
        """
        my_map = urllib2.urlopen(self.url)
        filepath = os.path.join(self.upload_to, self.map_name + ".png")

        # use buffer
        f = open(filepath, "w")

        block_size = 8192
        while True:
            buffer = my_map.read(block_size)
            if not buffer:
                break
            f.write(buffer)

        f.close()

        return filepath

    def build_url(self):
        """
        returns an url with zoom, latitude, longitude
        """
        self.url = MAP_URL % {'lat': self.lat, 'lon': self.lon, 'zoom': self.zoom}
        return self.url

    def deg2num(self, lat_deg, lon_deg, zoom):
        """
        lon/lat to tile numbers
        http://wiki.openstreetmap.org/wiki/Slippy_map_tilenames
        """
        lat_rad = math.radians(lat_deg)
        n = 2.0 ** zoom
        xtile = int((lon_deg + 180.0) / 360.0 * n)
        ytile = int((1.0 - math.log(math.tan(lat_rad) + 
            (1 / math.cos(lat_rad))) / math.pi) / 2.0 * n)
        return(xtile, ytile, zoom)

    def num2deg(xtile, ytile, zoom):
        """
        This returns the NW-corner of the square. Use the function with xtile+1
        and/or ytile+1 to get the other corners. With xtile+0.5 & ytile+0.5 it
        will return the center of the tile.
        """
        n = 2.0 ** zoom
        lon_deg = xtile / n * 360.0 - 180.0
        lat_rad = math.atan(math.sinh(math.pi * (1 - 2 * ytile / n)))
        lat_deg = math.degrees(lat_rad)
        return(lat_deg, lon_deg, zoom)

if __name__ == "__main__":
    "a simple example"
    m = DownloadMap("my_map", os.getcwd())
    m.set_center(51.752155300000005, -1.2582349576721181 ,15)
    m.build_url()
    m.download()
