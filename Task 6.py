import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

# Load the dataset (assuming the file is named 'googleplaystore.csv')
df = pd.read_csv('googleplaystore.csv')

# Function to convert 'Reviews' column
def convert_reviews(value):
    if isinstance(value, str):
        if 'M' in value:
            return float(value.replace('M', '')) * 1e6  # Convert millions to integer
        elif 'K' in value:
            return float(value.replace('K', '')) * 1e3  # Convert thousands to integer
    return float(value)  # For other cases, convert directly to float

# Apply the conversion function to the 'Reviews' column
df['Reviews'] = df['Reviews'].apply(convert_reviews)

# Data Preprocessing
# Filter out apps whose name contains 'C', reviews >= 10, and rating < 4.0
filtered_df = df[df['App'].str.contains('C', case=False, na=False)]
filtered_df = filtered_df[(filtered_df['Reviews'] >= 10)]
filtered_df = filtered_df[(filtered_df['Rating'] < 4.0)]

# Remove rows with missing or invalid category information
filtered_df = filtered_df.dropna(subset=['Category'])

# Count the number of apps in each category and filter categories with more than 50 apps
category_counts = filtered_df['Category'].value_counts()
valid_categories = category_counts[category_counts > 50].index

# Filter the dataset to only include valid categories
filtered_df = filtered_df[filtered_df['Category'].isin(valid_categories)]

# Time Restriction: Check if it's between 4 PM and 6 PM IST
current_time = datetime.now()
if current_time.hour >= 16 and current_time.hour < 18:
    # Create the violin plot
    plt.figure(figsize=(12, 6))
    sns.violinplot(x='Category', y='Rating', data=filtered_df)
    plt.xticks(rotation=90)  # Rotate category labels for better readability
    plt.title('Distribution of Ratings for Each App Category (Rating < 4.0, Apps with "C" in Name)')
    plt.show()
else:
    print("The plot can only be viewed between 4 PM IST and 6 PM IST.")
