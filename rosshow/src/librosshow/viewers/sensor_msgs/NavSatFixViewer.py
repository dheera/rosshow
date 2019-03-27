#!/usr/bin/env python3

import functools
from io import BytesIO
import math
import numpy as np
import requests
import time
import librosshow.termgraphics as termgraphics

def memoize(f):
    """ Memoization decorator for functions taking one or more arguments. """
    class memodict(dict):
        def __init__(self, f):
            self.f = f
        def __call__(self, *args):
            return self[args]
        def __missing__(self, key):
            ret = self[key] = self.f(*key)
            return ret
    return memodict(f)

try:
    from PIL import Image, ImageOps
except ImportError:
    print("This message type requires an additional Python package. Please run:")
    print("  $ sudo pip3 install pillow")
    print("and try again.")
    exit()

@memoize
def get_tile(xtile, ytile, zoom):
    url = 'http://a.tile.openstreetmap.org/%s/%s/%s.png' % (zoom, xtile, ytile)
    response = requests.get(url)
    img = Image.open(BytesIO(response.content))
    return img

def deg2num(lat_deg, lon_deg, zoom):
  lat_rad = math.radians(lat_deg)
  n = 2.0 ** zoom
  xtile = int((lon_deg + 180.0) / 360.0 * n)
  ytile = int((1.0 - math.log(math.tan(lat_rad) + (1 / math.cos(lat_rad))) / math.pi) / 2.0 * n)
  return (xtile, ytile)

def num2deg(xtile, ytile, zoom):
  n = 2.0 ** zoom
  lon_deg = xtile / n * 360.0 - 180.0
  lat_rad = math.atan(math.sinh(math.pi * (1 - 2 * ytile / n)))
  lat_deg = math.degrees(lat_rad)
  return (lat_deg, lon_deg)

class NavSatFixViewer(object):
    def __init__(self, canvas, title = ""):
        self.g = canvas
        self.title = title
        self.xmin = 0
        self.xmax = 1
        self.ymin = 0
        self.ymax = 1
        self.zoom = 17
        self.data = [ (0,0) ] * 128
        self.pointer = 0
        self.last_update_shape_time = 0

    def update(self, msg):
        self.pointer = (self.pointer + 1) % len(self.data)
        self.data[self.pointer] = (msg.latitude, msg.longitude)

    def draw(self):
        t = time.time()

        # capture changes in terminal shape at least every 0.25s
        if t - self.last_update_shape_time > 0.25:
            self.g.update_shape()
            self.last_update_shape_time = t

        lat_point = self.data[self.pointer][0]
        lon_point = self.data[self.pointer][1]
        width = self.g.shape[0]
        height = self.g.shape[1]

        xtile, ytile = deg2num(lat_point, lon_point, self.zoom)
        lat_min, lon_min = num2deg(xtile, ytile, self.zoom)
        lat_max, lon_max = num2deg(xtile + 1, ytile + 1, self.zoom)

        img = get_tile(xtile, ytile, self.zoom)

        self.g.clear()

        # background map image
        self.g.set_color(termgraphics.COLOR_BLUE)
        img = img.resize((width, height), Image.NEAREST)
        self.g.image(np.array(img.getdata(), dtype = np.uint8) >> 7, img.width, img.height, (0, 0), image_type = termgraphics.IMAGE_MONOCHROME)

        # trail of last few positions
        self.g.set_color(termgraphics.COLOR_WHITE)
        points = []
        for i in range(len(self.data)):
           points.append((
               width * (self.data[i][1] - lon_min) / (lon_max - lon_min),
               height * (self.data[i][0] - lat_min) / (lat_max - lat_min)
           ))
        self.g.points(points, clear_block = True)

        # current position
        self.g.set_color(termgraphics.COLOR_RED)
        for i in range(-1, 2):
            for j in range(-1, 2):
                self.g.point((
                    int(width * (self.data[self.pointer][1] - lon_min) / (lon_max - lon_min)) + i,
                    int(height * (self.data[self.pointer][0] - lat_min) / (lat_max - lat_min)) + j
                ), clear_block = True)
        for i in range(-1, 2):
            for j in range(-1, 2):
                self.g.point((
                    int(width * (self.data[self.pointer][1] - lon_min) / (lon_max - lon_min)) + i,
                    int(height * (self.data[self.pointer][0] - lat_min) / (lat_max - lat_min)) + j
                ), clear_block = False)

        if self.title:
            self.g.set_color((0, 127, 255))
            self.g.text(self.title, (0, self.g.shape[1] - 4))

        self.g.draw()

