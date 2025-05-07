import pandas as pd
import plotly.express as px
from datetime import datetime
from pytz import timezone
from IPython.display import display, HTML
import json

# Load the datasets
try:
    apps_df = pd.read_csv('googleplaystore.csv')
    reviews_df = pd.read_csv('googleplaystore_user_reviews.csv')
except FileNotFoundError:
    display(HTML("<p style='color:red;'>Error: One or both of the required CSV files were not found. Please make sure 'googleplaystore.csv' and 'googleplaystore_user_reviews.csv' are in the same directory as your Jupyter Notebook or provide the correct paths.</p>"))
    exit()

# Data Cleaning and Preprocessing for apps_df
apps_df = apps_df.dropna(subset=['Rating', 'Size', 'Installs', 'Category', 'Reviews'])

def clean_size(size):
    if 'M' in size:
        return float(size.replace('M', ''))
    elif 'k' in size:
        return float(size.replace('k', '')) / 1024  # Convert KB to MB
    elif 'Varies with device' in size:
        return None
    return None

apps_df['Size_MB'] = apps_df['Size'].apply(clean_size).dropna()

def clean_installs(installs):
    cleaned_str = ''.join(filter(str.isdigit, installs))
    if cleaned_str:
        return int(cleaned_str)
    else:
        return None  # Return None for empty strings

apps_df['Installs_Numeric'] = apps_df['Installs'].apply(clean_installs)
apps_df.dropna(subset=['Installs_Numeric'], inplace=True) # Drop rows where Installs_Numeric is None

apps_df['Reviews'] = pd.to_numeric(apps_df['Reviews'])
apps_df['Rating'] = pd.to_numeric(apps_df['Rating'])

# Data Cleaning and Preprocessing for reviews_df
reviews_df = reviews_df.dropna(subset=['App', 'Sentiment_Subjectivity'])

# Merge the two DataFrames to get Sentiment Subjectivity
merged_df = pd.merge(apps_df, reviews_df, on='App', how='inner')

# Filter the data
filtered_df = merged_df[
    (merged_df['Rating'] > 3.5) &
    (merged_df['Category'].isin(['GAME', 'BEAUTY', 'BUSINESS', 'COMICS', 'COMMUNICATION', 'DATING', 'ENTERTAINMENT', 'SOCIAL', 'EVENTS'])) &
    (merged_df['Reviews'] > 500) &
    (merged_df['Sentiment_Subjectivity'] > 0.5) &
    (merged_df['Installs_Numeric'] > 50000) &
    (merged_df['Size_MB'].notna())
]

# Group by App to get the average rating and size, and sum of installs
final_df = filtered_df.groupby('App').agg(
    Avg_Rating=('Rating', 'mean'),
    Avg_Size_MB=('Size_MB', 'mean'),
    Total_Installs=('Installs_Numeric', 'first'), # Taking the first install count as it should be consistent for an app
    Category=('Category', 'first')
).reset_index()

# Time-based display logic for Jupyter Notebook
now_ist = datetime.now(timezone('Asia/Kolkata'))
current_hour = now_ist.hour

if 17 <= current_hour < 19:  # 5 PM to 7 PM IST
    if not final_df.empty:
        fig = px.scatter(final_df,
                         x='Avg_Size_MB',
                         y='Avg_Rating',
                         size='Total_Installs',
                         color='Category',
                         hover_name='App',
                         size_max=60,
                         title='App Size vs. Average Rating (Bubble Chart)',
                         labels={'Avg_Size_MB': 'App Size (MB)', 'Avg_Rating': 'Average Rating', 'Total_Installs': 'Number of Installs'})
        fig.show()
    else:
        display(HTML("<p>No apps match the specified criteria for the bubble chart.</p>"))
else:
    display(HTML("<p>This visualization is available between 5 PM and 7 PM IST.</p>"))
