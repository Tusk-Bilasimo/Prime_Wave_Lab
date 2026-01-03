import numpy as np


def get_primes(n):
    """Efficient Sieve for high limits."""
    sieve = [True] * (n + 1)
    for p in range(2, int(n ** 0.5) + 1):
        if sieve[p]:
            for i in range(p * p, n + 1, p):
                sieve[i] = False
    return [p for p in range(2, n + 1) if sieve[p]]


def scan_event_horizon(max_power=6):
    print(f"{'Limit (10^n)':<15} | {'Ratio (L1/L2)':<15} | {'Deviation from 0.6667'}")
    print("-" * 55)

    for pwr in range(2, max_power + 1):
        limit = 10 ** pwr
        primes = get_primes(limit)

        # Categorize into Mod-24 spokes
        spoke_data = {i: [] for i in [1, 5, 7, 11, 13, 17, 19, 23]}
        for p in primes:
            if p > 3:
                spoke_data[p % 24].append(p)

        densities = {}
        for spoke in spoke_data.keys():
            nodes = spoke_data[spoke]
            if len(nodes) < 2:
                densities[spoke] = 0
                continue

            # Apply Logarithmic Scaling to the Spread (Maxel Algebra)
            # Intensity = 1 / log(Average Spread)
            avg_spread = np.mean(np.diff(nodes))
            log_intensity = 1 / np.log(avg_spread)
            densities[spoke] = log_intensity

        # Calculate Ratio
        l1_avg = (densities[5] + densities[7]) / 2
        l2_avg = (densities[11] + densities[13]) / 2

        # Avoid division by zero
        ratio = l1_avg / l2_avg if l2_avg != 0 else 0
        deviation = abs(ratio - 0.6667)

        print(f"10^{pwr:<12} | {ratio:<15.6f} | {deviation:.6f}")


if __name__ == "__main__":
    scan_event_horizon(6)