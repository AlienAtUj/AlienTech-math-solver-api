# solvemath/plot.py (updated)
import matplotlib
matplotlib.use('Agg')  # Critical fix for threading
from matplotlib import pyplot as plt
import numpy as np
import sympy
import os
import uuid

def plot_equation(equation):
    x = sympy.Symbol('x')
    y = sympy.sympify(equation)
    y_lambda = sympy.lambdify(x, y, "numpy")

    x_vals = np.linspace(-10, 10, 400)
    try:
        y_vals = y_lambda(x_vals)
    except TypeError:
        y_vals = np.full_like(x_vals, float(y))

    plt.figure(figsize=(8, 4))
    plt.plot(x_vals, y_vals, 'b-', linewidth=2)
    plt.title(f"Plot of {equation}", fontsize=14)
    plt.xlabel("x", fontsize=12)
    plt.ylabel("y", fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.tight_layout()

    plot_dir = "plots"
    os.makedirs(plot_dir, exist_ok=True)
    filename = f"plot_{uuid.uuid4().hex}.png"
    filepath = os.path.join(plot_dir, filename)
    plt.savefig(filepath, dpi=150)
    plt.close()
    
    return filename