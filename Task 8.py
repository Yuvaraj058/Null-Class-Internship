import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# Load the dataset (assuming the file is named 'googleplaystore.csv')
df = pd.read_csv('googleplaystore.csv')

# Clean up 'Reviews' and 'Installs' columns
df['Reviews'] = pd.to_numeric(df['Reviews'], errors='coerce')

# Remove non-numeric values like 'Free' in the 'Installs' column
df['Installs'] = df['Installs'].replace('Free', '0')  # Replace 'Free' with '0'

# Remove commas and plus signs from the 'Installs' column
df['Installs'] = df['Installs'].str.replace(',', '').str.replace('+', '')

# Convert 'Installs' to numeric, coercing errors to NaN
df['Installs'] = pd.to_numeric(df['Installs'], errors='coerce')

# Filter out apps with invalid 'Last Updated' dates
df['Last Updated'] = pd.to_datetime(df['Last Updated'], errors='coerce')
df = df.dropna(subset=['Last Updated'])

# Filter apps where name does not start with 'X', 'Y', 'Z' and category starts with 'E', 'C', or 'B'
df = df[~df['App'].str.startswith(('X', 'Y', 'Z'))]
df = df[df['Category'].str.startswith(('E', 'C', 'B'))]

# Filter apps with more than 500 reviews
df = df[df['Reviews'] > 500]

# Add a 'Month' column for time series analysis
df['Month'] = df['Last Updated'].dt.to_period('M')

# Group data by Month and Category, summing up 'Installs'
monthly_installs = df.groupby(['Month', 'Category'])['Installs'].sum().reset_index()

# Calculate the month-over-month percentage change in installs
monthly_installs['Installs Growth (%)'] = monthly_installs.groupby('Category')['Installs'].pct_change() * 100

# Time Restriction: Check if it's between 6 PM and 9 PM IST
current_time = datetime.now()
if current_time.hour >= 18 and current_time.hour < 21:
    plt.figure(figsize=(12, 8))
    
    # Plot time series lines for each category
    categories = monthly_installs['Category'].unique()
    for category in categories:
        category_data = monthly_installs[monthly_installs['Category'] == category]
        plt.plot(category_data['Month'].astype(str), category_data['Installs'], label=category)
        
        # Highlight areas where growth exceeds 20%
        significant_growth = category_data[category_data['Installs Growth (%)'] > 20]
        plt.fill_between(significant_growth['Month'].astype(str), 
                         significant_growth['Installs'], 
                         color='yellow', alpha=0.3)
    
    # Formatting plot
    plt.title('Trend of Total Installs Over Time (By Category)', fontsize=16)
    plt.xlabel('Month', fontsize=12)
    plt.ylabel('Total Installs', fontsize=12)
    plt.xticks(rotation=45)
    plt.legend(title='Categories')
    plt.tight_layout()
    plt.show()
else:
    print("The plot can only be viewed between 6 PM IST and 9 PM IST.")
