import networkx as nx
import matplotlib.pyplot as plt
from ..value import format_value
from ..component import Inductor, Capacitor, Resistor, SignalSource, Node, Terminal, ReactiveComponent, Source, Load
from ..math.rf import magnitude


def apply_directional_layer(G, source):
    leaves = [v for v, d in G.out_degree() if d == 0]

    for leaf in leaves:
        longest = None
        for x in nx.all_simple_paths(G, source, leaf):
            if longest is None or len(x) > len(longest):
                longest = x

        if longest is not None:
            for n in longest:
                if "layer" not in G.nodes[n]:
                    G.nodes[n]["layer"] = 0
                current_layer = G.nodes[n]["layer"]
                for s in G.successors(n):
                    if "layer" in G.nodes[s]:
                        continue
                    G.nodes[s]["layer"] = current_layer - 1

    for n in G.nodes():
        if "layer" not in G.nodes[n]:
            try:
                parent_layer = G.nodes[list(G.predecessors(n))[0]]["layer"]
            except Exception as e:
                G.nodes[n]["layer"] = 0
            else:
                G.nodes[n]["layer"] = parent_layer - 1


def apply_layer(G, source=None, layer=0):
    if source is None:
        source = G.source_node
    G.nodes[source]["layer"] = layer
    for n in G.neighbors(source):
        if "layer" in G.nodes[n] and G.nodes[n]["layer"] >= layer:
            continue
        apply_layer(G, n, layer - 1)
    if layer == 0:
        for n in G.nodes():
            if 'layer' not in G.nodes[n]:
                G.nodes[n]["layer"] = 0


def choose_color(c):
    if isinstance(c, Terminal):
        return "white"
    if isinstance(c, Node):
        return "lightgray"
    if type(c) is Inductor:
        return "lightblue"
    if type(c) is Capacitor:
        return "lightgreen"
    if type(c) is Resistor:
        return "pink"
    if type(c) is SignalSource:
        return "lightblue"
    return "gray"


def get_node_label(n, d, annotate=True):
    label = str(n)
    if not annotate:
        return n, label

    label += '\n'

    if "res_self" in d and not isinstance(n, (Node)):
        label += "\nresistance = {} / {}".format(format_value(d.get("res_self", 0), places=0),
                                                 format_value(d.get("res_total", 0), places=0))

    if "res_total" in d and isinstance(n, (Node)):
        label += "\nR={}".format(format_value(d.get("res_total", 0), places=0))

    if "equation" in d:
        equation = d.get("equation", '--')
        label += "\n{}".format(equation)

    if "depth" in d:
        depth = d.get("depth", '--')
        label += "\n{}".format(depth)

    if "gain" in d:
        g = d.get("gain", 0)
        label += "\nG = {}".format(format_value(g), places=0)

    if "v_drop" in d and not isinstance(n, Node):
        label += "\nvoltage = {}V / {}V".format(format_value(d['v_drop'],
                                                             places=0),
                                                format_value(d['voltage'],
                                                             places=0))
    elif 'voltage' in d:
        label += "\n{}V".format(format_value(d['voltage'], places=0))

    if "current" in d and not isinstance(n, Node):
        current = d.get("current", 0)
        label += "\ncurrent = {}A".format(format_value(current, places=0))

    if "pwr_dis" in d and not isinstance(n, Node):
        label += "\npower = {}W / {}W".format(
            format_value(d.get("pwr_dis", 0), places=0),
            format_value(d.get("pwr_tot", 0), places=0)
        )

    return n, label


def get_edge_label(n1, n2, d, annotate=True):
    label = ""
    if not annotate:
        return (n1, n2), label

    if "voltage" in d:
        label += "{}V".format(format_value(format_value(d['voltage'])))

    if "current" in d and d["current"] > 0:
        current = d["current"]
        label += " {}A".format(format_value(format_value(current)))

    return (n1, n2), label


def draw_circuit(c, annotate_edges=False, annotate_nodes=False, size=(20, 20)):
    fig, ax = plt.subplots()
    fig.set_size_inches(*size)
    plt.axis('off')
    # apply_layer(c)

    pos = nx.multipartite_layout(
        c,
        subset_key="layer",
        align="horizontal",
    )

    nx.draw(
        c,
        pos=pos,
        ax=ax,
        node_color=[choose_color(n) for n in c.nodes],
        node_size=1200,
        width=0.3,
        with_labels=False
    )

    impedance_labels = dict([get_node_label(n1, d, annotate_nodes)
                            for n1, d in c.nodes(data=True)])
    nx.draw_networkx_labels(
        c,
        pos,
        ax=ax,
        labels=impedance_labels,
        # verticalalignment="center",
        # horizontalalignment="left",
        font_size=12,
        font_family="monospace",
        bbox=dict(boxstyle='round,pad=0.4', fc="white", ec="blue", alpha=0.75)
    )

    edge_labels = dict([get_edge_label(n1, n2, d, annotate_edges) for n1, n2, d in c.edges(data=True)])

    nx.draw_networkx_edge_labels(
        c,
        pos,
        ax=ax,
        edge_labels=edge_labels,
        font_size=12,
        font_family="monospace",
        bbox=dict(boxstyle='round,pad=0.4', fc="white", ec="blue")
    )

    plt.show()
    return (fig, ax)
