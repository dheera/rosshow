import math
import librosshow.termgraphics as termgraphics
from librosshow.plotters import ScopePlotter

class SinglePlotViewer(object):
    def __init__(self, title = "", data_field = "data"):
        self.g = termgraphics.TermGraphics()
        self.xmax = 10
        self.title = title
        self.data_field = data_field

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
        self.g.clear()
        self.scope_plotter.plot()
        self.g.draw()

