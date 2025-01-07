#!/usr/bin/env python
# coding: utf-8

# In[3]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

"""
Created on Tuesday November 21 21:43 2023

@author: aras
"""
#--------------------------------------Plotting the peaks with Raw Datas-----------------#

# List of file names
file_names = ['Kr_PES_0.txt', 'Kr_PES_1.txt', 'Kr_PES_2.txt', 'Kr_PES_3.txt', 'Kr_PES_4.txt']

# Plotting all data on one scatter plot with different colors
plt.figure(figsize=(10, 6))

for i, file_name in enumerate(file_names):
    # Load the data from the current file
    data = np.genfromtxt(file_name, delimiter='')  # Modify the delimiter as needed
    
    # Extract the columns
    x_data = data[:, 0]  # The first column
    y_data = data[:, 1]  # The second column
    
    # Plot the data with a unique color for each file
    plt.scatter(x_data, y_data, label=f'Data from {file_name}', alpha=0.7)

# Adding labels and title
plt.xlabel('Kinetic Energies of photoelectrons')
plt.ylabel('Intensity (arbitrary units)')
plt.title('Scatter Plot of Data from Multiple Files')
plt.legend()
plt.grid(True)

# Show the plot
plt.show()
plt.savefig('Scatter Plot of Data from Multiple Files.png')
#------------------------------------------------------------------------------------------------#

#the datas in the following are extracted using the GaussianParameterFinder.py
#------Creating the dataframes-----

# Data for Kr_PES_1
data_kr_pes_1 = {
    'Peak': [1, 2, 3, 4, 5, 6],
    'A': [9834.40, 10645.77, 15391.52, 18422.65, 16721.35, 16594.20],
    'Mean': [16.51, 17.18, 19.92, 20.31, 23.28, 23.39],
    'Std_err_to_Mean': [0.0174, 0.0145, 0.0810, 0.0195, 0.2002, 0.0279],
    'Sigma': [0.49, 0.40, 0.70, 0.40, 0.88, 0.47],
    'FWHM': [1.14, 0.93, 1.64, 0.95, 2.08, 1.11],
    'Resolution': [0.07, 0.05, 0.08, 0.05, 0.09, 0.05]
}

df_kr_pes_1 = pd.DataFrame(data_kr_pes_1)

# Data for Kr_PES_2
data_kr_pes_2 = {
    'Peak': [1, 2, 3, 4, 5, 6],
    'A': [9887.85, 9955.11, 15494.68, 18468.20, 15071.33, 17189.09],
    'Mean': [16.99, 17.19, 19.97, 20.35, 22.98, 23.42],
    'Std_err_to_Mean': [0.4973, 0.0309, 0.1676, 0.0188, 0.0836, 0.0310],
    'Sigma': [1.18, 0.52, 0.78, 0.39, 0.65, 0.44],
    'FWHM': [2.78, 1.23, 1.84, 0.92, 1.53, 1.05],
    'Resolution': [0.16, 0.07, 0.09, 0.05, 0.07, 0.04]
}

df_kr_pes_2 = pd.DataFrame(data_kr_pes_2)

# Data for Kr_PES_3
data_kr_pes_3 = {
    'Peak': [1, 2, 3, 4, 5, 6],
    'A': [6254.84, 7592.78, 14849.80, 18598.59, 16412.07, 14510.88],
    'Mean': [16.68, 17.23, 19.82, 20.37, 23.75, 23.44],
    'Std_err_to_Mean': [0.0382, 0.0290, 0.0215, 0.0163, 0.7866, 0.0380],
    'Sigma': [0.36, 0.37, 0.50, 0.37, 1.29, 0.54],
    'FWHM': [0.84, 0.86, 1.18, 0.87, 3.04, 1.26],
    'Resolution': [0.05, 0.05, 0.06, 0.04, 0.13, 0.05]
}

df_kr_pes_3 = pd.DataFrame(data_kr_pes_3)

