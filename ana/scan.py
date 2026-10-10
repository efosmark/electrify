from collections import defaultdict
import collections.abc
from typing import Any, Callable, Final, Generator, Sequence

import logging
logging.basicConfig(format='%(name)-10s %(levelname)-8s %(message)s', level=logging.WARN)

import lang
import util


class ScanningError(lang.AnaException):
    def __init__(self, message:str, scanner:'Scanner'):
        self.scanner = scanner
        line, col = scanner.location
        m = [
            f"{message} LN:{line} COL:{col}",
            "",
            #scanner.get_snapshot()
        ]
        super().__init__("\n".join(m))

class UnexpectedSymbol(ScanningError):
    def __init__(self, scanner, symbol:str, expected:str|None=None):
        if expected is None:
            m = f"Recieved unexpected symbol {symbol!r}"
        else:
            m = f"Expected {expected!r}, but recieved {symbol!r}"
        super().__init__(m, scanner)

class UnexpectedEOF(ScanningError):
    ...

class ParserSearch:
    resolution:dict
    branchlets:dict[Sequence, set]
    
    def __init__(self):
        self.resolution = dict()
        self.branchlets = defaultdict(set)
    
    def add_to_tree(self, series:Sequence, res_value:Any):
        if series in self.resolution:
            raise IndexError(f"Series {repr(series)} is already in the tree.")
        self.resolution[series] = res_value        
        for i in range(len(series)):
            self.branchlets[series[:i]].add(series[i])

    def lookup(self, series:Sequence):
        return (self.resolution.get(series), self.branchlets[series])

lookup = ParserSearch()
for ttype in (lang.Operand, lang.Keyword, lang.DataType):
    for t in ttype:
        lookup.add_to_tree(t.value, t)
for um,combo in lang.all_unit_mag_combinations().items():
    lookup.add_to_tree(um, combo)


