import pandas as pd
import logging
import sys
import os
import shutil

import natcap.invest.pollination
import natcap.invest.utils

# Define paths
input_folder = r"C:\Users\jsnjz\files\base_data\invest_sample_data\pollination\output_i"
output_folder = r"C:\Users\jsnjz\files\base_data\invest_sample_data\pollination\result"

# Create the output folder if it doesn't exist
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Iterate over the input folder and move files to the output folder
for i in range(1, 4):
    input_file = os.path.join(f"C:\\Users\\jsnjz\\files\\base_data\\invest_sample_data\\pollination\\output_{i}", "total_pollinator_abundance_spring.tif")
    output_file = os.path.join(output_folder, f"total_pollinator_abundance_spring_{i}.tif")
    shutil.copy(input_file, output_file)

print("Files copied successfully.")
