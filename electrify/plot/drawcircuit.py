import math
from typing import Any
import networkx as nx
import matplotlib.pyplot as plt

from electrify.network.property import NegativePole, Pole, PositivePole, Property
from electrify.value import watt
from electrify.value.unit import farad, henry, ohm, ampere, volt, hertz

def shift_position(pos, shift_x=0, shift_y=0, keys=None):
    res = dict()
    for k,(x,y) in pos.items():
        if keys is None or k in keys:
            x = x + shift_x
            y = y + shift_y
            res[k] = [x, y]
    return res

def choose_color(c, d=None):
    if isinstance(c, Property):
        if type(c.value) is volt:
            return "#9cc669"
        if type(c.value) is hertz:
            return "yellow"
        if type(c.value) is ohm:
            return "#c67c69"
        if type(c.value) is farad:
            return "#69c686"
        if type(c.value) is henry:
            return "#8669c6"
    if isinstance(c, Pole):
        return "#FFFFFF"
    return "gray"

def choose_node_edge_color(c, d=None):
    if isinstance(c, NegativePole):
        return '#b03e49'
    if isinstance(c, PositivePole):
        return '#4b8346'
    return 'black'

def choose_edge_color(n1, n2, d):
    if isinstance(n1, NegativePole) and isinstance(n2, NegativePole):
        return '#FFFFFF'
    if isinstance(n2, NegativePole):
        return '#DDDDDD'
    return 'black'

def choose_edge_width(n1, n2, d):
    if isinstance(n2, NegativePole):
        return 1
    return 5

def choose_node_size(c, d=None):
    return 3000

def get_edge_label(n1, n2, d):
    if isinstance(n2, NegativePole):
        return (n1, n2), ""
    z = d.get('z')
    v = d.get('v')
    i = d.get('i')
    label = []
    if z:
        label.append('{}'.format(ohm(z)))
    if v:
        label.append('{}'.format(volt(v)))
    if i:
        label.append('{}'.format(ampere(i)))
    return (n1, n2), '\n'.join(label)

def get_node_label(n, d):
    label = []
    if isinstance(n, Pole):
        label.append(n.port.network.__class__.__name__)
        label.append(f'{n.symbol}')
        label = f'{n.port.network.__class__.__name__}[{n.symbol}{n.port.id}]'
    else:
        label.append(n.name)
        label.append(n.value)
        label = str(n)
    
    label += "\n"
    label += "—" * (len(label) - 1)
    
    zs = d.get('zs')
    if zs:
        label += '\nZ_self = {}'.format(ohm(zs))
    
    z = d.get('z')
    if z:
        label += '\nZ_load = {}'.format(ohm(z))
    
    V_in = d.get('v_in')
    if V_in:
       label += '\nV_in   = {}'.format(volt(d.get('v_in')))
    
    V_out = d.get('v_out')
    if V_out:
       label += '\nV_out  = {}'.format(volt(d.get('v_out')))
    
    V_drop = d.get('v_drop')
    if V_drop:
       label += '\nV_drop  = {}'.format(volt(d.get('v_drop')))
    
    i = d.get('i')
    if i:
        label += '\nI  = {}'.format(ampere(d.get('i')))
    
    P = d.get('p')
    if P:
       label += '\nP   = {}'.format(watt(d.get('p')))
    return (n, label)

def choose_node_linewidth(n, d):
    if isinstance(n, Pole):
        return 3
    return 1

def draw_circuit(c: nx.Graph, size=(10, 15), layered=False, pos=None):
    fig, ax = plt.subplots()
    fig.set_size_inches(*size)
    fig.tight_layout()
    plt.axis('off')
    ax.margins(0.1, 0.02)
    
    if pos is None:
        if layered:
            pos = nx.multipartite_layout( # type: ignore
                c,
                align="horizontal"
            )
        else:
            pos = nx.spring_layout(c)

    nodelist = [(n, d) for n,d in c.nodes(data=True)]
    valid_nodes = [n for n,d in nodelist]
    edgelist = [(n1, n2, d) for n1, n2, d in c.edges(data=True) if n2 in valid_nodes]

    default_params = dict(
        G=c,
        #pos=pos,
        font_size=8,
        font_family="monospace",
        ax=ax
    )
    
    shared_node_params:dict[str,Any] = dict(
        **default_params,
        node_size=[choose_node_size(n,d) for n,d in nodelist], # type: ignore
        node_shape='o',
        nodelist=valid_nodes,
    )
    
    nx.draw_networkx(
        **shared_node_params,
        pos=pos,
        with_labels=False,
        node_color=[choose_color(n,d) for n,d in nodelist], # type: ignore
        linewidths=[choose_node_linewidth(n,d) for n,d in nodelist], #type: ignore
        edgecolors=[choose_node_edge_color(n1, d) for n1, d in nodelist],
        
        edgelist=edgelist,
        width=[choose_edge_width(n1, n2, d) for n1, n2, d in edgelist],
        edge_color=[choose_edge_color(n1, n2, d) for n1, n2, d in edgelist],
        #style=":",
    )

    nx.draw_networkx_labels(
        **default_params,
        pos=shift_position(pos, shift_x=-0.035),
        horizontalalignment="left",
        labels=dict([
            get_node_label(n1, d)
            for n1, d in nodelist
        ]),
        bbox=dict(
            boxstyle='round',
            fc="#EEEEEE",
            mutation_aspect=0.5,
            pad=1,
            ec="#EEEEEE",      
            alpha=0.7
        )
    )

    nx.draw_networkx_edge_labels(
        **default_params,
        pos=pos,
        edge_labels=dict([
            get_edge_label(n1, n2, d)
            for n1, n2, d in c.edges(data=True)
        ]),
        bbox=dict(
            boxstyle='round',
            fc="#FFFFFF",
            mutation_aspect=0.5,
            pad=1,
            ec="#DDDDDD",      
            alpha=0.7
        ),
        #horizontalalignment="left",
        #verticalalignment="bottom",
        #label_pos=0.7,
        rotate=False
    )
    plt.show()
    return (fig, ax)
