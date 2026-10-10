
######################################################################
from lang import Operand, Keyword, Source, Command
from typing import *

class _ParserPattern:
    def __add__(self, other):...
    def __or__(self, other):...
    def __radd__(self, other):...
    def __ror__(self, other):...

class Match(_ParserPattern):
    def __init__(self, match):
        self.match = match

class ZeroToManyOf(Match):...
class ZeroToOneOf(Match):...

class OneOf(set, _ParserPattern):
    def __init__(self, *args):
        super().__init__({*args})
    def __hash__(self):
        return hash(frozenset(self))

class InOrder(tuple, _ParserPattern):
    def __new__(cls, *args):
        return super().__new__(cls, args)

ArithmeticOperation_ = OneOf(
    Operand.ADD,
    Operand.SUB,
    Operand.DIV,
    Operand.MUL,
    Operand.PARALLEL,
    Operand.SERIES
)

Assignment_ = InOrder(
    Source.LineStart,
    Keyword.SET,
    Identifier,
    Operand.ASSIGN,
    Expression,
    Source.LineBoundary
)

NumericTerm_ = InOrder(Number, ZeroToOneOf(Magnitude), ZeroToOneOf(Unit))
Scope_ = InOrder(Operand.LBRACE, ZeroToManyOf(Statement), Operand.RBRACE)

Command_ = InOrder(
    Source.LineStart,
    OneOf(Keyword.OUT, Keyword.IN),
    ZeroToOneOf(Expression),
    Source.LineBoundary
)

Statement_ = OneOf(
    Assignment_,
    Scope_,
    Command_
)
