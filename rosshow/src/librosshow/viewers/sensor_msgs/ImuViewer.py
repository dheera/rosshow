#!/usr/bin/env python3

import math
import librosshow.termgraphics as termgraphics
from librosshow.plotters import ScopePlotter, AnglePlotter

class ImuViewer(object):
    def __init__(self):
        self.g = termgraphics.TermGraphics()
        self.xmax = 10
        self.yaws = [ 0. ] * 128
        self.yaws_p = 0
        self.pitches = [ 0. ] * 128
        self.pitches_p = 0
        self.rolls = [ 0. ] * 128
        self.rolls_p = 0

        hmargin = self.g.shape[0]/40.
        vmargin = self.g.shape[1]/20.
        hsize = (self.g.shape[0] - 4*hmargin ) / 3
        vsize = (self.g.shape[1] - 4*vmargin ) / 3

        self.yaw_scope_plotter = ScopePlotter(self.g,
            xmin = hmargin,
            ymin = vmargin,
            xmax = hmargin + hsize,
            ymax = vmargin + vsize,
            vmin = -math.pi,
            vmax = math.pi,
        )

        self.pitch_scope_plotter = ScopePlotter(self.g,
            xmin = hmargin,
            ymin = 2*vmargin + vsize,
            xmax = hmargin + hsize,
            ymax = 2*vmargin + 2*vsize,
            vmin = -math.pi/2,
            vmax = math.pi/2,
        )

        self.roll_scope_plotter = ScopePlotter(self.g,
            xmin = hmargin,
            ymin = 3*vmargin + 2*vsize,
            xmax = hmargin + hsize,
            ymax = 3*vmargin + 3*vsize,
            vmin = 0,
            vmax = 2*math.pi,
        )

        self.avx_scope_plotter = ScopePlotter(self.g,
            xmin = 2*hmargin + hsize,
            ymin = vmargin,
            xmax = 2*hmargin + 2*hsize,
            ymax = vmargin + vsize,
            vmin = -math.pi,
            vmax = math.pi,
        )

        self.avy_scope_plotter = ScopePlotter(self.g,
            xmin = 2*hmargin + hsize,
            ymin = 2*vmargin + vsize,
            xmax = 2*hmargin + 2*hsize,
            ymax = 2*vmargin + 2*vsize,
            vmin = -math.pi,
            vmax = math.pi,
        )

        self.avz_scope_plotter = ScopePlotter(self.g,
            xmin = 2*hmargin + hsize,
            ymin = 3*vmargin + 2*vsize,
            xmax = 2*hmargin + 2*hsize,
            ymax = 3*vmargin + 3*vsize,
            vmin = -math.pi,
            vmax = math.pi,
        )

        self.lax_scope_plotter = ScopePlotter(self.g,
            xmin = 3*hmargin + 2*hsize,
            ymin = vmargin,
            xmax = 3*hmargin + 3*hsize,
            ymax = vmargin + vsize,
            vmin = -9.8,
            vmax = 9.8,
        )

        self.lay_scope_plotter = ScopePlotter(self.g,
            xmin = 3*hmargin + 2*hsize,
            ymin = 2*vmargin + vsize,
            xmax = 3*hmargin + 3*hsize,
            ymax = 2*vmargin + 2*vsize,
            vmin = -9.8,
            vmax = 9.8
        )

        self.laz_scope_plotter = ScopePlotter(self.g,
            xmin = 3*hmargin + 2*hsize,
            ymin = 3*vmargin + 2*vsize,
            xmax = 3*hmargin + 3*hsize,
            ymax = 3*vmargin + 3*vsize,
            vmin = -9.8,
            vmax = 9.8,
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

        self.yaw_scope_plotter.plot(yaw)
        self.pitch_scope_plotter.plot(pitch)
        self.roll_scope_plotter.plot(roll)

        self.avx_scope_plotter.plot(data.angular_velocity.x)
        self.avy_scope_plotter.plot(data.angular_velocity.y)
        self.avz_scope_plotter.plot(data.angular_velocity.z)

        self.lax_scope_plotter.plot(data.linear_acceleration.x)
        self.lay_scope_plotter.plot(data.linear_acceleration.y)
        self.laz_scope_plotter.plot(data.linear_acceleration.z)

        self.g.draw()
