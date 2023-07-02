import logging
from typing import Optional, Sequence
from electrify.util import logfunc
import numpy as np
from matplotlib.ticker import EngFormatter
from matplotlib.axes import Axes

HZ_FORMATTER = EngFormatter('Hz', places=0)


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class BodePlotManager(object):

    def __init__(self, axfq: Axes):
        self.axfq = axfq
        self._fqline = None
        self._phline = None
        self._y_phase_cache = None

    #@logfunc(logger)
    def configure(
        self,
        domain: Sequence,
        hlines=None,
        vlines=None,
        vspans=None,
        ylabel="Gain (dB)",
        xlabel="Frequency",
        grid=True,
        f_min: Optional[float] = None,
        f_max: Optional[float] = None,
    ):
        self.domain = domain
        self.zero = np.zeros(len(self.domain))
        self.minus3dB = self.zero - 3.0

        # Set up the primary axes that shows the gain / attenuation
        self.axfq.set_xscale('log')
        self.axfq.grid(grid)
        self.axfq.set_xlim(f_min, f_max)
        self.axfq.set_xbound(lower=f_min, upper=f_max)
        self.axfq.xaxis.set_tick_params('major', width=0.5, rotation=270, labelsize=8)
        self.axfq.xaxis.set_tick_params('minor', width=0.5, rotation=270, labelsize=8)
        self.axfq.xaxis.set_major_formatter(HZ_FORMATTER)
        self.axfq.xaxis.set_minor_formatter(HZ_FORMATTER)
        self.axfq.yaxis.set_tick_params('major', width=1, labelsize=8)
        self.axfq.yaxis.set_tick_params('minor', width=1, labelsize=8)
        if ylabel:
            self.axfq.set_ylabel(ylabel, color='b', fontsize=15)
        if xlabel:
            self.axfq.set_xlabel(xlabel, fontsize=15)

        # Set up the axes that plots the phase
        self.axph = self.axfq.twinx()
        self.axph.yaxis.set_tick_params('major', width=1, labelsize=8)
        self.axph.yaxis.set_tick_params('minor', width=1, labelsize=8)
        
        if hlines is not None:
            self.axhspan = self.axfq.twiny()
            self.axhspan.set_axis_off()
            for hline in hlines:
                self.axhspan.axhline(y=hline, color='black', linestyle='dotted')
        
        if vlines is not None or vspans is not None:
            self.axvspan = self.axfq.twinx()
            self.axvspan.set_axis_off()
            for vline in vlines or []:
                self.axvspan.axvline(x=vline, color='black', linestyle='dotted')
            for (lower, upper, color) in vspans or []:
                self.axvspan.axvspan(lower, upper, alpha=0.1, color=color)

    #@logfunc(logger)
    def plot_fq(self, y_data: Sequence, color='blue', label=None, width=2, style='-', alpha=1.0):
        if self._fqline is None:
            refs = self.axfq.plot(
                self.domain,
                y_data,
                color=color,
                linewidth=width,
                label=label or "Gain",
                linestyle=style,
                alpha=alpha,
            )
            self._fqline = refs[0]
        else:
            self._fqline.set_ydata(y_data)
            self.axfq.autoscale()

    def plot_ph(self, y_data):
        if self._y_phase_cache is None:
            ref = self.axph.plot(
                self.domain,
                y_data, #np.rad2deg(solution.y_phase_rad),
                color="green",
                linewidth=1
            )
            self._y_phase_cache = ref[0]
        else:
            self._y_phase_cache.set_ydata(y_data)

    def clear(self):
        self.axfq.lines.clear()
