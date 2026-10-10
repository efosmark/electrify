""" 
    expression -> ( expression ) | term | parallel | series | context | muldiv | addsub
    term       -> NUMBER { MAGNITUDE } { UNIT }
    parallel   -> expression OP_P expression
    series     -> expression OP_S expression
    context    -> expression OP_A factor
    muldiv     -> expression { OP_MUL|OP_DIV expression }
    addsub     -> muldiv { OP_ADD|OP_SUB muldiv }
    
    set z = (a, b, c, d) -> {
        
    }
    
    set y = {
        set x = 10
        set z = 20
        
        x + z
    }
    
    set threes := [1pF to 100pF] -> filter x { x % 3 == 0 }
    
    [1pF to 100pF]
        -> filter x { x % 3 == 0 }
        -> reduce (a, b) {
            a + b
        }
    
    (a, b) -> {
        y = a * b
        
        x = 1, y
    } -> map x { 
        
    }
    
    builtin types
        number 
        string   "..."
        array    [a, b, c, ...] , [0:a, 1:b, 2:c, ...]
        hashmap  [a:1, b:2, c:3, ...]
        hashset  
    
    builtin commands
        set out in map filter
        reduce series parallel

Assignment   = (Keyword.SET, Identifier, Operand.ASSIGN, Expression, EOL)
NumericTerm  = (NumberToken, Optional[MagnitudeToken], Optional[Unit])
Scope        = (Operand.LBRACE, Optional[Many[Expression]], Operand.RBRACE)

"""
import logging
from typing import *

import scan
import lang

logging.basicConfig(format='%(name)-10s %(levelname)-8s %(message)s', level=logging.WARN)

class AnaSyntaxError(lang.AnaException):...
class AnaTypeError(AnaSyntaxError):...

def is_end_of_statement(token:lang.Token) -> bool:
    token = token.content
    return isinstance(token, (lang.Source, lang.Comment)) \
           or token is lang.Operand.RBRACE \
           or token is None

def token_is_numeric(token:lang.Token) -> bool:
    return isinstance(token.content, (lang.NumericIdentifier, lang.NumericTerm, lang.Number))