class Scanner:
    class EOF(Exception):...
    
    source_code:str
    index:int = 0
    line_idx:list[int]
    
    logger:Final[logging.Logger] = logging.getLogger("Scanner")

    _token_start_loc:lang.Loc
    _token_end_loc:lang.Loc|None
    
    def __init__(self, value: str):
        self.source = value
        self.line_idx = [1]
        self._token_start_loc = self.location
        self._token_end_loc = None

    @property
    def location(self) -> lang.Loc:
        line = 1
        col = self.index
        if len(self.line_idx) > 0:
            line = len(self.line_idx)
            col = self.index - self.line_idx[-1]
        return lang.Loc(line, col)
    
    @property
    def current(self) -> str:
        return self.source[self.index]
    
    @property
    def next(self) -> str:
        return self.source[self.index+1]
    
    @property
    def has_chars(self) -> bool:
        try:
            self.source[self.index+1]
            return True
        except IndexError:
            return False
    
    def get_line(self, lineno:int) -> str:
        return self.source[self.line_idx[lineno-1]+1:self.line_idx[lineno]]
    
    def advance(self):
        if not self.has_chars:
            raise Scanner.EOF()
        self.index += 1
        if self.current == lang.EOL:
            self.line_idx.append(self.index)
        self.logger.debug("READ %r", self.current)
        return self.current
    
    def scan(self):
        for t in self._scan_all():
            self.logger.debug("EMIT %r", t)
            end = self.location if self._token_end_loc is None else self._token_end_loc
            yield lang.Token(t, start=self._token_start_loc, end=end)
    
    def _handle_symbol(self):
        self.logger.debug("_handle_symbol() %r", self.current)
        self._token_start_loc = self.location
        self._token_end_loc = None
        if self.current in lang.SymbolSet.IGNORED_CHARS:
            yield self._scan_empty()
        elif self.current == lang.COMMENT_START:
            yield self._scan_comment()
        elif self.current == lang.EOL:
            yield lang.Source.LineBoundary
        elif self.current.isdigit():
            yield self._scan_number()
        elif self.current == lang.STRING_DELIMITER:
            yield self._scan_string()
        else:
            for t in self._scan_tree():
                yield t
    
    def _scan_tree(self):
        self.logger.debug("_scan_tree() %r", self.current)
        buffer:str = self.current
        token, lookahead = lookup.lookup(buffer)
        self.logger.debug("LOOKUP:%r TOKEN:%r LOOKAHEAD:%r", buffer, token, lookahead)
        while len(lookahead) > 0 and self.has_chars and not self.next.isspace():
            self.advance()
            buffer += self.current
            token, lookahead = lookup.lookup(buffer)
            self.logger.debug("LOOKUP:%r TOKEN:%r LOOKAHEAD:%r", buffer, token, lookahead)
        if token is not None:
            if isinstance(token, collections.abc.Sequence):
                for t in token:
                    self._token_end_loc = self.location
                    yield t
            else:
                self._token_end_loc = self.location
                yield token
        elif util.is_valid_identifier(buffer):
            yield self._scan_identifier(buffer)
        elif len(buffer) > 0:
            self.logger.error("Reached EOF with unresolved symbols: %r", buffer)
            raise UnexpectedSymbol(self, buffer)
        else:
            self.logger.error("Unhandled state; buffer=%r")
        
    def _scan_all(self) -> Generator:
        if self.has_chars:
            yield lang.Source.LineBoundary
        
        while self.has_chars:
            try:    
                self.advance()
            except Scanner.EOF:
                self.logger.debug("Reached EOF")
                yield lang.Source.End
                break
            
            for t in self._handle_symbol():
                yield t

    def _scan_empty(self):
        self.logger.debug("_scan_empty()")
        while self.current.isspace():
            self.advance()

    def _scan_identifier(self, buffer:str) -> lang.Identifier:
        self.logger.debug("_scan_identifier(%r) START", buffer)
        self.advance()
        while self.current in lang.SymbolSet.IDENT_BODY:
            buffer += self.current
            try:
                self.advance()
            except Scanner.EOF:
                break
        self.logger.debug("_scan_identifier() END %r", buffer)
        return lang.Identifier(buffer)

    def _scan_until(self, callable:Callable[[], bool], *, allow_EOF:bool) -> str:
        buffer = []
        while callable():
            buffer.append(self.current)
            self._token_end_loc = self.location
            try:
                self.advance()
            except Scanner.EOF:
                if allow_EOF:
                    break
                raise
        return "".join(buffer)
    
    def _scan_number(self) -> lang.Number:
        self.logger.debug("_scan_number() START")
        buffer = self._scan_until(lambda:self.current.isdigit(), allow_EOF=False)
        self.logger.debug("_scan_number() END")
        return lang.Number(complex(buffer))

    def _scan_string(self) -> lang.Text:
        self.logger.debug("_scan_string() START")
        buffer:str = ""
        escaped = False
        while True:
            try:
                self.advance()
            except Scanner.EOF:
                raise UnexpectedEOF("End of file met from within a string.", self)
            if self.current == lang.STRING_ESCAPE and not escaped:
                escaped = True
                continue
            elif self.current is lang.STRING_DELIMITER and not escaped:
                break
            else:
                buffer += self.current
                escaped = False
        self.advance()
        self.logger.debug("_scan_string() END %r", buffer)
        return lang.Text(buffer)
        
    def _scan_comment(self):
        self.logger.debug("_scan_comment() START")
        buffer:str = ""
        while True:
            if self.current == lang.EOL:
                break
            buffer += self.current
            self.advance()
        comment = buffer.strip()
        self.logger.debug("_scan_comment() END %r", comment)
        return lang.Comment(comment)

if __name__ == "__main__":
    s = Scanner("""

set number x := 100nF
set text mesg := "hello"

out x
out mesg


""")
    
    s.logger.setLevel(logging.ERROR)
    s.logger.setLevel(logging.DEBUG)
    
    log = logging.getLogger("__main__")
    log.setLevel(logging.DEBUG)
    list(s.scan())
    # for n in [n for n in s.scan()]:
    #     line = s.get_line(n.start.line)
    #     start_idx = n.start.col
    #     end_idx = n.end.col
    #     if n.end.line != n.start.line:
    #         end_idx = s.line_idx[n.start.line+1] - s.line_idx[n.start.line]
        
    #     log.debug("% 40r %r", n, line)
    #     log.debug(
    #         (" " * 42) + 
    #         (" " * (n.start.col-1)) +
    #         ("^" * (n.end.col - n.start.col+1))
    #     )

#
