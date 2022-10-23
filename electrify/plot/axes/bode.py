from gfd.profile import GFDProfile
from gfd.solution import GFDSolution
import numpy as np
from matplotlib.ticker import EngFormatter, NullFormatter, FixedLocator

import matplotlib
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
matplotlib.use('Qt5Agg')


DEFAULT_TICK_PARAMS = dict(width=1, rotation=270, labelsize=8)
DEFAULT_HVLINE_PARAMS = dict(color='black', linestyle='dotted')
HZ_FORMATTER = EngFormatter('Hz', places=0)


def decibel_major_locator(ax):
    bottom, top = ax.get_ylim()
    ticks = []
    for f in range(int(bottom), int(top), 1):
        if -12 <= f <= 12:
            if f % 3 == 0:
                ticks.append(f)
        elif f % 10 == 0:
            ticks.append(f)
    ax.yaxis.set_major_locator(FixedLocator(ticks))


def configure(
    ax,
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
):
    ax.zero = np.zeros(self.profile.sample_count)
    ax.minus3dB = ax.zero - 3.0

    ax.set_xscale('log')
    ax.grid(grid)
    ax.set_xlim(self.profile.f_min, self.profile.f_max)
    ax.set_xbound(lower=self.profile.f_min, upper=self.profile.f_max)

    if xticks:
        ax.xaxis.set_tick_params('major', width=1, rotation=270, labelsize=8)
        ax.xaxis.set_tick_params('minor', width=1, rotation=270, labelsize=8)
        ax.xaxis.set_major_formatter(HZ_FORMATTER)
        ax.xaxis.set_minor_formatter(HZ_FORMATTER)
    else:
        ax.set_xticks([])
        ax.set_xticks([], minor=True)
        ax.set_xticklabels([])
        ax.set_xticklabels([], minor=True)

    if yticks:
        ax.yaxis.set_tick_params('major', width=1, labelsize=8)
        ax.yaxis.set_tick_params('minor', width=1, labelsize=8)
    else:
        ax.set_yticks([])
        ax.set_yticks([], minor=True)
        ax.set_yticklabels([])
        ax.set_yticklabels([], minor=True)

    if ylabel:
        ax.set_ylabel(ylabel, color='b', fontsize=15)
    if xlabel:
        ax.set_xlabel(xlabel, fontsize=15)
    if vlines is not None:
        for vline in vlines:
            ax.axvline(x=vline, **DEFAULT_HVLINE_PARAMS)
    if hlines is not None:
        for hline in hlines:
            ax.axhline(y=hline, **DEFAULT_HVLINE_PARAMS)
    if vspans is not None:
        for (lower, upper, color) in vspans:
            ax.axvspan(lower, upper, alpha=0.1, color=color)


def plot_fq(self, solution: GFDSolution, color='blue', label=None, width=2, style='-', alpha=1.0, persist=False):
    if self._fqline is None or persist:
        refs = ax.plot(
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
            while len(ax.lines) > 50:
                ax.lines.pop(0)
    else:
        self._fqline.set_ydata(solution.y_gain)
