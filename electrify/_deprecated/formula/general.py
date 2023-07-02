from electrify.value.unit import *
from electrify.quantity.reactance import get_capacitive_reactance, get_inductive_reactance


def current_divider(current: ampere, Z_branch: ohm, Z_total: ohm) -> ampere:
    """
    Given a current at a branch, determine how much of it will go to a branch.

    Args:
        current (ampere): _description_
        Z_branch (ohm): _description_
        Z_total (ohm): _description_

    Returns:
        ampere: _description_
    """
    if Z_branch == 0:
        return current
    return ampere(complex(current) * (Z_total.magnitude / Z_branch.magnitude))


def get_item_impedance(item, frequency: hertz) -> ohm:
    if isinstance(item, ohm):
        return item
    elif isinstance(item, farad):
        return get_capacitive_reactance(frequency, item, imag=True)
    elif isinstance(item, henry):
        return get_inductive_reactance(frequency, item, imag=True)
    return ohm(0 + 0j)
