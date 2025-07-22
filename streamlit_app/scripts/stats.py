import numpy as np
import pandas as pd

def get_summary_stats(df):
    """
    Generate summary statistics for PM2.5 levels grouped by period, region, and settlement type.
    
    Parameters:
    - df: The DataFrame containing the PM2.5 data.
    
    Returns:
    - A DataFrame with summary statistics (count, mean, median, min, max, std, 25th, and 75th percentiles)
      for each combination of 'Period', 'ParentLocation', and 'Dim1'.
    """
    # Group the data by 'Period', 'ParentLocation', and 'Dim1' columns
    return df.groupby(['Period', 'ParentLocation', 'Dim1'])['FactValueNumeric'].agg(
        ['count', 'mean', 'median', 'min', 'max', 'std', 
         lambda x: np.percentile(x, 25), lambda x: np.percentile(x, 75)]
    ).rename(columns={
        'count': 'Samples',               # Rename 'count' to 'Samples'
        'mean': 'Average',               # Rename 'mean' to 'Average'
        'median': 'Median',              # Rename 'median' to 'Median'
        'min': 'Minimum',                # Rename 'min' to 'Minimum'
        'max': 'Maximum',                # Rename 'max' to 'Maximum'
        'std': 'Std Dev',                # Rename 'std' to 'Std Dev' (Standard Deviation)
        '<lambda_0>': '25th Percentile', # Rename 25th percentile lambda function to '25th Percentile'
        '<lambda_1>': '75th Percentile'  # Rename 75th percentile lambda function to '75th Percentile'
    }).reset_index()  # Reset index to make the result more readable

def calculate_metrics(df):
    """
    Calculate key PM2.5 metrics: total samples, average, maximum, and minimum PM2.5 levels.
    
    Parameters:
    - df: The DataFrame containing the PM2.5 data.
    
    Returns:
    - A dictionary containing:
      - 'total_samples': The total number of rows in the DataFrame.
      - 'average_pm25': The mean PM2.5 value across all data.
      - 'max_pm25': The maximum PM2.5 value in the dataset.
      - 'min_pm25': The minimum PM2.5 value in the dataset.
    """
    # Calculate and return key metrics
    return {
        'total_samples': df.shape[0],                # Total number of rows (samples) in the DataFrame
        'average_pm25': df['FactValueNumeric'].mean(), # Mean PM2.5 level
        'max_pm25': df['FactValueNumeric'].max(),     # Maximum PM2.5 level
        'min_pm25': df['FactValueNumeric'].min()      # Minimum PM2.5 level
    }
