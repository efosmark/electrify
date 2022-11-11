from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib
import networkx as nx
from electrify.value import format_value
import electrify as e
from electrify.component import Inductor, Capacitor, Resistor, SignalSource, Node, Terminal, Gnd
import matplotlib.pyplot as plt
matplotlib.use('Qt5Agg')


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
    if not isinstance(n, (Gnd, Node)):
        label += '\n'

    parts = []
    if not isinstance(n, Gnd):
        parts.append(' V    = {: <15}'.format(format_value(d.get('voltage'))))
    if not isinstance(n, (Gnd, Node)):
        parts.append(' V_d  = {: <15}'.format(format_value(d.get('volt_drop'))))
    if not isinstance(n, Gnd):
        parts.append(' I    = {: <15}'.format(format_value(d.get('current'))))
    if not isinstance(n, (Gnd, Node)):
        parts.append(' R_s  = {: <15}'.format(format_value(d.get('res_self'))))
        parts.append(' R_t  = {: <15}'.format(format_value(d.get('res_total'))))

    return n, label + '\n'.join(parts)


def get_edge_label(n1, n2, d):
    label = ""

    if "voltage" in d:
        label += "{}V".format(format_value(e.magnitude(d['voltage'])))

    if "current" in d:
        label += " {}A".format(format_value(e.magnitude(d["current"])))

    return (n1, n2), label


def draw_circuit(ax, c):
    pos = nx.multipartite_layout(
        c,
        subset_key="layer",
        align="horizontal",
    )

    nx.draw_networkx_labels(
        c,
        pos,
        ax=ax,
        labels=dict([get_node_label(n1, d) for n1, d in c.nodes(data=True)]),
        font_size=7,
        font_family="monospace",
        bbox=dict(boxstyle='round,pad=0.4', fc="white", ec="blue", alpha=0.75)
    )

    nx.draw_networkx_nodes(c, pos=pos, ax=ax, node_size=800, node_color=[choose_color(n) for n in c.nodes], alpha=1)

    currents = [c.get_edge_data(u, v).get('current', 0).real for u, v in c.edges()]
    edgewidth = [1 + ((c/float(max(currents)))*20.0) for c in currents]

    # voltages = [e.magnitude(c.get_edge_data(u, v).get('voltage', 0)) for u, v in c.edges()]
    # edgewidth = [1 + ((v/float(max(voltages)))*30.0) for v in voltages]

    nx.draw_networkx_edges(
        c,
        pos=pos,
        ax=ax,
        alpha=0.5,
        width=edgewidth,
        #edge_color=list(range(0, int(max(voltages)))),
        # edge_cmap=plt.cm.plasma
    )

    # edge_labels = dict([get_edge_label(n1, n2, d) for n1, n2, d in c.edges(data=True)])
    # nx.draw_networkx_edge_labels(
    #     c,
    #     pos,
    #     ax=ax,
    #     edge_labels=edge_labels,
    #     font_size=7,
    #     font_family="monospace",
    #     bbox=dict(boxstyle='round,pad=0.3', fc="white", ec="blue", alpha=0.6)
    # )


class CircuitPlot(FigureCanvas):

    def __init__(self, parent=None):
        self.figure = Figure()
        FigureCanvas.__init__(self, self.figure)
        self.setParent(parent)
        self.setContentsMargins(0, 0, 0, 0)
        self.ax = self.figure.add_subplot(111)

    def configure(self, width=20, height=20):
        if width and height:
            self.figure.set_size_inches(width / 100.0, height / 100.0)
        self.figure.set_tight_layout(dict(pad=0))

    def draw_circuit(self, c, annotate_edges=False, annotate_nodes=True):
        draw_circuit(self.ax, c)
