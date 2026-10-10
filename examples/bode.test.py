# from typing import Optional
# from electrify.formula import attenuation_factor, magnitude, voltage_gain_db
# from electrify.network.filter import LowPassFilter
# from electrify.network.network import NegativePole, OnePortNetwork, Property
# from electrify.network.source import VoltageSource
# from electrify.plot import BodePlotManager, get_domain
# from electrify.plot.drawcircuit import draw_circuit
# from electrify.value.unit import ohm, hertz, volt
# import matplotlib.pyplot as plt

# import math, cmath

# f_min=1e6
# f_max=30e6
# f_target=10e6 
# f_graph=f_target
# z_load=50
# num_samples = 100

# d = get_domain(f_min, f_max, num_samples)


# class Load(OnePortNetwork):
#     load_impedance: Property[ohm]

#     def __init__(
#         self,
#         load_impedance: ohm,
#         com: Optional[NegativePole] = None
#     ):
#         OnePortNetwork.__init__(self)
#         if com is not None:
#             self[1].neg = com
#         self.load_impedance = Property(load_impedance, "load_impedance")

#         pos, neg = self[1]
#         self.add_series([neg, self.load_impedance, pos])


# class TestCircuit(OnePortNetwork):
    
#     def __init__(self):
#         OnePortNetwork.__init__(self)
        
#         self.source = VoltageSource(volt(1), ohm(0))
#         self.load = Load(ohm(50))
#         self.lpf = LowPassFilter(hertz(f_target), 5)
        
#         self.add_edges_from(self.source.edges())
#         self.add_edges_from(self.load.edges())
#         self.add_edges_from(self.lpf.edges())
        
#         self.add_edge(+self[1], -self.source[1])
#         self.add_edge(-self[1], -self.load[1])
#         self.add_edge(-self[1], -self.lpf[1])
#         self.add_edge(-self[1], -self.lpf[2])
        
#         self.add_edge(+self.lpf[2], +self.load[1])
#         self.add_edge(+self.source[1], +self.lpf[1])

#     def attenuation_factor(self):
#         result = []
#         for f in get_domain(f_min, f_max, num_samples):
#             ...
#             #V1 = sln.voltage(f, self.source.port(1).pos)
#             #V2 = sln.voltage(f, self.load.port(1).pos)
#             #Z1 = sln.impedance(f, self.source.series_resistance)
#             #Z2 = sln.impedance(f, self.load.load_impedance)
#             #g = voltage_gain_db(V1, V2, Z1, Z2)
#             #result.append(g)
#             #result.append(10.0 * (cmath.log10((V2/V1)**2.0)))# - cmath.log10(V1**2.0)))
#         return result

# test = TestCircuit()
# test.get_dag_solution(1, 1)
# sln = test.solutions[test[1], test[1]]
# digraph = sln.to_nx_graph(hertz(f_graph))
# draw_circuit(digraph, layered=False)

# y_data = test.attenuation_factor()
# print(y_data)

# fig, ax = plt.subplots()
# bpm = BodePlotManager(ax)
# bpm.configure(
#     d,
#     hlines=[-3],
#     vlines=[f_target, f_target*2.0],
#     f_min=f_min,
#     f_max=f_max
# )
# bpm.plot_fq(y_data)
# plt.show()
