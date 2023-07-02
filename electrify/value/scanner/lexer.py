"""
Lexical scanner for interpreting string representations of quantities/magnitudes/units.

Examples
--------
>>> # Not yet provided.

"""
import logging
from typing import Generator
from electrify.constants import VALUE_TYPES, UNIT_SYMBOLS
from . import tokens

DIGITS = "0123456789"
OPERAND_PARTS = ['+', '|', '@', "(", ")"]
KEYWORDS = ["at", "resistance", "reactance", "x",
            "of", "frequency", "wavelength", "angular"]

KW_AT = "at"

OP_KW_AT = "@"
OP_PARALLEL = "||"
OP_SERIES = "+"
OP_LPAREN = "("
OP_RPAREN = ")"


class ScanningError(Exception):
    """Primary exception raised by the scanner."""

    pass


class Lexer:
    """Lexical scanner for interpreting string representations of quantities/magnitudes/units."""

    _value: list[str]
    _result: list[tokens.LexicalToken]
    _last: str

    def __init__(self, value: str):
        """Create a new lexical scanner with the character buffer initialized."""
        self._value = list(value)
        self._value.reverse()
        self._result = []
        self._last = ""

        self.logger = logging.getLogger(__name__)

    def pop(self) -> str:
        """
        Take the next character off of the buffer, assign it to `_last`, and return it.

        Returns
        -------
         * `str` — The next (now current) character off of the buffer
        """
        self._last = self._value.pop()
        return self._last

    def push(self, value: str) -> None:
        """
        Append `value` on to the character buffer.

        Mainly used internally.

        Parameters
        ----------
        value (str): The value to be appended to the character buffer
        """
        self._value.append(value)

    def last(self) -> str:
        """
        Get the character that was most recently popped from the character buffer.

        This value changes each time `pop()` is called.

        Returns
        -------
         * `str` — The most recent character
        """
        return self._last

    def peek(self, idx_offset: int = 1) -> str:
        """
        Look at the character on the top of the character stack, but do not remove it.

        If no character can be peeked at, an empty string is returned instead.

        Parameters
        ----------
         * `idx_offset: int = 1` — Offset from the top of the stack

        Returns
        -------
         * `str` — The character at the top of the stack
        """
        try:
            return self._value[0 - idx_offset]
        except IndexError:
            return ""

    def has_chars(self) -> bool:
        """
        Determine whether or not the stack still has characters.

        Returns
        -------
         * `bool` — `True` if there are characters remaining, `False` otherwise
        """
        return len(self._value) > 0

    def scan_all(self) -> tuple:
        """
        Scan all of the characters in the buffer, and return a tuple of tokens.

        This is a simple helper that consumes the generator from `scan()`. For large input values,
        `scan()` should be used instead.

        Returns
        -------
         * `tuple[tokens.LexicalToken]` — The sequence of tokens from the input buffer
        """
        return tuple([t for t in self.scan()])

    def scan(self) -> Generator:
        """
        Scan the character buffer and yield tokens as their found.

        Raises:
            ScanningError: Raised if an unknown character is discovered

        Yields:
            Generator: Each token is yielded as they're found
        """
        while self.has_chars():
            c = self.pop()
            token_found = False

            # Handle things we don't care about
            if c.isspace() or c == '-':
                continue

            # Handle numbers
            if self._is_digit(c, self.last(), self.peek()):
                for token in self._handle_digit(c):
                    token_found = True
                    self.logger.debug(f'Number: {token}')
                    yield token
                if token_found:
                    continue

            # Handle string data (e.g. pF, nano, MHz)
            if c.isalpha():
                for token in self._handle_string(c):
                    token_found = True
                    self.logger.debug(f'String data token found: {token}')
                    yield token
                if token_found:
                    continue

            # Handle operators
            if c in OPERAND_PARTS:
                for token in self._handle_operand(c):
                    token_found = True
                    self.logger.debug(f'Operand token found: {token}')
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
        yield tokens.NumberToken(buffer)

    def _handle_operand(self, char: str) -> Generator:
        """Build a `tokens.Operator` token based on scanned-in characters."""
        buffer = char
        if char == '|':
            if self.peek() == '|':
                buffer += self.pop()
                yield tokens.OperatorToken(OP_PARALLEL)
            else:
                yield False
        elif char == '+':
            yield tokens.OperatorToken(OP_SERIES)
        elif char == '@':
            yield tokens.KeywordToken(KW_AT)
        elif char == '(':
            yield tokens.OperatorToken(OP_LPAREN)
        elif char == ')':
            yield tokens.OperatorToken(OP_RPAREN)

    def _handle_string(self, string: str) -> Generator:
        """Build `tokens.Keyword`, `tokens.Magnitude`, or `tokens.Unit` based on scanned input."""
        buffer = string

        # Read in the rest of the alpha text
        while self.peek() is not None and self.peek().isalpha():
            buffer += self.pop()

        # Check keywords
        if buffer.upper() in KEYWORDS:
            yield tokens.KeywordToken(buffer.upper())

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
            yield tokens.MagnitudeToken(*magnitude)
            buffer = buffer[len(type_found):]

        # Check unit symbols (e.g. V, F, H)
        for name, symbol in UNIT_SYMBOLS.items():
            unit_str = buffer.upper()
            if unit_str in (name, symbol) or (unit_str.endswith('S') and unit_str[:-1] == name):
                yield tokens.UnitToken(name)
                buffer = ""

        if len(buffer) > 0:
            raise ScanningError("Unknown string: '{}'".format(buffer))
