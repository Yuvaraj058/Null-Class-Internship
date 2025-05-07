import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from datetime import datetime

# Load the dataset (assuming the file is named 'googleplaystore.csv')
df = pd.read_csv('googleplaystore.csv')

# Clean 'Last Updated' column: Try to convert it to datetime, invalid values will be set to NaT
df['Last Updated'] = pd.to_datetime(df['Last Updated'], errors='coerce')

# Filter out rows where 'Last Updated' is NaT
df = df.dropna(subset=['Last Updated'])

# Get the current date and filter apps that have been updated in the last year
current_date = pd.to_datetime('today')
one_year_ago = current_date - pd.DateOffset(years=1)
df = df[df['Last Updated'] > one_year_ago]

# Convert 'Reviews' and 'Installs' columns to numeric, removing commas and '+' signs
df['Reviews'] = pd.to_numeric(df['Reviews'], errors='coerce')
df['Installs'] = df['Installs'].str.replace(',', '').str.replace('+', '').astype(int)

# Filter apps with at least 100,000 installs and more than 1,000 reviews
filtered_df = df[(df['Installs'] >= 100000) & (df['Reviews'] > 1000)]

# Exclude genres starting with certain letters
excluded_genres = ['A', 'F', 'E', 'G', 'I', 'K']
filtered_df = filtered_df[~filtered_df['Category'].str.startswith(tuple(excluded_genres))]

# Time Restriction: Check if it's between 2 PM and 4 PM IST
current_time = datetime.now()
if current_time.hour >= 14 and current_time.hour < 16:
    # Select only the required columns for correlation matrix
    correlation_data = filtered_df[['Installs', 'Rating', 'Reviews']]

    # Compute the correlation matrix
    correlation_matrix = correlation_data.corr()

    # Generate the heatmap
    plt.figure(figsize=(8, 6))
    sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt='.2f', cbar=True)
    plt.title('Correlation Matrix Between Installs, Ratings, and Reviews Count')
    plt.show()
else:
    print("The plot can only be viewed between 2 PM IST and 4 PM IST.")
