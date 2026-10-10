# from electrify.network.resistor import Resistor
# from electrify.value.unit import *

# if __name__ == "__main__":
#     r = Resistor(
#         resistance=ohm(100),
#         body_capacitance=farad(2.2e-12),
#         interlead_capacitance=farad(1e-12),
#         lead_inductance=henry(10e-6),
#         internal_inductance=henry(123e-5)
#     )

#     test_f = hertz(1e6)

#     print('-' * 20)
#     print('test_f', test_f)
#     print('Z', r.impedance(test_f))
#     print('-' * 20)
