import matplotlib.pyplot as plt
import numpy as np


def plot_mod24_wheel():
    # Set up the figure for a polar plot
    fig, ax = plt.subplots(figsize=(8, 8), subplot_kw={'projection': 'polar'})

    # The 24 spokes (angles)
    theta = np.linspace(0, 2 * np.pi, 24, endpoint=False)
    radii = np.ones(24)
    width = np.pi / 12  # Width of each slice

    # The "Prime Spokes" (numbers coprime to 24, where primes > 3 must fall)
    # 1, 5, 7, 11, 13, 17, 19, 23
    prime_indices = [1, 5, 7, 11, 13, 17, 19, 23]

    # Colors
    base_color = '#e0e0e0'  # Light gray for non-prime spokes
    prime_color = '#FF5733'  # Vibrant orange/red for prime spokes

    # Plot non-prime spokes
    bars = ax.bar(theta, radii, width=width, bottom=0.0, color=base_color, edgecolor='white')

    # Highlight prime spokes
    for i in prime_indices:
        bars[i].set_color(prime_color)
        bars[i].set_alpha(0.8)

    # Set labels (0 through 23) around the wheel
    ax.set_xticks(theta)
    ax.set_xticklabels([str(i) for i in range(24)], fontsize=10)

    # Remove radial gridlines and y-ticks for cleaner look
    ax.set_yticklabels([])
    ax.grid(False)
    ax.spines['polar'].set_visible(False)

    # Title
    plt.title("Layer 1: The Modulo 24 Prime Sieve", fontsize=16, pad=20)

    plt.show()


if __name__ == "__main__":
    plot_mod24_wheel()