# Data for Kr_PES_4
data_kr_pes_4 = {
    'Peak': [1, 2, 3, 4, 5, 6],
    'A': [19554.04, 24786.81, 51447.42, 66606.89, 52703.98, 58481.97],
    'Mean': [16.60, 17.18, 19.83, 20.33, 23.05, 23.41],
    'Std_err_to_Mean': [0.0079, 0.0141, 0.0291, 0.0143, 0.0858, 0.0285],
    'Sigma': [0.32, 0.29, 0.52, 0.36, 0.71, 0.46],
    'FWHM': [0.75, 0.68, 1.22, 0.85, 1.67, 1.09],
    'Resolution': [0.05, 0.04, 0.06, 0.04, 0.07, 0.05]
}

df_kr_pes_4 = pd.DataFrame(data_kr_pes_4)

# Concatenate the DataFrames along columns
df_kr_pes = pd.concat([df_kr_pes_1, df_kr_pes_2, df_kr_pes_3, df_kr_pes_4], axis=1, keys=['kr_pes_1', 'kr_pes_2', 'kr_pes_3', 'kr_pes_4'])

# If you want to remove the duplicate 'Peak' columns from the second and subsequent DataFrames
df_kr_pes = df_kr_pes.loc[:,~df_kr_pes.columns.duplicated()]

# Display the resulting DataFrame
print(df_kr_pes)


#-------Plot of Means with respect to Peaks-------

# Extracting the relevant data from the DataFrame
peaks = df_kr_pes['kr_pes_1']['Peak']  # Assuming 'Peak' is the common column in all source DataFrames
means_1 = df_kr_pes['kr_pes_1']['Mean']
means_2 = df_kr_pes['kr_pes_2']['Mean']
means_3 = df_kr_pes['kr_pes_3']['Mean']
means_4 = df_kr_pes['kr_pes_4']['Mean']
std_err_1 = df_kr_pes['kr_pes_1']['Std_err_to_Mean']
std_err_2 = df_kr_pes['kr_pes_2']['Std_err_to_Mean']
std_err_3 = df_kr_pes['kr_pes_3']['Std_err_to_Mean']
std_err_4 = df_kr_pes['kr_pes_4']['Std_err_to_Mean']

# Calculating the 95% confidence interval
lower_bound_1 = means_1 - (1.96 * std_err_1)
upper_bound_1 = means_1 + (1.96 * std_err_1)
lower_bound_2 = means_2 - (1.96 * std_err_2)
upper_bound_2 = means_2 + (1.96 * std_err_2)
lower_bound_3 = means_3 - (1.96 * std_err_3)
upper_bound_3 = means_3 + (1.96 * std_err_3)
lower_bound_4 = means_4 - (1.96 * std_err_4)
upper_bound_4 = means_4 + (1.96 * std_err_4)

# Plotting the scatter plot
plt.figure(figsize=(10, 6))
plt.scatter(peaks, means_1, label='kr_pes_1')
plt.scatter(peaks, means_2, label='kr_pes_2')
plt.scatter(peaks, means_3, label='kr_pes_3')
plt.scatter(peaks, means_4, label='kr_pes_4')

# Plotting the 95% confidence interval
plt.errorbar(peaks, means_1, yerr=std_err_1 * 1.96, fmt='none', color='black', capsize=5, label='95% CI kr_pes_1')
plt.errorbar(peaks, means_2, yerr=std_err_2 * 1.96, fmt='none', color='red', capsize=5, label='95% CI kr_pes_2')
plt.errorbar(peaks, means_3, yerr=std_err_3 * 1.96, fmt='none', color='blue', capsize=5, label='95% CI kr_pes_3')
plt.errorbar(peaks, means_4, yerr=std_err_4 * 1.96, fmt='none', color='green', capsize=5, label='95% CI kr_pes_4')

# Adding labels and title
plt.xlabel('Peak')
plt.ylabel('Mean')
plt.title('Scatter Plot of Means by Peaks with 95% Confidence Interval')
plt.legend()
plt.grid(True)

# Show the plot
plt.show()
plt.savefig('Scatter Plot of Means by Peaks with 95% Confidence Interval',format='png')

