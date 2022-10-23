from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg

import matplotlib
matplotlib.use('Qt5Agg')


class FigureCanvas(FigureCanvasQTAgg):

    def __init__(self, parent=None):
        self.figure = Figure()
        self.figure.set_tight_layout(True)
        FigureCanvasQTAgg.__init__(self, self.figure)
        self.setParent(parent)
        self.setContentsMargins(0, 0, 0, 0)
