import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import pytz

# Assuming df is your DataFrame, and it's already loaded with the required columns

# Step 1: Filter the data based on the conditions
df_filtered = df[
    (df['Installs'] > 10000) & 
    ((df['Type'] == 'Paid') & (df['Price'] * df['Installs'] > 10000) | (df['Type'] == 'Free')) & 
    (df['Android Ver'].astype(str).str.split('.').str[0].astype(float) > 4.0) &  # Ensure 'Android Ver' is treated as a string
    (df['Size'].astype(str).str.replace('M', '').astype(float) > 15) &  # Ensure 'Size' is treated as a string
    (df['Content Rating'] == 'Everyone') & 
    (df['App'].str.len() <= 30)
]

# Step 2: Get the top 3 app categories by the number of apps
top_categories = df_filtered['Category'].value_counts().head(3).index

# Filter data to only include these top 3 categories
df_top3 = df_filtered[df_filtered['Category'].isin(top_categories)]

# Step 3: Calculate Revenue for each app (Price * Installs)
df_top3['Revenue'] = df_top3['Price'] * df_top3['Installs']

# Step 4: Group by Type (Free vs Paid) and Category, and calculate the mean of Installs and Revenue
category_stats = df_top3.groupby(['Category', 'Type'])[['Installs', 'Revenue']].mean().reset_index()

# Step 5: Check if the current time is between 1 PM and 2 PM IST
ist = pytz.timezone('Asia/Kolkata')
current_time = datetime.now(ist)
current_hour = current_time.hour

# Check if the time is between 1 PM (13:00) and 2 PM (14:00)
if 13 <= current_hour < 14:
    # Step 6: Create the dual-axis chart
    fig, ax1 = plt.subplots(figsize=(12, 6))

    # Plot average installs on the primary y-axis
    sns.barplot(x='Category', y='Installs', data=category_stats, ax=ax1, hue='Type', palette='Set2')
    ax1.set_xlabel('Category')
    ax1.set_ylabel('Average Installs')
    ax1.tick_params(axis='y')

    # Create a secondary y-axis for average revenue
    ax2 = ax1.twinx()
    sns.lineplot(x='Category', y='Revenue', data=category_stats, ax=ax2, hue='Type', marker='o', palette='Set2', linewidth=2)
    ax2.set_ylabel('Average Revenue ($)')
    ax2.tick_params(axis='y')

    # Title and layout adjustments
    plt.title('Average Installs and Revenue by Type (Free vs Paid) in Top 3 Categories')
    fig.tight_layout()

    # Show the plot
    plt.show()

else:
    print("The graph is only available between 1 PM and 2 PM IST.")
