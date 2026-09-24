"""
Proof of concept for the control zone analysis tool. This script runs locally and will be the demonstrator for the eventual streamlit based app.
"""

import numpy as np
from matplotlib import pyplot as plt
from matplotlib.widgets import Slider


def calc_y_max(q: int,k: int, b: int, i: float|int) -> float:
    """
    Args:
        q: extraction rate
        k: hydraulic conductivity
        b: saturated thickness
        i: regional hydraulic gradient

    Returns: Maximum capture zone width from the central line of the plume
    """
    return q / (2 * k * b * i)

def calc_x_array(y_array: np.ndarray, k: int, b: int, i: float|int, q: int) -> np.ndarray:
    x = -y_array / (np.tan(((2 * np.pi * k * b * i) / q) * y_array))
    return x

def get_capture_zone_boundary(x_locs: np.ndarray, y_locs: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """
    Filter capture zone points to keep only the boundary.
    For each unique x location, keep the smallest positive y and largest negative y (closest to y=0).
    
    Args:
        x_locs: Array of x coordinates
        y_locs: Array of y coordinates
    
    Returns:
        Tuple of filtered (x_locs, y_locs) arrays representing the zone boundary
    """
    # Round x values to group similar values (handle floating point precision)
    x_rounded = np.round(x_locs, decimals=1)
    
    # Create array of indices
    indices = np.arange(len(x_locs))
    
    # Get unique x values and their first occurrence indices
    unique_x, unique_indices = np.unique(x_rounded, return_index=True)
    
    filtered_x = []
    filtered_y = []
    
    # For each unique x value, find and keep boundary points
    for x_val in unique_x:
        mask = x_rounded == x_val
        y_at_x = y_locs[mask]
        
        # Find smallest positive y (upper boundary, closest to zero)
        positive_y = y_at_x[y_at_x > 0]
        if len(positive_y) > 0:
            min_positive = np.min(positive_y)
            filtered_x.append(x_val)
            filtered_y.append(min_positive)
        
        # Find largest negative y (lower boundary, closest to zero)
        negative_y = y_at_x[y_at_x < 0]
        if len(negative_y) > 0:
            max_negative = np.max(negative_y)
            filtered_x.append(x_val)
            filtered_y.append(max_negative)
    
    return np.array(filtered_x), np.array(filtered_y)


def main():
    # Define the parameters
    q_init = 1920  # extraction rate
    i_init = 0.006  # regional hydraulic gradient
    k_init = 20  # hydraulic conductivity
    b_init = 20  # saturated thickness

    # Define the y array
    y_locs: np.ndarray = np.arange(-1000, 1000.1, step=20, dtype=int)

    # Create figure with space for sliders
    fig = plt.figure(figsize=(12, 8))
    gs = fig.add_gridspec(5, 1, height_ratios=[4, 0.5, 0.5, 0.5, 0.5], hspace=0.6)
    
    ax_plot = fig.add_subplot(gs[0])
    ax_q = fig.add_subplot(gs[1])
    ax_i = fig.add_subplot(gs[2])
    ax_k = fig.add_subplot(gs[3])
    ax_b = fig.add_subplot(gs[4])

    # Calculate initial plot
    x_locs = calc_x_array(y_locs, k_init, b_init, i_init, q_init)
    y_max = calc_y_max(q_init, k_init, b_init, i_init)
    line, = ax_plot.plot(x_locs, y_locs)
    ax_plot.set_xlim(-400, 1000)
    ax_plot.set_ylim(-y_max, y_max)
    ax_plot.set_xlabel("Distance (x)")
    ax_plot.set_ylabel("Distance (y)")
    ax_plot.set_title("Control Zone Analysis")
    ax_plot.grid(True, alpha=0.3)

    # Create sliders with ±50% ranges based on current values
    slider_q = Slider(ax_q, 'q (extraction rate)', 960, 2880, valinit=q_init, valstep=10)
    slider_i = Slider(ax_i, 'i (hydraulic gradient)', 0.003, 0.009, valinit=i_init, valstep=0.0001)
    slider_k = Slider(ax_k, 'k (conductivity)', 10, 30, valinit=k_init, valstep=1)
    slider_b = Slider(ax_b, 'b (thickness)', 10, 30, valinit=b_init, valstep=1)

    def update(val):
        q = int(slider_q.val)
        i = slider_i.val
        k = int(slider_k.val)
        b = int(slider_b.val)
        
        x_locs = calc_x_array(y_locs, k, b, i, q)

        line.set_data(x_locs, y_locs)
        fig.canvas.draw_idle()

    slider_q.on_changed(update)
    slider_i.on_changed(update)
    slider_k.on_changed(update)
    slider_b.on_changed(update)

    plt.show()




if __name__ == "__main__":
    main()