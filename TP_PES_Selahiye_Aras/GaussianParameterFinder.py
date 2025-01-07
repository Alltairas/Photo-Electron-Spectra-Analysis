# -*- coding: utf-8 -*-
"""
Created on Thu Oct 26 00:08:44 2023
@author: aras
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

# Define the Gaussian function
def gaussian(x, A, mean, sigma):
    return A *( np.exp(-((x - mean) ** 2) / (2 * sigma ** 2)))

# Read interval values from the text file
intervals = []
with open('fitting_intervals.txt', 'r') as file:
    for line in file:
        min_val, max_val = map(float, line.strip().split(', '))
        intervals.append((min_val, max_val))

# Iterate over the file names Kr_PES_0.txt through Kr_PES_4.txt
for file_number in range(5):
    file_name = f'Kr_PES_{file_number}.txt'  # Generate the file name

    # Load the data from the current file
    data = np.genfromtxt(file_name, delimiter='')  # Modify the delimiter as needed

    # Extract the columns
    x_data = data[:, 0]  # The first column
    y_data = data[:, 1]  # The second column

    # Initialize a list to store parameters for all peaks
    all_params = []

    for peak_number in range(6):
        print(f"Fitting Peak {peak_number + 1}")
        min_val, max_val = intervals[peak_number]  # Get the min and max values for the current peak

        # Filter data within the specified x-value interval
        mask = (x_data >= min_val) & (x_data <= max_val)
        x_fit = x_data[mask]
        y_fit = y_data[mask]

        # Perform the Gaussian fit
        initial_guess = [max(y_fit), np.mean(x_fit), np.std(x_fit)]
        params, params_covariance = curve_fit(gaussian, x_fit, y_fit, p0=initial_guess)

        # Extract the standard error for the mean
        mean_std_error = np.sqrt(params_covariance[1, 1])

        A, mean, sigma = params
        fwhm = 2 * np.sqrt(2 * np.log(2)) * sigma
        R = fwhm / mean

        # Store parameters for this peak
        all_params.append((A, mean, mean_std_error, sigma, fwhm, R))

        # Print the parameters for this peak
        params_str = f'A = {A:.2f}, Mean = {mean:.2f}, Std_err_to_Mean = {mean_std_error:.4f}, Sigma = {sigma:.2f}, FWHM = {fwhm:.2f}, Resolution = {R:.2f}'
        print(params_str)

    # Save the parameters to a text file for the current data file
    with open(f'parameters_Kr_PES_{file_number}.txt', 'w') as file:
        for i, params in enumerate(all_params):
            A, mean, mean_std_error, sigma, fwhm, R = params
            line = f'Peak {i + 1}: A = {A:.2f}, Mean = {mean:.2f}, Std_err_to_Mean = {mean_std_error:.4f}, Sigma = {sigma:.2f}, FWHM = {fwhm:.2f}, Resolution = {R:.2f}\n'
            file.write(line)

    print(f"Parameter values for {file_name} saved to parameters_Kr_PES_{file_number}.txt")