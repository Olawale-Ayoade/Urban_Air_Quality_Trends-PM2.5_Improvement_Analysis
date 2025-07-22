# Urban Air Quality Trends — PM2.5 Improvement Analysis

## Interactive Dashboard (Streamlit App)

**Explore the project interactively by clicking: [Streamlit App](./streamlit_app/Home.py)**


## **Project Overview**

This project investigates changes in urban air quality over time by analyzing **annual mean PM2.5 concentrations** across countries and cities. Fine particulate matter (PM2.5) is a major environmental health risk, especially in urban areas where population density and emissions are high.

The core question we address is:

**Which countries and cities have made the most progress in reducing PM2.5 pollution — and how do improvements in urban areas compare to rural ones?**

We follow a complete end-to-end exploratory data analysis (EDA) workflow, including data cleaning, anomaly detection, statistical feature engineering, and a comparative study across area types.

⸻

## Objectives
	•	Track PM2.5 trends across time and geography
	•	Identify countries and urban areas with the most improvement
	•	Compare improvements between urban and rural/town areas
	•	Flag unusual pollution patterns using residual-based modeling
	•	Communicate insights through code, markdown, and visualizations

⸻

## Data Source

### Dataset Origin:
WHO Global Air Quality Database (2022)
### **Downloaded from:** 
   * https://www.who.int/data/gho/data/themes/air-pollution/who-air-quality-database/2022

### Key Details:
	•	Metric: Annual mean PM2.5 concentration (µg/m³)
	•	Coverage: Urban population across countries
	•	Collection: Satellite + ground monitoring
	•	Fields: Country, Year, Area Type (Cities, Rural, Urban, etc.), PM2.5
	•	Frequency: Every 2–3 years

⸻
## 🔬 Project Walkthrough


### Notebook Workflow

All notebooks are located in the notebooks/ directory.

#### 1. 01_data_loading_exploration.ipynb
	•	Loads and previews the dataset
	•	Explores structure, columns, and data coverage
	•	Visualizes PM2.5 distribution and top polluted locations

#### 2. 02_cleaning_missing_outliers.ipynb
	•	Handles missing values and dropped duplicates
	•	Detects outliers using IQR and Z-score
	•	Compares outlier methods visually (Venn + scatter)
	•	Saves cleaned dataset to processed/ folder

#### 3. 03_data_summary_and_features.ipynb
	•	Analyzes trends in PM2.5 by country, city, and area type
	•	Ranks countries and cities by improvement over time
	•	Compares urban vs rural PM2.5 change
	•	Fits a linear regression model to flag anomalies (residual analysis)
	•	Prepares final dataset for use in dashboards or modeling

⸻

### Custom Twist: Urban vs Rural Comparison

A key addition to this project is a comparison of air quality trends between different area types, such as:
	•	Cities / Urban 
	•	Towns / Rural 

This helps evaluate how improvements vary depending on region type and whether policy efforts are equally effective.
## Interactive Dashboard (Streamlit App)

App Sections:
	•	Home: Summary of the project
	•	Global Trends: PM2.5 maps + trends
	•	Improvement Rankings: Countries and cities with progress
	•	Missing & Outliers: Data health reports
	•	Anomalies: Residual-based anomaly detection

## Project Structure

├── data/
│   ├── raw/
│   ├── interim/
│   └── processed/
├── notebooks/
│   ├── 01_data_loading_exploration.ipynb
│   ├── 02_cleaning_missing_outliers.ipynb
│   └── 03_data_summary_and_features.ipynb
├── streamlit_app/
│   ├── Home.py
│   ├── pages/
│   ├── scripts/
│   └── tests/
├── requirements.txt
└── README.md



### Full meta data:
```
Indicator name:
Annual mean concentration of particulate matter of less than 2.5 microns of diameter (PM2.5) [ug/m3] in urban areas
Short name:
Annual mean PM2.5 concentration in urban areas
Data type:
Statistic
Indicator Id:
4674
Topic:
Risk factors
ISO Health Indicators Framework
Environmental factors
Rationale:
Air pollution consists of many pollutants, among other particulate matter. These particles are able to penetrate deeply into the respiratory tract and therefore constitute a risk for health by increasing mortality from respiratory infections and diseases, lung cancer, and selected cardiovascular diseases.
Definition:
The mean annual concentration of fine suspended particles of less than 2.5 microns in diameters is a common measure of air pollution. The mean is a population-weighted average for urban population in a country.
Method of measurement
Concentration of PM2.5 are regularly measured from fixed-site,  population-oriented monitors located within the metropolitan areas. High-quality measurements of PM concentration from all the monitors in the metropolitan area can be averaged to develop a single estimate.  
Method of estimation:
Although PM is measured at many thousands of locations throughout the world, the amount of monitors in different geographical areas vary, with some areas having little or no monitoring. In order to produce global estimates at high resolution (0.1◦ grid‐cells), additional data is required. Annual urban mean concentration of PM2.5 is estimated with improved modelling using data integration from satellite remote sensing, population estimates, topography and ground measurements.
Preferred data sources:
Special studies
Expected frequency of data dissemination:
Every 2-3 years
Expected frequency of data collection:
Every 2-3 years
```