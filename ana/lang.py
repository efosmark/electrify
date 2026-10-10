from collections import defaultdict
from functools import cache
from typing import Any, ClassVar, Container, Generic, Literal, NamedTuple, Optional, TypeVar, Union, Sequence
import enum

EOF = '\0'
EOL = '\n'

CHR_EOL = '\n'
CHR_TAB = '\t'
CHR_SPACE = ' '
CHR_UNDERSCORE = '_'

# Numeric symbols
DECIMAL_MARK = '.'
DIGIT_GROUP_DELIM = ' '
E_NOTATION_MARK = 'e'
IMAGINARY_MARK = 'i'

STRING_DELIMITER = '"'
STRING_ESCAPE = "\\"

COMMENT_START = '#'
COMMENT_STOP = EOL

class SymbolSet:
    ALPHA_LOWER = 'abcdefghijklmnopqrstuvwxyz'
    ALPHA_UPPER = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    ALPHA = ALPHA_LOWER + ALPHA_UPPER
    NUMBER = '01234567890'
    ALNUM = ALPHA + NUMBER
    
    IDENT_FIRST = ALPHA + '_'
    IDENT_BODY = ALNUM + '_'
    
    IGNORED_CHARS = {CHR_SPACE, CHR_TAB}

#############################
## Tokens
#############################

class Identifier(str):
    def __repr__(self):
        return f'Identifier({super().__repr__()})'

class NumericIdentifier(Identifier):...
class TextualIdentifier(Identifier):...
class BooleanIdentifier(Identifier):...
class ContainerIdentifier(Identifier):...

class Boolean(enum.Enum):
    FALSE = 0
    TRUE = 1
    def __repr__(self):
        return f'Boolean({self.name})'

class Number(complex):
    def __repr__(self):
        return f'Number({super().__repr__()})'

class Text(str):
    def __repr__(self):
        return f'Text({super().__repr__()})'

class Comment(str):
    def __repr__(self):
        return f'Comment({super().__repr__()})'

class Source(enum.Enum):
    LineBoundary = 0
    End = 1

class Magnitude(enum.Enum):
    PICO = 'pico'
    NANO = 'nano'
    MICRO = 'micro'
    MILLI = 'milli'
    KILO = 'kilo'
    MEGA = 'mega'
    GIGA = 'giga'
    TERA = 'tera'

class Unit(enum.Enum):
    AMPERE = 'ampere'
    FARAD = 'farad'
    HENRY = 'henry'
    HERTZ = 'hertz'
    JOULE = 'joule'
    METRE = 'metre'
    OHM = 'ohm'
    RADIAN = 'radian'
    RADPERSEC = 'radpersec'
    SIEMENS = 'siemens'
    VOLT = 'volt'
    WATT = 'watt'

class Keyword(enum.Enum):
    NOOP = 'noop'
    SET = 'set'
    OUT = 'out'
    TRUE = 'true'
    FALSE = 'false'

class DataType(enum.Enum):
    NUMBER = 'number'
    TEXT = 'text'
    BOOLEAN = 'bool'
    HASHSET = 'hashset'
    HASHMAP = 'hashmap'
    LIST = 'list'
    TUPLE = 'tuple'

class Operand(enum.Enum):
    COMMENT_START = '#'
    AT = '@'
    PARALLEL = '||'
    SERIES = '&&'
    LPAREN = '('
    RPAREN = ')'
    LBRACE = '{'
    RBRACE = '}'
    ADD = '+'
    SUB = '-'
    MUL = '*'
    DIV = '/'
    ASSIGN = ':='
    
    GT = '>'
    LT = '<'
    GTE = '>='
    LTE = '<='
    EQ = '=='
    NEQ = '!='
    
Token_T = TypeVar('Token_T', bound=Identifier|DataType|Source|Comment|Unit|Magnitude|Number|Keyword|Operand|Text)

class Loc(NamedTuple):
    line:int
    col:int
    def __str__(self):
        return f'{self.line}.{self.col}'
    
