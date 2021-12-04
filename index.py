import numpy as np
from auxilliary import *
from verify import *
from tabulate import tabulate

ending_string = ""

working_freq = int(input("Masukkan f (dalam MegaHertz): "))*1e6 # Working frequency
dl = float(input("Masukkan dl (dalam cm): "))*1e-2 # Panjang transmission line kanan setelah stub
ds = float(input("Masukkan ds (dalam cm): "))*1e-2 # Panjang stub

while True:
    typ = input("Jenis stub? [short/open] : ")
    if typ == "short":
        stub_type = True
        break
    elif typ == "open":
        stub_type = False
        break
    else:
        print("Input salah, coba lagi dong. ", end="")

# working_freq = 390e6
# dl = 19.388e-2
# ds = 22.715e-2
# stub_type = True # Jenis stub, apabila True berarti short, apabila False berarti open

load_impedance = parallel(50, 1/(1j*2*np.pi*working_freq*22e-12)) # Impedance at load, will be changed in sweep
trans_line_inherent_impedance = 50

d = 100e-2 # Length of transmission line
da = d-dl

# Sweeping frequencies
f = 390e6
freqs = []
coefs = []
coefs_abs = []

ending_string += "Sweeping frequency for the following configuration:\nf = {:.3e} Hz\ndl = {:.6e} m\nds = {:.6e} m ({} circuit)\n\n".format(working_freq, dl, ds, typ)
while f <= 410e6:  
    load_impedance = parallel(50, 1/(1j*2*np.pi*f*22e-12)) # Impedance at load
    # print(load_impedance)
    Gg_ = get_reflection_coefficient_at_generator(
        load_impedance, trans_line_inherent_impedance, f, dl, ds, da, stub_type)
    Gg_r = display_rounded_complex_number(Gg_, 3)
    freqs.append("{:.3e}".format(f))
    coefs.append("{}".format(Gg_r))
    coefs_abs.append("{:.3}".format(abs(Gg_r)))
    # print("{:.3e} \t {} \t {:3}".format(f,Gg_r,abs(Gg_r)))
    f += 1e6

table = {'Frequency': freqs, 'Reflection coef.': coefs, 'Magnitude for ref. coef.': coefs_abs}

ending_string += tabulate(table, headers='keys',
                        # tablefmt='grid', 
                          showindex=True) + "\n\n"

print(ending_string)

to_text_prompt = input("Print to file? [y/n] : ")

if to_text_prompt == "y":
    file = open("outputs.txt", "a")
    file.write(ending_string)
    print("All done! See outputs.txt for the output.")
else: 
    print("No text file needed, bye!")