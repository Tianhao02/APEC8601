import numpy as np
from scipy.optimize import minimize

# Parameters
n = 10  # Number of periods
delta = 0.95  # Discount factor
p = 0.3  # Probability p
lambda_ = 0.1  # Parameter lambda
tildeP = 0.2  # Tilde p
T = 100  # Parameter T
L = 100  # Total labor available
eta = 0.9  # Parameter eta
r = 0.05  # Return rate
alpha = 0.5  # Example value for alpha
M = 50  # Example value for M
A = 1  # Example value for A

# Cost function c(Lpt)
def c(Lpt):
    return 10 + 0.5 * Lpt

# Production function f(Lat, M)
def f(Lat, M):
    return 20 * Lat + 0.1 * M

# Beta function (as a function of Lpt)
def beta(Lpt):
    return 0.2 + 0.01 * Lpt

# Phi_t function definition
def phi(t, Lpts):
    product_part = np.prod([alpha + beta(Lpts[i]) for i in range(t)])
    sum_part = 0
    for k in range(1, t + 1):
        inner_sum = sum([np.prod([1 / (alpha + beta(Lpts[i])) for i in range(j)]) for j in range(k)])
        sum_part += (p * tildeP) ** (t - k) * (1 - p * tildeP) ** k * inner_sum
    return eta ** (t - 1) * product_part * r * A * ((p * tildeP) ** t + sum_part)

# Define the total income Y_s=AC
def total_income(vars):
    Lat = vars[:n]
    Lpt = vars[n:]
    return -sum([delta ** (t - 1) * ((1 - p + lambda_) * f(Lat[t], M) + phi(t, Lpt) + tildeP * (T - c(Lpt[t]))) for t in range(n)])

# Constraints
def constraints(vars):
    Lat = vars[:n]
    Lpt = vars[n:]
    return [L - (Lat[t] + Lpt[t]) for t in range(n)]

# Bounds for the variables
bounds = [(0, L)] * (2 * n)

# Initial values for Lat and Lpt
initial_values = [L / 2] * (2 * n)

# Optimization
constraints = [{'type': 'ineq', 'fun': lambda vars: con} for con in constraints(initial_values)]
solution = minimize(total_income, initial_values, bounds=bounds, constraints=constraints, method='SLSQP')

# Extract the optimal values of Lat and Lpt
optimal_vars = solution.x
optimal_Lat = optimal_vars[:n]
optimal_Lpt = optimal_vars[n:]

# Calculate total income, yearly income, labor income, and capital income
total_income_value = -total_income(optimal_vars)
yearly_income = [delta ** (t - 1) * ((1 - p + lambda_) * f(optimal_Lat[t], M) + phi(t, optimal_Lpt) + tildeP * (T - c(optimal_Lpt[t]))) for t in range(n)]
labor_income = [(1 - p + lambda_) * f(optimal_Lat[t], M) for t in range(n)]
capital_income = [phi(t, optimal_Lpt) for t in range(n)]

# Results
results = {
    "total_income": total_income_value,
    "yearly_income": yearly_income,
    "labor_income": labor_income,
    "capital_income": capital_income
}

results