#-------Plot of Resolutions with respect to Peaks------

# Extracting the relevant data from the DataFrame
resolutions_1 = df_kr_pes['kr_pes_1']['Resolution']
resolutions_2 = df_kr_pes['kr_pes_2']['Resolution']
resolutions_3 = df_kr_pes['kr_pes_3']['Resolution']
resolutions_4 = df_kr_pes['kr_pes_4']['Resolution']
std_err_to_mean_1 = df_kr_pes['kr_pes_1']['Std_err_to_Mean']
std_err_to_mean_2 = df_kr_pes['kr_pes_2']['Std_err_to_Mean']
std_err_to_mean_3 = df_kr_pes['kr_pes_3']['Std_err_to_Mean']
std_err_to_mean_4 = df_kr_pes['kr_pes_4']['Std_err_to_Mean']

# Calculating the 95% confidence interval for resolutions using Std_err_to_Mean from the Gaussian fit
lower_bound_res_1 = resolutions_1 - (1.96 * std_err_to_mean_1)
upper_bound_res_1 = resolutions_1 + (1.96 * std_err_to_mean_1)
lower_bound_res_2 = resolutions_2 - (1.96 * std_err_to_mean_2)
upper_bound_res_2 = resolutions_2 + (1.96 * std_err_to_mean_2)
lower_bound_res_3 = resolutions_3 - (1.96 * std_err_to_mean_3)
upper_bound_res_3 = resolutions_3 + (1.96 * std_err_to_mean_3)
lower_bound_res_4 = resolutions_4 - (1.96 * std_err_to_mean_4)
upper_bound_res_4 = resolutions_4 + (1.96 * std_err_to_mean_4)

# Plotting the scatter plot
plt.figure(figsize=(10, 6))
plt.scatter(peaks, resolutions_1, label='kr_pes_1')
plt.errorbar(peaks, resolutions_1, yerr=std_err_to_mean_1 * 1.96, fmt='none', color='black', capsize=5, label='95% CI kr_pes_1')
plt.scatter(peaks, resolutions_2, label='kr_pes_2')
plt.errorbar(peaks, resolutions_2, yerr=std_err_to_mean_2 * 1.96, fmt='none', color='red', capsize=5, label='95% CI kr_pes_2')
plt.scatter(peaks, resolutions_3, label='kr_pes_3')
plt.errorbar(peaks, resolutions_3, yerr=std_err_to_mean_3 * 1.96, fmt='none', color='blue', capsize=5, label='95% CI kr_pes_3')
plt.scatter(peaks, resolutions_4, label='kr_pes_4')
plt.errorbar(peaks, resolutions_4, yerr=std_err_to_mean_4 * 1.96, fmt='none', color='green', capsize=5, label='95% CI kr_pes_4')
# Plotting the 95% confidence interval for resolutions
#plt.errorbar(peaks, resolutions_1, yerr=std_err_to_mean_1 * 1.96, fmt='none', color='black', capsize=5, label='95% CI kr_pes_1')
#plt.errorbar(peaks, resolutions_2, yerr=std_err_to_mean_2 * 1.96, fmt='none', color='red', capsize=5, label='95% CI kr_pes_2')
#plt.errorbar(peaks, resolutions_3, yerr=std_err_to_mean_3 * 1.96, fmt='none', color='blue', capsize=5, label='95% CI kr_pes_3')
#plt.errorbar(peaks, resolutions_4, yerr=std_err_to_mean_4 * 1.96, fmt='none', color='green', capsize=5, label='95% CI kr_pes_4')

# Adding labels and title
plt.xlabel('Peak number')
plt.ylabel('Resolution')
plt.title('Scatter Plot of Resolutions by Peaks with 95% Confidence Interval (Using Std_err_to_Mean)')
plt.legend()
plt.grid(True)

# Show the plot
plt.show()
plt.savefig('Scatter Plot of Resolutions by Peaks with 95% Confidence Interval (Using Std_err_to_Mean).png')

# In[ ]:




