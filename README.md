# E-Commerce Public Data Exploratory Data Analysis - Dicoding

## Overview
This project is a comprehensive exploratory data analysis focused on e-commerce public data. It also include streamlit dashboard for interactive data exploration. The project is specifically focused on the E-Commerce Public Dataset, and aims to provide valuable insights and recommendations for improving e-commerce performance.

## Project Structure
- dashboard/: This directory contains dashboard.py, which is a dashboard created with streamlit.
- data/: Directory containing the raw CSV data files.
- notebook.ipynb: This file is used to perform exploratory data analysis.
- README.md: This documentation file.

## Setup Environment
First way:
1. Clone this repository to your local machine:
   
   git clone https://github.com/fawazatha/EDA-Dicoding.git

2. Go to the project directory
   
   cd EDA-Dicoding

3. Install the required Python packages by running:
   
   pip install -r requirements.txt

Additional way
1. Create a new environment
   
   conda create --name eda-dicoding python=3.9
   
2. Activate new environment
   
   conda activate eda-dicoding

3. install necessary libraries
   
   pip install numpy pandas scipy matplotlib seaborn jupyter streamlit ipykernel

## Usage
Data Wrangling: Scripts are available in the notebook.ipynb file to prepare and clean the data.

Exploratory Data Analysis (EDA): Explore and analyze the data. 
Exploring data from e-commerce sources can help uncover interesting patterns and trends. These insights can give us a better understanding of how people shop online and how markets work.

Visualization: Run the Streamlit dashboard for interactive data exploration:

- cd EDA-Dicoding/dashboard
- streamlit run dashboard.py

Access the dashboard in your web browser at http://localhost:8501.
