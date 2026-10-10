import logging
from numbers import Number
from typing import Any, Dict, Generic, Literal, Optional, Sequence, Tuple, TypeVar

from matplotlib.ticker import EngFormatter
from matplotlib.axes import Axes

VOLT_FORMATTER = EngFormatter('V', places=1)
AMPERE_FORMATTER = EngFormatter('A')

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

def generate_domain(start, stop, num_steps, max_inclusive=True) -> list:
    """
    Generate an evenly spaced numeric domain.

    Examples:
        >>> generate_domain(0, 1, 4)
        [0.0, 0.25, 0.5, 0.75, 1]
    """
    step_size = (stop - start) / float(num_steps)
    domain = [start + (x * step_size) for x in range(num_steps)]
    if max_inclusive and stop not in domain:
        domain.append(stop)
    return domain

Scale = Literal["linear", "log"]
Bound = Tuple[Number, Number]

_X = TypeVar("_X", float, complex)
_Y = TypeVar("_Y", float, complex)

class PlotManager2D(Generic[_X, _Y]):
    
    DEFAULT_LINE_SETTINGS:Dict[Any,Any] = dict(color='black', linestyle='dotted')
    DEFAULT_TEXT_SETTINGS:Dict[Any,Any] = dict(
        fontsize=8,
        fontstyle="italic",
        color='red',
        fontfamily="monospace",
    )
    DEFAULT_PLOT_SETTINGS:Dict[Any,Any] = dict(color='blue', label=None, linewidth=2, linestyle='-', alpha=1.0)
    
    domain:Sequence[_X]
    
    def __init__(self, ax: Axes, domain:Sequence[_X]):
        self.ax = ax
        self.domain = domain
        
        self.axv = ax.twinx()
        self.axv.set_axis_off()
        
        self.axh = ax.twiny()
        self.axh.set_axis_off()
        

    def vline(self, x:_X, text:Optional[str] = None, *, text_kwargs:Optional[dict]=None, **kwargs):
        line_settings = dict(self.DEFAULT_LINE_SETTINGS)
        line_settings.update(kwargs)
        line = self.axv.axvline(x.real, **line_settings)
        if text is not None:
            text_settings = dict(self.DEFAULT_TEXT_SETTINGS,
                #verticalalignment='top',
                #horizontalalignment='center',
                rotation=90,
            )
            if text_kwargs is not None:
                text_settings.update(text_kwargs)
            
            ylim = self.ax.axes.get_ylim()
            y_text_offset = ylim[0] - (((ylim[1]-ylim[0])/100.0) * 2.5)
            self.ax.text(
                x=x.real,
                y=y_text_offset,
                s=text,
                **text_settings,
            )
        return line

    def hline(self, y:_Y, text:Optional[str] = None, *, text_kwargs:Optional[dict]=None, **kwargs):
        line_settings = dict(self.DEFAULT_LINE_SETTINGS)
        line_settings.update(kwargs)
        line = self.axh.axhline(y.real, **line_settings)
        if text is not None:
            text_settings = dict(self.DEFAULT_TEXT_SETTINGS,
                #verticalalignment='center',
                #horizontalalignment='right'
            )
            if text_kwargs is not None:
                text_settings.update(text_kwargs)
            
            xlim = self.ax.axes.get_xlim()
            x_text_offset = xlim[0] - (((xlim[1]-xlim[0])/100.0) * 2.5)
            self.ax.text(
                x=x_text_offset,
                y=y.real,
                s=text,
                **text_settings,
            )
        return line

    def plot(self, ydata:Sequence[_Y], **kwargs):
        settings = dict(self.DEFAULT_PLOT_SETTINGS, **kwargs)
        refs = self.ax.plot([d.real for d in self.domain], ydata, **settings)
        return refs[0]
