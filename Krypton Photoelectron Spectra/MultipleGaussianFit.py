import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from scipy.signal import find_peaks

# Load the data from a text file
data = np.genfromtxt('Kr_PES_2.txt')  # No delimiter needed if it's space-separated

# Extract the columns
x_data = data[:, 0]  # The first column
y_data = data[:, 1]  # The second column

# Define the multiple Gaussian function
def multiple_gaussian(x, *params):
    num_peaks = len(params) // 3
    result = np.zeros_like(x)
    for i in range(num_peaks):
        A = params[i * 3]
        mean = params[i * 3 + 1]
        sigma = params[i * 3 + 2]
        result += A * np.exp(-((x - mean) ** 2) / (2 * sigma ** 2))
    return result

# Ask the user for the x-value intervals for fitting each peak
num_peaks = 6
x_min_values = []
x_max_values = []

for i in range(num_peaks):
    x_min = float(input(f"Enter the lower bound of the x-value interval for peak {i + 1}: "))
    x_max = float(input(f"Enter the upper bound of the x-value interval for peak {i + 1}: "))
    x_min_values.append(x_min)
    x_max_values.append(x_max)

# Create masks for each x-value interval and calculate initial guesses
masks = []
initial_guess = []
for i in range(num_peaks):
    mask = (x_data >= x_min_values[i]) & (x_data <= x_max_values[i])
    masks.append(mask)
    if np.any(mask):
        initial_guess += [max(y_data[mask]), np.mean(x_data[mask]), np.std(x_data[mask])]
    else:
        # If the interval is empty, provide reasonable initial guesses
        initial_guess += [0.0, x_min_values[i] + (x_max_values[i] - x_min_values[i]) / 2, 1.0]

# Perform the multiple Gaussian fit
params, params_covariance = curve_fit(multiple_gaussian, x_data, y_data, p0=initial_guess, maxfev=10000)

# Plot the original data
plt.figure(figsize=(8, 6))
plt.plot(x_data, y_data, marker='o', linestyle='-', color='blue', label='Original Data')

# Plot the multiple Gaussian fit
x_fit_range = np.linspace(min(x_data), max(x_data), 1000)
y_fit_curve = multiple_gaussian(x_fit_range, *params)
plt.plot(x_fit_range, y_fit_curve, 'r', label='Multiple Gaussian Fit')

# Customize plot
plt.xlabel('X-axis Label')
plt.ylabel('Y-axis Label')
plt.title('Data and Multiple Gaussian Fit')
plt.grid(True)
plt.legend()

# Show the plot
plt.show()

# Display the parameters of the multiple Gaussian fit after plotting
params_str = ""
for i in range(num_peaks):
    A, mean, sigma = params[i * 3], params[i * 3 + 1], params[i * 3 + 2]
    fwhm = 2 * np.sqrt(2 * np.log(2)) * sigma
    params_str += f'Peak {i + 1}: A = {A:.2f}, Mean = {mean:.2f}, Sigma = {sigma:.2f}, FWHM = {fwhm:.2f}\n'

print(params_str)

# Save the parameters to a text file
with open('parameters.txt', 'w') as file:
    file.write(params_str)
