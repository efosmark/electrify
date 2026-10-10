import doctest
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

import electrify
from electrify import ac, component, constants, dc, parsetext, prefix, sum, types, util, value
from electrify.network import filter, fixture, net, network, nxcompat, solve
from electrify.quantity import (
    angular_frequency,
    capacitance,
    charge,
    current,
    duration,
    energy,
    frequency,
    impedance,
    inductance,
    magnetic_flux,
    phase,
    power,
    reactance,
    resistance,
    voltage,
    wavelength,
)


modules = [
    ac,
    component,
    constants,
    dc,
    filter,
    fixture,
    net,
    network,
    nxcompat,
    parsetext,
    angular_frequency,
    capacitance,
    charge,
    current,
    duration,
    energy,
    frequency,
    impedance,
    inductance,
    magnetic_flux,
    phase,
    power,
    reactance,
    resistance,
    voltage,
    wavelength,
    prefix,
    solve,
    sum,
    types,
    util,
    value,
]

failures = 0
for m in modules:
    result = doctest.testmod(m)
    failures += result.failed

sys.exit(1 if failures else 0)
