import cmath
import logging
from typing import Any, ClassVar, Generic, Optional, TypeVar, Callable

from electrify.network.property import Property
from ..value.unit import *
from ..value.depsolver import DependencySolver, BFS_DependencySolver

_UT = TypeVar("_UT", bound=base_unit | float)
_F = TypeVar("_F", bound=Callable[..., Any])

logging.basicConfig(encoding='utf-8', format='%(levelname)s:%(message)s')


class Quantity(Property[_UT]):
    solver: ClassVar[DependencySolver] = BFS_DependencySolver()
    by_symbol: ClassVar[dict[str, "Quantity"]] = {}
    by_name: ClassVar[dict[str, "Quantity"]] = {}
    symbol: str = ""
    name: str = ""
    logger: ClassVar[Optional[logging.Logger]] = logging.getLogger(__name__)

    # def __new__(cls, symbol: str, name: Optional[str] = None):
    #     if symbol in cls.by_symbol:
    #         if cls != type(cls.by_symbol[symbol]):
    #             raise NameError(f"A quantity already exists with the symbol '{symbol}'.")
    #         else:
    #             return cls.by_symbol[symbol]

    #     if name is None:
    #         name = cls.__name__

    #     if name in cls.by_name:
    #         return cls.by_name[name]

    #     obj = super(Quantity, cls).__new__(cls)
    #     obj.symbol = symbol
    #     cls.by_symbol[symbol] = obj

    #     if type(obj) != Quantity:
    #         new_members = set(dir(cls)) - set(dir(Quantity))
    #         for nm in new_members:
    #             cls.solver.register_solution(obj.symbol, getattr(cls, nm))
    #     return obj

    def __str__(self) -> str:
        """Provide a string representation of the quantity object."""
        return f"<{self.__class__.__name__}(Quantity) symbol={self.symbol} unit={type(self.symbol)}>"

    def solution(self, func: _F) -> _F:
        self.solver.register_solution(self.symbol, func)
        return func

    def get(self, **kwargs) -> _UT:
        """Solve for the quantity based on the values given."""
        result = self.solver.solve(self.symbol, **kwargs)
        self.solver.logger.debug("N: %s", self.solver._N)
        if result is None:
            raise TypeError("No value found.")
        return result

    __call__ = get
