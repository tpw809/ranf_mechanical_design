import numpy as np

# wire diameter:
d = 1.0

# mean coil diameter at free length:
D = 10.0

# pitch at free length:
p = 1.0


############################################
# MIL-STD-29A, section 21.3: Diameter Changes in Compression Springs
############################################

# Increase in outside diameter when compressed:

# OD_c = outside diameter at solid length:
OD_c = np.sqrt(D**2 + (p**2 - d**2)/np.pi**2) + d


############################################
# MIL-STD-29A, section 21.4: Bucking
############################################

# Slenderness Ratio = Free Length / Mean Diameter
# Springs with slenderness ratio > 4 are critical in lateral stability (buckling)


############################################
# MIL-STD-29A, section 21.4: Direction of Helix
############################################





############################################
# MIL-STD-29A, section 21.11: Curvature Stress-Correction Factors
############################################

# Curvature Stress Correction Factor: K

K = (4.0 * C - 1.0) / (4.0 * C - 4.0) + 0.615 / C

# S_max - S_t * K



############################################
# MIL-STD-29A, section 21.12: Keystone Effect
############################################

# *For square and rectangular wire only*

# t_prime = new thickness of inner edge after coiling
# t = thickness before coiling

t_prime = 0.48 * t * (OD / D + 1.0)
