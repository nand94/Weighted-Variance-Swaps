import math
import numpy as np
import matplotlib.pyplot as plt

# Parameters from the paper
S0 = 1
y0 = 100
x0 = 100
L = math.sqrt(y0 * x0)
T = 1  # As given in the paper
num_simulations = 1000000  # Number of Monte Carlo simulations

def compute_sigma(u, delta_t=1):
    """Compute sigma given u and Delta t."""
    return math.log(u) / math.sqrt(delta_t)

def monte_carlo_simulation(r, sigma, num_simulations, T, S0):
    """Simulate ST using Geometric Brownian Motion and compute expected H(T)"""
    dt = T
    # Generate standard normally distributed random numbers
    Z = np.random.standard_normal(num_simulations)
    
    # Simulate ST using GBM formula
    ST = S0 * np.exp((r - 0.5 * sigma**2) * dt + sigma * math.sqrt(dt) * Z)
    
    # Calculate the payoff for each simulation
    payoff = (np.sqrt(ST) - np.sqrt(S0))**2
    
    # Calculate the expected payoff, discounted to present value
    H0 = 100*np.exp(-r * T) * np.mean(payoff)
    
    return H0

# Replicating paper's results
u = 5/4
sigma_estimated = compute_sigma(u)
H0_estimated = monte_carlo_simulation(0, sigma_estimated, num_simulations, T, S0)

print(f"Estimated sigma: {sigma_estimated:.4f}")
print(f"Estimated H0: {H0_estimated:.4f}")
print("\n")
              # %%


# Experimenting with different values of r and sigma
r_values = np.linspace(0, 0.20, 21)
sigma_values = np.linspace(0, 0.7, 71)

# Store results for plots
H0_vs_r = []
H0_vs_sigma = []

for r in r_values:
    H0 = monte_carlo_simulation(r, sigma_estimated, num_simulations, T, S0)
    H0_vs_r.append(H0)

for sigma in sigma_values:
    H0 = monte_carlo_simulation(0, sigma, num_simulations, T, S0)
    H0_vs_sigma.append(H0)

# Plotting H0 against r
output_file_path = 'cont_interest_rate_variation.png'
plt.figure(figsize=(10, 6))
plt.plot(100*r_values, H0_vs_r, label='H0 vs. r', color='blue')
plt.axvline(x=0, color='red', linestyle='--', label='Paper r value (0)')
plt.xlabel('Risk Free Interest Rate (%)')
plt.ylabel('Returns (%) from Fees needed to Break Even')
plt.title('H0 against Interest Rate r')
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.savefig("H0_vs_r.png", dpi=300, bbox_inches='tight')
plt.show()

# Plotting H0 against sigma
output_file_path = 'cont_sigma_variation.png'
plt.figure(figsize=(10, 6))
plt.plot(100*sigma_values, H0_vs_sigma, label='H0 for different $\sigma$', color='green')
plt.axvline(x=100*sigma_estimated, color='red', linestyle='--', label=f'Paper sigma value ({sigma_estimated:.4f})')
plt.xlabel('Implied Volatility % ($\sigma$)')
plt.ylabel('Returns (%) from Fees needed to Break Even')
plt.title('H0 against Volatility sigma')
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.savefig("H0_vs_sigma.png", dpi=300, bbox_inches='tight')
plt.show()
