# Electrify

Electrify is a small Python library for electronics math, circuit-value parsing, simple
component models, and exploratory circuit/network analysis. It is organized around SI
electrical units such as `ohm`, `farad`, `henry`, `volt`, `ampere`, `hertz`, and `watt`,
with helpers for common AC/DC formulas, equivalent-value sums, filter prototypes,
NetworkX conversion, and Matplotlib plotting.

## Installation

From this folder:

```bash
python -m pip install -r requirements.txt
python -m pip install -e .
```

## Quick Start

```python
from electrify.value import from_string, format_value
from electrify.types import ohm, farad, henry, hertz, volt
from electrify.quantity.reactance import get_capacitive_reactance
from electrify.dc import voltage_divider

cap = from_string("121pF")
res = ohm(k=10)
freq = hertz(M=10)

print(cap)                              # 121pF
print(res)                              # 10kΩ
print(get_capacitive_reactance(freq, cap))
print(voltage_divider(volt(12), ohm(k=2), ohm(k=1)))  # 4V
print(format_value([ohm(100), " || ", ohm(200)]))
```

Unit instances behave like complex numbers for arithmetic, while keeping a display unit
and a more descriptive type:

```python
from electrify.types import ohm, farad

series_r = ohm(100) & ohm(220)          # resistors in series
parallel_r = ohm(100) | ohm(220)        # resistors in parallel

parallel_c = farad(n=100) | farad(n=47) # capacitors in parallel
series_c = farad(n=100) & farad(n=47)   # capacitors in series
```

For explicit list-based sums, use `electrify.sum`:

```python
from electrify.sum import sum_series, sum_parallel
from electrify.types import ohm, farad

sum_series([ohm(10), ohm(22), ohm(47)])
sum_parallel([ohm(100), ohm(100)])
sum_series([farad(u=10), farad(u=10)])
sum_parallel([farad(n=47), farad(n=100)])
```

## Project Layout

```text
electrify/
  types.py              Unit classes and numeric behavior.
  prefix.py             SI prefix objects and engineering notation formatting.
  value.py              String parsing and user-facing value formatting.
  parsetext.py          Tokenizer used by value parsing.
  dc.py                 DC helpers and diode/thermal-voltage formulas.
  ac.py                 AC, RF, impedance, gain, and loss helpers.
  sum.py                Series and parallel equivalent-value helpers.
  component.py          Simple R/C/L/V component wrappers.
  quantity/             Formula modules for derived electrical quantities.
  network/              Netlists, port networks, filters, solver, NetworkX bridge.
  plot/                 Matplotlib helpers for Bode, I/V, and circuit plots.
examples/               Scratch/example scripts; some are historical or commented.
scripts/                Utility scripts and notebooks.
```

## Core Concepts

### Unit Types

`electrify.types` defines `ElectricUnit`, the base class for unit-bearing values. Each
unit stores a complex value internally and implements Python's `numbers.Complex`
interface. The exported concrete units are:

| Class | Meaning | Symbol |
| --- | --- | --- |
| `ampere` | current | `A` |
| `coulomb` | charge | `C` |
| `farad` | capacitance | `F` |
| `henry` | inductance | `H` |
| `hertz` | frequency | `Hz` |
| `joule` | energy | `J` |
| `metre` | length | `m` |
| `ohm` | resistance, reactance, impedance | `Ω` |
| `siemens` | conductance, susceptance, admittance | `S` |
| `second` | time | `s` |
| `volt` | voltage | `V` |
| `watt` | power | `W` |
| `weber` | magnetic flux | `Wb` |

Construction supports either a raw base-unit value or a prefix keyword:

```python
from electrify.types import ohm, farad, hertz

ohm(4700)
ohm(k=4.7)
farad(n=100)
hertz(M=14.2)
```

Supported prefix keywords/symbols are `femto`/`f`, `pico`/`p`, `nano`/`n`,
`micro`/`u`/`µ`, `milli`/`m`, `kilo`/`k`, `mega`/`M`, `giga`/`G`, `tera`/`T`, and
`peta`/`P`.

### Series and Parallel Operators

Some unit classes overload `&` and `|` as circuit-composition shortcuts:

| Unit      | `a & b`    | `a \| b`     |
| --------- | ---------- | ------------ |
| `ohm`     | series sum | parallel sum |
| `henry`   | series sum | parallel sum |
| `farad`   | series sum | parallel sum |
| `siemens` | series sum | parallel sum |


