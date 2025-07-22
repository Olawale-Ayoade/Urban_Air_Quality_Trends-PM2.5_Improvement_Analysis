# ======================== Import Required Libraries ========================
import streamlit as st
import pandas as pd
# Custom script imports for modular code organization
from scripts.data_loader import load_data            # Loads the main PM2.5 dataset
from scripts.filters import apply_filters            # Applies user-selected filters
from scripts.visualizations import (                 # Functions to generate visualizations
    create_box_plot, 
    create_violin_plot, 
    create_trend_plot
)
from scripts.stats import (                          # Statistical computations
    get_summary_stats, 
    calculate_metrics
)

# ======================== Load Cleaned Data ========================
df = load_data()  # This function reads and returns the dataset

# ======================== Page Configuration ========================
st.title("🌍 General PM2.5 Air Quality Analysis")  # Page title
st.markdown("Explore PM2.5 (µg/m³) measurements across different regions and locations")  # Short description

# Sidebar filter section
st.sidebar.header("Filters")  # Sidebar title

# Year range slider to filter data by year
selected_years = st.sidebar.slider(
    "Select Year Range",
    min_value=int(df['Period'].min()),  # Earliest year in the data
    max_value=int(df['Period'].max()),  # Latest year in the data
    value=(int(df['Period'].min()), int(df['Period'].max()))  # Default is full range
)

# Region filter (multi-select)
selected_regions = st.sidebar.multiselect(
    "Select Regions",
    options=df['ParentLocation'].unique(),  # All unique regions
    default=df['ParentLocation'].unique()   # Default is all regions selected
)

# Location type filter (Urban, Rural, etc.)
selected_dim1 = st.sidebar.multiselect(
    "Select Location Type",
    options=df['Dim1'].unique(),           # All unique location types
    default=df['Dim1'].unique()            # Default is all types selected
)

# Apply user-selected filters to the dataset
filtered_df = apply_filters(df, selected_years, selected_regions, selected_dim1)

# Define three tabs: for visualizations, statistics, and raw data
tab1, tab2, tab3 = st.tabs(["Visualizations", "Summary Statistics", "Raw Data"])

# ======================== TAB 1: Visualizations ========================
with tab1:
    # Two columns side by side for comparison plots
    col1, col2 = st.columns(2)
    
    # Box plot by region
    with col1:
        st.subheader("PM2.5 Distribution by Region")
        st.plotly_chart(create_box_plot(filtered_df), use_container_width=True)

    # Violin plot by location type
    with col2:
        st.subheader("PM2.5 Distribution by Location Type")
        st.plotly_chart(create_violin_plot(filtered_df), use_container_width=True)
    
    # Line plot for PM2.5 trend over years by region
    st.subheader("PM2.5 Trends Over Time")
    trend_df = filtered_df.groupby(['Period', 'ParentLocation'])['FactValueNumeric'].mean().reset_index()
    st.plotly_chart(create_trend_plot(trend_df), use_container_width=True)

# ===================== TAB 2: Summary Statistics =======================
with tab2:
    st.subheader("Interactive PM2.5 Statistics")

    # Generate descriptive statistics
    summary_stats = get_summary_stats(filtered_df)

    # Show formatted summary stats in a table
    st.dataframe(
        summary_stats.style.format({
            'Average': '{:.2f}',
            'Median': '{:.2f}',
            'Std Dev': '{:.2f}',
            '25th Percentile': '{:.2f}',
            '75th Percentile': '{:.2f}'
        }), 
        use_container_width=True,
        height=600
    )

    # Button to download the summary stats as CSV
    st.download_button(
        label="Download Summary Statistics",
        data=summary_stats.to_csv(index=False),
        file_name='pm25_summary_statistics.csv',
        mime='text/csv'
    )

# ======================== TAB 3: Raw Data ==============================
with tab3:
    st.subheader("Filtered Raw Data")

    # Display filtered raw data table
    st.dataframe(filtered_df, use_container_width=True, height=600)

    # Button to download filtered data as CSV
    st.download_button(
        label="Download Filtered Data",
        data=filtered_df.to_csv(index=False),
        file_name='filtered_pm25_data.csv',
        mime='text/csv'
    )

# ======================== Metrics Section =============================
# Calculate important metrics for quick insights
metrics = calculate_metrics(filtered_df)

# Display key metrics in a horizontal layout
st.subheader("Key Metrics")
col1, col2, col3 = st.columns(3)

# Metric: Total number of PM2.5 samples
col1.metric("Total Samples", f"{metrics['total_samples']:,}")

# Metric: Average PM2.5 level
col2.metric("Average PM2.5", f"{metrics['average_pm25']:.2f} µg/m³")

# Metric: Highest recorded PM2.5 level
col3.metric("Highest PM2.5", f"{metrics['max_pm25']:.2f} µg/m³")