from auxilliary import *
import numpy as np
from scipy.constants import speed_of_light as c

def get_reflection_coefficient_at_generator(load_impedance, trans_line_inherent_impedance, working_freq, dl, ds, da, stub_type):

    working_lambda = c/working_freq
    
    # ! Stage One
    # -------''' '''--------OL # Right near load
    Gl = find_reflection_coef(load_impedance, trans_line_inherent_impedance)
    #print("Normalised load impedance:\n ", normalize(load_impedance, trans_line_inherent_impedance))

    # ! Stage Two
    # -------''' '''O--------L # Right near stub
    Gs2 = rotate_on_smith_chart(Gl, True, dl/working_lambda)
    Zs2 = find_point_impedance(Gs2, trans_line_inherent_impedance)
    #print("Normalised impedance right of stub:\n ", normalize(Zs2, trans_line_inherent_impedance))

    # ! Stage Three
    # -------'''O'''---------L # The stub
    if stub_type: # Jika short
        Gsx = rotate_on_smith_chart(-1+0j, True, ds/working_lambda)
    else:
        Gsx = rotate_on_smith_chart(1+0j, True, ds/working_lambda)

    Zsx = find_point_impedance(Gsx, trans_line_inherent_impedance)
    #print("Equivalent impedance to stub:\n ", normalize(Zsx, trans_line_inherent_impedance))

    # ! Stage Four
    # ------O''''''---------L # Left near stub
    Zs1 = Zs2 + Zsx
    #print("Normalised impedance left of stub (should have very little reactance):\n ", normalize(Zs1, trans_line_inherent_impedance))
    Gs1 = find_reflection_coef(Zs1, trans_line_inherent_impedance)

    # ! Stage Five
    # O------''''''---------L # Left near generator
    Gg = rotate_on_smith_chart(Gs1, True, da/working_lambda)
    #print("Reflection coefficient near generator (should be near enough to 0):\n ",Gg)

    return Gg