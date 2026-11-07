"""Streamlit application for control zone analysis."""

import matplotlib.pyplot as plt
import numpy as np
import streamlit as st


def calc_y_max(q: int, k: int, b: int, i: float) -> float:
    """Return the y-coordinate of the control zone asymptote."""
    return q / (2 * k * b * i)


def calc_x_array(
    y_array: np.ndarray, k: int, b: int, i: float, q: int
) -> np.ndarray:
    """Calculate x coordinates for the supplied y coordinates."""
    angle = ((2 * np.pi * k * b * i) / q) * y_array
    x_array = np.empty_like(y_array, dtype=float)
    np.divide(-y_array, np.tan(angle), out=x_array, where=angle != 0)
    x_array[angle == 0] = -q / (2 * np.pi * k * b * i)
    return x_array


def filter_asymptotes(
    x_array: np.ndarray, y_array: np.ndarray, asymptote_y: float
) -> tuple[np.ndarray, np.ndarray]:
    """Remove curve points at and beyond the asymptote."""
    mask = np.abs(y_array) < asymptote_y
    return x_array[mask], y_array[mask]


def create_control_zone_plot(q: int, i: float, k: int, b: int) -> plt.Figure:
    """Build the control zone plot for the selected parameters."""
    y_locs = np.arange(-1000, 1000.1, step=5, dtype=int)
    x_locs = calc_x_array(y_locs, k, b, i, q)
    asymptote_y = calc_y_max(q, k, b, i)
    x_filtered, y_filtered = filter_asymptotes(x_locs, y_locs, asymptote_y)

    fig, ax_plot = plt.subplots(figsize=(6, 3.5))
    ax_plot.plot(x_filtered, y_filtered)
    ax_plot.plot(0, 0, "ro", markersize=8)
    ax_plot.set_xlim(-400, 1000)
    ax_plot.set_ylim(-asymptote_y, asymptote_y)
    ax_plot.set_xlabel("X")
    ax_plot.set_ylabel("Y")
    ax_plot.set_title("Control Zone Analysis")
    ax_plot.grid(True, alpha=0.3)
    fig.tight_layout()
    return fig


def main() -> None:
    """Render the Streamlit control zone analysis application."""
    st.set_page_config(page_title="Control Zone Analysis", layout="wide")
    st.title("Control Zone Analysis")
    st.write("Adjust the parameters to update the control zone plot.")

    with st.sidebar:
        st.header("Parameters")
        q = st.slider(
            "q (extraction rate)",
            min_value=960,
            max_value=2880,
            value=1920,
            step=10,
        )
        i = st.slider(
            "i (hydraulic gradient)",
            min_value=0.003,
            max_value=0.009,
            value=0.006,
            step=0.0001,
            format="%.4f",
        )
        k = st.slider(
            "k (conductivity)",
            min_value=10,
            max_value=30,
            value=20,
            step=1,
        )
        b = st.slider(
            "b (thickness)",
            min_value=10,
            max_value=30,
            value=20,
            step=1,
        )

    figure = create_control_zone_plot(q, i, k, b)
    st.pyplot(figure, width="content")
    plt.close(figure)


if __name__ == "__main__":
    main()
