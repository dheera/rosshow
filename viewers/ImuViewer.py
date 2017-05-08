#!/usr/bin/env python3

import math
from .termgraphics import TermGraphics

class ImuViewer(object):
    def __init__(self):
        self.g = TermGraphics()
        self.xmax = 10

    def update(self, data):
        a = data.orientation.x / 16384.
        b = data.orientation.y / 16384.
        c = data.orientation.z / 16384.
        d = data.orientation.w / 16384.
        yaw = math.atan2(2*a*b+2*c*d, 1-2*b*b-2*c*c)
        pitch = math.asin(2*(a*c-b*d))
        roll = math.atan2(2*a*d+2*b*c, 1-2*c*c-2*d*d)+math.pi
        width = self.g.shape[0]
        height = self.g.shape[1]
        hmargin = height / 16
        self.g.clear()
        # yaw
        self.g.rect((int(hmargin), int(hmargin)), (int(hmargin + height/4), int(hmargin + height/4)))
        self.g.line(
          (int(1 + hmargin + height/8 - height/8 * math.cos(yaw)),
          int(1 + hmargin + height/8 - height/8 * math.sin(yaw))),
          (int(1 + hmargin + height/8 + height/8 * math.cos(yaw)),
          int(1 + hmargin + height/8 + height/8 * math.sin(yaw))),
         )
        # pitch
        self.g.rect((int(hmargin), int(2*hmargin + height/4)), (int(hmargin + height/4), int(2*hmargin + 2*height/4)))
        self.g.line(
          (int(1 + hmargin + height/8 - height/8 * math.cos(pitch)),
          int(1 + 2 * hmargin + 3*height/8 - height/8 * math.sin(pitch))),
          (int(1 + hmargin + height/8 + height/8 * math.cos(pitch)),
          int(1 + 2 * hmargin + 3*height/8 + height/8 * math.sin(pitch))),
         )
        # roll
        self.g.rect((int(hmargin), int(3*hmargin + 2*height/4)), (int(hmargin + height/4), int(3*hmargin + 3*height/4)))
        self.g.line(
          (int(1 + hmargin + height/8 - height/8 * math.cos(roll)),
          int(1 + 3 * hmargin + 5*height/8 - height/8 * math.sin(roll))),
          (int(1 + hmargin + height/8 + height/8 * math.cos(roll)),
          int(1 + 3 * hmargin + 5*height/8 + height/8 * math.sin(roll))),
         )
        self.g.draw()
