# Definitions and imports
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize

# Define the parameters based on the given Black-Scholes model
mu = np.log(5/4)
sigma_values = np.linspace(0.01, 1.5, 100)
S0 = 1
x0 = 100
y0 = 100
T = 1
num_simulations = 1000000

# Function to calculate impermanent loss for a given ST
def impermanent_loss(ST, S0):
    return x0 * (np.sqrt(ST) - np.sqrt(S0))**2

# Function to calculate hedged loss using gamma swaps for a given ST
def gamma_swap_hedged_loss(ST, S0):
    return x0 * 0.5 * (ST * np.log(ST/S0) - (ST - S0))

# Function to calculate hedged loss using variance swaps for a given ST
def variance_swap_hedged_loss(ST, S0):
    return x0 * (-0.5 * S0 * np.log(ST/S0) + 0.5 * (ST - S0))

# Function to calculate hedged loss using a weighted average of gamma and variance swaps for a given ST
def weighted_hedged_loss(ST, S0, w=0.6):
    return w * variance_swap_hedged_loss(ST, S0) + (1 - w) * gamma_swap_hedged_loss(ST, S0)

# Define the error function for optimization of w
def error_func(w, STs):
    weighted_loss = weighted_hedged_loss(STs, S0, w)
    imp_loss = impermanent_loss(STs, S0)
    mse = np.mean((weighted_loss - imp_loss)**2)
    return mse

# Containers to hold the average losses for each sigma value
avg_impermanent_losses = []
avg_gamma_hedged_losses = []
avg_variance_hedged_losses = []
avg_weighted_hedged_losses = []
optimal_ws = []

# Simulate paths for each volatility and calculate the average losses
for sigma in sigma_values:
    STs = np.exp(mu + sigma * np.random.randn(num_simulations))
    
    # Calculate average impermanent losses
    avg_impermanent_losses.append(np.mean(impermanent_loss(STs, S0)))
    
    # Calculate average hedged losses using gamma swaps
    avg_gamma_hedged_losses.append(np.mean(gamma_swap_hedged_loss(STs, S0)))
    
    # Calculate average hedged losses using variance swaps
    avg_variance_hedged_losses.append(np.mean(variance_swap_hedged_loss(STs, S0)))
    
    # Optimize for w
    optimal_w = minimize(error_func, 0.5, args=(STs,), bounds=[(0, 1)]).x[0]
    optimal_ws.append(optimal_w)
    
    # Calculate average hedged losses using the optimal w for weighted hedging
    avg_weighted_hedged_losses.append(np.mean(weighted_hedged_loss(STs, S0, optimal_w)))


              # %%

# Plotting the results
# Saving the first plot: Impermanent Loss vs. Hedged Loss across Volatility

plt.figure(figsize=(12, 7))
plt.plot(100*sigma_values, avg_impermanent_losses, label='Impermanent Loss', color='blue')
plt.plot(100*sigma_values, avg_gamma_hedged_losses, '--', label='Gamma Swap Hedged Loss', color='green')
plt.plot(100*sigma_values, avg_variance_hedged_losses, '-.', label='Variance Swap Hedged Loss', color='red')
plt.plot(100*sigma_values, avg_weighted_hedged_losses, ':', label='Weighted Hedged Loss', color='purple')
plt.title('Impermanent Loss vs. Hedged Loss across Volatility')
plt.xlabel('Volatility (%) (σ)')
plt.ylabel('Loss (%) ')
plt.legend()
plt.grid(True)
plt.xlim(0, 110)
plt.ylim(0, 100)
plt.savefig('hedge.png', dpi=300, bbox_inches='tight', format='png')
plt.show()
plt.close()
              # %%

# Calculate the unhedged amounts
unhedged_gamma = [abs(imp_loss - gamma_hedged_loss) for imp_loss, gamma_hedged_loss in zip(avg_impermanent_losses, avg_gamma_hedged_losses)]
unhedged_variance = [abs(imp_loss - variance_hedged_loss) for imp_loss, variance_hedged_loss in zip(avg_impermanent_losses, avg_variance_hedged_losses)]
unhedged_weighted = [abs(imp_loss - weighted_hedged_loss) for imp_loss, weighted_hedged_loss in zip(avg_impermanent_losses, avg_weighted_hedged_losses)]

# Plotting the unhedged amounts
plt.figure(figsize=(12, 7))
plt.plot(100*sigma_values, unhedged_gamma, label='Unhedged Amount (Gamma Swap)', color='green')
plt.plot(100*sigma_values, unhedged_variance, '--', label='Unhedged Amount (Variance Swap)', color='red')
plt.plot(100*sigma_values, unhedged_weighted, '-.', label='Unhedged Amount (Weighted Variance Swap)', color='purple')
plt.title('Unhedged Amounts using Different Hedging Strategies')
plt.xlabel('Volatility (%) (σ)')
plt.ylabel('Unhedged Amount (%) ')
plt.legend()
plt.grid(True)
plt.xlim(0, 100)  # Adjusted the x-limit for better visualization
plt.ylim(0, 20)
plt.savefig('unhedged.png', dpi=300, bbox_inches='tight', format='png')
plt.show()
plt.close()

