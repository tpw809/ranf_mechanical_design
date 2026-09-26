"""Existing python packages for interval arithemtic:

incorrect: pip install pyia
pip install git+https://github.com/mickleness/pyinterval-arithmetic.git

incorrect: pip install pyball
pip install git+https://github.com/mickleness/pyball.git

PyInterval:
https://github.com/taschini/pyinterval
https://pyinterval.readthedocs.io/en/latest/
https://pypi.org/project/crlibm/

ERROR: Failed to build 'crlibm' when getting requirements to build wheel

pip install pyinterval

None of these work for various reasons... sep 26, 2026
"""
########################
# pyia:
########################

# from pyia.interval_arithmetic import Interval
# 
# A = Interval(2, 5)
# B = Interval(-3, 4)
# 
# print("A =", A)
# print("B =", B)
# 
# C = A + B
# D = A * B
# E = A / Interval(2, 3)
# 
# print("A + B =", C)
# print("A * B =", D)
# print("A / [2,3] =", E)


########################
# pyball:
########################

# from pyball import Ball
# 
# # Create balls (midpoint, radius)
# A = Ball(3, 1)   # represents [2, 4]
# B = Ball(10, 2)  # represents [8, 12]
# 
# print("A =", A)
# print("B =", B)
# 
# # Arithmetic
# C = A + B
# D = A * B
# E = B / A
# 
# print("A + B =", C)
# print("A * B =", D)
# print("B / A =", E)

from ball import Ball

# Ball(midpoint, radius)
A = Ball(10, 2)   # represents [8, 12]
B = Ball(3, 1)    # represents [2, 4]

print("A =", A)
print("B =", B)

C = A + B
D = A * B
E = A / B

print("A + B =", C)
print("A * B =", D)
print("A / B =", E)


########################
# pyinterval
########################

from interval import interval

# Create intervals
A = interval[2, 5]
B = interval[-3, 4]

print("A =", A)
print("B =", B)

# Arithmetic
C = A + B
D = A * B
E = A / interval[2, 3]

print("A + B =", C)
print("A * B =", D)
print("A / [2,3] =", E)

