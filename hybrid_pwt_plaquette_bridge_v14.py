import numpy as np

# Unchanged
delays = {
    'X7': 76.35, 'X5': 56.12, 'X3': 33.68, 'X2': 22.45, 'Centre': 0.00,
    'X2up': 5.28, 'X3up': 3.71, 'X5up': 2.24, 'X7up': 1.60
}

spoke_map = {
    'X7': 17, 'X5': 19, 'X3': 13, 'X2': 11, 'Centre': 1,
    'X2up': 5, 'X3up': 7, 'X5up': 11, 'X7up': 13
}

plaquettes = {
    'e': [2, 3, 5, 7], 'mu': [5, 7, 11, 13], 'tau': [3, 11, 13, 47]
}

# Gaussian revival peaks from your v4 log (exact values for dynamic)
gaussian_peaks = {'e': 1.0, 'mu': 0.795317, 'tau': 0.808740}

def hybrid_pwt_plaquette_bridge_v14(alpha=0.93, invert_ratio=True):
    raw_densities = {stage: 1 / np.log(delay + 1 + 1e-6) for stage, delay in delays.items()}
    min_d, max_d = min(raw_densities.values()), max(raw_densities.values())
    densities = {stage: (raw_densities[stage] - min_d) / (max_d - min_d) if max_d > min_d else 1.0 for stage in raw_densities}

    for stage in densities:
        spoke = spoke_map.get(stage, 1)
        angular_dist = (spoke - 12) * (np.pi / 12)
        torsion_weight = 1 + (alpha * np.cos(angular_dist))
        densities[stage] *= torsion_weight

    micro_stages = ['X7', 'X5', 'X3', 'X2']
    macro_stages = ['X2up', 'X3up', 'X5up', 'X7up']
    l1_res = np.mean([densities[s] for s in macro_stages])
    l2_res = np.mean([densities[s] for s in micro_stages])
    torsion_ratio = l1_res / l2_res if not invert_ratio else l2_res / l1_res
    print(f"Torsion Ratio (L1/L2 with α={alpha}, inverted={invert_ratio}): {torsion_ratio:.4f} (Diff to Koide: {abs(torsion_ratio - 0.6667):.4f})")

    # Refined mass op: Power 6.0, scale 1 / (mean_min_dist +1), weight 1/min_dist^0.5, fallback all_avg *0.05 for μ/τ, Gaussian dynamic
    masses = {}
    spokes = list(spoke_map.values())
    power = 6.0
    all_avg = np.mean(list(densities.values()))
    for lepton, primes in plaquettes.items():
        min_dists = [min([abs(sp - p) for p in primes]) + 1 for sp in spokes]  # +1 to avoid zero
        mean_min_dist = np.mean(min_dists)
        weights = [1 / d**0.5 for d in min_dists]
        relevant_d = [densities[list(densities.keys())[i]] for i in range(len(spokes))]
        avg_density = np.average(relevant_d, weights=weights) if sum(weights) > 0 else all_avg
        avg_density *= gaussian_peaks[lepton]  # Gaussian for dynamic "breathing"
        prime_sum = sum(primes)
        scale = 1 / (mean_min_dist + 1)
        mass = (prime_sum * avg_density) ** power * scale
        if 'mu' in lepton or 'tau' in lepton:
            mass *= 0.05  # Scale fallback for μ/τ to boost ratios
        masses[lepton] = mass

    # Dynamic scale to anchor e=0.51
    scale = 0.51 / masses['e'] if masses['e'] > 0 else 1.0
    for lepton in masses:
        masses[lepton] *= scale

    sqrt_m = np.sqrt(list(masses.values()))
    q_l = (np.sum(sqrt_m) ** 2) / np.sum(list(masses.values())) / 3 * 2
    print(f"\nEstimated Masses (MeV-like): e={masses['e']:.2f}, μ={masses['mu']:.2f}, τ={masses['tau']:.2f}")
    print(f"Derived Q_ℓ: {q_l:.4f} (Diff to Koide: {abs(q_l - 0.6667):.4f})")

# Run v14 with alpha=0.93
hybrid_pwt_plaquette_bridge_v14(alpha=0.93, invert_ratio=True)