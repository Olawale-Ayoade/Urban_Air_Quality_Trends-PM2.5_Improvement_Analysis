import os

# Define folder structure
folders = [
    "data/raw",
    "data/interim",
    "data/processed",
    "notebooks",
    "scripts",
    "streamlit_app/pages",
    "streamlit_app/utils",
    "tests"
]

# Files to optionally initialize (empty)
files = [
    "data/raw/WHO_PM25_urban_2022.csv",
    "data/interim/pm25_with_missing_flags.csv",
    "data/processed/pm25_cleaned.csv",
    "notebooks/01_data_loading_exploration.ipynb",
    "notebooks/02_cleaning_missing_outliers.ipynb",
    "notebooks/03_data_summary_and_features.ipynb",
    "scripts/data_loader.py",
    "scripts/cleaning.py",
    "scripts/preprocessing.py",
    "scripts/config.py",
    "streamlit_app/Home.py",
    "streamlit_app/pages/1_Urban_PM25_Overview.py",
    "streamlit_app/pages/2_Missing_Outlier_Report.py",
    "streamlit_app/pages/3_Data_Cleaning_Workflow.py",
    "streamlit_app/utils/visualizations.py",
    "tests/test_cleaning.py",
    "requirements.txt",
    "README.md",
    ".gitignore"
]

def create_structure():
    for folder in folders:
        os.makedirs(folder, exist_ok=True)
        print(f"📁 Created folder: {folder}")

    for file_path in files:
        if not os.path.exists(file_path):
            with open(file_path, 'w') as f:
                f.write("")  # Empty placeholder
            print(f"📝 Created file: {file_path}")

if __name__ == "__main__":
    create_structure()
