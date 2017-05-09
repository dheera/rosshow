#!/usr/bin/env python3

import math
from .termgraphics import TermGraphics

class AnglePlotter(object):
    def __init__(self, g, xmin = 0, xmax = 1, ymin = 0, ymax = 1):
        self.g = g
        self.xmin = xmin
        self.xmax = xmax
        self.ymin = ymin
        self.ymax = ymax

    def plot(self, angle):
        width, height = self.g.shape
        self.g.rect(
          (int(self.xmin), int(self.ymin)),
          (int(self.xmax), int(self.ymax)),
        )
        self.g.line(
          (int(1 + self.xmin + (self.xmax - self.xmin)/2 - (self.xmax - self.xmin)/2*math.cos(angle)),
          int(1 + self.ymin + (self.ymax - self.ymin)/2 + (self.ymax - self.ymin)/2*math.sin(angle))),
          (int(1 + self.xmin + (self.xmax - self.xmin)/2 + (self.xmax - self.xmin)/2*math.cos(angle)),
          int(1 + self.ymin + (self.ymax - self.ymin)/2 - (self.ymax - self.ymin)/2*math.sin(angle))),
        )

class ScopePlotter(object):
    def __init__(self, g, xmin = 0, xmax = 1, ymin = 0, ymax = 1, vmin = -1, vmax = 1, n = 128):
        self.g = g
        self.xmin = xmin
        self.xmax = xmax
        self.ymin = ymin
        self.ymax = ymax
        self.vmax = vmax
        self.vmin = vmin
        self.data = [ 1. ] * n
        self.pointer = 0

    def plot(self, value):
        self.data[self.pointer] = value
        points = []
        for i in range(len(self.data)):
           points.append(
             (i/len(self.data)*(self.xmax - self.xmin) + self.xmin,
             (1 - (self.data[i] - self.vmin) / (self.vmax - self.vmin)) * (self.ymax - self.ymin) + self.ymin)
           )
        self.g.points(points)
        self.pointer = (self.pointer + 1) % len(self.data)

class ImuViewer(object):

    def __init__(self):
        self.g = TermGraphics()
        self.xmax = 10
        self.yaws = [ 0. ] * 128
        self.yaws_p = 0
        self.pitches = [ 0. ] * 128
        self.pitches_p = 0
        self.rolls = [ 0. ] * 128
        self.rolls_p = 0

        margin = self.g.shape[1]/16.
        plotter_size = self.g.shape[1]/4.

        self.yaw_angle_plotter = AnglePlotter(self.g,
            xmin = margin,
            ymin = margin,
            xmax = margin + plotter_size,
            ymax = margin + plotter_size,
        )

        self.yaw_scope_plotter = ScopePlotter(self.g,
            xmin = 2*margin + plotter_size,
            ymin = margin,
            xmax = self.g.shape[0]/2 - margin/2,
            ymax = margin + plotter_size,
            vmin = -math.pi,
            vmax = math.pi,
        )

        self.pitch_angle_plotter = AnglePlotter(self.g,
            xmin = margin,
            ymin = 2*margin + plotter_size,
            xmax = margin + plotter_size,
            ymax = 2*margin + 2*plotter_size,
        )

        self.pitch_scope_plotter = ScopePlotter(self.g,
            xmin = 2*margin + plotter_size,
            ymin = 2*margin + plotter_size,
            xmax = self.g.shape[0]/2 - margin/2,
            ymax = 2*margin + 2*plotter_size,
            vmin = 0,
            vmax = math.pi,
        )

        self.roll_angle_plotter = AnglePlotter(self.g,
            xmin = margin,
            ymin = 3*margin + 2*plotter_size,
            xmax = margin + plotter_size,
            ymax = 3*margin + 3*plotter_size,
        )

        self.roll_scope_plotter = ScopePlotter(self.g,
            xmin = 2*margin + plotter_size,
            ymin = 3*margin + 2*plotter_size,
            xmax = self.g.shape[0]/2 - margin/2,
            ymax = 3*margin + 3*plotter_size,
            vmin = 0,
            vmax = math.pi,
        )

    def update(self, data):
        a = data.orientation.x / 16384.
        b = data.orientation.y / 16384.
        c = data.orientation.z / 16384.
        d = data.orientation.w / 16384.

        yaw = math.atan2(2*a*b+2*c*d, 1-2*b*b-2*c*c)
        pitch = math.asin(2*(a*c-b*d))
        roll = math.atan2(2*a*d+2*b*c, 1-2*c*c-2*d*d)+math.pi

        self.g.clear()

        self.yaw_angle_plotter.plot(yaw)
        self.pitch_angle_plotter.plot(pitch)
        self.roll_angle_plotter.plot(roll)

        self.yaw_scope_plotter.plot(yaw)
        self.pitch_scope_plotter.plot(pitch)
        self.roll_scope_plotter.plot(roll)

        self.g.draw()
