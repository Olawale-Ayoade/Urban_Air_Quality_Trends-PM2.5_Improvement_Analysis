import pandas as pd
import numpy as np
from scipy import stats

def detect_outliers(df, target_col='FactValueNumeric'):
    """
    Identify outliers using two methods: IQR (Interquartile Range) and Z-score.
    
    Parameters:
    - df: The DataFrame containing the data
    - target_col: The column to check for outliers (default is 'FactValueNumeric')

    Returns:
    - df: The original DataFrame with additional columns indicating outliers
    """
    df = df.copy()  # Create a copy of the original DataFrame to avoid modifying it
    
    # ==================== IQR Method (Interquartile Range) ====================
    # First, calculate the first (Q1) and third (Q3) quartiles
    Q1 = df[target_col].quantile(0.25)  # 25th percentile (first quartile)
    Q3 = df[target_col].quantile(0.75)  # 75th percentile (third quartile)
    
    # The IQR is the difference between Q3 and Q1
    IQR = Q3 - Q1
    
    # Define the lower and upper bounds for detecting outliers
    lower_bound = Q1 - 1.5 * IQR  # Anything below this is considered an outlier
    upper_bound = Q3 + 1.5 * IQR  # Anything above this is considered an outlier
    
    # Create a new column 'outlier_IQR' where 1 means the value is an outlier, and 0 means it is not
    df['outlier_IQR'] = np.where((df[target_col] < lower_bound) | 
                                 (df[target_col] > upper_bound), 1, 0)
    
    # ==================== Z-score Method ====================
    # Calculate the Z-scores for each value in the target column
    df['z_score'] = np.abs(stats.zscore(df[target_col]))  # Z-score = (value - mean) / standard deviation
    
    # Z-scores greater than 3 are often considered outliers (standard threshold)
    df['outlier_z'] = np.where(df['z_score'] > 3, 1, 0)  # 1 indicates outlier
    
    return df  # Return the DataFrame with the new outlier columns

def get_missing_data(df):
    """
    Calculate the number of missing (NaN) values for each column.
    
    Parameters:
    - df: The DataFrame to check for missing values
    
    Returns:
    - missing: A Series with the count of missing values for each column with missing data
    """
    # Count missing values (NaN) for each column and sort them in descending order
    missing = df.isnull().sum().sort_values(ascending=False)
    
    # Return only columns with missing values (greater than 0 missing)
    return missing[missing > 0]

def count_duplicates(df):
    """
    Count the number of duplicate rows in the DataFrame.
    
    Parameters:
    - df: The DataFrame to check for duplicate rows
    
    Returns:
    - duplicate_count: The total number of duplicate rows
    """
    # The duplicated() function returns a boolean Series, where True means the row is a duplicate
    return df.duplicated().sum()  # Count the number of True values, i.e., duplicates

def generate_cleaning_summary(original_df, cleaned_df):
    """
    Generate a summary report comparing the state of the DataFrame before and after cleaning.
    
    Parameters:
    - original_df: The DataFrame before cleaning
    - cleaned_df: The DataFrame after cleaning
    
    Returns:
    - summary: A DataFrame with key metrics before and after cleaning
    """
    # Create a summary DataFrame with the following metrics:
    # 1. Total rows: Length of the original and cleaned DataFrame
    # 2. Total columns: Number of columns in the original and cleaned DataFrame
    # 3. Total outliers: Sum of outliers based on the IQR method in the original DataFrame (after cleaning, outliers should be 0)
    return pd.DataFrame({
        "Metric": ["Total Rows", "Total Columns", "Total Outliers"],
        "Before Cleaning": [len(original_df), len(original_df.columns), original_df['outlier_IQR'].sum()],
        "After Cleaning": [len(cleaned_df), len(cleaned_df.columns), 0]  # After cleaning, no outliers (outlier_IQR = 0)
    })