The operator meanings are chosen from electrical behavior, not from the literal Python
operator names. For example, `ohm(100) | ohm(100)` returns the 50 ohm parallel equivalent,
while `farad(u=10) | farad(u=10)` returns the 20 uF parallel equivalent.

### Parsing and Formatting Values

`electrify.value.from_string()` parses compact engineering values:

```python
from electrify.value import from_string, format_value

from_string("880Ω")       # ohm(880.0)
from_string("121pF")      # farad(1.21e-10)
from_string("154.2k")     # 154200.0, no unit means a float
from_string("220")        # 220.0

format_value(0.0000068)   # 6.8µ
```

The parser accepts values in `[number][prefix][unit]`, `[number][unit]`,
`[number][prefix]`, or `[number]` form. Units are resolved through the symbols and names
in `electrify.constants.UNIT_SYMBOLS`.

## Formula Modules

The `quantity/` package contains small functions named after the inputs they use. Most
modules expose both explicit `from_*` helpers and overloaded `get_*` helpers.

Examples:

```python
from electrify.types import ampere, farad, hertz, ohm, volt
from electrify.quantity.current import from_RV
from electrify.quantity.power import from_RV as power_from_RV
from electrify.quantity.capacitance import get_capacitance
from electrify.quantity.reactance import get_capacitive_reactance

current = from_RV(R=ohm(100), V=volt(5))
power = power_from_RV(R=ohm(100), V=volt(5))
cap = get_capacitance(f=hertz(k=1), X=ohm(1000))
xc = get_capacitive_reactance(hertz(k=1), farad(n=100))
```

Available quantity areas include:

| Module | Result |
| --- | --- |
| `angular_frequency.py` | `rad_per_sec` from time or frequency |
| `capacitance.py` | `farad` from charge/voltage, RC time, reactance, or energy |
| `charge.py` | `coulomb` from time/current, capacitance/voltage, energy/voltage, or resistance/flux |
| `current.py` | `ampere` from Ohm's law, power, inductance/flux, or energy/flux |
| `duration.py` | `second` from frequency, RC, LR, current/charge, or flux/voltage |
| `energy.py` | `joule` from time/power, charge/voltage, or current/flux |
| `frequency.py` | `hertz` from period, LC resonance, wavelength, or angular frequency |
| `impedance.py` | complex impedance/admittance helpers |
| `inductance.py` | `henry` from time/resistance, reactance/frequency, flux/current, energy/current, resonance, or simple inductor geometry |
| `magnetic_flux.py` | `weber` from current/inductance, resistance/charge, energy/current, or time/voltage |
| `phase.py` | phase angle from resistance/reactance or impedance |
| `power.py` | `watt` from current/voltage, current/resistance, voltage/resistance, or time/energy |
| `reactance.py` | capacitive/inductive reactance and susceptance conversion |
| `voltage.py` | `volt` from Ohm's law, capacitance/charge, energy/charge, or current/power |
| `wavelength.py` | `metre` from period, frequency, or angular frequency |

## DC Helpers

`electrify.dc` contains compact formulas for common DC and device calculations:

```python
from electrify.dc import voltage_divider, current_divider, shockley_diode_equation, thermal_voltage
from electrify.types import ampere, ohm, volt

vout = voltage_divider(volt(12), ohm(k=10), ohm(k=10))
branch_i = current_divider(ampere(1), ohm(100), ohm(50))
diode_i = shockley_diode_equation(volt(0.65), ampere(1e-12))
vt_300k = thermal_voltage(300)
```

Important functions:

| Function | Purpose |
| --- | --- |
| `voltage_divider(V_in, R1, R2)` | Output voltage of a two-resistor divider |
| `current_divider(current, Z_branch, Z_total)` | Branch current from branch and total impedances |
| `voltage_drop(V_in, R_value, R_total)` | Series voltage drop |
| `harmonic_sum(values)` | Reciprocal sum helper |
| `shockley_diode_equation(...)` | Ideal diode current model |
| `thermal_voltage(temperature)` | `kT/q` thermal voltage |

## AC and RF Helpers

`electrify.ac` handles impedance coercion, reactance-aware component impedance, and RF
figures of merit:

