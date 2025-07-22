import pandas as pd
import statsmodels.api as sm
import plotly.express as px
import plotly.graph_objects as go
from sklearn.preprocessing import StandardScaler

def prepare_regression_data(df, target_col, categorical_cols):
    """
    Prepare the data for regression analysis by:
    - Creating dummy variables for categorical columns
    - Extracting the target variable and independent variables
    
    Parameters:
    - df: The DataFrame containing the data.
    - target_col: The name of the target variable column (dependent variable).
    - categorical_cols: A list of categorical columns to be converted into dummy variables.
    
    Returns:
    - X: The independent variables with dummy variables for categorical columns.
    - y: The target variable as a numeric column.
    """
    # Convert categorical columns into dummy variables (one-hot encoding)
    X = pd.get_dummies(df[categorical_cols], drop_first=True).astype(float)
    
    # The target variable (y)
    y = df[target_col].astype(float)
    
    # Add a constant column for the intercept in the regression model
    return sm.add_constant(X), y

def fit_ols_model(X, y):
    """
    Fit an Ordinary Least Squares (OLS) regression model.
    
    Parameters:
    - X: Independent variables (predictors).
    - y: Dependent variable (target).
    
    Returns:
    - model: The fitted OLS regression model.
    """
    # Fit the OLS model
    model = sm.OLS(y, X).fit()
    return model

def get_regression_diagnostics(model):
    """
    Extract key regression diagnostics for model evaluation.
    
    Parameters:
    - model: The fitted OLS regression model.
    
    Returns:
    - A dictionary containing:
        - Fitted values
        - Residuals
        - R-squared and Adjusted R-squared
        - AIC (Akaike Information Criterion)
    """
    # Collect model diagnostics
    return {
        'fitted_values': model.fittedvalues,  # Predicted values
        'residuals': model.resid,             # Residuals (actual - predicted)
        'rsquared': model.rsquared,           # R-squared (model fit)
        'rsquared_adj': model.rsquared_adj,   # Adjusted R-squared
        'aic': model.aic                      # AIC (model quality indicator)
    }

def detect_residual_outliers(residuals):
    """
    Identify potential outliers in the residuals using the Interquartile Range (IQR) method.
    
    Parameters:
    - residuals: The residuals (difference between actual and predicted values).
    
    Returns:
    - A DataFrame containing the outlier residuals.
    """
    # Convert residuals to a DataFrame for easy manipulation
    resid_df = pd.DataFrame({'Residuals': residuals})
    
    # Calculate the IQR (Interquartile Range) to detect outliers
    Q1 = resid_df['Residuals'].quantile(0.25)
    Q3 = resid_df['Residuals'].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR  # Outlier lower bound
    upper_bound = Q3 + 1.5 * IQR  # Outlier upper bound
    
    # Return the outliers (residuals outside the IQR bounds)
    return resid_df[(resid_df['Residuals'] < lower_bound) | (resid_df['Residuals'] > upper_bound)]