import rasterio
from rasterio.warp import calculate_default_transform, reproject, Resampling
import numpy as np
import os

# Path to the input directory
input_dir = r"C:\Users\jsnjz\Files\base_data\invest_sample_data\Annual_Water_Yield\input"

# Function to multiply and transform a file
def process_file(base_file, other_file, output_file):
    # Load the base file
    with rasterio.open(base_file) as src:
        base_data = src.read(1)
        base_meta = src.meta

    # Load the other file
    with rasterio.open(other_file) as src:
        other_data = src.read(1)
        meta = src.meta

        # Multiply the data with the base data
        multiplied_data = base_data * other_data

        # Transform the projection system from EPSG 4326 to EPSG 54030
        transform, width, height = calculate_default_transform(
            src.crs, "EPSG:54030", src.width, src.height, *src.bounds
        )
        meta.update({"crs": "EPSG:54030", "transform": transform, "width": width, "height": height})

        # Reproject the multiplied data
        transformed_data = np.zeros((height, width), dtype=np.float32)
        reproject(
            source=multiplied_data,
            destination=transformed_data,
            src_transform=src.transform,
            src_crs=src.crs,
            dst_transform=transform,
            dst_crs="EPSG:54030",
            resampling=Resampling.nearest
        )

        # Save the transformed data with "_c" suffix
        output_path = os.path.join(input_dir, output_file)
        with rasterio.open(output_path, "w", **meta) as dst:
            dst.write(transformed_data, 1)

# Base file path
base_file = os.path.join(input_dir, "country.tif")

# Process each file individually
process_file(base_file, os.path.join(input_dir, "Average Annual Reference Evapotranspiration.tif"),
             "Average Annual Reference Evapotranspiration_c.tif")
process_file(base_file, os.path.join(input_dir, "Plant Available Water Content.tif"),
             "Plant Available Water Content_c.tif")
process_file(base_file, os.path.join(input_dir, "Precipitation.tif"),
             "Precipitation_c.tif")
process_file(base_file, os.path.join(input_dir, "Root Restricting Layer Depth.tif"),
             "Root Restricting Layer Depth_c.tif")

print("Processing complete!")
