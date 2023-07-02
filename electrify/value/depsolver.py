"""
Dependency-solving tools.

Given a series of functions representing solutions, this will search for which function(s) can be
solved with the input variables. It will resolve in a cascade-style if a dependency of a dependency
can be resolved.
"""
from abc import ABCMeta, abstractmethod
from collections import defaultdict
import inspect
import logging
from typing import Any, Generic, TypeVar, Callable
from .unit import *

_UT = TypeVar("_UT", bound=base_unit | float)
_F = TypeVar("_F", bound=Callable[..., Any])

logging.basicConfig(encoding='utf-8', format='%(levelname)s:%(message)s')


def get_func_dependencies(func: Callable) -> set[str]:
    """Given a function, return a set containing the names of each argument."""
    argspec = inspect.getfullargspec(func)
    args = argspec[0]
    defaults = argspec[3]
    if defaults is not None and len(defaults) > 0:
        return set(args[0:0 - len(defaults or [])])
    return set(args)


class DependencySolver(Generic[_UT], metaclass=ABCMeta):
    """Abstract class describing the dependency solvers."""

    _N: int = 0
    _former_resolved_values: dict[str, base_unit | float | complex] = {}

    solutions: dict[str, dict[frozenset[str], Callable[..., _UT]]]

    def __init__(self):
        """Set up a new dependency solver and initialize the solutions map."""
        self.solutions = defaultdict(dict[frozenset[str], Callable[..., _UT]])
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.WARN)

    def register_solution(self, target: str, func: _F) -> _F:
        """
        Given a target symbol and a function, register the function as a solution to the symbol.

        This inspects the function arguments and uses them as dependencies for the solution.

        Args:
            target (str): Symbol for which the function will solve.
            func (_F): Function that solves for target based on the input arguments.

        Returns:
            _F: The original function passed-in.
        """
        deps = get_func_dependencies(func)
        self.solutions[target][frozenset(deps)] = func
        return func

    @abstractmethod
    def solve(self, target: str, **known_values):
        """Attempt to solve for the target based on the provided known values."""
        ...


class BFS_DependencySolver(DependencySolver[_UT]):
    """Solve dependency-based problems using a breadth-first-search."""

    def _init_queue(self, target, resolved_symbols) -> list[tuple[str, frozenset, Callable]]:
        queue: list[tuple[str, frozenset, Callable]] = []
        for deps, func in self.solutions[target].items():
            queue.append((target, frozenset(deps), func))
        return sorted(queue, key=lambda x: len(x[1] - resolved_symbols))

    def solve(self, target: str, **known_values):
        """Attempt to solve for the target based on the provided known values."""
        self._N = 0
        resolving = set([target])
        resolved_symbols: set[str] = set(known_values.keys())
        self.logger.debug("Solving for %s with %s", target, known_values)

        queue = self._init_queue(target, resolved_symbols)
        while len(queue) > 0:
            (symbol, alldeps, func) = queue.pop(0)
            if symbol in resolved_symbols:
                continue
            unmet = alldeps - resolved_symbols
            self.logger.debug("%s GETTING (%s)", symbol, (symbol, alldeps, func.__name__))

            if len(unmet) == 0:
                # Resolve it
                kw = dict([(d, known_values[d]) for d in alldeps])
                self.logger.debug("%s RESOLVING %s(%s)", symbol, func.__name__, kw)
                known_values[symbol] = func(**kw)
                resolved_symbols.add(symbol)
                resolving.remove(symbol)
                self.logger.debug("%s RESOLVED TO %s", symbol, known_values[symbol])
                if symbol == target:
                    self._former_resolved_values = known_values
                    return known_values[symbol]
                continue

            new_entries = []
            for unmet_symbol in (unmet - resolving):
                resolving.add(unmet_symbol)
                self._N += 1
                for dset, dfunc in self.solutions[unmet_symbol].items():
                    new_entries.append((unmet_symbol, frozenset(dset), dfunc))

            if len(new_entries) > 0:
                new_entries = sorted(new_entries, key=lambda x: len(x[1] - resolved_symbols))
                queue.extend(new_entries)
                if self.logger.getEffectiveLevel() >= logging.DEBUG:
                    for n in new_entries:
                        self.logger.debug("%s ADD-TO-QUEUE (%s)", symbol,
                                          (n[0], n[1], n[2].__name__))
                queue.append((symbol, alldeps, func))
                self.logger.debug("%s RE-ADD-TO-QUEUE (%s) ", symbol,
                                  (symbol, alldeps, func.__name__))


class DFS_DependencySolver(DependencySolver[_UT]):
    """A depth-first-search dependency solver."""

    def solve(self, target: str, **known_values):
        """Attempt to solve for the target based on the provided known values."""
        resolving = set([target])
        resolved_symbols: set[str] = set(known_values.keys())
        stack: list[tuple[str, frozenset[str], Callable]] = []

        stack.extend(
            sorted(((target, d, f) for d, f in self.solutions[target].items()),
                   key=lambda x: len(x[1] - resolved_symbols), reverse=True))

        self.logger.debug("%s STARTING STACK %s", target, stack)

        while len(stack) > 0:
            current_target, deps, func = stack.pop()
            if current_target in resolved_symbols:
                continue
            self.logger.debug("%s POP-FROM-STACK %s", current_target,
                              (current_target, deps, func.__name__))
            self._N += 1

            unmet = deps - resolved_symbols
            if len(unmet) == 0:
                kw = dict([(d, known_values[d]) for d in deps])
                known_values[current_target] = func(**kw)
                self.logger.debug("%s RESOLVING %s(%s)", current_target, func.__name__, kw)
                resolved_symbols.add(current_target)
                self.logger.debug("%s RESOLVED TO %s", current_target, known_values[current_target])
                if current_target == target:
                    self._former_resolved_values = known_values
                    return known_values[target]
                continue

            for unmet_target in unmet:
                if unmet_target in resolving:
                    continue
                resolving.add(unmet_target)

                new_entries = [(unmet_target, d, f)
                               for d, f in self.solutions[unmet_target].items()]
                new_entries = sorted(new_entries, key=lambda x: len(x[1]), reverse=True)
                stack.append((current_target, deps, func))
                self.logger.debug("%s PUSH-BACK-TO-STACK", current_target)
                stack.extend(new_entries)
                if self.logger.getEffectiveLevel() >= logging.DEBUG:
                    for n in new_entries:
                        self.logger.debug("%s PUSH-TO-STACK (%s)", current_target,
                                          (n[0], n[1], n[2].__name__))
