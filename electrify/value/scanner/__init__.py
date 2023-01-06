"""
Scanning utility for analyzing input text and providing a sequence of tokens.

This is largely used by other modules that require parsing values from string data.

Example
    >>> from electrify.value import scanner
    >>> tokens = scanner.scan("6.32 pF")
    >>> print(tokens)
    (Number(6.32), Magnitude('pico', 1e-12), Unit('farad'))
    >>> if scanner.match(tokens, (scanner.NumberToken, scanner.MagnitudeToken, scanner.UnitToken)):
    ...     print("It matches!")
    It matches!
"""
from typing import Sequence
from .lexer import Lexer, ScanningError
from .tokens import NumberToken, MagnitudeToken, UnitToken, OperatorToken, KeywordToken


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
        (Number(954), Magnitude('nano', 1e-09), Unit('henry'))
        >>> scan("1.21 GW")
        (Number(1.21), Magnitude('giga', 1000000000.0), Unit('watt'))
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


__all__ = ["scan", "match", "ScanningError", "NumberToken", "MagnitudeToken",
           "UnitToken", "OperatorToken", "KeywordToken"]
