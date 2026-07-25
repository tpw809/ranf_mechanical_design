"""Helical Compression Spring Analysis

References:

- MIL-STD-29A
- AFFDL-TR-69-42 Stress Analysis Manual, section 1.5.4
"""
import numpy as np

# wire shape:
#shape = 'square'
#shape = 'rectangular'
shape = 'round'

# [mm], wire diameter:
d_wire = 1.0

# [mm], wire side length of square wire:
b = 1.0

# [mm], mean coil diameter at free length:
D_mean = 10.0

# [mm/turn], pitch at free length:
p = 1.0

# [mm], spring radius:
r = D_mean / 2.0


# [-], Spring Index (C):
# Spring index should be from 5 to 15, 7 to 9 is ideal
if shape == 'round':
    C = D_mean / d_wire
elif shape == 'square':
    C = D_mean / b
print(f"Spring Index, C = D / d = {C}")
# called 'm' in stress analysis manual

# [mm], Outer diameter (at free length):
OD = D_mean + d_wire

# [mm], Inner diameter (at free length):
ID = D_mean - d_wire

# [N/mm], spring rate:
k = 1.0

# number of active coils:
N = 10.0


# Factor of Safety:
# Ratio of max load a spring can sustain without permanent set to the max applied load.



# Material:

# Modulus of Elasticity:
E = 200.0e3

# Modulus of Torsion:
G = 85.0e3

# Elastic Limit:
EL = 0.6


# [n], Axial Load:
P = 1.0

# [N-mm], torsional load:
T = P * r




############################################
# MIL-STD-29A, section 21.1: Design Formulas
############################################

# Table II:

if shape == 'round':
    # torsional stress:
    # S_t = (P * D) / (0.393 * d**2)
    S_t = 8.0 * P * D_mean / (np.pi * d_wire**3)
    # S_t = (G * d * F) / (np.pi * N *D**2)

    # deflection:
    F = (8.0 * P * N * D_mean**3) / (G * d_wire**4)
    # F = (w * S_t * N * D**3) / (G * d)
    
    # helical compression spring rate:
    k = (G * d_wire**4) / (8.0 * D_mean**3 * N)
    
    # max shear stress in the spring:
    # stress analysis manual, pg 1-95:
    # s_max = 16.0 * P * r / (np.pi * d**3) * (1.0 + d / (4.0 * r))
    s_max = 16.0 * P * r / (np.pi * d_wire**3)
    
    # deflection:
    # stress analysis manual, pg 1-95:
    delta = 64.0 * P*r**3*N / (G * d_wire**4)

elif shape == 'square':
    # max shear stress in the spring:
    # stress analysis manual, pg 1-96:
    s_max = 4.80 * P * r / b**3
    
    # deflection:
    # stress analysis manual, pg 1-96:
    delta = 44.5 * P * r**3 * N / (G * b**4)


# MIL-STD-29A Table III:

# position of max stress is at the inside of the wire

print(f"Spring Deflection:")
print(f"delta = {delta} [mm]")
print(f"F = {F} [mm]")

print(f"Spring Rate:") # F = k * x
print(f"k = {k} [mm]")

P_est = k * delta
print(f"P_est = {P_est}")

############################################
# MIL-STD-29A, section 21.3: Diameter Changes in Compression Springs
############################################

# Increase in outside diameter when compressed:

# OD_c = outside diameter at solid length:
OD_c = np.sqrt(D_mean**2 + (p**2 - d_wire**2)/np.pi**2) + d_wire


############################################
# MIL-STD-29A, section 21.4: Bucking
############################################

# Slenderness Ratio = Free Length / Mean Diameter
# Springs with slenderness ratio > 4 are critical in lateral stability (buckling)


############################################
# MIL-STD-29A, section 21.5: Direction of Helix
############################################

# use opposite hand coils for nested springs
# use opposite hand coils if spring must slide over threads

############################################
# MIL-STD-29A, section 21.6: Natural Frequency, Vibration, Surge
############################################

# natural frequency of the spring should be 13X the frequency of the applied load.

# W = weight of load = applied load
W = P

# slowly applied load:
F = W / r

# suddenly applied load:
F = 2.0 * W / r

# applied load dropped vertically:
# (spring initially compressed)
# F = (W - F1 + np.sqrt((w - F1)**2 + 2.0 * W * r)) / r

# applied load with striking velocity of V:
# (spring in horizontal plane)

# velocity of impact:
V = 1.0
# F = (-F1 + np.sqrt(F1**3 + (W*r*V**2) / 336)) / r

############################################
# MIL-STD-29A, section 21.11: Curvature Stress-Correction Factors
############################################

# Curvature Stress Correction Factor: K
# Wahl Stress Correction Factor, K_w
K = (4.0 * C - 1.0) / (4.0 * C - 4.0) + 0.615 / C

s_max = s_max * K
print(f"s_max = {s_max} [MPa]")

S_t_max = S_t * K
print(f"S_t_max = {S_t_max} [MPa]")

# as spring diameter increases, this approaches:
# (1.0 + d / (4.0 * r))


############################################
# MIL-STD-29A, section 21.12: Keystone Effect
############################################

# *For square and rectangular wire only*

# t = thickness before coiling
t = b

# t_prime = new thickness of inner edge after coiling

t_prime = 0.48 * t * (OD / D_mean + 1.0)
