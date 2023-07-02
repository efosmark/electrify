from electrify.network.resistor import Resistor
from electrify.value.unit import *
from electrify.plot.drawcircuit import draw_circuit

r = Resistor(
    resistance=ohm(100),
    body_capacitance=farad(2.2e-12),
    interlead_capacitance=farad(1e-12),
    lead_inductance=henry(10e-6),
    internal_inductance=henry(123e-5)
)

sln = r.get_dag_solution(1, 1)

digraph = sln.to_nx_graph()
print('digraph', digraph)
test_f = hertz(1e6)
print('-' * 20)
print('test_f', test_f)
print('Z', r.impedance(test_f))
print('-' * 20)

draw_circuit(digraph)