```python
from electrify.ac import impedance, refl_coef, voltage_swr, return_loss_db, rc_filter_cutoff
from electrify.types import farad, hertz, ohm, watt

z_c = impedance(farad(n=100), hertz(k=1))
gamma = refl_coef(ohm(50), ohm(75))
swr = voltage_swr(ohm(50), ohm(75))
rl = return_loss_db(refl_coef=gamma)
fc = rc_filter_cutoff(ohm(k=1), ohm(k=10), farad(n=10))
```

Selected helpers:

| Function | Purpose |
| --- | --- |
| `impedance(item, frequency)` | Convert `ohm`, `siemens`, `farad`, `henry`, or any `SupportsImpedance` object to impedance |
| `characteristic_impedance(...)` | Transmission-line characteristic impedance estimate |
| `refl_coef(Z_src, Z_load)` | Reflection coefficient |
| `voltage_swr(R_ref, R_load)` | Voltage standing wave ratio |
| `return_loss_db(...)` | Return loss from powers, reflection coefficient, or SWR |
| `insertion_loss_db(...)` | Insertion loss from powers, reflection coefficient, or SWR |
| `to_db(value)` | Magnitude to dB |
| `magnitude(value)` | Complex magnitude |
| `hz_center_from_bw(lower, upper)` | Geometric center frequency |
| `rc_filter_cutoff(RS, RL, C)` | Loaded RC 3 dB cutoff |
| `voltage_gain*`, `power_gain_db`, `transducer_gain` | Gain-related helpers |

## Components

`electrify.component` wraps unit values in simple component classes that provide an
`impedance(frequency)` method:

```python
from electrify.component import R, C, L
from electrify.types import hertz, ohm

r = R(ohm(k=1))
c = C(n=100)
l = L(u=10)

for item in [r, c, l]:
    print(item, item.impedance(hertz(k=1)))
```

Current component classes:

| Class | Base unit | Impedance behavior |
| --- | --- | --- |
| `R` | `ohm` | Constant resistance |
| `C` | `farad` | Capacitive reactance at frequency |
| `L` | `henry` | Inductive reactance at frequency |
| `V` | `volt` | Voltage source with equivalent series resistance (`ESR`) |

## Networks and Filters

The `electrify.network` package models a circuit as components connected by nets. It is
built around two-terminal edges (`Side.A` and `Side.B`) and port networks.

Important types:

| Module | Types |
| --- | --- |
| `net.py` | `Side`, `Edge`, `Net`, `NetList`, `VirtualItem` |
| `network.py` | `Port`, `PortNetwork`, `OnePortNetwork`, `TwoPortNetwork`, `Series` |
| `filter.py` | `LowPassFilter`, `HighPassFilter`, `BandPassFilter` |
| `solve.py` | `Solution` and related exceptions |
| `nxcompat.py` | `to_nx(network)` for NetworkX conversion |

A minimal network:

```python
from electrify.component import R
from electrify.network.network import Series
from electrify.network.net import Side
from electrify.types import ohm

network = Series(R(ohm(100)), R(ohm(220)))
exported = network.export()

for net_id, edges in exported["nets"].items():
    print(net_id, edges)
```

Butterworth filter prototypes can be generated as two-port networks:

```python
from electrify.network.filter import LowPassFilter, HighPassFilter
from electrify.types import hertz, ohm

lpf = LowPassFilter(cutoff=hertz(M=15), num_elements=5, characteristic_impedance=ohm(50))
hpf = HighPassFilter(cutoff=hertz(M=1), num_elements=3)
```

`BandPassFilter` also exists, but its constructor currently uses raw `upper` and `lower`
values and is less polished than the low-pass/high-pass classes.

### NetworkX and Drawing

If NetworkX and Matplotlib are installed, a `PortNetwork` can be converted and drawn:

```python
import matplotlib.pyplot as plt
from electrify.network.filter import LowPassFilter
from electrify.network.nxcompat import to_nx
from electrify.plot.drawcircuit import draw_circuit
from electrify.types import hertz

network = LowPassFilter(hertz(M=10), 5)
graph = to_nx(network)
draw_circuit(graph)
plt.show()
```

## Plotting

Plot helpers are thin wrappers around Matplotlib axes.

### I/V Curves

```python
import matplotlib.pyplot as plt
from electrify.dc import shockley_diode_equation
from electrify.plot.ivcurve import IVCurvePlot2D
from electrify.types import ampere, volt

fig, ax = plt.subplots()
plot = IVCurvePlot2D(ax, imax=ampere(m=100))

y = [
    float(shockley_diode_equation(volt(v), ampere(1e-13)).magnitude)
    for v in plot.domain
]

plot.plot(y, color="orange")
plt.show()
```

