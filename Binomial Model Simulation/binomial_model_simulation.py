import math
import matplotlib.pyplot as plt
import numpy as np

# Parameters from the paper
S0 = 1
u = 5/4
y0 = 100
x0 = 100
L = math.sqrt(y0 * x0)

def compute_probabilities(u, r):
    """Compute pi_u and pi_d given u and r."""
    pi_u = (1 + r - 1/u) / (u - 1/u)
    pi_d = 1 - pi_u
    return pi_u, pi_d

def compute_option_premiums(u, d, pi_u, pi_d):
    # Call Option calculations
    call_up_move_payoff = max(u - 1, 0)
    call_down_move_payoff = max(1/u - 1, 0)
    call_present_value = pi_u * call_up_move_payoff + pi_d * call_down_move_payoff

    # Put Option calculations
    put_up_move_payoff = max(1 - u, 0)
    put_down_move_payoff = max(1 - 1/u, 0)
    put_present_value = pi_u * put_up_move_payoff + pi_d * put_down_move_payoff

    # European Straddle Premium
    straddle_premium = call_present_value + put_present_value
    return straddle_premium

# Replicating paper's calculations with r=0
r = 0
pi_u, pi_d = compute_probabilities(u, r)
G0 = compute_option_premiums(u, 1/u, pi_u, pi_d)
VLP_0 = 2 * L * math.sqrt(S0)
Delta = abs(1 - math.sqrt(u)) / (1 + math.sqrt(u))
Delta_G0_r0 = 100*(VLP_0 + Delta * G0 - VLP_0)

# Print key variables
print("For r = 0:")
print(f"Risk-neutral pi_u: {pi_u}")
print(f"Risk-neutral pi_d: {pi_d}")
print(f"Straddle Premium (G0): {G0}")
print(f"VLP(0): {VLP_0}")
print(f"Delta: {Delta}")
print(f"Delta * G0 for r=0: {Delta_G0_r0}")
print("\n")
              # %%

# Compute and plot Delta * G0 as a function of r
interest_rates = np.linspace(0, 0.20, 500)
Delta_G0_values = []

for r in interest_rates:
    pi_u, pi_d = compute_probabilities(u, r)
    G0 = compute_option_premiums(u, 1/u, pi_u, pi_d)
    Delta = abs(1 - math.sqrt(u)) / (1 + math.sqrt(u))
    Delta_G0 = 100*(VLP_0 + Delta * G0 - VLP_0)
    Delta_G0_values.append(Delta_G0)

# Plotting
output_file_path = 'binomial_interest_rate_variation.png'
plt.figure(figsize=(10, 6))
plt.plot(100*interest_rates, Delta_G0_values, label=r'$\Delta G_0$', color='blue')
plt.axvline(x=0, color='red', linestyle='--', label='Paper r value (0)')
plt.xlabel('Risk Free Interest Rate (%)')
plt.ylabel('Returns (%) from Fees needed to Break Even')
plt.title(r'Variation of $\Delta G_0$ with Interest Rate')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig(output_file_path, dpi=300, bbox_inches='tight', format='png')

              # %%

# Additional experimentation with different values of u

u_values = np.linspace(1.01, 2, 100)  # Exploring upward movement factors from 1.01 to 2
Delta_G0_u_values = []

for u in u_values:
    pi_u, pi_d = compute_probabilities(u, 0)  # Using r=0 for this experiment
    G0 = compute_option_premiums(u, 1/u, pi_u, pi_d)
    Delta = abs(1 - math.sqrt(u)) / (1 + math.sqrt(u))
    Delta_G0 = 100*(VLP_0 + Delta * G0 - VLP_0)
    Delta_G0_u_values.append(Delta_G0)

def compute_sigma(u, delta_t=1):
    """Compute sigma given u and Delta t."""
    return 100*math.log(u) / math.sqrt(delta_t) 

u_values = np.linspace(1.01, 2, 100)  # Exploring upward movement factors from 1.01 to 2
sigma_values = [compute_sigma(u) for u in u_values]  # Compute corresponding sigma values
Delta_G0_u_values = []

for u in u_values:
    pi_u, pi_d = compute_probabilities(u, 0)  # Using r=0 for this experiment
    G0 = compute_option_premiums(u, 1/u, pi_u, pi_d)
    Delta = abs(1 - math.sqrt(u)) / (1 + math.sqrt(u))
    Delta_G0 = 100*(VLP_0 + Delta * G0 - VLP_0)
    Delta_G0_u_values.append(Delta_G0)

# Plotting
output_file_path_sigma = 'binomial_sigma_variation.png'
plt.figure(figsize=(10, 6))
plt.plot(sigma_values, Delta_G0_u_values, label=r'$\Delta G_0$ for different $\sigma$', color='green')
plt.axvline(x=compute_sigma(5/4), color='red', linestyle='--', label='Paper $\sigma$ value for u=5/4')
plt.xlabel('Implied Volatility % ($\sigma$)')
plt.ylabel('Returns (%) from Fees needed to Break Even')
plt.title(r'Variation of $\Delta G_0$ with Volatility $\sigma$')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig(output_file_path_sigma, dpi=300, bbox_inches='tight', format='png')


