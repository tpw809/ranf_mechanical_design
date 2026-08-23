import numpy as np
import matplotlib.patches as patches
import matplotlib.pyplot as plt
from sympy import symbols, Eq, solve, cos, sin

# initial positions:

# Point 1 (positive):
P1p = np.array([1.0, 0.0])

# Point 2 (positive):
P2p = np.array([1.0, 0.1])

# Point 3 (positive):
P3p = np.array([1.1, 1.1])

# Link Lengths:
L_A = np.linalg.norm(P3p - P1p)
L_B = np.linalg.norm(P3p - P2p)
print(f"L_A = {L_A}")
print(f"L_B = {L_B}")


# solve for position 3 when p2 moves:
tht_A, tht_B = symbols('tht_A tht_B')

eq1 = Eq(P1p[0] + L_A*cos(tht_A),P2p[0] + L_B*cos(tht_B))
eq2 = Eq(P1p[1] + L_A*sin(tht_A),P2p[1] + L_B*sin(tht_B))

sol_p = solve((eq1, eq2), (tht_A, tht_B))
print(sol_p)

print(f"pi/2 = {np.pi/2.0}")

# solution provides both branches of solutions:
PC = [P1p[0] + L_A*cos(sol_p[0][0]), P1p[1] + L_A*sin(sol_p[0][0])]
print(f"PC = {PC}")

PC = [P1p[0] + L_A*cos(sol_p[1][0]), P1p[1] + L_A*sin(sol_p[1][0])]
print(f"PC = {PC}")

PC = [P2p[0] + L_B*cos(sol_p[0][1]), P2p[1] + L_B*sin(sol_p[0][1])]
print(f"PC = {PC}")





# Create a figure and an axes object
fig, ax = plt.subplots()

# Define the rectangle patch
# Parameters: (lower-left x, y), width, height
rect_body1 = patches.Rectangle(
    (-1, -3), 2, 3, 
    linewidth=2, 
    edgecolor="r", 
    facecolor="yellow",
)
rect_body2 = patches.Rectangle(
    (-1, 0), 2, 2, 
    linewidth=2, 
    edgecolor="r", 
    facecolor="purple",
)

# Add the rectangle patch to the axes
ax.add_patch(rect_body1)
ax.add_patch(rect_body2)

# Define the circle: Circle((x, y), radius, properties)
circle_1p = plt.Circle(
    P1p, 
    0.05, 
    color='blue', 
    fill=True, 
    alpha=0.6,
)

circle_2p = plt.Circle(
    P2p, 
    0.05, 
    color='green', 
    fill=True, 
    alpha=0.6,
)

circle_3p = plt.Circle(
    P3p, 
    0.05, 
    color='cyan', 
    fill=True, 
    alpha=0.6,
)

# Add the circle patch to the axis
ax.add_patch(circle_1p)
ax.add_patch(circle_2p)
ax.add_patch(circle_3p)

# Draw Links:
plt.plot([P1p[0], P3p[0]], [P1p[1], P3p[1]], 
    color="red", 
    linestyle="--", 
    linewidth=2)
plt.plot([P2p[0], P3p[0]], [P2p[1], P3p[1]], 
    color="red", 
    linestyle="--", 
    linewidth=2)

#plt.axis('equal')
plt.axis('square')

# Set explicit axis limits (necessary since patches do not auto-scale)
ax.set_xlim(-0.5, 3.5)
ax.set_ylim(-0.5, 3.5)

# show grid:
# plt.grid()


# animate:
plt.ion()

for d in np.arange(0.1, 2.11, 0.1):
    # print(d)
    # Clear previous frame content
    ax.clear()
    
    # Point 2 (positive):
    P2p = np.array([1.0, d])
    
    eq1 = Eq(P1p[0] + L_A*cos(tht_A),P2p[0] + L_B*cos(tht_B))
    eq2 = Eq(P1p[1] + L_A*sin(tht_A),P2p[1] + L_B*sin(tht_B))

    sol_p = solve((eq1, eq2), (tht_A, tht_B))
    P3p = [P1p[0] + L_A*cos(sol_p[0][0]), P1p[1] + L_A*sin(sol_p[0][0])]
    
    
    circle_2p = plt.Circle(
        P2p, 
        0.05, 
        color='green', 
        fill=True, 
        alpha=0.6,
    )
    
    circle_3p = plt.Circle(
        P3p, 
        0.05, 
        color='cyan', 
        fill=True, 
        alpha=0.6,
    )
    
    ax.add_patch(circle_1p)
    ax.add_patch(circle_2p)
    ax.add_patch(circle_3p)
    
    # Draw Links:
    plt.plot([P1p[0], P3p[0]], [P1p[1], P3p[1]], 
        color="red", 
        linestyle="--", 
        linewidth=2)
    plt.plot([P2p[0], P3p[0]], [P2p[1], P3p[1]], 
        color="red", 
        linestyle="--", 
        linewidth=2)
    
    rect_body1 = patches.Rectangle(
        (-1, -3), 2, 3, 
        linewidth=2, 
        edgecolor="r", 
        facecolor="yellow",
    )
    rect_body2 = patches.Rectangle(
        (P2p[0]-2.0, P2p[1]-0.1), 2, 2, 
        linewidth=2, 
        edgecolor="r", 
        facecolor="purple",
    )

    # Add the rectangle patch to the axes
    ax.add_patch(rect_body1)
    ax.add_patch(rect_body2)
    

    plt.axis('square')
    ax.set_xlim(-0.5, 3.5)
    ax.set_ylim(-0.5, 3.5)
    
    # Force canvas redraw and pause briefly to render
    fig.canvas.draw()
    fig.canvas.flush_events()
    plt.pause(0.001)


plt.ioff()

# Display the plot
plt.show()
