from typing import Optional
from electrify.network.property import Resistance
from electrify.network.solution import Z_Solution
from electrify.network.filter import LowPassFilter
from electrify.network.network import NegativePole, OnePortNetwork, Property, TwoPortNetwork
from electrify.network.source import VoltageSource
from electrify.plot.drawcircuit import draw_circuit
from electrify.value.unit import ohm, hertz, volt

f_min=1e6
f_max=30e6
f_target=10e6 
f_graph=f_target
z_load=50
num_samples = 100

class Load(OnePortNetwork):

    load_impedance: Property[ohm]

    def __init__(
        self,
        load_impedance: ohm,
        com: Optional[NegativePole] = None
    ):
        OnePortNetwork.__init__(self)
        if com is not None:
            self[1].neg = com
        self.load_impedance = Property(load_impedance, "load_impedance")

        pos, neg = self[1]
        self.add_series([neg, self.load_impedance, pos])


class DrivenTwoPortNetwork(OnePortNetwork):
    
    def __init__(self, network:TwoPortNetwork):
        OnePortNetwork.__init__(self)
        self.source = VoltageSource(volt(10), ohm(50))
        self.load = Load(ohm(50))
        
        self.add_edges_from(self.source.edges())
        self.add_edges_from(self.load.edges())
        self.add_edges_from(network.edges())
        
        self.add_edge(self.source[1].pos, self[1].pos)
        self.add_edge(self.source[1].neg, self[1].neg)
        
        self.add_edge(network[1].pos, self[1].pos)
        self.add_edge(network[1].neg, self[1].neg)
        
        self.add_edge(network[2].pos, self.load[1].pos)
        self.add_edge(network[2].neg, self[1].neg)
        self.add_edge(network[2].neg, self.load[1].neg)
        
        self.add_edge(self.load[1].neg, self[1].neg)
                
        self.nodes[self[1].pos]["layer"] = 1000
        self.nodes[self[1].neg]["layer"] = -1000


lpf = LowPassFilter(hertz(f_target), 5)
lpf.add_series([lpf[2].pos, Resistance(ohm(50)), lpf[2].neg])

#test = DrivenTwoPortNetwork(lpf)
sln =  Z_Solution(lpf, lpf.ports[1], lpf.ports[2])
digraph = sln.to_nx_graph(hertz(f_graph))
#draw_circuit(digraph, layered=True)
draw_circuit(digraph, layered=True)
