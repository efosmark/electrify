from .figurecanvas import FigureCanvas
import matplotlib.gridspec as gridspec
from gfd.profile import GFDProfile
from gfd.solution import GFDSolution
import numpy as np
from matplotlib.ticker import EngFormatter

import matplotlib
matplotlib.use('Qt5Agg')


DEFAULT_TICK_PARAMS = dict(width=1, rotation=270, labelsize=8)
DEFAULT_HVLINE_PARAMS = dict(color='black', linestyle='dotted')
HZ_FORMATTER = EngFormatter('Hz', places=0)


class BodePlotCanvas(FigureCanvas):

    def __init__(self, parent=None):
        FigureCanvas.__init__(self, parent=parent)
        self._fqline = None
        self._fqrefs = []
        self._phline = None
        self._y_derivative_cache = None
        self._y_phase_cache = None
        self._y_polar_phase_cache = None

    def configure(
        self,
        profile: GFDProfile,
        hlines=None,
        vlines=None,
        vspans=None,
        width=800,
        height=400,
        tight=True,
        ylabel="Gain (dB)",
        xlabel="Frequency",
        yticks=True,
        xticks=True,
        grid=True,
        include_polar=False
    ):
        if width and height:
            self.figure.set_size_inches(width / 100.0, height / 100.0)
        self.figure.set_tight_layout(tight)
        self.profile = profile
        self.zero = np.zeros(self.profile.sample_count)
        self.minus3dB = self.zero - 3.0
        self.include_polar = include_polar

        if include_polar:
            self.gs = gridspec.GridSpec(1, 3)
            self.axfq = self.figure.add_subplot(self.gs[0:2])

            self.axpolar = self.figure.add_subplot(self.gs[2], projection='polar')
            # self.axpolar.set_thetamin(-90)
            # self.axpolar.set_thetamax(90)
            self.axpolar.xaxis.set_tick_params('major', width=1, labelsize=8, direction='out', pad=-4)
            self.axpolar.set_yticklabels([])
        else:
            self.axfq = self.figure.add_subplot(111)

        #
        self.axvspan = self.axfq.twinx()
        self.axhspan = self.axfq.twiny()
        self.axvspan.set_axis_off()
        self.axhspan.set_axis_off()

        # Derivative axis
        self.axdv = self.axfq.twinx()

        # Phase axis
        self.axph = self.axfq.twinx()
        self.axph.set_ylim(-100, 100)
        self.axph.set_ybound(-100, 100)
        self.axph.yaxis.set_tick_params('major', width=1, labelsize=8)
        self.axph.yaxis.set_tick_params('minor', width=1, labelsize=8)

        self.configure_axfq(hlines, vlines, vspans, ylabel, xlabel, yticks, xticks, grid)

    def configure_axfq(
        self,
        hlines=None,
        vlines=None,
        vspans=None,
        ylabel="Gain (dB)",
        xlabel="Frequency",
        yticks=True,
        xticks=True,
        grid=True,
    ):
        self.axfq.set_xscale('log')
        self.axfq.grid(grid)
        self.axfq.set_xlim(self.profile.f_min, self.profile.f_max)
        self.axfq.set_xbound(lower=self.profile.f_min, upper=self.profile.f_max)

        if xticks:
            self.axfq.xaxis.set_tick_params('major', width=1, rotation=270, labelsize=8)
            self.axfq.xaxis.set_tick_params('minor', width=1, rotation=270, labelsize=8)
            self.axfq.xaxis.set_major_formatter(HZ_FORMATTER)
            self.axfq.xaxis.set_minor_formatter(HZ_FORMATTER)
        else:
            self.axfq.set_xticks([])
            self.axfq.set_xticks([], minor=True)
            self.axfq.set_xticklabels([])
            self.axfq.set_xticklabels([], minor=True)

        if yticks:
            self.axfq.yaxis.set_tick_params('major', width=1, labelsize=8)
            self.axfq.yaxis.set_tick_params('minor', width=1, labelsize=8)
        else:
            self.axfq.set_yticks([])
            self.axfq.set_yticks([], minor=True)
            self.axfq.set_yticklabels([])
            self.axfq.set_yticklabels([], minor=True)

        if ylabel:
            self.axfq.set_ylabel(ylabel, color='b', fontsize=15)
        if xlabel:
            self.axfq.set_xlabel(xlabel, fontsize=15)
        if vlines is not None:
            for vline in vlines:
                self.axvspan.axvline(x=vline, **DEFAULT_HVLINE_PARAMS)
        if hlines is not None:
            for hline in hlines:
                self.axhspan.axhline(y=hline, **DEFAULT_HVLINE_PARAMS)
        if vspans is not None:
            for (lower, upper, color) in vspans:
                self.axvspan.axvspan(lower, upper, alpha=0.1, color=color)

    def plot_fq(self, solution: GFDSolution, color='blue', label=None, width=2, style='-', alpha=1.0, persist=False):
        if self._fqline is None or persist:
            refs = self.axfq.plot(
                solution.profile.domain,
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
            self.axfq.autoscale()
        else:
            self._fqline.set_ydata(solution.y_gain)

    def plot_dv(self, solution: GFDSolution):
        if self._y_derivative_cache is None:
            ref = self.axdv.plot(
                solution.profile.derivative_domain,
                solution.gain_derivative,
                color="purple",
                linewidth=1
            )
            self._y_derivative_cache = ref[0]
        else:
            self._y_derivative_cache.set_ydata(solution.gain_derivative)

    def plot_ph(self, solution: GFDSolution):
        if self.include_polar:
            if self._y_polar_phase_cache is None:
                ref = self.axpolar.plot(
                    solution.y_phase_rad,
                    solution.profile.domain,
                    color="green",
                    linewidth=1,
                )
                self._y_polar_phase_cache = ref[0]
            else:
                self._y_polar_phase_cache.set_data(solution.y_phase_rad, solution.profile.domain)

        if self._y_phase_cache is None:
            ref = self.axph.plot(
                solution.profile.domain,
                np.rad2deg(solution.y_phase_rad),
                color="green",
                linewidth=1
            )
            self._y_phase_cache = ref[0]
        else:
            self._y_phase_cache.set_ydata(solution.y_phase)

    def fq_clear(self):
        self.axfq.lines.clear()