class Token(Generic[Token_T]):
    start:Loc
    end:Loc
    content:Token_T
    
    def __init__(self, value:Token_T, start:Loc, end:Loc):
        self.content = value
        self.start = start
        self.end = end
        
    def __str__(self):
        return f'{self.content!r}@[{self.start}-{self.end}]'
    
    __repr__ = __str__

Statement = Any

symbol_to_unit:dict[str, Unit] = {
    'A': Unit.AMPERE,
    'F': Unit.FARAD,
    'H': Unit.HENRY,
    'Hz': Unit.HERTZ,
    'J': Unit.JOULE,
    'm': Unit.METRE,
    'R': Unit.OHM,
    'Ω': Unit.OHM,
    'rad': Unit.RADIAN,
    'rad/s': Unit.RADPERSEC,
    'S': Unit.SIEMENS,
    '℧': Unit.SIEMENS,
    'V': Unit.VOLT,
    'W': Unit.WATT
}

symbol_to_magnitude:dict[str, Magnitude] = {
    'p': Magnitude.PICO,
    'n': Magnitude.NANO,
    'u': Magnitude.MICRO,
    'm': Magnitude.MILLI,
    'k': Magnitude.KILO,
    'M': Magnitude.MEGA,
    'G': Magnitude.GIGA,
    'T': Magnitude.TERA
}

magnitude_to_power:dict[Magnitude, int] = {
    Magnitude.PICO: -12,
    Magnitude.NANO: -9,
    Magnitude.MICRO: -6,
    Magnitude.MILLI: -3,
    Magnitude.KILO: 3,
    Magnitude.MEGA: 6,
    Magnitude.GIGA: 9,
    Magnitude.TERA: 12
}

NUMERIC_OPERANDS:set[Operand] = {
    Operand.ADD,
    Operand.SUB,
    Operand.MUL,
    Operand.DIV,
    Operand.PARALLEL,
    Operand.SERIES
}

COMMANDS:set[Keyword] = {
    Keyword.OUT,
    Keyword.SET,
    Keyword.NOOP
}

#############################
## Nodes
#############################

class Command(NamedTuple):
    id:Token[Keyword]
    args:list[Token]

class Assignment(NamedTuple):
    data_type:Token[DataType]
    identifier:Token[Identifier]
    value:Any
    is_const:bool

class NumericTerm(NamedTuple):
    number: Token[Number]
    magnitude: Optional[Token[Magnitude]]
    unit: Optional[Token[Unit]]

class Scope:
    locals:dict[Identifier, Any]
    statements: list[Statement]
    def __init__(self):
        self.locals = {}
        self.statements = []

class NumericOperation:
    node_type:Operand
    children:list['NumericExpression|NumericIdentifier']
    
    def __init__(self, node_type:Operand):
        self.node_type = node_type
        self.children = list()
    
    def __str__(self):
        return f'({self.node_type} {", ".join([str(b) for b in self.children])})'
    
    __repr__ = __str__


NumericExpression = Union[
    Token[Number],
    NumericTerm,
    NumericIdentifier,
    NumericOperation
]

Expression = Union[
    NumericExpression,
    Token[Text],
    Text,
    Identifier,
    TextualIdentifier,
    BooleanIdentifier,
    ContainerIdentifier
]

class AnaException(Exception):
    ...


#############################
## LOADER FUNCS
#############################

@cache
def all_unit_mag_combinations() -> dict[str, tuple[Magnitude, Unit]]:
    result = {}
    
    for unit in Unit:
        for magnitude in Magnitude:
            result[f"{magnitude.value}{unit.value}"] = (magnitude, unit)
    
    for unit_symbol, unit in symbol_to_unit.items():
        for mag_symbol, magnitude in symbol_to_magnitude.items():
            result[f"{mag_symbol}{unit_symbol}"] = (magnitude, unit)
    
    result.update([(m.value, (m, None)) for m in Magnitude])
    result.update([(u.value, (None, u)) for u in Unit])
    result.update([(mstr, (Magnitude(mag), None)) for mstr, mag in symbol_to_magnitude.items()])
    #result.update([(ustr, (None, Unit(unit))) for ustr, unit in symbol_to_unit.items()])
    
    return result

#
