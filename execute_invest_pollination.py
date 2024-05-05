import pandas as pd
import logging
import sys
import os
import shutil

import natcap.invest.pollination
import natcap.invest.utils

LOGGER = logging.getLogger(__name__)
root_logger = logging.getLogger()

handler = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter(
    fmt=natcap.invest.utils.LOG_FMT,
    datefmt='%m/%d/%Y %H:%M:%S ')
handler.setFormatter(formatter)
logging.basicConfig(level=logging.INFO, handlers=[handler])

# Function to change the value in guild_table.csv
def change_value_in_csv(csv_file_path):
    # Read CSV file
    df = pd.read_csv(csv_file_path)

    # Loop to change the value in cell G2 from 0.1 to 1, step = 0.1
    for i in range(10):
        value = 100 * (i + 1)
        df.at[0, 'alpha'] = value
        df.at[1, 'alpha'] = value
        df.at[2, 'alpha'] = value
        df.at[3, 'alpha'] = value

        # Write back to the CSV file
        output_folder = os.path.join(os.path.dirname(csv_file_path), 'output_' + str(i+1))
        os.makedirs(output_folder, exist_ok=True)
        output_file_path = os.path.join(output_folder, os.path.basename(csv_file_path))
        df.to_csv(output_file_path, index=False)

        # Print confirmation
        print(f"Changed value in relative_abundance to {value} in {output_file_path}")

        # Execute the model with the updated CSV file
        args['guild_table_path'] = output_file_path
        args['workspace_dir'] = output_folder
        natcap.invest.pollination.execute(args)

# Initial arguments
args = {
    'farm_vector_path': '',
    'guild_table_path': 'C:\\Users\\jsnjz\\files\\base_data\\invest_sample_data\\pollination\\guild_table.csv',
    'landcover_biophysical_table_path': 'C:\\Users\\jsnjz\\files\\base_data\\invest_sample_data\\pollination\\landcover_biophysical_table.csv',
    'landcover_raster_path': 'C:\\Users\\jsnjz\\files\\base_data\\invest_sample_data\\pollination\\landcover.tif',
    'results_suffix': '',
    'workspace_dir': 'C:\\Users\\jsnjz\\files\\base_data\\invest_sample_data\\pollination\\output2',
}

if __name__ == '__main__':
    change_value_in_csv(args['guild_table_path'])

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
for i in range(1, 11):
    input_file = os.path.join(f"C:\\Users\\jsnjz\\files\\base_data\\invest_sample_data\\pollination\\output_{i}", "total_pollinator_abundance_spring.tif")
    output_file = os.path.join(output_folder, f"total_pollinator_abundance_spring_{i}.tif")
    shutil.copy(input_file, output_file)

print("Files copied successfully.")

