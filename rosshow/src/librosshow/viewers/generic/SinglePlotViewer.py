import time
import math
import librosshow.termgraphics as termgraphics
from librosshow.plotters import ScopePlotter

class SinglePlotViewer(object):
    def __init__(self, title = "", data_field = "data"):
        self.g = termgraphics.TermGraphics()
        self.msg = None
        self.xmax = 10
        self.title = title
        self.data_field = data_field
        self.last_update_shape_time = 0

        hmargin = self.g.shape[0]/40.
        vmargin = self.g.shape[1]/20.
        hsize = (self.g.shape[0] - 4*hmargin )
        vsize = (self.g.shape[1] - 4*vmargin )

        self.scope_plotter = ScopePlotter(self.g,
            left = hmargin,
            top = vmargin,
            right = hmargin + hsize,
            bottom = vmargin + vsize,
            ymin = None,
            ymax = None,
        )

    def update(self, msg):
        self.scope_plotter.update(float(getattr(msg, self.data_field)))

    def draw(self):
        if not self.msg:
            return

        t = time.time()

        # capture changes in terminal shape at least every 0.5s
        if t - self.last_update_shape_time > 0.5:
            self.g.update_shape()
        self.g.clear()

        self.g.set_color(termgraphics.COLOR_WHITE)
        self.scope_plotter.plot()
        if self.title:
            self.g.set_color((0, 127, 255))
            self.g.text(self.title, (0, self.g.shape[1] - 4))
        self.g.draw()

