"""
Scanning utility for analyzing input text and providing a sequence of tokens.

Examples
--------
>>> # Not yet provided.
"""
from typing import Sequence
from .lexer import Lexer as __Lexer, ScanningError
from . import tokens

ValueMagnitudeUnit = (tokens.Number, tokens.Magnitude, tokens.Unit)
ValueUnit = (tokens.Number, tokens.Unit)


def scan(text: str) -> tuple:
    """
    Scan the input text using `lexer.Lexer` and return a sequence of tokens.

    Parameters
    ----------
     * `text: str` — The input text we would like to scan

    Returns
    -------
     * `tuple` — Tokens representing the input text

    Examples
    --------
    >>> # Not yet provided.
    """
    lexer = __Lexer(text)
    return lexer.scan_all()


def match(tlist: Sequence, token_types: Sequence) -> bool:
    """
    Given a sequence of tokens, determine whether the types match the token types provided.

    Parameters
    ----------
     * `tlist: Sequence` — Sequence of tokens
     * `token_types: Sequence` — Sequence of token types

    Returns
    -------
     * `bool` — `True` if all types match. `False` otherwise.

    Examples
    --------
    >>> # Not yet provided.
    """
    if len(tlist) != len(token_types):
        return False
    for i, t in enumerate(tlist):
        if type(t) != token_types[i]:
            return False
    return True


__all__ = ["scan", "match", "ScanningError", "ValueMagnitudeUnit", "ValueUnit"]
