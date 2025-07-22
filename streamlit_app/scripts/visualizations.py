import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
from statsmodels.graphics.gofplots import qqplot

def create_box_plot(df):
    """
    Create a box plot to visualize PM2.5 distribution by region.
    
    Parameters:
    - df: The DataFrame containing the PM2.5 data.
    
    Returns:
    - A box plot visualization showing the PM2.5 levels across different regions.
    """
    return px.box(
        df, x="ParentLocation", y="FactValueNumeric", color="ParentLocation",
        labels={"FactValueNumeric": "PM2.5 (µg/m³)", "ParentLocation": "Region"},
        template="plotly_white"
    )

def create_violin_plot(df):
    """
    Create a violin plot to visualize PM2.5 distribution by location type.
    
    Parameters:
    - df: The DataFrame containing the PM2.5 data.
    
    Returns:
    - A violin plot visualization showing the PM2.5 levels across different location types.
    """
    return px.violin(
        df, x="Dim1", y="FactValueNumeric", color="Dim1", box=True,
        labels={"FactValueNumeric": "PM2.5 (µg/m³)", "Dim1": "Location Type"},
        template="plotly_white"
    )

def create_trend_plot(trend_df, x_column="Period"):
    """
    Create a line chart to visualize PM2.5 trends over time.
    
    Parameters:
    - trend_df: The DataFrame containing the PM2.5 trend data.
    - x_column: The column name to be used on the x-axis (usually "Period").
    
    Returns:
    - A line plot showing PM2.5 trends over time by region.
    """
    return px.line(
        trend_df,
        x=x_column,
        y="FactValueNumeric",
        color="ParentLocation",
        markers=True,
        labels={"FactValueNumeric": "Average PM2.5 (µg/m³)", "Period": "Year"},
        template="plotly_white"
    )

def create_choropleth(df, year, range_color=(0, 50)):
    """
    Create a choropleth map to visualize global PM2.5 concentrations by region.
    
    Parameters:
    - df: The DataFrame containing the PM2.5 data with location codes.
    - year: The year to display data for.
    - range_color: The color scale range for PM2.5 values (default is 0 to 50 µg/m³).
    
    Returns:
    - A choropleth map showing PM2.5 concentrations globally for a specific year.
    """
    return px.choropleth(
        df,
        locations="SpatialDimValueCode",
        color="FactValueNumeric",
        hover_name="Location",
        hover_data=["ParentLocation", "FactValueNumeric"],
        color_continuous_scale="RdYlGn_r",
        range_color=range_color,
        title=f"Global PM2.5 Concentration ({year}) (µg/m³)"
    )

def create_pollution_barchart(df, year, n=10):
    """
    Create a bar chart to visualize the top N most polluted cities.
    
    Parameters:
    - df: The DataFrame containing the PM2.5 data.
    - year: The year to display data for.
    - n: The number of top cities to display (default is 10).
    
    Returns:
    - A horizontal bar chart showing the top N most polluted cities for a specific year.
    """
    top_df = df.sort_values("FactValueNumeric", ascending=False).head(n)
    return px.bar(
        top_df,
        x="FactValueNumeric",
        y="Location",
        orientation='h',
        color="ParentLocation",
        labels={"FactValueNumeric": "PM2.5 (µg/m³)", "Location": ""},
        title=f"Top {n} Most Polluted Urban Areas ({year})"
    )

def create_outlier_scatterplot(df, time_col='Period', value_col='FactValueNumeric'):
    """
    Create a scatter plot to visualize PM2.5 levels over time with outliers highlighted.
    
    Parameters:
    - df: The DataFrame containing the PM2.5 data.
    - time_col: The column name to be used on the x-axis (default is "Period").
    - value_col: The column name to be used on the y-axis (default is "FactValueNumeric").
    
    Returns:
    - A scatter plot showing PM2.5 levels over time, with IQR and Z-score outliers highlighted.
    """
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.scatterplot(data=df, x=time_col, y=value_col, 
                   label='PM2.5', alpha=0.4, ax=ax)
    
    # Overlay outliers
    sns.scatterplot(data=df[df['outlier_IQR'] == 1], 
                   x=time_col, y=value_col, 
                   color='red', label='IQR Outliers', ax=ax)
    
    sns.scatterplot(data=df[df['outlier_z'] == 1], 
                   x=time_col, y=value_col, 
                   color='green', label='Z-score Outliers', marker='X', ax=ax)
    
    plt.title('Time Series of PM2.5 with IQR and Z-Score Outliers')
    plt.ylabel('PM2.5 (µg/m³)')
    plt.grid(True)
    plt.legend()
    return fig

def plot_residuals_vs_fitted(fitted, residuals):
    """
    Create a residuals vs fitted values plot.
    
    Parameters:
    - fitted: The fitted values from the regression model.
    - residuals: The residuals (errors) from the regression model.
    
    Returns:
    - A scatter plot showing residuals versus fitted values, with a trendline.
    """
    fig = px.scatter(
        x=fitted, 
        y=residuals,
        labels={'x': 'Fitted Values', 'y': 'Residuals'},
        title='Residuals vs Fitted Values',
        trendline="lowess"
    )
    fig.add_hline(y=0, line_dash="dash", line_color="red")
    fig.update_layout(template="plotly_white")
    return fig

def plot_residual_distribution(residuals):
    """
    Create a histogram to visualize the distribution of residuals.
    
    Parameters:
    - residuals: The residuals (errors) from the regression model.
    
    Returns:
    - A histogram showing the distribution of residuals with a box plot.
    """
    fig = px.histogram(
        residuals, 
        nbins=50,
        labels={'value': 'Residuals'},
        title='Residual Distribution',
        marginal="box"
    )
    fig.update_layout(template="plotly_white")
    return fig

def plot_qq(residuals):
    """
    Create a Q-Q plot to visualize the normality of residuals.
    
    Parameters:
    - residuals: The residuals (errors) from the regression model.
    
    Returns:
    - A Q-Q plot showing if residuals follow a normal distribution.
    """
    fig, ax = plt.subplots(figsize=(6, 4))
    qqplot(residuals, line='45', fit=True, ax=ax)
    plt.title('Q-Q Plot of Residuals')
    plt.tight_layout()
    return fig

def plot_residual_boxplot(residuals):
    """
    Create a box plot to visualize the distribution of residuals.
    
    Parameters:
    - residuals: The residuals (errors) from the regression model.
    
    Returns:
    - A box plot showing the distribution of residuals.
    """
    fig = px.box(
        residuals, 
        orientation='h',
        labels={'value': 'Residuals'},
        title='Residual Distribution Boxplot'
    )
    fig.update_layout(template="plotly_white", showlegend=False)
    return fig
