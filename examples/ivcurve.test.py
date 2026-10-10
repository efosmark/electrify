from typing import Sequence
from electrify.dc import shockley_diode_equation
from electrify.plot import IVCurvePlot2D, get_domain
from electrify.plot.ivcurve import IVCurvePlot2D
from electrify.types import *
import matplotlib.pyplot as plt

def numeric_derivative(xdata:Sequence, ydata:Sequence, delta:int = 1):
    """Determine an approximation of the derivative of the given sequences."""
    return [
        abs(ya-yb)/abs(xa-xb)
        for ya, yb, xa, xb in zip(ydata[::delta], ydata[1::delta], xdata[::delta], xdata[1::delta])
    ]

def find_threshold_idx(xdata:Sequence, ydata:Sequence, delta:int = 1):
    """Find the threshold at which the ydata begins increasing faster than xdata."""
    y_diff = numeric_derivative(xdata, ydata, delta)
    th_idx = 0
    th = None
    for i, y in enumerate(y_diff):
        if xdata[i] == 0:
            continue
        ratio = abs(1-(y/xdata[i]))
        if th is None or ratio < th:
            th_idx = i
            th = ratio
    return th_idx

def plot_diode_characteristics(
    saturation_current:ampere|float,
    quality_factor:int = 1,
    thermal_voltage:volt|float = volt(0.026),
    v_min:volt|float = 0.0,
    v_max:volt|float = volt(1.0),
    i_min:ampere|float = 0.0,
    i_max:ampere|float = ampere(m=100)
):
    fig, ax = plt.subplots()
    ax.set_title("I/V Curve")
    ivc = IVCurvePlot2D(ax, imax=ampere(0.1))

    diode_data = [
        float(shockley_diode_equation(
            voltage=volt(r), 
            saturation_current=ampere(saturation_current),
            quality_factor=quality_factor,
            thermal_voltage=volt(thermal_voltage)
        ).magnitude) for r in ivc.domain
    ]
    
    print(diode_data)
    
    #th_idx = find_threshold_idx(ivc.domain, diode_data, 1)
    #ivc.hline(diode_data[th_idx].real, str(ampere(diode_data[th_idx])))
    #ivc.vline(ivc.domain[th_idx].real, str(volt(ivc.domain[th_idx])))
    
    ivc.plot(diode_data, color='orange')
    plt.show()

if __name__ == "__main__":
    plot_diode_characteristics(1e-13)
