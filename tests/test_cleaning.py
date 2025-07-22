import sys
import os
import pytest
import pandas as pd
import numpy as np
from scipy import stats

# Add the path to the scripts folder of the Streamlit app
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'streamlit_app', 'scripts')))
from data_cleaning import detect_outliers, get_missing_data, count_duplicates

# Test data for outlier detection
@pytest.fixture
def sample_data():
    """
    Fixture that returns sample data for outlier detection.
    The data is a simple DataFrame with a numeric column.
    """
    return pd.DataFrame({
        'FactValueNumeric': [1, 2, 3, 4, 5, 20]  # The last value (20) will be considered an outlier.
    })

@pytest.fixture
def data_with_nan():
    """
    Fixture that returns data with NaN values for testing handling of missing data in outlier detection.
    """
    return pd.DataFrame({
        'FactValueNumeric': [1, 2, 3, np.nan, 5, 20]  # There is a NaN value at index 3.
    })

@pytest.fixture
def data_z_score_outlier():
    """
    Fixture that returns data with a clear outlier based on z-scores.
    """
    return pd.DataFrame({
        'FactValueNumeric': [1]*10 + [20]  # The last value (20) is an outlier compared to the rest.
    })

# Tests for detect_outliers
def test_detect_outliers_iqr(sample_data):
    """
    Test that verifies outlier detection using the IQR (Interquartile Range) method.
    It should correctly mark the last value as an outlier.
    """
    df = detect_outliers(sample_data)
    # Ensure that the 'outlier_IQR' column exists
    assert 'outlier_IQR' in df.columns
    # The last value (20) is an outlier based on IQR, so the last entry should be marked as 1
    assert df['outlier_IQR'].tolist() == [0, 0, 0, 0, 0, 1]

def test_detect_outliers_z_score(data_z_score_outlier):
    """
    Test that verifies outlier detection using z-scores.
    It should correctly mark the last value (20) as an outlier.
    """
    df = detect_outliers(data_z_score_outlier)
    # Ensure that the 'outlier_z' column exists
    assert 'outlier_z' in df.columns
    # The last value (20) has a z-score greater than the threshold, so it should be marked as 1
    assert df['outlier_z'].iloc[-1] == 1

def test_outlier_nan_handling(data_with_nan):
    """
    Test that verifies NaN values are correctly handled by the outlier detection method.
    NaN values should not be marked as outliers.
    """
    df = detect_outliers(data_with_nan)
    # Ensure that the NaN value (at index 3) is not considered an outlier
    assert df['outlier_IQR'].iloc[3] == 0
    assert df['outlier_z'].iloc[3] == 0

def test_detect_outliers_empty_df():
    """
    Test the outlier detection function with an empty DataFrame.
    The function should handle the case gracefully.
    """
    empty_df = pd.DataFrame({'FactValueNumeric': []})
    df = detect_outliers(empty_df)
    # The function should still return a DataFrame with the correct columns, even if it's empty
    assert 'outlier_IQR' in df.columns
    assert 'outlier_z' in df.columns
    # The DataFrame should be empty
    assert df.empty

# Tests for get_missing_data
def test_get_missing_data():
    """
    Test that verifies the handling of missing data.
    The function should identify columns with missing values and return the correct counts.
    """
    df = pd.DataFrame({
        'A': [1, np.nan, 3],  # Column A has one missing value
        'B': [np.nan, np.nan, 3],  # Column B has two missing values
        'C': [4, 5, 6]  # Column C has no missing values
    })
    missing = get_missing_data(df)
    # Check that the function correctly identifies columns with missing data
    assert missing.tolist() == [2, 1]  # Column B has 2 missing, Column A has 1 missing
    assert missing.index.tolist() == ['B', 'A']  # The correct column names should be returned

def test_get_missing_data_no_missing():
    """
    Test that verifies the behavior when there are no missing values in the DataFrame.
    The function should return an empty result.
    """
    df = pd.DataFrame({'A': [1, 2], 'B': [3, 4]})
    missing = get_missing_data(df)
    # The DataFrame has no missing values, so the result should be empty
    assert missing.empty

# Tests for count_duplicates
def test_count_duplicates():
    """
    Test that verifies counting duplicate rows in a DataFrame.
    The function should return the correct number of duplicates.
    """
    df = pd.DataFrame({
        'A': [1, 2, 2],  # One duplicate in column A
        'B': ['x', 'y', 'y']  # One duplicate in column B
    })
    # There is 1 duplicate row (index 2 has the same values as index 1)
    assert count_duplicates(df) == 1

def test_count_duplicates_none():
    """
    Test that verifies counting duplicates when there are none.
    The function should return 0 if there are no duplicates.
    """
    df = pd.DataFrame({'A': [1, 2, 3]})
    # No duplicates in the DataFrame
    assert count_duplicates(df) == 0

def test_count_duplicates_all_duplicates():
    """
    Test that verifies counting duplicates when all rows are duplicates.
    The function should return the correct number of duplicate rows.
    """
    df = pd.DataFrame({'A': [1, 1, 1]})
    # There are 2 duplicate rows (index 1 and 2 are duplicates of index 0)
    assert count_duplicates(df) == 2