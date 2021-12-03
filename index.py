import numpy as np
from auxilliary import *
from scipy.constants import speed_of_light as c

working_freq = int(input("Masukkan f (dalam MegaHertz): "))*10e6 # Working frequency
working_lambda = c/working_freq

load_impedance = parallel(50, 1/(1j*2*np.pi*working_freq*22e-12)) # Impedance at load
trans_line_inherent_impedance = 50

d = 100e-2 # Length of transmission line

dl = float(input("Masukkan dl (dalam cm): "))*10e-2 # Panjang transmission line kanan setelah stub
ds = float(input("Masukkan ds (dalam cm): "))*10e-2 # Panjang stub
stub_type = True # Jenis stub, apabila True berarti short, apabila False berarti open

da = d-dl

# ! Stage One
# -------''' '''--------OL # Right near load
Gl = find_reflection_coef(load_impedance, trans_line_inherent_impedance)

# ! Stage Two
# -------''' '''O--------L # Right near stub
Gs2 = rotate_on_smith_chart(Gl, True, dl/working_lambda)
Zs2 = find_point_impedance(Gl, trans_line_inherent_impedance)

# ! Stage Three
# -------'''O'''---------L # The stub
if stub_type: # Jika short
    Gsx = rotate_on_smith_chart(-1+0j, False, ds/working_lambda)
else:
    Gsx = rotate_on_smith_chart(1+0j, False, ds/working_lambda)

Zsx = find_point_impedance(Gsx, trans_line_inherent_impedance)

# ! Stage Four
# ------O''''''---------L # Left near stub
Zs1 = Zs2 - Zsx
Gs1 = find_reflection_coef(Zs1, trans_line_inherent_impedance)

# ! Stage Five
# O------''''''---------L # Left near generator
Gg = rotate_on_smith_chart(Gs1, True, da/working_lambda)

print(Gg)


