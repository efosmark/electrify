
import doctest
import electrify

modules = [
    # electrify.common,
    # electrify.circuit,
    # electrify.element,
    # electrify.value,
    # electrify.value.unit,
    # electrify.value.prefix,
    electrify.network,
    # electrify.quantity,
    # electrify.value.scanner,
    # electrify.value.scanner.lexer,
    # electrify.value.scanner.tokens
    # electrify.
    # electrify.circuit.circuit,
    # electrify.circuit.reducer,
    # electrify.circuit.solver,
    # electrify.derived.filter,
    # electrify.derived.crystal,
]

for m in modules:
    doctest.testmod(m)
