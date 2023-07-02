import logging
from typing import Literal, Optional, Sequence
from electrify.util import logfunc
from matplotlib.ticker import EngFormatter
from matplotlib.axes import Axes

VOLT_FORMATTER = EngFormatter('V', places=1)
AMPERE_FORMATTER = EngFormatter('A')

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

class IVCurvePlotManager(object):

    _default_ylabel = "Current (I)"
    _default_xlabel = "Voltage (V)"
    
    def __init__(self, ax: Axes):
        self.ax = ax
        self._fqline = None

    @logfunc(logger)
    def configure(
        self,
        domain: Sequence,
        hlines=None,
        vlines=None,
        vspans=None,
        ylabel=None,
        xlabel=None,
        grid:bool=True,
        x_scale:Literal["linear", "log"]="linear",
        x_bound: Optional[tuple[float,float]] = None,
        y_bound: Optional[tuple[float,float]] = None
    ):
        self.domain = domain

        self.ax.set_xscale(x_scale)
        self.ax.grid(grid)
        
        if x_bound:
            self.ax.set_xlim(x_bound[0], x_bound[1])
            self.ax.set_xbound(lower=x_bound[0], upper=x_bound[1])
        self.ax.xaxis.set_tick_params('major', width=0.5, rotation=270, labelsize=8)
        self.ax.xaxis.set_tick_params('minor', width=0.5, rotation=270, labelsize=8)
        self.ax.xaxis.set_major_formatter(VOLT_FORMATTER)
        self.ax.xaxis.set_minor_formatter(VOLT_FORMATTER)
        if xlabel is not False:
            self.ax.set_xlabel(xlabel or self._default_xlabel, fontsize=15)

        if y_bound:
            self.ax.set_ylim(y_bound[0], y_bound[1])
            self.ax.set_ybound(lower=y_bound[0], upper=y_bound[1])
        self.ax.yaxis.set_tick_params('major', width=1, labelsize=8)
        self.ax.yaxis.set_tick_params('minor', width=1, labelsize=8)
        self.ax.yaxis.set_major_formatter(AMPERE_FORMATTER)
        self.ax.yaxis.set_minor_formatter(AMPERE_FORMATTER)
        if ylabel is not False:
            self.ax.set_ylabel(ylabel or self._default_ylabel, color='b', fontsize=15)

        if hlines is not None:
            self.axhspan = self.ax.twiny()
            self.axhspan.set_axis_off()
            for hline in hlines:
                self.axhspan.axhline(y=hline, color='black', linestyle='dotted')
        
        if vlines is not None or vspans is not None:
            self.axvspan = self.ax.twinx()
            self.axvspan.set_axis_off()
            for vline in vlines or []:
                self.axvspan.axvline(x=vline, color='black', linestyle='dotted')
            for (lower, upper, color) in vspans or []:
                self.axvspan.axvspan(lower, upper, alpha=0.1, color=color)

    @logfunc(logger)
    def plot(self,  ydata, color='blue', label=None, width=2, style='-', alpha=1.0):
        self.ax.autoscale()
        if self._fqline is None:
            refs = self.ax.plot(
                self.domain,
                ydata,
                color=color,
                linewidth=width,
                label=label,
                linestyle=style,
                alpha=alpha,
            )
            self._fqline = refs[0]
        else:
            self._fqline.set_ydata(ydata)
        
    def clear(self):
        self.ax.lines.clear()
