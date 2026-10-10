from typing import TypeVar




def harmonic_sum(values: Sequence[SupportsComplex]):
    try:
        return 1.0 / sum([(1.0 / complex(n)) for n in values])
    except ZeroDivisionError:
        return complex(0.0)

def get_capacitive_reactance(f: hertz, C: farad) -> ohm:
    if f == 0:
        return ohm(cmath.inf)
    elif C == 0:
        return ohm(0)
    return ohm(1.0 / (2.0 * cmath.pi * hertz(f) * farad(C)) * -1j)

def get_inductive_reactance(f: hertz, L: henry) -> ohm:
    if f == 0:
        return ohm(0)
    return ohm(2.0 * cmath.pi * hertz(f) * henry(L) * 1j)



def parallel(a:_T, b:_T) -> _T:...
def series(a:_T, b:_T) -> _T:...

_T = TypeVar("_T")
def add(a:_T, b:_T) -> _T:
    return a + b

def sub(a:_T, b:_T) -> _T:...
def mul(a:_T, b:_T) -> _T:...
def div(a:_T, b:_T) -> _T:...
def concat(a:_T, b:_T) -> _T:...



#
