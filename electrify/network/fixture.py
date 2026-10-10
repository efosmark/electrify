from typing import *
from electrify.network.net import Side
from electrify.types import *
from electrify.network.network import OnePortNetwork, TwoPortNetwork
from electrify.component import  R
from electrify.network.solve import Solution
from electrify.ac import insertion_loss, magnitude, transducer_gain


class TwoPortTestFixture(OnePortNetwork):
    """
    A test fixture for two-port networks.
    
    
    ```
                                    ╭─────────╮     
               ╭─╮   ╭───────╮   ╭──┤         ├──╮
         V1 ═══╡+╞═══╡ Z_src ╞═══╡+1│   2PN   │+2╞═════════╦══════ V2
             ╭─┴─┴─╮ ╰───────╯ ╔═╡-1│   DUT   │-2╞═╗  ╭────╨───╮
             │ P-1 │           ║ ╰──┤         ├──╯ ║  │ Z_load │
             ╰─┬─┬─╯           ║    ╰─────────╯    ║  ╰────╥───╯
        GND ═══╡-╞═════════════╩═══════════════════╩═══════╝
               ╰─╯
    ```
    """
    
    test_network:TwoPortNetwork
    RS:R
    RL:R
    solution:Solution
    
    def __init__(self, network:TwoPortNetwork, z_src:ohm, z_load:ohm):
        super().__init__()
        self.test_network = network
        self.RS = R(z_src)
        self.RL = R(z_load)
        
        self.import_netlist(network)
        self.series(
            self.ports[1].pos,
            self.RS,
            network.ports[1].pos
        )
        
        self.series(
            network.ports[2].pos,
            self.RL,
            self.ports[1].neg
        )
        
        self.connect(self.ports[1].neg, network.ports[1].neg)
        self.connect(network.ports[1].neg, network.ports[2].neg)
        
        pos = self.ports[1].pos
        neg = self.ports[1].neg
        self.solution = Solution(
            self,
            self.get_net(pos.item, pos.pin),
            #self.get_net(self.RS, Side.B),
            self.get_net(neg.item, neg.pin)
        )

    def transducer_gain(self, f: hertz) -> complex:
        v_src = self.solution.volts_in(self.RS, hertz(f))
        v_load = self.solution.volts_in(self.RL, hertz(f))
        z_load = self.RL
        z_src = self.RS
        return transducer_gain(v_src, z_src, v_load, z_load)
    
    def insertion_loss(self, f: hertz)  -> complex:
        R_src = (self.solution.load_impedance(self.RS, hertz(f)) or ohm(0.0))
        R_load = ohm((self.solution.load_impedance(self.RL, hertz(f)) or ohm(0.0)) - R_src)
        v_src = self.solution.volts_in(self.RS, hertz(f))
        v_load = self.solution.volts_in(self.RL, hertz(f))
        return insertion_loss(v_src, R_src, R_load)
    
    def voltage_gain(self, f: hertz) -> complex:
        v_src = magnitude(self.solution.volts_drop(self.RS, hertz(f)))
        v_load = magnitude(self.solution.volts_drop(self.RL, hertz(f)))
        return v_load / v_src
    
    # def power_gain(self, f: hertz) -> complex:
    #     p_src = self.solution.power(self.RS, hertz(f))
    #     p_load = self.solution.power(self.RL, hertz(f))
    #     return p_src/p_load

    def attenuation_factor(self, f):
        R_src = self.solution.load_impedance(self.RS, f, include_self=False)
        R_load = self.solution.load_impedance(self.RL, f)
        if R_load == ohm(0.0):
            return -1
        return (R_src / R_load)
