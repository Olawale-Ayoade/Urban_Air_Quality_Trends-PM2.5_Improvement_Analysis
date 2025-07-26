import pandas as pd
import streamlit as st

# Using Streamlit's caching to speed up repeated data loading
@st.cache_data
def load_data(filepath="./data/processed/pm25_cleaned.csv"):
    """
    This function loads the cleaned PM2.5 dataset from the given filepath.
    It also extracts the 'Year' from the 'Period' column and adds it as a new column.

    Parameters:
    - filepath: The file path to the CSV file containing the cleaned dataset

    Returns:
    - df: The cleaned DataFrame with an additional 'Year' column
    """
    
    # Load the data from the provided CSV file path
    df = pd.read_csv(filepath)
    
    # Convert the 'Period' column (which represents year in string format) to datetime and extract the year
    df['Year'] = pd.to_datetime(df['Period'], format='%Y').dt.year  # Only extract the year part
    
    # Return the dataframe with the new 'Year' column
    return df
