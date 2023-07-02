import doctest

import electrify


modules = [
    electrify.value,
    electrify.value.unit,
    electrify.value.prefix,
    electrify.value.scanner,
    electrify.value.scanner.lexer,
    electrify.value.scanner.tokens,
    electrify.network,
    # electrify.quantity,
    # electrify.
    # electrify.circuit.circuit,
    # electrify.circuit.reducer,
    # electrify.circuit.solver,
]

for m in modules:
    doctest.testmod(m)
