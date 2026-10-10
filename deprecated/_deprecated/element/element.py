"""
Base elements to be used for building other elements.

Examples
--------
>>> # Not yet provided.

References
----------
None.

"""
from electrify.value import *


class Element:
    """
    Core element from which all other elements should inherit.

    See Also
    --------
    `protocol.py` -- Typing protocols for different element features

    Examples
    --------
    >>> # Not yet provided.

    References
    ----------
    None.
    """

    name: str | None

    def __init__(self, name: str | None = None):
        """
        Initialize the element with a name.

        If no name is given, it will generate one based on the `id()` of the instance.

        Parameters
        ----------
        name (str|None = None): Optional element name

        """
        if name is None:
            self.name = str(hex(id(self)))[-4:]
        else:
            self.name = name

    def __str__(self):
        """Get the string representation of the element."""
        return "<{}:{}>".format(self.__class__.__name__, self.name)

    def __repr__(self):
        """Get the string representation of the element."""
        return self.__str__()