### Bode Plots

```python
import matplotlib.pyplot as plt
from electrify.plot import get_domain
from electrify.plot.bode import BodePlotManager

domain = get_domain(1e3, 10e6, 100)
y_data = [0 for _ in domain]

fig, ax = plt.subplots()
bode = BodePlotManager(ax)
bode.configure(domain, hlines=[-3], f_min=1e3, f_max=10e6)
bode.plot_fq(y_data)
plt.show()
```

## The `ana` Folder

`ana/` contains an experimental analysis language with a scanner, parser, reducer, and
executor. It can parse small statements such as:

```ana
set number x := 100 pF
set text mesg := "hello"

out x
out (22pF + 33pF)
```

The executor still has unfinished operations for series and parallel expressions, and it
imports sibling modules as script-local imports. Treat this area as a prototype rather than
a supported public API.

## Running Checks

There is no central test suite configuration in this folder. Practical checks include:

```bash
python -m compileall electrify examples scripts
python scripts/run-doctests.py
python examples/ivcurve.test.py
```

`scripts/run-doctests.py` exercises doctest examples from the core API modules, including
units, parsing, AC/DC helpers, sums, components, networks, and quantity formulas. When
adding a public helper, prefer adding a short doctest to its docstring so the example stays
honest.

## Editor And Types

Electrify ships inline type annotations and a `py.typed` marker, so Pylance, Pyright, and
other PEP 561-aware tools can inspect the package directly after editable installation.
The annotations are best for API discovery and catching obvious call-shape mistakes; some
older experimental modules still use broad unions or placeholder overload implementations.

For the best editor experience:

```bash
python -m pip install -e .
```

Then import from stable modules such as:

```python
from electrify.types import farad, hertz, ohm, volt
from electrify.value import from_string, format_value
from electrify.quantity.reactance import get_capacitive_reactance
from electrify.sum import sum_parallel, sum_series
```

## Development Notes

- Prefer `electrify.types` for unit classes and `electrify.value.from_string()` for parsing
  user-entered values.
- Public functions should include a concise docstring, typed parameters/return values, and
  at least one runnable doctest when the behavior does not require a display backend.
- Use the explicit `electrify.sum` helpers when operating on sequences; use `&` and `|`
  when quick scalar composition reads better.
- Functions in `quantity/` usually return typed unit objects. If a function returns a raw
  `float` or `complex`, that is usually because the result is dimensionless, such as phase,
  gain, or a coefficient.
- The network solver is path-based and exploratory. Verify non-trivial circuit results
  against a known calculator, SPICE, or hand analysis before relying on them.
- `deprecated/` preserves older design experiments and should not be used for new code.

## Abbreviations

| Abbreviation | Meaning |
| --- | --- |
| `cap` | capacitance, capacitor |
| `ind` | inductance, inductor |
| `res` | resistance, resistor |
| `freq` | frequency |
| `pwr` | power |
| `coef` | coefficient |
| `ang` | angular |
| `len` | length |
| `deg` | degree |
| `src` | source |
| `RS` | source resistance |
| `RL` | load resistance |
| `refl` | reflection, reflected |
| `incid` | incident |
| `imp` | impedance |
| `cond` | conductance |
| `reac` | reactance |
| `ref` | reference |

Common variable conventions:

| Form | Meaning |
| --- | --- |
| `R_x` | resistance of `x` |
| `C_x` | capacitance of `x` |
| `L_x` | inductance of `x` |
| `X_x` | reactance of `x` |

## Conceptual Circuit Reference

```text
      V_src            V_in                                 V_out / V_load
        |               |                                         |
        |               |  .-----------------------------------.  |
        |               |  |                                   |  |
        |  .---------.  |  |  .--------.          .---------.  |  |  .--------.
        +--|  R_src  |--+--|--|  R_in  |--+    +--|  R_out  |--|--+--| R_load |--+
        |  '---------'     |  '--------'  |    |  '---------'  |     '--------'  |
        |                  |              |    |               |                 |
        |                  |             [G]  [G]              |                [G]
    .--------.             |                                   |
    | signal |             |                                   |
    | source |             '-----------------------------------'
    '--------'
        |
       [G]
```
