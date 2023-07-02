from electrify.formula import shockley_diode_equation, thermal_voltage
from electrify.plot import IVCurvePlotManager, get_domain
from electrify.value import *
import matplotlib.pyplot as plt

fig, ax = plt.subplots()

d = get_domain(0, 1, 1000)
    
diode_data = [
    shockley_diode_equation(
        voltage=volt(r), 
        saturation_current=ampere(1e-15),
        quality_factor=1,
        thermal_voltage=volt(0.026)
    ) for r in d
]

ivc = IVCurvePlotManager(ax)
ivc.configure(d, vlines=[0.7], y_bound=(0, 0.1))
ivc.plot(diode_data)

plt.show()
