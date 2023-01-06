
from .energy import E
from .capacitance import C
from .charge import Q
from .current import I
from .frequency import f
from .impedance import Z, Y
from .inductance import L
from .magnetic_flux import U
from .phase import phase
from .power import P
from .reactance import X, B
from .resistance import R, G
from .duration import t
from .voltage import V


by_symbol = {
    "C": C,
    "E": E,
    "Q": Q,
    "I": I,
    "f": f,
    "Z": Z,
    "Y": Y,
    "L": L,
    "U": U,
    "phase": phase,
    "P": P,
    "X": X,
    "B": B,
    "R": R,
    "G": G,
    "t": t,
    "V": V
}
