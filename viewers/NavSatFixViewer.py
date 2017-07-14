#!/usr/bin/env python3

from PIL import Image, ImageOps
import functools
from io import BytesIO
import math
import requests
import time
from . import termgraphics

@functools.lru_cache()
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

class LocationPlotter(object):
    def __init__(self, g, xmin = 0, xmax = 1, ymin = 0, ymax = 1, zoom = 15, n = 128):
        self.g = g
        self.xmin = xmin
        self.xmax = xmax
        self.ymin = ymin
        self.ymax = ymax
        self.zoom = 17
        self.data = [ (0,0) ] * n
        self.pointer = 0

    def plot(self, value):
        self.data[self.pointer] = value
        lat_point = self.data[self.pointer][0]
        lon_point = self.data[self.pointer][1]
        width = self.g.shape[0]
        height = self.g.shape[1]

        xtile, ytile = deg2num(lat_point, lon_point, self.zoom)
        lat_min, lon_min = num2deg(xtile, ytile, self.zoom)
        lat_max, lon_max = num2deg(xtile + 1, ytile + 1, self.zoom)

        img = get_tile(xtile, ytile, self.zoom)

        self.g.clear()

        self.g.set_color(termgraphics.COLOR_BLUE)

        img = img.resize((width, height), Image.NEAREST)
        self.g.image(list(img.getdata()), img.width, img.height, (0, 0), image_type = termgraphics.IMAGE_UINT8)

        points = []

        for i in range(len(self.data)):
           points.append((
               width * (self.data[i][1] - lon_min) / (lon_max - lon_min),
               height * (self.data[i][0] - lat_min) / (lat_max - lat_min)
           ))
        self.g.set_color(termgraphics.COLOR_WHITE)

        self.g.points(points, clear_block = True)
        self.g.set_color(termgraphics.COLOR_RED)
        self.g.point((
           width * (self.data[self.pointer][1] - lon_min) / (lon_max - lon_min),
           height * (self.data[self.pointer][0] - lat_min) / (lat_max - lat_min)
        ), clear_block = True)
        self.pointer = (self.pointer + 1) % len(self.data)

class NavSatFixViewer(object):

    def __init__(self):
        self.g = termgraphics.TermGraphics()
        self.location_plotter = LocationPlotter(self.g)

    def update(self, data):

        self.location_plotter.plot((data.latitude, data.longitude))

        self.g.draw()