class Parser:
    logger:Final[logging.Logger] = logging.getLogger("Parser")
    scanner:scan.Scanner
    tokens:Generator
    token:lang.Token
    assigned:dict[lang.Identifier, lang.Assignment]
    
    def __init__(self, scanner:scan.Scanner):
        self.scanner = scanner
        self.tokens = scanner.scan()
        self.has_tokens = True
        self.token = next(self.tokens)
        self.assigned = {}

    def _next_token(self) -> lang.Token:
        prev = self.token
        try:
            self.token = next(self.tokens)
        except StopIteration:
            self.has_tokens = False
            self.token = lang.Token(lang.Source.End, self.scanner.location, self.scanner.location)
        self.logger.debug("accept(): %r", prev)
        return prev
    
    def accept_type(self, ttype:Type[lang.Token_T]) -> lang.Token[lang.Token_T]:
        if not isinstance(self.token.content, ttype):
            raise AnaSyntaxError(f"Unexpected {self.token.content!r}. Expected type {ttype}.")
        return self._next_token()
    
    def accept(self, *, token:lang.Token_T|None=None) -> lang.Token[lang.Token_T]:
        if token is not None and self.token.content != token:
            raise AnaSyntaxError(f"Unexpected {self.token}. Expected {token}.")
        return self._next_token()
    
    def _magnitude(self) -> lang.Token[lang.Magnitude]:
        self.logger.debug("_magnitude() START")
        if isinstance(self.token.content, lang.Magnitude):
            mag = self.accept_type(lang.Magnitude)
        else:
            raise AnaSyntaxError(f"Expected lang.Magnitude, but recieved {self.token.content}")
        self.logger.debug("_magnitude() END")
        return mag

    def _unit(self) -> lang.Token[lang.Unit]:
        self.logger.debug("_unit() START")
        if isinstance(self.token.content, lang.Unit):
            unit = self.accept_type(lang.Unit)
        else:
            raise AnaSyntaxError(f"Expected lang.Unit, but recieved {self.token.content}")
        self.logger.debug("_unit() END")
        return unit
    
    def _term(self) -> lang.NumericTerm|lang.NumericIdentifier:
        self.logger.debug("_term() START")
        if isinstance(self.token.content, lang.Number):
            term = lang.NumericTerm(
                self.accept_type(lang.Number),
                self._magnitude(),
                self._unit()
            )
        elif isinstance(self.token.content, lang.Identifier):
            term = self._identifier().content
            if not isinstance(term, lang.NumericIdentifier):
                raise AnaTypeError(f"Identifier {term!r} is not numeric.")
        else:
            raise AnaSyntaxError(f"Expected Number or NumericIdentifier, but recieved {self.token.content!r}")
        self.logger.debug("_term() END")
        return term
    
    def _identifier(self) -> lang.Token[lang.Identifier]:
        self.logger.debug("_identifier() START")
        ident_token = self.accept_type(lang.Identifier)
        ident = ident_token.content
        if ident not in self.assigned:
            raise lang.AnaException(f"Identifier {ident!r} used before assignment.")
        self.logger.debug("_identifier() Found assignment %r", self.assigned[ident])
        dtype = self.assigned[ident].data_type.content
        if dtype == lang.DataType.NUMBER:
            ident_token.content = lang.NumericIdentifier(ident)
        elif dtype == lang.DataType.TEXT:
            ident_token.content = lang.TextualIdentifier(ident)
        elif dtype == lang.DataType.BOOLEAN:
            ident_token.content = lang.BooleanIdentifier(ident)
        else:
            self.logger.warn("No data type found. %r", self.assigned[ident].data_type)
        self.logger.debug("_identifier() END %r", ident_token)
        return ident_token
    
    def _assignment(self) -> lang.Assignment:
        self.logger.debug("_assignment() START")
        self.accept(token=lang.Keyword.SET)
        dtype_token = self.accept_type(lang.DataType)
        ident_token = self.accept_type(lang.Identifier)
        self.accept(token=lang.Operand.ASSIGN)
        assignment = lang.Assignment(
            dtype_token,
            ident_token,
            self.expression(),
            ident_token.content.capitalize() == ident_token.content
        )
        ident = ident_token.content
        if ident in self.assigned:
            existing = self.assigned[ident]
            if existing.data_type.content is not dtype_token.content:
                raise AnaTypeError(f"{ident!r} is already assigned to type {existing.data_type.content!r}, not {dtype_token.content!r}.")
            elif existing.is_const:
                raise AnaTypeError(f"Cannot reassign {ident!r}, as it is marked as const.")
        else:
            self.assigned[ident] = assignment
            existing = assignment    
        self.assigned[ident_token.content] = assignment
        self.logger.debug("_assignment() END")
        return assignment
    
    def _scope(self) -> lang.Scope:
        self.logger.debug("_scope() START")
        self.accept(token=lang.Operand.LBRACE)
        scope = lang.Scope()
        for stmt in self._statement():
            scope.statements.append(stmt)
        self.accept(token=lang.Operand.RBRACE)
        self.logger.debug("_scope() END")
        return scope
    
    def _command(self) -> lang.Command:
        self.logger.debug("_command() START")
        command = self.accept_type(lang.Keyword)
        args = []
        while not is_end_of_statement(self.token):
            self.logger.debug("_command() %r", self.token)
            args.append(self.expression())
        cmd = lang.Command(command, args)
        self.logger.debug("_command() END")
        return cmd
    
    def _statement(self):
        self.logger.debug("_statement() START")
        while self.has_tokens and isinstance(self.token.content, (lang.Source, lang.Comment)):
            self.accept()
        while self.has_tokens:
            self.logger.debug("_statement() token=%r", self.token)
            token = self.token.content
            starts_at = self.token.start
            ends_at = self.token.end
            if token == lang.Keyword.SET:
                yield self._assignment()
            elif token == lang.Operand.LBRACE:
                yield self._scope()
            elif token == lang.Operand.RBRACE:
                # TODO this doesnt deal with random RBRACE tokens.
                break
            elif token in lang.COMMANDS:
                yield self._command()
            elif token == lang.Source.End:
                self.logger.debug("EOF")
                self.accept()
                yield token
                break
            elif isinstance(token, (lang.Source, lang.Comment)):
                self.accept()
            else:
                self.logger.error("_statement(): Unhandled token %r at %s to %s", token, starts_at, ends_at)
                self.accept()
        self.logger.debug("_statement() END")
        
    def numeric_expression(self) -> lang.NumericExpression:
        self.logger.debug("_expression() START token=%r", self.token)
        n = None
        while self.has_tokens and isinstance(self.token.content, (lang.Source, lang.Comment)):
            self.accept()
        if not isinstance(self.token.content, lang.Operand):
            n = self._term()
        while self.has_tokens and type(self.token.content) is lang.Operand:
            if self.token.content == lang.Operand.LPAREN:
                self.accept()
                n = self.numeric_expression()
                self.accept(token=lang.Operand.RPAREN)
            
            elif self.token.content in lang.NUMERIC_OPERANDS and n is not None:
                op = self.token.content
                op_node = lang.NumericOperation(op)
                while self.has_tokens and self.token.content == op:
                    self.accept()
                    op_node.children.append(self.numeric_expression())
                op_node.children.append(n)
                n = op_node
            
            elif self.token.content == lang.Operand.RPAREN:
                #TODO handle misc rparen tokens. should raise exception
                break

        self.logger.debug("_expression() END")
        if n is None:
            raise AnaSyntaxError("Expected an expression, but recieved none.")
        return n
    
    def expression(self) -> lang.Expression:
        while self.has_tokens and isinstance(self.token.content, (lang.Source, lang.Comment)):
            self.accept()
        
        n = None
        t = self.token.content
        if t == lang.Operand.LPAREN:
            self.accept()
            n = self.expression()
            self.accept(token=lang.Operand.RPAREN)
        
        elif t == lang.Operand.RPAREN:
            self.accept()
            # TODO
            n = None
        
        elif isinstance(t, lang.Identifier):
            if t not in self.assigned:
                raise lang.AnaException(f"{t} referenced before assignment")
            n = t
            self.accept()
        elif isinstance(t, lang.Text):
            n = t
            self.accept()
        elif token_is_numeric(self.token):
            n = self.numeric_expression()

        if n is None:
            raise AnaSyntaxError(f"Cannot evaluate expression with token {self.token!r}")
        return n
    
    def execute(self) -> Generator:
        self.logger.debug("execute() START")
        for stmt in self._statement():
            yield stmt
        if self.has_tokens:
            raise AnaSyntaxError(f"Unexpected: {self.token}")
        self.logger.debug("execute() END")

if __name__ == "__main__":
    scanner = scan.Scanner("""

set number x := 100nF
set text mesg := "hello"

out x
out mesg
""")
    
    parser = Parser(scanner)
    parser.logger.setLevel(logging.DEBUG)
    list(parser.execute())
