import logging
from typing import Optional
from matplotlib.axes import Axes

from electrify.plot.manager import PlotManager2D, generate_domain
from electrify.types import ampere, volt


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

t_electric_current = ampere|float|complex
t_voltage = volt|float|complex

class IVCurvePlot2D(PlotManager2D):
    
    def __init__(
        self,
        ax:Axes,
        vmin:t_voltage = volt(0.0),
        vmax:t_voltage = volt(1.0),
        imin:Optional[t_electric_current] = ampere(0.0),
        imax:Optional[t_electric_current] = None,
        samples:int = 100
    ):
        PlotManager2D.__init__(self, ax, generate_domain(vmin, vmax, samples))
        self.ax.grid(True)
        self.ax.set_xscale("linear")
        self.ax.set_xlabel("Voltage (V)", color="blue", fontsize=13)
        self.ax.set_xbound(lower=vmin.real, upper=vmax.real)
        self.ax.set_yscale("linear")
        self.ax.set_ylabel("Current (I)", color="red", fontsize=13)
        if imin is not None:
            self.ax.set_ylim(bottom=imin.real)
        if imax is not None:
            self.ax.set_ylim(top=imax.real)
