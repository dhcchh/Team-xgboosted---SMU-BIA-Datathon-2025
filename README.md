# Team-xgboosted---SMU-BIA-Datathon-2025

This project develops **Sentinel**, an innovative analytics solution for the Internal Security Department (ISD), Ministry of Home Affairs, Singapore. It focuses on analyzing unstructured text data, extracting meaningful insights, and presenting them through interactive dashboards and visualisations. The goal is to showcase the feasibility and effectiveness of leveraging data-driven intelligence to enhance security analysis.

It is currently developed by [Chan Ding Hao](https://www.linkedin.com/in/dhchan/), [Lew Choon Hean](https://www.linkedin.com/in/choon-hean-lew-4584782b6/), [Hoo Kai Sng](https://www.linkedin.com/in/kai-sng-hoo-081a3622a/) and [Yip Kai Men](https://www.linkedin.com/in/yipkaimen/). 

# Setup Instructions to run the Plotly Dash App Locally 
---
## 1. Prerequisites
Ensure you have the following installed. 
* Python 3.x (Latest version recommended)
* pip (Python package manager)
* Virtual Environment (Optional, **but recommended for dependency isolation**)
* Web Browser (For viewing the Dash app)
* An Integrated Development Environment (IDE) like Visual Studio Code, **optional** but makes running the application easier. 
---
## 2. Installation Steps. 
### A. Ensure Required Files Are Available 
Make sure the following files and folders are present in the working directory, i.e. all of these files must be in the same folder. 
```
- dataset/                # Folder containing necessary dataset files
- visualisations_utils/   # Folder containing visualization utilities
- app.py                  # Main Dash application script
- requirements.txt        # List of required Python packages
```
Make sure your current working directory is set to the folder where the required files are located. You can do so using:
```
cd /your/path/to/directory/dash_app
```

### B. Set Up the Environment 
1. Create and Activate a Virtual Environment (Optional, but recommended)
It’s good practice to use a virtual environment to avoid dependency conflicts. Enter the following commands in your machine's terminal. 
```
python -m venv venv
source venv/bin/activate  # For Mac/Linux
venv\Scripts\activate     # For Windows
```
2. Install Required Python Packages
Once inside the virtual environment, install dependencies:
```
python -m pip install -r requirements.txt
```
--- 
## Running the Dash App 
### A. Start the Local Server 
Run the following command: 
```
python app.py
```
or run the Python file in your IDE. 
If everything is set up correctly, you will see an output like: 
```
Running on http://127.0.0.1:8050/
```
This means that the application is running locally on port 8050 of your machine. No internet connectivity is required.  
### B. Open the App in Your Browser
1. Copy the local server URL from the terminal.
2. Open any web browser and paste the URL into the address bar. 

# Features 

# Data Processing 

# Visualisations 
