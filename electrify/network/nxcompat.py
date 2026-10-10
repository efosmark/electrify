from .network import Port, PortNetwork

try:
    
    import networkx as nx
    import random
    
    _rc = lambda: random.randrange(10, 90) / 100.0
    
    def to_nx(network:PortNetwork):
        nxgraph = nx.Graph()
        for net in network.nets():
            color = color = (_rc(), _rc(), _rc(), 0.3)
            nxgraph.add_node(net, color=color)
            for prop, side in net.edges:
                if not isinstance(prop, Port):
                    nxgraph.add_node(prop, identifier=network.id(prop))
                    nxgraph.add_edge(prop, net, label=side, color=color)
        return nxgraph

except ImportError:
    
    def to_nx_not_implemented(network:PortNetwork):
        raise NotImplementedError("Package networkx is not installed."
                                  "Converting to an nx graph is unavailable.")
    
    to_nx = to_nx_not_implemented

__ALL__ = ["to_nx"]
