import logging
import cmath
from typing import *
#from electrify.types import *

import lang
import scan
import parse

logging.basicConfig(format='%(name)-10s %(levelname)-8s %(message)s', level=logging.WARN)

class AnaRuntimeError(lang.AnaException):
    ...

# def harmonic_sum(values: Sequence[SupportsComplex]):
#     try:
#         return 1.0 / sum([(1.0 / lang.Number(n)) for n in values])
#     except ZeroDivisionError:
#         return lang.Number(0.0)

# def get_capacitive_reactance(f: hertz, C: farad) -> ohm:
#     if f == 0:
#         return ohm(cmath.inf)
#     elif C == 0:
#         return ohm(0)
#     return ohm(1.0 / (2.0 * cmath.pi * hertz(f) * farad(C)) * -1j)

# def get_inductive_reactance(f: hertz, L: henry) -> ohm:
#     if f == 0:
#         return ohm(0)
#     return ohm(2.0 * cmath.pi * hertz(f) * henry(L) * 1j)

class Executor:
    logger:Final[logging.Logger] = logging.getLogger("Executor")
    scope_stack:list[lang.Scope]
    
    def __init__(self, parser:parse.Parser):
        self.parser = parser
        self.scope_stack = [lang.Scope()]
        self._resolvers = {
            lang.Operand.ADD: self.resolve_addition,
            lang.Operand.SUB: self.resolve_subtraction,
            lang.Operand.MUL: self.resolve_multiplication,
            lang.Operand.DIV: self.resolve_division,
            lang.Operand.SERIES: self.resolve_series,
            lang.Operand.PARALLEL: self.resolve_parallel,
        }
    
    @property
    def current_scope(self) -> lang.Scope:
        return self.scope_stack[-1]
    
    @property
    def locals(self) -> dict[lang.Identifier, lang.Expression]:
        result = {}
        for scope in self.scope_stack:
            result.update(scope.locals)
        return result
    
    def resolve_term(self, term:lang.NumericTerm|lang.Identifier) -> SupportsComplex:
        if isinstance(term, lang.Identifier):
            num = self.locals[term]
            return self.evaluate_numeric(cast(lang.NumericExpression, num))
        value = term.number.content
        if term.magnitude is not None:
            value = value * (10 ** lang.magnitude_to_power[term.magnitude.content])
        #if term.unit is not None:
        #    unit_name = term.unit.content.value
        #    value = units_by_name[unit_name](value)
        return value
    
    def resolve_addition(self, addition:lang.NumericOperation) -> lang.Number:
        result = self.evaluate_numeric(addition.children[0])
        for a in addition.children[1:]:
            result = result + self.evaluate_numeric(a)
        return lang.Number(result)
    
    def resolve_subtraction(self, subtraction:lang.NumericOperation) -> lang.Number:
        result = self.evaluate_numeric(subtraction.children[0])
        for a in subtraction.children[1:]:
            result = result - self.evaluate_numeric(a)
        return lang.Number(result)
        
    def resolve_multiplication(self, multiplication:lang.NumericOperation) -> lang.Number:
        result = self.evaluate_numeric(multiplication.children[0])
        for a in multiplication.children[1:]:
            result = result * self.evaluate_numeric(a)
        return lang.Number(result)
    
    def resolve_division(self, division:lang.NumericOperation) -> lang.Number:
        result = self.evaluate_numeric(division.children[0])
        for a in division.children[1:]:
            result = result / self.evaluate_numeric(a)
        return lang.Number(result)
        
    def resolve_parallel(self, parallel:lang.NumericOperation) -> lang.Number:
        raise NotImplementedError("Not finished. Needs to look at units in the asssignment table.")
    
    def resolve_series(self, series:lang.NumericOperation) -> lang.Number:
        raise NotImplementedError("Not finished. Needs to look at units in the asssignment table.")

    def evaluate_numeric(self, node:lang.NumericExpression) -> lang.Number:
        self.logger.debug("evaluate(%r)", node)
        value:Any = node
        if isinstance(value, lang.Token):
            value = value.content
        if isinstance(value, lang.NumericTerm):
            value = self.resolve_term(value)
        elif isinstance(value, lang.NumericOperation):
            if value.node_type not in self._resolvers:
                raise AnaRuntimeError("No resolution for node %r", value)
            value = self._resolvers[value.node_type](value)
        elif isinstance(value, lang.NumericIdentifier):
            value = self.locals[value]
        else:
            raise AnaRuntimeError(f"Cannot evaluate {value!r}")
        return lang.Number(value)

    def evaluate(self, node:lang.Expression) -> lang.Number|lang.Text:
        self.logger.debug("evaluate(%r)", node)
        value:Any = node
        if isinstance(value, lang.Token):
            value = value.content
        
        if isinstance(value, lang.NumericTerm):
            value = self.resolve_term(value)
        elif isinstance(value, lang.NumericOperation):
            if value.node_type not in self._resolvers:
                raise AnaRuntimeError("No resolution for node %r", value)
            value = self._resolvers[value.node_type](value)
        elif isinstance(value, lang.Identifier):
            value = self.locals[value]
        elif isinstance(value, lang.Text):
            pass
        else:
            raise AnaRuntimeError(f"Unknown value type {value!r}")
        return value

    def execute_scope(self, scope:lang.Scope):
        self.scope_stack.append(scope)
        for stmt in scope.statements:
            self.execute(stmt)
        last_scope = self.scope_stack.pop()
        if last_scope is not scope:
            raise AnaRuntimeError("Scope out of sync!")
    
    def execute_command(self, command:lang.Command):
        self.logger.debug(f"execute_command({command})")
        if command.id.content == lang.Keyword.OUT:
            for a in command.args:
                print(self.evaluate(a), end=" ")
    
    def execute_assignment(self, assign:lang.Assignment):
        self.logger.debug(f"execute_assignment({assign})")
        self.current_scope.locals[assign.identifier.content] = self.evaluate(assign.value)
    
    def execute(self, node:lang.Scope):
        self.logger.debug(f"execute({node})")
        value:SupportsComplex|lang.Scope = node
        if isinstance(value, lang.Token):
            value = value.content
            
        if isinstance(value, lang.Command):
            self.execute_command(value)
        elif isinstance(value, lang.Assignment):
            self.execute_assignment(value)
        elif isinstance(value, lang.Scope):
            self.execute_scope(value)
        elif isinstance(value, (lang.Source, lang.Comment)):
            self.logger.debug(f"Skipping {value}")
        else:
            raise AnaRuntimeError(f"Unexpected: {value}")
    
    def result(self):
        return self.evaluate(self.parser.numeric_expression())

if __name__ == "__main__":
    def evaluate(text:str):
        parser = parse.Parser(scan.Scanner(text))
        executor = Executor(parser)
        return executor.result()
    
    #assert evaluate("100pF || 100pF") == farad(p=200)
    #assert evaluate("(10ohm && 5ohm)") == ohm(15)
    #assert evaluate("10uH && 11nH") == henry(u=10.011)
    #assert evaluate("( 50.0 / 25 * 4 + ( 9 - 7 ))") == -6

    log_level = logging.DEBUG    
    file_contents = open("./ana/test.ana").read()

    scanner = scan.Scanner(file_contents)
    scanner.logger.setLevel(log_level)
    
    parser = parse.Parser(scanner)
    parser.logger.setLevel(log_level)
    
    exec = Executor(parser)
    exec.logger.setLevel(log_level)
    
    for stmt in parser.execute():
        exec.execute(stmt)
