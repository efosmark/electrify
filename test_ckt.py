import numpy as np

from electrify.math import voltage_divider
from electrify.circuit.circuit import Circuit, Shunt
from electrify.component import Capacitor, Inductor, Load, VoltageSource, Resistor

import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def get_test_ckt_plot_func():
    src = VoltageSource(voltage=100.0, ESR=50.0)
    load = Load(50.0)

    c = Circuit()
    c + src
    c + Shunt(Capacitor(pF=131.5))
    c + Inductor(nH=858.4)
    c + Shunt(Capacitor(pF=424.4))
    c + Inductor(nH=858.4)
    c + Shunt(Capacitor(pF=131.5))
    c + load
    c + c.GND
    c.reduce(max_iteration=15)

    def v_plt_db(f):
        sln = c.solve(f=f, source=src, load=load)
        V_in = voltage_divider(
            sln[src]['voltage'],   # V_source
            sln[src]['res_self'],  # R_source
            sln[load]['res_self']  # R_load
        )
        V_load = sln[load]['voltage']
        return (20 * np.log10(V_load / V_in)).real

    return v_plt_db


@timing.log(logger)
def example(a, b, c=1):
    return a + b + c


@timing.log(logger)
def example2(a, b, c=1):
    return a + b - c


example(1, 2)
example(1, 2)
example2(231, 2, c=34)
example2(1, 6735)
example(1, 2)
example(1, 2)
example2(1, 2, c=6)
