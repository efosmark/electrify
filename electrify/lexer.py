from .constants import VALUE_TYPES, UNIT_SYMBOLS

DIGITS = "0123456789"
OPERAND_PARTS = ['+', '|', '@', "(", ")"]
KEYWORDS = ["at", "resistance", "reactance", "x",
            "of", "frequency", "wavelength", "angular"]


class LexerToken(object):
    pass


class OperatorToken(LexerToken):
    def __init__(self, op):
        self.op = op


class NumberToken(LexerToken):
    def __init__(self, value):
        self.value = float(value)


class KeywordToken(LexerToken):
    def __init__(self, kw):
        self.kw = kw


class MagnitudeToken(LexerToken):
    def __init__(self, magname, magnitude):
        self.magname = magname
        self.magnitude = magnitude


class UnitToken(LexerToken):
    def __init__(self, unit):
        self.unit = unit


class LexerError(Exception):
    pass


class ElectrifyLexer(object):

    def __init__(self, value):
        self._value = list(value)
        self._value.reverse()
        self._result = []
        self._last = ""

    def pop(self):
        self._last = self._value.pop()
        return self._last

    def push(self, value):
        return self._value.append(value)

    def last(self):
        return self._last

    def peek(self, n=1):
        try:
            return self._value[0-n]
        except IndexError:
            return ""

    def has_chars(self):
        return len(self._value) > 0

    def is_digit(self, c, prev, peek):
        if c in ['.', ',', 'e']:
            return prev in DIGITS and peek in DIGITS
        return c in DIGITS

    def scan_all(self):
        return [t for t in self.scan()]

    def scan(self):
        while self.has_chars():
            c = self.pop()
            token_found = False

            # Handle things we don't care about
            if c.isspace() or c == '-':
                continue

            # Handle numbers
            if self.is_digit(c, self.last(), self.peek()):
                for token in self.handle_digit(c):
                    token_found = True
                    yield token
                if token_found:
                    continue

            # Handle string data (e.g. pF, nano, MHz)
            if c.isalpha():
                for token in self.handle_string(c):
                    token_found = True
                    yield token
                if token_found:
                    continue

            # Handle operators
            if c in OPERAND_PARTS:
                for token in self.handle_operand(c):
                    token_found = True
                    yield token
                if token_found:
                    continue

            raise LexerError("Unexpected character: '{}'".format(c))

    def handle_digit(self, char):
        
        buffer = char
        while self.has_chars():
            last = self.last()
            char = self.pop()
            peek = self.peek()
            if not self.is_digit(char, last, peek):
                self.push(char)
                break
            if not self.has_chars():
                break
            buffer += char
        yield NumberToken(buffer)

    def handle_operand(self, char):
        buffer = char
        if char == '|':
            if self.peek() == '|':
                buffer += self.pop()
                yield OperatorToken(PARALLEL)
            else:
                yield False
        elif char == '+':
            yield OperatorToken(SERIES)
        elif char == '@':
            yield KeywordToken(KEYWORD, "at")
        elif char == '(':
            yield OperatorToken(LPAREN)
        elif char == ')':
            yield OperatorToken(RPAREN)

    def handle_string(self, string):
        buffer = string

        # Read in the rest of the alpha text
        while self.peek() is not None and self.peek().isalpha():
            buffer += self.pop()

        # Check keywords
        if buffer.upper() in KEYWORDS:
            yield KeywordToken(KEYWORD, buffer)

        # Check value types (e.g. pico, nano, etc)
        type_found = None
        for types, exp in VALUE_TYPES.items():
            for t in types:
                if buffer.startswith(t):
                    if type_found is None or len(t) > len(type_found):
                        type_found = t
                        magnitude = (types[0], exp)
        if type_found:
            yield MagnitudeToken(*magnitude)
            buffer = buffer[len(type_found):]

        # Check unit symbols (e.g. V, F, H)
        for name, symbol in UNIT_SYMBOLS.items():
            unit_str = buffer.upper()
            if unit_str in (name, symbol) or (unit_str.endswith('S') and unit_str[:-1] == name):
                yield UnitToken(name)
                buffer = ""

        if len(buffer) > 0:
            raise LexerError("Unknown string: '{}'".format(buffer))


def matches_types(tokens, token_types):
    for i, t in enumerate(tokens):
        if type(t) != token_types[i]:
            return False
    return True
