# -*- coding: utf-8 -*-
"""
Created on Wed Oct 25 17:53:20 2023

@author: aras
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

# Load the data from a text file

data = np.genfromtxt('Kr_PES_0.txt', delimiter='')  # Modify the delimiter as needed

# Extract the columns
x_data = data[:, 0]  # The first column
y_data = data[:, 1]  # The second column

# Define the Gaussian function
def gaussian(x, A, mean, sigma):
    return (A * np.exp(-((x - mean) ** 2) / (2 * sigma ** 2)))

# Ask the user for the x-value interval for fitting
x_min = float(input("Enter the lower bound of the x-value interval for fitting: "))
x_max = float(input("Enter the upper bound of the x-value interval for fitting: "))

# Filter data within the specified x-value interval
mask = (x_data >= x_min) & (x_data <= x_max)
x_fit = x_data[mask]
y_fit = y_data[mask]

# Perform the Gaussian fit
initial_guess = [max(y_fit), np.mean(x_fit), np.std(x_fit)]
params, params_covariance = curve_fit(gaussian, x_fit, y_fit, p0=initial_guess)

# Plot the original data
plt.figure(figsize=(8, 6))
plt.plot(x_data, y_data, marker='o', linestyle='-', color='blue', label='Original Data')

# Plot the fitted Gaussian
x_fit_range = np.linspace(x_min, x_max, 1000)
y_fit_curve = gaussian(x_fit_range, *params)
plt.plot(x_fit_range, y_fit_curve, 'r', label='Gaussian Fit')

# Display the parameters of the Gaussian fit
A, mean, sigma = params
fwhm = 2 * np.sqrt(2 * np.log(2)) * sigma
R = fwhm/mean
# Extract the standard error for the mean
mean_std_error = np.sqrt(params_covariance[1, 1])

params_str = f'A = {A:.2f}, Mean = {mean:.2f}, Std_err_to_Mean = {mean_std_error:.4f}, Sigma = {sigma:.2f}, FWHM = {fwhm:.2f}, Resolution = {R:.2f}'

print(params_str)  # Display the parameters in the command prompt

# Customize plot
plt.xlabel('Kinetic Energy of the Photoelectrons [eV]')
plt.ylabel('Intensity [arbitrary units] ')
plt.title('Data and Gaussian Fit')
plt.grid(True)
plt.legend()
# Show the plot
plt.show()