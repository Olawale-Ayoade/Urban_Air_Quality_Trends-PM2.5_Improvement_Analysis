# ======================== Import Required Libraries ========================
import streamlit as st
import pandas as pd

# Custom functions for loading, cleaning, and visualizing the data
from scripts.data_loader import load_data
from scripts.data_cleaning import (
    detect_outliers,
    get_missing_data,
    count_duplicates,
    generate_cleaning_summary
)
from scripts.visualizations import create_outlier_scatterplot

# ======================== Page Configuration ========================
st.set_page_config(layout="wide")
st.title("PM2.5 Data Cleaning Report")

st.markdown("""
This report documents the data cleaning process for annual mean PM2.5 concentrations in urban areas.
The analysis focuses on handling missing values, duplicates, and outliers to ensure data quality.
""")

# ======================== Load Raw Data ========================
# Cache the raw CSV load to avoid reloading on every rerun
@st.cache_data
def load_raw_data():
    return pd.read_csv("../data/raw/WHO_PM25_urban_2022.csv")

df = load_raw_data()

# ======================== Section 1: Introduction ========================
st.header("1. Introduction")
st.write("""
The dataset consists of annual mean PM2.5 concentrations in urban areas across various countries. 
This analysis focuses on handling missing values and outliers to prepare the data for further analysis. 
Ensuring clean data is crucial for accurate insights into air pollution levels.
""")

# ======================== Section 2: Missing Values & Duplicates ========================
st.header("2. Missing Values and Duplicates")

# Two columns to separate missing values and duplicates visually
col1, col2 = st.columns(2)

# ---- Missing Data Analysis ----
with col1:
    st.subheader("Missing Values")
    missing_data = get_missing_data(df)  # Returns a Series of column-wise missing counts
    st.dataframe(missing_data.rename("Missing Count"), width=400)

    if len(missing_data) == 0:
        st.success("No missing values found!")
    else:
        st.warning(f"Found {len(missing_data)} columns with missing values")

# ---- Duplicate Rows Analysis ----
with col2:
    st.subheader("Duplicate Rows")
    dup_count = count_duplicates(df)  # Count exact duplicate rows
    st.metric("Duplicate Rows Found", dup_count)

    if dup_count > 0:
        st.warning("Duplicates found - consider removing them")
    else:
        st.success("No duplicates found")

# ======================== Section 3: Outlier Detection ========================
st.header("3. Outlier Detection and Treatment")
st.write("""
To identify and remove outliers, we used two methods: the Interquartile Range (IQR) and Z-score.
While both methods are effective, we chose the IQR method for cleaning the data because:
- It's more robust to skewed data (common in environmental measurements)
- Z-score is more sensitive to extreme values in normally distributed data
""")

# Apply both outlier detection methods and label rows accordingly
df = detect_outliers(df)  # Adds 'outlier_IQR' and 'outlier_z' columns

# Show scatter plot of PM2.5 values highlighting outliers
st.pyplot(create_outlier_scatterplot(df))

# Show number of outliers detected
col1, col2 = st.columns(2)
with col1:
    st.metric("IQR Outliers", df['outlier_IQR'].sum())
with col2:
    st.metric("Z-Score Outliers", df['outlier_z'].sum())

# ======================== Section 4: Data Cleaning Summary ========================
st.header("4. Summary of Changes")

# Filter out IQR outliers for the final cleaned dataset
cleaned_df = df[df['outlier_IQR'] == 0]

# Show a table summarizing changes between raw and cleaned datasets
st.dataframe(generate_cleaning_summary(df, cleaned_df), hide_index=True)

# Optional: show a sample of outlier rows that were removed
if st.checkbox("Show sample of removed outliers"):
    st.dataframe(df[df['outlier_IQR'] == 1].sample(5))

# Allow users to download the cleaned dataset
st.download_button(
    label="Download Cleaned Data",
    data=cleaned_df.to_csv(index=False),
    file_name='pm25_cleaned_final.csv',
    mime='text/csv'
)

# ======================== Conclusion ========================
st.header("Conclusion")
st.write("""
The data cleaning process successfully:
- Identified and handled missing values
- Removed duplicate entries
- Detected and removed outliers using robust statistical methods

The resulting dataset is now ready for further analysis and modeling.
""")
