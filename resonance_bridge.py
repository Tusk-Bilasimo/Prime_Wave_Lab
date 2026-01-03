import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

# set style for a professional blog look
sns.set_theme(style="whitegrid")


def plot_resonance_bridge():
    fig, ax = plt.subplots(figsize=(12, 7))

    # 1. Setup Data
    # The 24 Spokes
    spokes = np.arange(24)

    # The 8 Active Prime Spokes
    active_spokes_indices = [1, 5, 7, 11, 13, 17, 19, 23]

    # Simulated normalized resonance density based on PWT theory constraints.
    # Inactive spokes have near-zero resonance (the "gaps").
    # Active spokes show high resonance peaks.
    resonance_density = np.zeros(24) + 0.02  # Baseline noise floor

    # Relative peak amplitudes representing PWT nodal interference
    # Highlighting the "Koide" zones with slightly different amplitudes
    peak_map = {
        1: 0.85,  # Anchor
        5: 1.0,  # Pentad (Koide L1)
        7: 1.0,  # Septad (Koide L1)
        11: 0.92,  # Torsion Bridge (Koide L2)
        13: 0.92,  # Torsion Complement (Koide L2)
        17: 0.75,  # Octave
        19: 0.75,  # Return
        23: 0.85  # Mirror Anchor
    }
    for spoke, value in peak_map.items():
        resonance_density[spoke] = value

    # 2. Define Colors
    # Deep blue for active resonance, light gray for inactive gaps
    bar_colors = ['#004488' if s in active_spokes_indices else '#D3D3D3' for s in spokes]

    # 3. Create the Bar Plot
    bars = ax.bar(spokes, resonance_density, color=bar_colors, width=0.8, edgecolor='none')

    # 4. Highlight the "Berry Phase / Koide Zones"
    # Zone 1: Spokes 5 & 7
    ax.axvspan(4.5, 7.5, color='#FFD700', alpha=0.2, lw=0, label='Koide Zone L1 (Max Resonance)')
    # Zone 2: Spokes 11 & 13
    ax.axvspan(10.5, 13.5, color='#00C4CC', alpha=0.2, lw=0, label='Koide Zone L2 (Max Torsion)')

    # 5. Formatting and Labels
    ax.set_xticks(spokes)
    ax.set_xticklabels(spokes, fontsize=10)
    ax.set_xlim(-1, 24)
    ax.set_ylim(0, 1.1)

    ax.set_xlabel("Modulo 24 Spoke Index (Topology)", fontsize=12, fontweight='bold', labelpad=10)
    ax.set_ylabel("PWT Resonance Density (Normalized Amplitude)", fontsize=12, fontweight='bold', labelpad=10)

    ax.set_title("The Resonance Bridge: PWT Rational Nodes vs. Mod-24 Topology", fontsize=16, fontweight='bold', pad=20)

    # 6. Annotations for the Researcher
    # Pointing out the Torsion Bridge
    ax.annotate('Torsion Bridge\n(High Berry Curvature)', xy=(12, 0.92), xytext=(15, 1.02),
                arrowprops=dict(facecolor='black', shrink=0.05, width=1.5, headwidth=8),
                fontsize=10, ha='center')

    # Adding a legend
    ax.legend(loc='upper right', frameon=True, shadow=True)

    # Clean up layout
    plt.tight_layout()

    # Save or show
    # plt.savefig("PWT_Resonance_Bridge.png", dpi=300)
    plt.show()


if __name__ == "__main__":
    plot_resonance_bridge()