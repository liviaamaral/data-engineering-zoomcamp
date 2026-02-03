#!/usr/bin/env python3
"""
Script to download NYC Yellow Taxi Trip Records for January - June 2024
Data source: NYC Taxi & Limousine Commission (TLC)
"""

import os
import requests
from datetime import datetime
from pathlib import Path

# Base URL for the trip data
BASE_URL = "https://d37ci6vzurychx.cloudfront.net/trip-data/"

# Define the months to download (January - June 2024)
YEAR = 2024
MONTHS = range(1, 7)  # January (1) through June (6)

# Output directory
OUTPUT_DIR = "nyc_taxi_data_2024"


def download_file(url, output_path):
    """
    Download a file from a URL to the specified output path.
    
    Args:
        url (str): URL to download from
        output_path (Path): Path where the file will be saved
    
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        print(f"Downloading: {url}")
        
        # Stream the download to handle large files
        response = requests.get(url, stream=True)
        response.raise_for_status()
        
        # Get file size if available
        total_size = int(response.headers.get('content-length', 0))
        
        # Download with progress indication
        downloaded = 0
        with open(output_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
                    downloaded += len(chunk)
                    if total_size > 0:
                        progress = (downloaded / total_size) * 100
                        print(f"  Progress: {progress:.1f}%", end='\r')
        
        print(f"\n  ✓ Saved to: {output_path}")
        print(f"  File size: {os.path.getsize(output_path) / (1024*1024):.2f} MB\n")
        return True
        
    except requests.exceptions.RequestException as e:
        print(f"  ✗ Error downloading {url}: {e}\n")
        return False


def main():
    """Main function to download all Yellow Taxi trip records."""
    
    # Create output directory if it doesn't exist
    output_path = Path(OUTPUT_DIR)
    output_path.mkdir(exist_ok=True)
    print(f"Output directory: {output_path.absolute()}\n")
    
    # Track download statistics
    successful = 0
    failed = 0
    start_time = datetime.now()
    
    # Download each month's data
    for month in MONTHS:
        # Format filename: yellow_tripdata_2024-01.parquet
        filename = f"yellow_tripdata_{YEAR}-{month:02d}.parquet"
        url = BASE_URL + filename
        output_file = output_path / filename
        
        # Skip if file already exists
        if output_file.exists():
            print(f"⊘ File already exists: {filename}")
            print(f"  Skipping download. Delete the file to re-download.\n")
            successful += 1
            continue
        
        # Download the file
        if download_file(url, output_file):
            successful += 1
        else:
            failed += 1
    
    # Print summary
    end_time = datetime.now()
    duration = (end_time - start_time).total_seconds()
    
    print("=" * 60)
    print("DOWNLOAD SUMMARY")
    print("=" * 60)
    print(f"Total files: {successful + failed}")
    print(f"Successful: {successful}")
    print(f"Failed: {failed}")
    print(f"Duration: {duration:.1f} seconds")
    print(f"Output directory: {output_path.absolute()}")
    print("=" * 60)


if __name__ == "__main__":
    main()