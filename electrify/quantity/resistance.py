"""Functions for determining resistance and conductance values."""
import cmath
from typing import *
from ..types import *
from .quantity import Quantity
from ..constants import COLOR_CODES as CC

class R(Quantity, ohm):
    @overload
    def __new__(cls, *, I: ampere, V: volt) -> Self: ...
    @overload
    def __new__(cls, *, P: watt, V: volt) -> Self: ...
    @overload
    def __new__(cls, *, I: ampere, P: watt) -> Self: ...
    @overload
    def __new__(cls, *, Q: coulomb, U: weber) -> Self: ...
    @overload
    def __new__(cls, *, Z: ohm) -> Self: ...
    @overload
    def __new__(cls, *, Z: ohm, phase: float) -> Self: ...
    @overload
    def __new__(cls, *, G: siemens) -> Self: ...
    @overload
    def __new__(cls, value: complex | SupportsComplex | SupportsFloat | SupportsIndex):...
    def __new__(
        cls,
        value: Optional[complex | SupportsComplex | SupportsFloat | SupportsIndex] = None,
        **kwargs,
    ) -> Self:
        self = super().__new__(cls)
        
        
        return self
    
    def impedance(self, frequency:hertz) -> ohm:
        return ohm(self)
    
    @classmethod
    def from_IV(cls, I: ampere, V: volt) -> Self:
        """Get resistance in ohms from electric current in amperes and voltage in volts."""
        return cls(ohm(volt(V) / ampere(I)))

    @classmethod
    def from_tL(cls, t: second, L: henry) -> Self:
        """Get resistance in ohms from time in seconds and inductance in henrys."""
        return cls(ohm(henry(L) / second(t)))

    @classmethod
    def from_tC(cls, t: second, C: farad) -> Self:
        """Get resistance in ohms from time in seconds and capacitance in farads."""
        return cls(ohm(second(t) / farad(C)))

    @classmethod
    def from_PV(cls, P: watt, V: volt) -> Self:
        """Get resistance in ohms from power in watts and voltage in volts."""
        return cls(ohm(volt(V)**2 / watt(P)))

    @classmethod
    def from_IP(cls, I: ampere, P: watt) -> Self:
        """Get resistance in ohms from electric current in amperes and power in watts."""
        return cls(ohm(watt(P) / ampere(I)**2))

    @classmethod
    def from_QU(cls, Q: coulomb, U: weber) -> Self:
        """Get resistance in ohms from electric charge in coulombs and magnetic flux in webers."""
        return cls(ohm(weber(U) / coulomb(Q)))

    @classmethod
    def from_Z(cls, Z: ohm, phase: Optional[float] = None) -> Self:
        """Get reactance in ohms from impedance in the form (R+Xj) in ohms."""
        if phase is not None:
            Z = ohm(cmath.rect(Z.real, phase))
        if not isinstance(Z, complex):
            raise TypeError("Z must be a complex value in the form of (R+Xj)."
                            "Otherwise, the phase angle must be supplied.")
        return cls(ohm(Z.real))

    @classmethod
    def resistance_from_Q(cls, Q: float, X: float) -> Self:
        """
        Get the element resistance from its quality factor and reactance.

        Args:
            Q (float): Quality Factor
            X (float): Reactance in Ohms

        Returns:
            float : Resistance in Ohms

        Examples
        --------
        >>> # Not yet provided.

        References
        ----------
        None.
        """
        if X == 0:
            return cls(0)
        return cls(ohm(Q / abs(X)))

    @classmethod
    def from_G(cls, G: siemens) -> Self:
        """Get resistance in ohms from conductance in siemens."""
        return cls(ohm(1.0 / siemens(G)))

    @overload
    @classmethod
    def from_color_code(cls, first: str, second: str, third: str) -> Self: ...
    
    @overload
    @classmethod
    def from_color_code(cls, first: str, second: str, third: str, forth: str) -> Self: ...
    
    @classmethod
    def from_color_code(cls, first: str, second: str, third: str, forth: Optional[str|None] = None) -> Self:
        """
        Create a new `Resistor` with a resistance value defined by the color codes.

        ```
            Code     Digit
            ------   ------
            black    0
            brown    1
            red      2
            orange   3
            yellow   4
            green    5
            blue     6
            violet   7
            gray     8
            white    9
            gold     0.1
            silver   0.01
        ```

        Args:
            first (str): First color code band
            second (str): Second color code band
            third (str): Third color code band
            forth (str | None = None): Optional forth color code band
        """
        if forth is None:
            value = (CC[first] * 10) + CC[second]
            return cls(ohm(value * (10**CC[third])))
        value = (CC[first] * 100) + (CC[second] * 10) + CC[third]
        return cls(ohm(value * (10**CC[forth])))
