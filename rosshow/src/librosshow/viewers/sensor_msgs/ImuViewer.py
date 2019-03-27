import time
import math
import librosshow.termgraphics as termgraphics
from librosshow.plotters import ScopePlotter, AnglePlotter

class ImuViewer(object):
    def __init__(self, canvas, title = ""):
        self.g = canvas
        self.last_update_shape_time = 0
        self.title = title
        self.right = 10
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
            left = hmargin,
            top = vmargin,
            right = hmargin + hsize,
            bottom = vmargin + vsize,
            ymin = -math.pi,
            ymax = math.pi,
        )

        self.pitch_scope_plotter = ScopePlotter(self.g,
            left = hmargin,
            top = 2*vmargin + vsize,
            right = hmargin + hsize,
            bottom = 2*vmargin + 2*vsize,
            ymin = -math.pi/2,
            ymax = math.pi/2,
        )

        self.roll_scope_plotter = ScopePlotter(self.g,
            left = hmargin,
            top = 3*vmargin + 2*vsize,
            right = hmargin + hsize,
            bottom = 3*vmargin + 3*vsize,
            ymin = 0,
            ymax = 2*math.pi,
        )

        self.avx_scope_plotter = ScopePlotter(self.g,
            left = 2*hmargin + hsize,
            top = vmargin,
            right = 2*hmargin + 2*hsize,
            bottom = vmargin + vsize,
            ymin = -math.pi,
            ymax = math.pi,
        )

        self.avy_scope_plotter = ScopePlotter(self.g,
            left = 2*hmargin + hsize,
            top = 2*vmargin + vsize,
            right = 2*hmargin + 2*hsize,
            bottom = 2*vmargin + 2*vsize,
            ymin = -math.pi,
            ymax = math.pi,
        )

        self.avz_scope_plotter = ScopePlotter(self.g,
            left = 2*hmargin + hsize,
            top = 3*vmargin + 2*vsize,
            right = 2*hmargin + 2*hsize,
            bottom = 3*vmargin + 3*vsize,
            ymin = -math.pi,
            ymax = math.pi,
        )

        self.lax_scope_plotter = ScopePlotter(self.g,
            left = 3*hmargin + 2*hsize,
            top = vmargin,
            right = 3*hmargin + 3*hsize,
            bottom = vmargin + vsize,
            ymin = -9.8,
            ymax = 9.8,
        )

        self.lay_scope_plotter = ScopePlotter(self.g,
            left = 3*hmargin + 2*hsize,
            top = 2*vmargin + vsize,
            right = 3*hmargin + 3*hsize,
            bottom = 2*vmargin + 2*vsize,
            ymin = -9.8,
            ymax = 9.8
        )

        self.laz_scope_plotter = ScopePlotter(self.g,
            left = 3*hmargin + 2*hsize,
            top = 3*vmargin + 2*vsize,
            right = 3*hmargin + 3*hsize,
            bottom = 3*vmargin + 3*vsize,
            ymin = -9.8,
            ymax = 9.8,
        )

    def update(self, data):
        a = data.orientation.x / 16384.
        b = data.orientation.y / 16384.
        c = data.orientation.z / 16384.
        d = data.orientation.w / 16384.

        yaw = math.atan2(2*a*b+2*c*d, 1-2*b*b-2*c*c)
        pitch = math.asin(2*(a*c-b*d))
        roll = math.atan2(2*a*d+2*b*c, 1-2*c*c-2*d*d)+math.pi

        self.yaw_scope_plotter.update(yaw)
        self.pitch_scope_plotter.update(pitch)
        self.roll_scope_plotter.update(roll)
        self.avx_scope_plotter.update(data.angular_velocity.x)
        self.avy_scope_plotter.update(data.angular_velocity.y)
        self.avz_scope_plotter.update(data.angular_velocity.z)
        self.lax_scope_plotter.update(data.linear_acceleration.x)
        self.lay_scope_plotter.update(data.linear_acceleration.y)
        self.laz_scope_plotter.update(data.linear_acceleration.z)

    def draw(self):
        t = time.time()

        # capture changes in terminal shape at least every 0.5s
        if t - self.last_update_shape_time > 0.25:
            self.g.update_shape()
            self.last_update_shape_time = t

        self.g.clear()
        self.g.set_color(termgraphics.COLOR_WHITE)
        self.yaw_scope_plotter.plot()
        self.pitch_scope_plotter.plot()
        self.roll_scope_plotter.plot()
        self.avx_scope_plotter.plot()
        self.avy_scope_plotter.plot()
        self.avz_scope_plotter.plot()
        self.lax_scope_plotter.plot()
        self.lay_scope_plotter.plot()
        self.laz_scope_plotter.plot()
        if self.title:
            self.g.set_color((0, 127, 255))
            self.g.text(self.title, (0, self.g.shape[1] - 4))
        self.g.draw()
