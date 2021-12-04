import numpy as np
from auxilliary import *
from scipy.constants import speed_of_light as c

# working_freq = int(input("Masukkan f (dalam MegaHertz): "))*1e6 # Working frequency
# dl = float(input("Masukkan dl (dalam cm): "))*1e-2 # Panjang transmission line kanan setelah stub
# ds = float(input("Masukkan ds (dalam cm): "))*1e-2 # Panjang stub
working_freq = 410e6
dl = 18.280e-2
ds = 3.875e-2

stub_type = False  # Jenis stub, apabila True berarti short, apabila False berarti open

working_lambda = c/working_freq

load_impedance = parallel(50, 1/(1j*2*np.pi*working_freq*22e-12)) # Impedance at load
trans_line_inherent_impedance = 50

d = 100e-2 # Length of transmission line
da = d-dl

# ! Stage One
# -------''' '''--------OL # Right near load
Gl = find_reflection_coef(load_impedance, trans_line_inherent_impedance)
print("Normalised load impedance:\n ", normalize(load_impedance, trans_line_inherent_impedance))

# ! Stage Two
# -------''' '''O--------L # Right near stub
Gs2 = rotate_on_smith_chart(Gl, True, dl/working_lambda)
Zs2 = find_point_impedance(Gs2, trans_line_inherent_impedance)
print("Normalised impedance right of stub:\n ", normalize(Zs2, trans_line_inherent_impedance))

# ! Stage Three
# -------'''O'''---------L # The stub
if stub_type: # Jika short
    Gsx = rotate_on_smith_chart(-1+0j, True, ds/working_lambda)
else:
    Gsx = rotate_on_smith_chart(1+0j, True, ds/working_lambda)

Zsx = find_point_impedance(Gsx, trans_line_inherent_impedance)
print("Equivalent impedance to stub:\n ", normalize(Zsx, trans_line_inherent_impedance))

# ! Stage Four
# ------O''''''---------L # Left near stub
Zs1 = Zs2 + Zsx
print("Normalised impedance left of stub (should have very little reactance):\n ", normalize(Zs1, trans_line_inherent_impedance))
Gs1 = find_reflection_coef(Zs1, trans_line_inherent_impedance)

# ! Stage Five
# O------''''''---------L # Left near generator
Gg = rotate_on_smith_chart(Gs1, True, da/working_lambda)

print("Reflection coefficient near generator (should be near enough to 0):\n ",Gg)