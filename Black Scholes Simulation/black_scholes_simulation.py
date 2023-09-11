import math
import numpy as np
import matplotlib.pyplot as plt

# Initial parameters
x0 = 100
y0 = 100
S0 = 1
T = 1
u = 5/4
sigma = math.log(u)
L = math.sqrt(x0 * y0)

def calculate_hedge_BS(T, sigma):
    """
    Compute the liquidity provision for the Black-Scholes model.
    """
    return 2 * y0 * (1 - math.exp(-sigma**2 * T / 8))

def BS_hedge_for_varying_volatilities(sigma_values):
    """
    Compute the liquidity provision for a range of volatilities.
    """
    return [calculate_hedge_BS(T, sigma) for sigma in sigma_values]

# Numerical example for the paper's given values
BS_hedge_value = calculate_hedge_BS(T, sigma)

# Experiment with different volatilities
sigma_values = np.linspace(0, 0.7, 500)
hedge_values = BS_hedge_for_varying_volatilities(sigma_values)
              # %%

# Plotting
output_file_path_sigma = 'black_scholes.png'
plt.figure(figsize=(10, 6))
plt.plot(100*sigma_values, hedge_values, label='Liquidity Provision in BS model', color='blue')
plt.axvline(x=100*sigma, color='red', linestyle='--', label=f'Paper Sigma Value ({sigma:.4f})')
plt.xlabel('Volatility (Sigma)')
plt.ylabel('Returns (%) from Fees needed to Break Even')
plt.title('Variation of Liquidity Provision with Volatility in Black-Scholes model')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig('volatility_variation_BS.png', dpi=300, bbox_inches='tight', format='png')
plt.show()

print(f"Black-Scholes dynamic hedging result for paper's sigma: {BS_hedge_value:.5f}")
              # %%
