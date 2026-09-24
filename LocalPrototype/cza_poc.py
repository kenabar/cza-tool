"""
Proof of concept for the control zone analysis tool. This script runs locally and will be the demonstrator for the eventual streamlit based app.
"""

import numpy as np
from matplotlib import pyplot as plt
from matplotlib.widgets import Slider


def calc_y_max(q: int,k: int, b: int, i: float|int) -> float:
    return q / (2 * k * b * i)

def calc_x_array(y_array: np.ndarray, k: int, b: int, i: float|int, q: int) -> np.ndarray:
    x = -y_array / (np.tan(((2 * np.pi * k * b * i) / q) * y_array))
    return x

def calc_asymptote_y_val(q: int, k: int, b: int, i: float|int) -> float:
    return q / (2 * k * b * i)

def filter_asymptotes(x_array: np.ndarray, y_array: np.ndarray, asymptote_y):
    # Filter out points from the arrays where y is greater than y_max
    mask = np.abs(y_array) < asymptote_y
    x_filtered = x_array[mask]
    y_filtered = y_array[mask]
    return x_filtered, y_filtered

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
    asymptote_y_val = calc_asymptote_y_val(q_init, k_init, b_init, i_init)
    x_filt, y_filt = filter_asymptotes(x_locs, y_locs, asymptote_y_val)
    y_max = calc_y_max(q_init, k_init, b_init, i_init)
    line, = ax_plot.plot(x_filt, y_filt)
    ax_plot.plot(0, 0, 'ro', markersize=8)
    ax_plot.set_xlim(-400, 1000)
    ax_plot.set_ylim(-y_max, y_max)
    ax_plot.set_xlabel("X")
    ax_plot.set_ylabel("Y")
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
        asymptote_y_val = calc_asymptote_y_val(q, k, b, i)
        x_filt, y_filt = filter_asymptotes(x_locs, y_locs, asymptote_y_val)

        line.set_data(x_filt, y_filt)
        fig.canvas.draw_idle()

    slider_q.on_changed(update)
    slider_i.on_changed(update)
    slider_k.on_changed(update)
    slider_b.on_changed(update)

    plt.show()




if __name__ == "__main__":
    main()