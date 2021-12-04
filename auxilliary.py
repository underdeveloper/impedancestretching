import numpy as np

def parallel(Z1: complex, Z2: complex):
    return ((Z1*Z2)/(Z1+Z2))

def normalize(Z: complex, Zo:complex):
    return Z/Zo

def denormalize(Zn: complex, Zo:complex):
    return Zn*Zo

def find_reflection_coef(Z: complex, Zo: complex):
    return (Z-Zo)/(Z+Zo)

def find_point_impedance(G: complex, Zo: complex):
    return Zo*(G+1)/(1-G)

def rotate_on_smith_chart(G: complex, towards_generator: bool, distance_in_lambdas: float):
    direction = 1 if towards_generator else -1
    angle = (distance_in_lambdas / (0.5)) * 2*np.pi
    G_prime = G * np.exp(direction*-1j*angle)
    G_prime_rounded = round(np.real(G_prime),6) + 1j * round(np.imag(G_prime),6)
    return G_prime_rounded