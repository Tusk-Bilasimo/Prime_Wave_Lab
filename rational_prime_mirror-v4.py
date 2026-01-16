from fractions import Fraction
import numpy as np
import matplotlib.pyplot as plt

# Prime sequence and exact mirror frequencies
primes = [2, 3, 5, 7]
freq_below = [Fraction(1, p) for p in reversed(primes)]
freq_above = [Fraction(p, 1) for p in primes]
freqs = freq_below + [Fraction(1,1)] + freq_above

N = len(freqs)
print(f"Using {N} rational frequencies symmetric across 1/1:")
for f in freqs: print(f"  {f}")

# Initial state: Gaussian wavepacket centered at 1/1
center = N // 2
sigma = 1.5  # Adjust for spread: smaller = more localized (like hardware pulse)
psi_0 = [np.exp(-0.5 * ((k - center) / sigma)**2) for k in range(N)]
norm = np.sqrt(sum(p**2 for p in psi_0))
psi_0 = [p / norm for p in psi_0]

# Time points: finer over 0-5 for breathing visibility
times = np.linspace(0, 5, 10001)
return_prob = []

for t in times:
    psi_t = [psi_0[k] * np.cos(2 * np.pi * float(freqs[k]) * t) for k in range(N)]
    overlap = sum(psi_0[j] * psi_t[j] for j in range(N))
    return_prob.append(overlap ** 2)

# Print at integers
integer_times = [0, 1, 2, 3, 4, 5]
for it in integer_times:
    idx = int(it / 5 * 10000)
    print(f"Return probability at t={it}: {return_prob[idx]:.6f}")

# Plot
plt.figure(figsize=(12, 6))
plt.plot(times, return_prob, lw=1.2, color='#0066ff')
plt.title("Return Probability with Gaussian Wavepacket (Prime-Mirror Modes)")
plt.xlabel("Time (fundamental periods)")
plt.ylabel("|⟨ψ(0)|ψ(t)⟩|²")
plt.ylim(0, 1.05)
plt.grid(True, alpha=0.3)
plt.show()