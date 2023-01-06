"""Tokens emitted by the scanner."""


class LexicalToken:
    """Base class from which all tokens should inherit."""

    pass


class OperatorToken(LexicalToken):
    """
    Lexical token for operators.

    Currently supported operators:
     * `@` -- At symbol
     * `||` -- Parallel symbol
     * `+` -- Series symbol
     * `(` -- Left-parenthesis
     * `)` -- Right-parenthesis

    The operator is stored in the `<Operator>.id` property.
    """

    id: str

    def __init__(self, op: str):
        """Initialize a new `Operator` token with the `id` equal to the op input."""
        self.id = op

    def __repr__(self) -> str:
        """Get the string representation of the token."""
        return f'Operator(\'{self.id}\')'


class NumberToken(LexicalToken):
    """Lexical token for numeric values."""

    number: str
    value: float

    def __init__(self, value: str):
        """Initialize a new `Number` token with the input value being a float-compatible string."""
        self.number = value
        self.value = float(value)

    def __repr__(self) -> str:
        """Get the string representation of the token."""
        return f'Number({self.number})'


class KeywordToken(LexicalToken):
    """
    Lexical token for keywords.

    Currently supported keywords:
     * `at`
     * `resistance`
     * `reactance`
     * `x`
     * `of`
     * `frequency`
     * `wavelength`
     * `angular`
    """

    id: str

    def __init__(self, kw: str):
        """Create a new `Keyword` token with the given keyword string."""
        self.id = kw

    def __repr__(self) -> str:
        """Get the string representation of the token."""
        return f'Keyword({self.id})'


class MagnitudeToken(LexicalToken):
    """
    Lexical token for magnitudes.

    The supported magnitudes can be found in `electrify.constants.VALUE_TYPES`.
    """

    id: str
    magnitude: float

    def __init__(self, magname: str, magnitude: float):
        """Create a new `Magnitude` token with the given name and magnitude value."""
        self.id = magname
        self.magnitude = magnitude

    def __repr__(self) -> str:
        """Get the string representation of the token."""
        return f'Magnitude(\'{self.id}\', {self.magnitude})'


class UnitToken(LexicalToken):
    """
    Lexical token for units / data-types.

    The supported units can be found in `electrify.constants.UNIT_SYMBOLS`.
    """

    id: str

    def __init__(self, unit: str):
        """Create a new `Unit` token with the given unit string value."""
        self.id = unit

    def __repr__(self) -> str:
        """Get the string representation of the token."""
        return f'Unit(\'{self.id}\')'
