"""
A SECOND-ORDER METHOD FOR ASSEMBLY TOLERANCE ANALYSIS

Charles G. Glancy, Kenneth W. Chase

Proceedings of the 1999 ASME Design Engineering Technical Conferences
"""
import numpy as np

# One-Way Clutch Example:

# A:
A_mean = 27.645
# standard deviation 
A_sigma = 0.01666
# distribution = normal

# C, D:
C_mean = 11.430
# standard deviation 
C_sigma = 0.00333
# distribution = normal

# E:
E_mean = 50.800
# standard deviation 
E_sigma = 0.00416
# distribution = normal

# Vector Loop Equations:
# A + C + D * cos(phi1) = E * cos(phi)
# B + D * sin(phi1) = E * sin(phi1)

# x = knowns
# u = unknowns


# example sympy solve two simultaneous equations:

from sympy import symbols, Eq, solve

# 1. Define symbolic variables
x, y = symbols('x y')

# 2. Define the equations
eq1 = Eq(2*x + y, 5)
eq2 = Eq(x - 3*y, 7)

# 3. Solve the system for variables x and y
solution = solve([eq1, eq2], (x, y))
print(solution)


# example sympy partial differential:

import sympy as sp

# 1. Define symbolic variables
x, y = sp.symbols('x y')

# 2. Create a multivariable expression: f(x, y) = x^2 * y + sin(x * y)
f = x**2 * y + sp.sin(x * y)

# 3. First-order partial derivative with respect to x
df_dx = sp.diff(f, x)
print("∂f/∂x:", df_dx)  # Output: 2*x*y + y*cos(x*y)

# 4. First-order partial derivative with respect to y
df_dy = sp.diff(f, y)
print("∂f/∂y:", df_dy)  # Output: x**2 + x*cos(x*y)

# 5. Higher-order partial derivative (Second derivative with respect to x)
# Pass the variable multiple times or provide the order as an argument
d2f_dx2 = sp.diff(f, x, 2)
print("∂²f/∂x²:", d2f_dx2)  # Output: y*(-y*sin(x*y) + 2)

# 6. Mixed partial derivative (differentiate by x, then by y)
d2f_dxdy = sp.diff(f, x, y)
print("∂²f/(∂x∂y):", d2f_dxdy)


# sympy matrices:
from sympy import Matrix, symbols, sqrt
M = Matrix([[1, -1], [3, 4]])

# column vector:
v = Matrix([1, 2, 3])

# By dimensions: Specify the row count, column count, and a flat list of entries
A = Matrix(2, 3, [1, 2, 3, 4, 5, 6])

from sympy import eye, zeros, ones, diag
I = eye(3)      # 3x3 Identity matrix
Z = zeros(2, 3) # 2x3 Matrix of zeros
O = ones(3, 1)  # 3x1 Matrix of ones
D = diag(1, 2, 3) # Diagonal matrix

# Multiplication of compatible matrices
# result = M * v 

# M_transposed = M.T

# determinant = M.det()

# M_inverse = M.inv()

# rref_matrix, pivots = M.rref()

# Returns a dictionary of {eigenvalue: multiplicity}
# eigenvals = M.eigenvals() 

# Returns a list of tuples: (eigenvalue, multiplicity, [eigenvectors])
# eigenvects = M.eigenvects() 


# Python statistics:
# https://medium.com/codetodeploy/your-python-toolkit-for-statistics-8e32b018805f
# numpy, pandas, scipy, seaborn, statsmodels, pingouin

# one line to rule them all
# pip install numpy pandas scipy statsmodels seaborn pingouin

# let's see if everything survived the trip
import numpy as np          # the number cruncher
import pandas as pd         # the spreadsheet brain
from scipy import stats     # the hypothesis tester
import statsmodels.api as sm  # the full report generator
import seaborn as sns        # the chart artist
import pingouin as pg        # the overachiever
print("All six loaded. We're good.")
