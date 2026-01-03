import numpy as np


def get_primes(n):
    sieve = [True] * (n + 1)
    for p in range(2, int(n ** 0.5) + 1):
        if sieve[p]:
            for i in range(p * p, n + 1, p):
                sieve[i] = False
    return [p for p in range(2, n + 1) if sieve[p]]


def run_torsion_simulation(limit=1000000, alpha=0.25):
    """
    alpha: The Torsion Coefficient.
    A higher alpha simulates greater 'geometric bending' at the Bridge.
    """
    primes = get_primes(limit)
    spoke_data = {i: [] for i in [1, 5, 7, 11, 13, 17, 19, 23]}
    for p in primes:
        if p > 3:
            spoke_data[p % 24].append(p)

    densities = {}
    for spoke in spoke_data.keys():
        nodes = spoke_data[spoke]
        avg_spread = np.mean(np.diff(nodes))

        # Base Intensity (Maxel Algebra)
        base_intensity = 1 / np.log(avg_spread)

        # APPLY PRIME TORSION WEIGHT
        # Weight is maximized at Spoke 12 (The Bridge)
        # Weight = 1 + alpha * cos(angular distance to 12)
        angular_dist = (spoke - 12) * (np.pi / 12)
        torsion_weight = 1 + (alpha * np.cos(angular_dist))

        densities[spoke] = base_intensity * torsion_weight

    l1_res = (densities[5] + densities[7]) / 2
    l2_res = (densities[11] + densities[13]) / 2
    ratio = l1_res / l2_res

    return ratio


print(f"{'Torsion (Alpha)':<15} | {'Resonance Ratio':<15} | {'Status'}")
print("-" * 50)

# Scanning alpha values to find the Event Horizon
for a in np.linspace(0, 0.5, 11):
    res_ratio = run_torsion_simulation(1000000, alpha=a)
    diff = abs(res_ratio - 0.6667)
    status = "EVENT HORIZON" if diff < 0.01 else ""
    print(f"{a:<15.2f} | {res_ratio:<15.6f} | {status}")