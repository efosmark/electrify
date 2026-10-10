"""
Scanning utility for analyzing input text and providing a sequence of tokens.

This is largely used by other modules that require parsing values from string data.

Example
    >>> from electrify import parsetext
    >>> tokens = parsetext.scan("6.32 pF")
    >>> print(tokens)
    (NumberToken(value=6.32), MagnitudeToken(id='pico', magnitude=1e-12), UnitToken(id='farad'))
    >>> if parsetext.match(tokens, (parsetext.NumberToken, parsetext.MagnitudeToken, parsetext.UnitToken)):
    ...     print("It matches!")
    It matches!
"""
import enum
from functools import cache
import logging
from typing import Any, Generator, NamedTuple, Optional, Sequence, Type, TypeVar, overload
from electrify.constants import VALUE_TYPES, UNIT_SYMBOLS

DIGITS = "0123456789"

class Keyword(enum.Enum):
    AT = 'at'
    SERIES = 'series'
    PARALLEL = 'parallel'
    RESISTANCE = 'resistance'
    REACTANCE = 'reactance'
    OF = 'of'
    FREQ = 'freq'
    FREQUENCY = 'frequency'
    WAVELENGTH = 'wavelength'
    WL = 'wl'
    ANG = 'ang'
    ANGULAR = 'angular'
    PHASE = 'phase'
    MAGNITUDE = 'magnitude'
    MAG = 'mag'
    
    @classmethod
    def all_keywords(cls) -> set[str]:
        return set([kw.value for kw in Keyword])

class Operand(enum.Enum):
    AT = '@'
    PARALLEL = '|'
    SERIES = '&'
    LPAREN = '('
    RPAREN = ')'
    ADD = '+'
    SUB = '-'
    MUL = '*'
    DIV = '/'
    ASSIGN = '='
    
    @classmethod
    def parts(cls) ->set[str]:
        result = set()
        for op in cls:
            for c in op.value:
                result.add(c)
        return result
    
    @classmethod
    def all_operands(cls) -> set[str]:
        return set([op.value for op in Operand])

class IdentToken(NamedTuple):
    value:str

class NumberToken(NamedTuple):
    value: float

class MagnitudeToken(NamedTuple):
    id: str
    magnitude: float

class UnitToken(NamedTuple):
    id: str

Token = Operand|NumberToken|Keyword|MagnitudeToken|UnitToken

class ScanningError(Exception):...

