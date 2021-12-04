import numpy as np
from auxilliary import *
from verify import *
from tabulate import tabulate

# working_freq = int(input("Masukkan f (dalam MegaHertz): "))*1e6 # Working frequency
# dl = float(input("Masukkan dl (dalam cm): "))*1e-2 # Panjang transmission line kanan setelah stub
# ds = float(input("Masukkan ds (dalam cm): "))*1e-2 # Panjang stub
working_freq = 410e6
dl = 18.280e-2
ds = 3.875e-2

stub_type = False  # Jenis stub, apabila True berarti short, apabila False berarti open


load_impedance = parallel(50, 1/(1j*2*np.pi*working_freq*22e-12)) # Impedance at load
trans_line_inherent_impedance = 50

d = 100e-2 # Length of transmission line
da = d-dl

# Verification of ref. coef. at generatorside


# Sweeping frequencies
f = 390e6
freqs = []
coefs = []
coefs_abs = []
while f <= 410e6:
    Gg_ = get_reflection_coefficient_at_generator(
        load_impedance, trans_line_inherent_impedance, f, dl, ds, da, stub_type)
    Gg_r = display_rounded_complex_number(Gg_, 3)
    freqs.append("{:.3e}".format(f))
    coefs.append("{}".format(Gg_r))
    coefs_abs.append("{:.3}".format(abs(Gg_r)))
    # print("{:.3e} \t {} \t {:3}".format(f,Gg_r,abs(Gg_r)))
    f += 1e6

table = {'Frequency': freqs, 'Gamma': coefs, '|Gamma|': coefs_abs}

print(tabulate(table, headers='keys'))