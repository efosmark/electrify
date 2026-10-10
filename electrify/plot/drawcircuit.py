from typing import *
import networkx as nx
import matplotlib.pyplot as plt

from electrify.network.network import Net, Port
from electrify.component import C, L, R, V
from electrify.ac import impedance
from electrify.types import *

MPLColor = Tuple[float,float,float] | Tuple[float,float,float,float] | str
EdgeLabels = Dict[Tuple[Any, Any], str]
NodeLabels = Dict[Any, str]

class BBox(TypedDict):
    boxstyle: str
    fc: NotRequired[MPLColor]
    ec: NotRequired[MPLColor]
    alpha: NotRequired[float]
    pad: NotRequired[float]
    rounding_size: NotRequired[float]
    mutation_aspect: NotRequired[float]
    mutation_scale: NotRequired[float]

class Font(TypedDict):
    font_color: NotRequired[MPLColor]
    font_size: NotRequired[float]
    font_family: NotRequired[str]
    font_weight: NotRequired[str]

# def shift_position(pos, shift_x=0, shift_y=0, keys=None):
#     res = dict()
#     for k,(x,y) in pos.items():
#         if keys is None or k in keys:
#             x = x + shift_x
#             y = y + shift_y
#             res[k] = [x, y]
#     return res

NODE_COLORS = {
    V: "#ADD77A",
    R: "#D78D7A",
    C: "#7AD797",
    L: "#977AD7",
    Any: "gray"
}

def node_color(node, d=None):
    if d is not None and "color" in d:
        return [((1.0 - c) * 0.7) + c for c in d["color"][0:3]]
    return NODE_COLORS.get(type(node), NODE_COLORS[Any])

def node_label(n, d):
    if isinstance(n, Net):
        return (n, '')
    label = []
    if "identifier" in d:
        label.append(f'{d["identifier"]} {str(n)}')
    else:
        label.append(str(n))
    props = {
        "z_self":  ("Z_self", ohm),
        "z_load":  ("Z_load", ohm),
        "v_in":    (" V IN", volt),
        "v_out":   ("V OUT", volt),
        "v_drop":  ("V DRP", volt),
        #"i": ("I", ampere),
        "power": ("P", watt),
    }
    for k, (lbl, typ) in props.items():
        if k in d and d[k] is not None:
            v = str(d[k])
            label.append(f"{lbl: >6}  =  {v}")
    return (n, "\n".join(label))

def node_size(c, d=None):
    if isinstance(c, (Net, Port)):
        return 100
    return 600

def node_edge_color(c, d=None) -> MPLColor:
    return (0,0,0,0)

def node_edge_width(n, d):
    return 1

def edge_label(n1, n2, d):
    if isinstance(n1, Port) or isinstance(n2, Port):
        return (n1, n2), ""
    #if d.get('label'):
    #    return (n1, n2), d.get("label").name
    label = []
    z = d.get('z')
    if z:
        label.append('{}'.format(ohm(z)))
    v = d.get('v')
    if v:
        label.append('{}'.format(volt(v)))
    i = d.get('i')
    if i:
        label.append('{}'.format(ampere(i)))
    return (n1, n2), '\n'.join(label)

def edge_color(n1, n2, d) -> MPLColor:
    if "color" in d:
        return d["color"]
    return (0, 0, 0, 0.3)

def edge_width(n1, n2, d) -> float:
    if isinstance(n1, Port) or isinstance(n2, Port):
        return 1
    return 2

def edge_list(c: nx.Graph) -> Sequence[tuple]:
    edgelist = []
    for n1, n2, d in c.edges(data=True):
        if isinstance(n1, Net):
            edgelist.append((n1, n2, d))
        else:
            edgelist.append((n2, n1, d))
    return edgelist

def draw_circuit(c: nx.Graph, size=(10, 10), sln=None, f=None, pos=None):
    fig, ax = plt.subplots()
    fig.set_size_inches(*size)
    fig.tight_layout()
    plt.axis('off')
    ax.margins(0.1, 0.02)
    
    if sln is not None and f is not None:
        for n in c.nodes:
            c.nodes[n]["z_load"] = sln.load_impedance(n, f, include_self=False)
            c.nodes[n]["z_self"] = impedance(n, f)
            #c.nodes[n]["i"] = sln.electric_current(n, f)
            c.nodes[n]["v_in"] = sln.volts_in(n, f)
            c.nodes[n]["v_out"] = sln.volts_out(n, f)
            #c.nodes[n]["v_drop"] = sln.volts_drop(n, f)
            #c.nodes[n]["power"] = sln.power(n, f)
    
    if pos is None and sln is not None:
        for n in c.nodes:
            try:
                c.nodes[n]['subset'] = max(len(p) for p in sln.paths_to_end[n])
            except ValueError:
                c.nodes[n]['subset'] = 0
        pos = nx.multipartite_layout(c, align="horizontal")
    else:
        pos = nx.spring_layout(c)

    nodelist = sorted(
        [(n, d) for n,d in c.nodes(data=True)],
        key=lambda k: 0 if isinstance(k[0], Net) else 1
    )
    


    default_params = dict(
        G=c,
        pos=pos,
        ax=ax
    )
    
    nx.draw_networkx_nodes(
        **default_params, # type: ignore
        nodelist=[n for n,d in nodelist],
        node_shape='o',
        node_size=[node_size(n,d) for n,d in nodelist], # type: ignore
        node_color=[node_color(n,d) for n,d in nodelist], # type: ignore
        linewidths=[node_edge_width(n,d) for n,d in nodelist],
        edgecolors=[node_edge_color(n1, d) for n1, d in nodelist],
    )

    nx.draw_networkx_labels(
        **default_params, # type: ignore
        font_size=6,
        font_family="monospace",
        horizontalalignment="left",
        labels=dict([
            node_label(n1, d)
            for n1, d in nodelist
        ]),
        
        bbox=BBox(
           boxstyle='round',
            fc="#EEEEEE",
            mutation_aspect=0.5,
            pad=0.5,
            ec="#EEEEEE",
           alpha=0.8
        )
    )
    
    edgelist = edge_list(c)
    
    nx.draw_networkx_edges(
        **default_params, # type: ignore
        edgelist=edgelist,
        width=[edge_width(n1, n2, d) for n1, n2, d in edgelist], # type: ignore
        edge_color=[edge_color(n1, n2, d) for n1, n2, d in edgelist], # type: ignore
        arrows=True,
        arrowstyle="-",
        node_size=100,
        #min_source_margin=35,
        #min_target_margin=35,
    )

    nx.draw_networkx_edge_labels(
        **default_params, # type: ignore
        edge_labels=dict([
            edge_label(n1, n2, d)
            for n1, n2, d in edgelist
        ]),
        font_size=6,
        font_family="monospace",
        font_color="black",
        #font_weight="bold",
        #bbox=BBox(
            #boxstyle='square',
            #fc=(1, 1, 1, 1),
            #ec=(1, 1, 1, 1),
            #pad=0.7,
            #mutation_aspect=0.3,
            #mutation_scale=10
        #),
        horizontalalignment="center",
        verticalalignment="center",
        label_pos=0.3,
        #rotate=False
    )
    
    plt.show()
    return (fig, ax)
