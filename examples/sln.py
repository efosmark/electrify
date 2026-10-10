# #%load_ext autoreload
# #%autoreload 2

# from calendar import c
# from typing import *
# import logging
# import matplotlib.pyplot as plt # mypy:ignore

# from electrify.formula import transducer_gain_db, voltage_gain_db
# from electrify.value import from_string
# from electrify.value.unit import *

# from electrify.network.filter import LowPassFilter
# from electrify.network.net import Net, Side
# from electrify.network.network import Series, OnePortNetwork, TwoPortNetwork, logger
# from electrify.network.property import Capacitance, Inductance, Resistance
# from electrify.network.component import VoltageSource
# from electrify.network.solve import Solution
# from electrify.network.nxcompat import to_nx

# from electrify.plot import get_domain
# from electrify.plot.bode import BodePlotManager
# from electrify.plot.drawcircuit import draw_circuit

# logger.setLevel(logging.WARN)

# class TwoPortTestFixture(OnePortNetwork):
#     """
#     A simple test fixture for two-port networks.
    
#     ```
#                    V1                    V2
#                    │     ╭─────────╮     │
#     ╭──╮   ╭────╮  │  ╭──┤         ├──╮  │  ╭────╮
#     │+1╞═══╡ RS ╞══╧══╡+1│   2PN   │+2╞══╧══╡ RL ╞╗
#     │  │   ╰────╯   ╔═╡-1│   DUT   │-2╞═╗   ╰────╯║
#     │  │            ║ ╰──┤         ├──╯ ║         ║
#     │  │            ║    ╰─────────╯    ║         ║
#     │-1╞════════════╩═══════════════════╩═════════╝
#     ╰──╯

#     ```
#     """
    
#     test_network:TwoPortNetwork
#     RS:Resistance
#     RL:Resistance
#     solution:Solution
    
#     def __init__(self, network:TwoPortNetwork, z_src:number[ohm], z_load:number[ohm]):
#         super().__init__()
#         self.test_network = network
#         self.RS = Resistance(ohm(z_src))
#         self.RL = Resistance(ohm(z_load))
#         self.V1 = VoltageSource(volt(1.0))
        
#         self.import_netlist(network)
#         self.series(
#             self.port(1).pos,
#             self.V1.voltage,
#             self.RS,
#             network.port(1).pos
#         )
        
#         self.series(
#             network.port(2).pos,
#             self.RL,
#             self.port(1).neg
#         )
        
#         self.connect(network.port(1).neg, network.port(2).neg)
    
#         self.port(1).pos.label = "POS"
#         self.port(1).neg.label = "NEG"
#         #self.solution = Solution(self.test_network, self.signal_in, self.signal_out)
    
#     @property
#     def signal_in(self) -> Net:
#         return self.test_network.get_net(self.RS, Side.B)
    
#     @property
#     def signal_out(self) -> Net:
#         return self.test_network.get_net(self.RL, Side.A)

#     # def transducer_gain_db(self, f: number[hertz]) -> float:
#     #     v_src = sln.volts_in(RS, hertz(f)) or volt(0)
#     #     v_load = sln.volts_in(RL, hertz(f)) or volt(0)
#     #     z_load = RL.value
#     #     z_src = RS.value
#     #     return transducer_gain_db(v_src, z_src, v_load, z_load)

# test = LowPassFilter(hertz(15e6), 5)

# draw_circuit(to_nx(test))
# filter = TwoPortTestFixture(test, ohm(50), ohm(50))

# draw_circuit(to_nx(test))
# draw_circuit(to_nx(filter))

# def verifier():
#     f_min=1e6
#     f_max=30e6
#     f_target=15e6 
#     num_samples = 30

#     d = get_domain(f_min, f_max, num_samples)

#     RS = Resistance(ohm(50))
#     RL = Resistance(ohm(50))

#     L1 = Inductance(henry(from_string('858.4nH')))
#     L2 = Inductance(henry(from_string('858.4nH')))

#     C1 = Capacitance(farad(from_string("131.2pF")))
#     C2 = Capacitance(farad(from_string('424.4pF')))
#     C3 = Capacitance(farad(from_string("131.2pF")))

#     V1 = VoltageSource(volt(10.0))

#     lpf = Series(
#         V1.voltage,
#         RS,
#         L1,
#         L2,
#         RL,
#         V1.gnd
#     )

#     lpf.connect(RS, C1)
#     lpf.connect(C1, V1.gnd)

#     lpf.connect(L1, C2)
#     lpf.connect(C2, V1.gnd)

#     lpf.connect(L2, C3)
#     lpf.connect(C3, V1.gnd)

#     src_ref = lpf[lpf._ports[1], Side.A]
#     zero_ref = lpf[lpf._ports[1], Side.B]
#     sln = Solution(lpf, src_ref, zero_ref)

#     fig, ax = plt.subplots()
#     bpm = BodePlotManager(ax)
#     bpm.configure(
#         d,
#         hlines=[-3],
#         vlines=[f_target, f_target*2.0],
#         f_min=f_min,
#         f_max=f_max
#     )

#     def tdg(sln:Solution, f):
#         v_src = sln.volts_in(RS, f) or volt(0)
#         v_load = sln.volts_in(RL, f) or volt(0)
#         z_load = RL.value
#         z_src = RS.value
#         return transducer_gain_db(v_src, z_src, v_load, z_load)

#     bpm.plot_fq(
#         [ tdg(sln, f) for f in d ],
#         width=1,
#         alpha=0.5
#     )

#     plt.show()
#     #draw_circuit(to_nx(lpf))

# verifier()
from electrify.types import *

a = ohm(k=100)|ohm(100)|ohm(100)
print(a)

b = farad(u=100) | farad(u=100) | farad(u=100)
print(b)

c = farad(u=100) & farad(u=100) & farad(u=100)
print(c)

d = sum([ohm(k=100), ohm(100), ohm(100)])
print(d)

d = ohm(100) + ohm(100) + ohm(100)
print(d)

e = ohm(100) & ohm(100) & ohm(100)
print(e)

#
