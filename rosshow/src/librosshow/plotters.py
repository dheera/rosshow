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
        self.g.text("{:2.4f}".format(self.vmax), (int(self.xmin), int(self.ymin)))
        self.g.text("{:2.4f}".format(self.vmin), (int(self.xmin), int(self.ymax)))
        self.pointer = (self.pointer + 1) % len(self.data)

