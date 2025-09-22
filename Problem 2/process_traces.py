import os
import re
import pandas as pd
import numpy as np

# --- Configuration (should match your collection script) ---
BASE_DIR = "my_collected_traces2"
MODELS = [
    "Resnet", "AlexNet", "VGG", "DenseNet", 
    "Inception_V3", "MobileNet_V2", "ShuffleNet_V2"
]
EVENTS = [
    "cycles", "instructions", "cache-misses", 
    "branch-instructions", "branch-misses"
]
NUM_RUNS = 5

def parse_perf_file(file_path):
    """Parses a perf stat output file to extract the time-series data."""
    values = []
    # Regex to find lines with a timestamp and a counter value.
    # It handles commas in the numbers.
    line_regex = re.compile(r"^\s*(\d+\.\d+)\s+([\d,]+)\s+.*$")
    
    try:
        with open(file_path, 'r') as f:
            for line in f:
                match = line_regex.match(line)
                if match:
                    # Remove commas and convert to integer
                    value_str = match.group(2).replace(',', '')
                    values.append(int(value_str))
    except FileNotFoundError:
        print(f"Warning: File not found {file_path}")
        return [] # Return empty list if a file is missing
        
    return values

def calculate_features(time_series):
    """Calculates a dictionary of features from a list of numbers."""
    if not time_series:
        # Return a dictionary of NaNs if the time series is empty
        return {
            'mean': np.nan, 'std': np.nan, 'median': np.nan,
            'min': np.nan, 'max': np.nan, 'var': np.nan
        }
    
    ts = np.array(time_series)
    features = {
        'mean': np.mean(ts),
        'std': np.std(ts),
        'median': np.median(ts),
        'min': np.min(ts),
        'max': np.max(ts),
        'var': np.var(ts)
    }
    return features

# --- Main Script Logic ---
all_rows = []
print("Starting data processing...")

# Loop through each model and each run
for model in MODELS:
    for run in range(1, NUM_RUNS + 1):
        # This dictionary will hold all features for a single run of a single model
        current_run_features = {'model': model, 'run': run}
        
        # For each run, collect features from all event files
        for event in EVENTS:
            file_path = os.path.join(BASE_DIR, model, f"{event}_run{run}.txt")
            
            # 1. Parse the file to get the raw numbers
            time_series_data = parse_perf_file(file_path)
            
            # 2. Calculate statistical features from the numbers
            stats = calculate_features(time_series_data)
            
            # 3. Add the features to our dictionary for the current run
            # We create unique column names like 'cycles_mean', 'cycles_std', etc.
            for key, value in stats.items():
                current_run_features[f"{event}_{key}"] = value
        
        all_rows.append(current_run_features)

print("Processing complete. Creating DataFrame...")

# Create a pandas DataFrame from our list of dictionaries
df = pd.DataFrame(all_rows)

# Save the structured data to a CSV file
output_csv_path = "features.csv"
df.to_csv(output_csv_path, index=False)

print(f"Successfully created feature dataset at: {output_csv_path}")
print("Here are the first 5 rows of your new dataset:")
print(df.head())