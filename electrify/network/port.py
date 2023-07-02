
from electrify.network.property import NegativePole, PositivePole


class Port:
    """
    Representation of a network port.

    A port comprises two poles, which can be accessed at <instance>.pos for the Polarity.POSITIVE
    pole, and <instance>.neg for the Polarity.NEGATIVE pole.

    A shorthand is available which utilizes the ``__pos__`` and ``__neg__`` methods.

    >>> port = new Port(network, 1)
    >>> positive_pole = +port
    >>> negative_pole = -port

    A port should never be an element inside of the graph that represents the network.
    Instead, it should always be referenced toward one of its two poles.
    """
    
    pos: PositivePole
    neg: NegativePole
    
    #network
    id: int

    def __init__(self, network, port_id: int):
        """Create a new port for the given network."""
        self.network = network
        self.id = port_id
        self.pos = PositivePole()
        self.neg = NegativePole()
        self.pos.port = self
        self.neg.port = self
    
    def __iter__(self):
        yield self.pos
        yield self.neg
    
    def __pos__(self) -> PositivePole:
        return self.pos

    def __neg__(self) -> NegativePole:
        return self.neg

    def __repr__(self):
        return f'Port(port_id={self.id})'

    def __str__(self):
        return f'<{self.__repr__()} at {hex(id(self))}>'