class Lexer:
    """Lexical scanner for interpreting string representations of quantities/magnitudes/units."""

    _value:list[str]
    _last:str
    _line_number:int

    def __init__(self, value: str):
        """Create a new lexical scanner with the character buffer initialized."""
        self._value = list(value)
        self._value.reverse()
        self._last = ""
        self._line_number = 0
        self._column = 0
        self.logger = logging.getLogger(__name__)

    def pop(self) -> str:
        """Take the next character off of the buffer, assign it to `_last`, and return it."""
        self._last = self._value.pop()
        self._column += 1
        return self._last

    def push(self, value: str) -> None:
        """Append `value` on to the character buffer."""
        self._value.append(value)

    def last(self) -> str:
        """Get the character that was most recently popped from the character buffer."""
        return self._last

    def peek(self, idx_offset: int = 1) -> str:
        """ Look at the character on the top of the character stack, but do not remove it.

        If no character can be peeked at, an empty string is returned instead.
        """
        try:
            return self._value[0 - idx_offset]
        except IndexError:
            return ""

    def has_chars(self) -> bool:
        """Determine whether or not the stack still has characters."""
        return len(self._value) > 0

    def scan_all(self) -> tuple:
        """ Scan all of the characters in the buffer, and return a tuple of tokens.

        This is a simple helper that consumes the generator from `scan()`. For large input values,
        `scan()` should be used instead.
        """
        return tuple([t for t in self.scan()])

    def scan(self) -> Generator:
        """ Scan the character buffer and yield tokens as their found.

        Raises:
            ScanningError: Raised if an unknown character is discovered

        Yields:
            Generator: Each token is yielded as they're found
        """
        while self.has_chars():
            c = self.pop()
            token_found = False

            if c == '\n':
                self._line_number += 1
                self._column = 0
                continue
            
            # Handle things we don't care about
            if c.isspace():
                continue

            # Handle numbers
            if self._is_digit(c, self.last(), self.peek()):
                for token in self._handle_digit(c):
                    token_found = True
                    yield token
                if token_found:
                    continue

            # Handle string data (e.g. pF, nano, MHz)
            if c.isalpha():
                for token in self._handle_string(c):
                    token_found = True
                    yield token
                if token_found:
                    continue

            # Handle operators
            if c in Operand.parts():
                for token in self._handle_operand(c):
                    token_found = True
                    yield token
                if token_found:
                    continue

            raise ScanningError("Unexpected character: '{}'".format(c))

    def _is_digit(self, char: str, prev: str, peek: str) -> bool:
        """Determine whether the current character is part of a number."""
        if char in ['.', ',', 'e']:
            return prev in DIGITS and peek in DIGITS
        return char in DIGITS

    def _handle_digit(self, char: str) -> Generator:
        """Build a `tokens.Number` token based on scanned-in chars."""
        buffer = char
        while self.has_chars():
            last = self.last()
            char = self.pop()
            peek = self.peek()
            if not self._is_digit(char, last, peek):
                self.push(char)
                break
            if not self.has_chars():
                buffer += char
                break
            buffer += char
        yield NumberToken(float(buffer))

    def _handle_operand(self, char: str) -> Generator:
        """Build a `tokens.Operator` token based on scanned-in characters."""
        if char in Operand.all_operands():
            yield Operand(char)
        else:
            raise ScanningError(f"Unknown operand: '{char}'")

    def _handle_string(self, string: str) -> Generator:
        """Build tokens based on scanned input."""
        buffer = string

        # Read in the rest of the alpha text
        while self.peek() is not None and self.peek().isalpha():
            buffer += self.pop()

        # Check keywords
        if buffer.lower() in Keyword.all_keywords():
            yield Keyword(buffer.lower())

        # Check value types (e.g. pico, nano, etc)
        type_found = None
        magnitude = None
        for types, exp in VALUE_TYPES.items():
            for t in types:
                if buffer.startswith(t):
                    if type_found is None or len(t) > len(type_found):
                        type_found = t
                        magnitude = (types[0], exp)
        if type_found and magnitude is not None:
            yield MagnitudeToken(*magnitude)
            buffer = buffer[len(type_found):]

        # Check unit symbols (e.g. V, F, H)
        unit_str = buffer.upper()
        for name, symbol in UNIT_SYMBOLS.items():
            if unit_str in (name.upper(), symbol.upper()) or (unit_str.endswith('S') and unit_str[:-1] == name):
                yield UnitToken(name)
                buffer = ""

        if len(buffer) > 0:
            while self.peek() is not None and (self.peek().isalpha() or self.peek() in ['_']):
                buffer += self.pop()
            
            yield IdentToken(buffer)
            buffer = ""


def scan(text: str) -> tuple:
    """
    Scan the input text using return a sequence of tokens.

    The scanning is handled by :class:`scanner.lexer.Lexer`.

    Args:
        text(str): The input text we would like to scan

    Returns:
        tuple: Tokens representing the input text

    Example:
        >>> scan("954nH")
        (NumberToken(value=954.0), MagnitudeToken(id='nano', magnitude=1e-09), UnitToken(id='henry'))
        >>> scan("1.21 GW")
        (NumberToken(value=1.21), MagnitudeToken(id='giga', magnitude=1000000000.0), UnitToken(id='watt'))
    """
    lexer = Lexer(text)
    return lexer.scan_all()


def match(tlist: Sequence, token_types: Sequence) -> bool:
    """
    Given a sequence of tokens, determine whether the types match the token types provided.

    Args:
        tlist (Sequence): Sequence of tokens
        token_types (Sequence): Sequence of token types

    Returns:
        bool: ``True`` if all types match. ``False`` otherwise.

    Example:
        >>> match([NumberToken(123), MagnitudeToken("k", 3)], [NumberToken, MagnitudeToken])
        True
        >>> match([NumberToken(123), UnitToken("F")], [NumberToken, MagnitudeToken])
        False
    """
    if len(tlist) != len(token_types):
        return False
    for i, t in enumerate(tlist):
        if type(t) != token_types[i]:
            return False
    return True
