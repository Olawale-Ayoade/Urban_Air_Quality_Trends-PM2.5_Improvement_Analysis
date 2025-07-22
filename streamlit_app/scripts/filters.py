import pandas as pd

def apply_filters(df, years, regions, dim1):
    """
    This function filters the dataset based on the provided criteria:
    - Years: a range of years.
    - Regions: a list of specific regions (locations).
    - Dim1: a list of specific values for the 'Dim1' column.

    Parameters:
    - df: The DataFrame to filter.
    - years: A tuple (start_year, end_year) defining the range of years to filter by.
    - regions: A list of regions ('ParentLocation') to filter by.
    - dim1: A list of values for the 'Dim1' column to filter by.

    Returns:
    - filtered_df: The DataFrame after applying the filters.
    """
    
    # Apply filters to the DataFrame
    filtered_df = df[
        (df['Period'].between(years[0], years[1])) &  # Filter for years in the specified range
        (df['ParentLocation'].isin(regions)) &         # Filter for rows where 'ParentLocation' is in the list of regions
        (df['Dim1'].isin(dim1))                        # Filter for rows where 'Dim1' is in the list of specified values
    ]
    return filtered_df
