
from electrify.formula import attenuation_factor, voltage_divider
from electrify.quantity.reactance import get_capacitive_reactance, get_inductive_reactance
from electrify.value import from_string, hertz, farad, henry, volt
from electrify.value.sum import sum_parallel_resistance, sum_series_resistance
from electrify.value.prefix import pico, nano
from electrify.plot import BodePlotManager, get_domain
import matplotlib.pyplot as plt

import math, cmath

f_min=1e6
f_max=30e6
f_samples=1000
f_target=15e6 
z_load=50

def circuit(f):
    '''
            V1      V2      V3
   VG---R---.---L---.---L---.----RL
    |       |       |       |    |
    |       C       C       C    |
    |       |       |       |    |
    G-------G-------G-------G----G
    
      (VG)
       |
      [R1]
       |
       +---(V1)
       |    |
      [C1] [L1]
       |    |
      -G-   +---(V2)
            |    |
           [C2] [L2]
            |    |
           -G-   +---(V3)
                 |     |
                [C3]  [RL]
                 |     |
                -G-   -G-
    
    '''
    
    VG = 1
    
    # Component values
    R1 = 50
    C1 = from_string("131.2pF") #farad(p=131.2)
    L1 = from_string('858.4nH') #henry(n=858.4)
    C2 = from_string('424.4pF') #farad(p=424.4)
    L2 = L1
    C3 = C1
    RL = 50
    
    # Get the reactances of all components at the frequency
    Zc1 = get_capacitive_reactance(f, C1)
    Zl1 = get_inductive_reactance(f, L1)
    Zc2 = get_capacitive_reactance(f, C2)
    Zl2 = Zl1
    Zc3 = Zc1
    

    # Find the impedances at each intermediate node
    ZR3 = sum_parallel_resistance([Zc3, RL])
    ZR2 = sum_parallel_resistance([Zc2, Zl2 + ZR3])
    ZR1 = sum_parallel_resistance([Zc1, Zl1 + ZR2])
    
    # Calculate the voltage at each intermediate node
    V1 = voltage_divider(VG, R1, ZR1)
    V2 = voltage_divider(V1, Zl1, ZR2)
    V3 = voltage_divider(V2, Zl2, ZR3)
    
    
    # print()z
    # print(f'  f = {hertz(f)}')
    # print(f' C1 = {str(C1): <13}  L1 = {str(L1): <13}  C2 = {str(C2): <13}')
    # print(f'Zc1 = {str(Zc1): <13} Zl1 = {str(Zl1): <13} Zc2 = {str(Zc2): <13}')
    # print(f'ZR1 = {str(ZR1): <13} ZR2 = {str(ZR2): <13} ZR3 = {str(ZR3): <13}')
    # print(f' V1 = {str(volt(V1.magnitude)): <13}  V2 = {str(volt(V2.magnitude)): <13}  V3 = {str(volt(V3.magnitude)): <10}')

    return 10.0 * (cmath.log10((V3)**2.0))


x_data = get_domain(f_min, f_max, f_samples)
y_data = [circuit(f) for f in x_data]

# print()
# print()
# print()
# for f,a in zip(x_data, y_data):
#     print(f'{str(hertz(f)):>20} {a}')


fig, ax = plt.subplots()
bpm = BodePlotManager(ax)
bpm.configure(
    x_data,
    hlines=[-3, y_data[0].real-3.0],
    vlines=[f_target, f_target*2.0],
    f_min=f_min,
    f_max=f_max
)
bpm.plot_fq(y_data)
plt.show()
