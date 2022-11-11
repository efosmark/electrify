import logging
from electrify.util import logfunc
from gfd.solution import GFDSolution
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

    @logfunc(logger)
    def configure(
        self,
        domain: list,
        miniplot=False,
        hlines=None,
        vlines=None,
        vspans=None,
        ylabel="Gain (dB)",
        xlabel="Frequency",
        grid=True,
        f_min: float = None,
        f_max: float = None,
    ):
        self.domain = domain
        self.zero = np.zeros(len(self.domain))
        self.minus3dB = self.zero - 3.0

        self.axfq.set_xscale('log')
        self.axfq.grid(grid)
        #self.axfq.set_xlim(f_min, f_max)
        #self.axfq.set_xbound(lower=f_min, upper=f_max)

        # Secondary axes
        self.axph = self.axfq.twinx()
        self.axvspan = self.axfq.twinx()
        self.axhspan = self.axfq.twiny()
        self.axvspan.set_axis_off()
        self.axhspan.set_axis_off()

        # Phase axis
        #self.axph.set_ylim(-100, 100)
        #self.axph.set_ybound(-100, 100)
        self.axph.yaxis.set_tick_params('major', width=1, labelsize=8)
        self.axph.yaxis.set_tick_params('minor', width=1, labelsize=8)

        if miniplot:
            self.axfq.set_ylim(bottom=-65, top=1)
            self.axfq.set_ybound(lower=-65, upper=1)
            self.axfq.set_axis_off()
            self.axph.set_axis_off()
            return

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
        if vlines is not None:
            for vline in vlines:
                self.axvspan.axvline(x=vline, color='black', linestyle='dotted')
        if hlines is not None:
            for hline in hlines:
                self.axhspan.axhline(y=hline, color='black', linestyle='dotted')
        if vspans is not None:
            for (lower, upper, color) in vspans:
                self.axvspan.axvspan(lower, upper, alpha=0.1, color=color)

    @logfunc(logger)
    def plot_fq(self, solution: GFDSolution, color='blue', label=None, width=2, style='-', alpha=1.0, persist=False):
        if self._fqline is None or persist:
            refs = self.axfq.plot(
                self.domain,
                solution.y_gain,
                color=color,
                linewidth=width,
                label=label or "Gain",
                linestyle=style,
                alpha=alpha,
            )
            self._fqline = refs[0]
            if persist:
                while len(self.axfq.lines) > 50:
                    self.axfq.lines.pop(0)
            # else:
            #    self.axfq.set_ybound(min(solution.y_gain), max(solution.y_gain))
            #    self.axfq.set_ylim(min(solution.y_gain), max(solution.y_gain))

        else:
            self._fqline.set_ydata(solution.y_gain)
            self.axfq.autoscale()
            #self.axfq.set_ybound(min(solution.y_gain), max(solution.y_gain))
            #self.axfq.set_ylim(min(solution.y_gain), max(solution.y_gain))

    def plot_ph(self, solution: GFDSolution):
        if self._y_phase_cache is None:
            ref = self.axph.plot(
                self.domain,
                np.rad2deg(solution.y_phase_rad),
                color="green",
                linewidth=1
            )
            self._y_phase_cache = ref[0]
        else:
            self._y_phase_cache.set_ydata(solution.y_phase)
