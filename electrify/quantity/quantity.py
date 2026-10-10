import logging
from typing import ClassVar

from ..types import *

class Quantity:
    symbol: ClassVar[str]
    logger: ClassVar[logging.Logger] = logging.getLogger(__name__)

    def __str__(self) -> str:
        return f"<{self.__class__.__name__}(Quantity) symbol={self.symbol} unit={type(self.symbol)}>"
    
    def __hash__(self):
        return hash(id(self))
