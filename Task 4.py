import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
import pytz

# Load your dataset
df = pd.read_csv("googleplaystore.csv")  # Replace with your actual file path

# Drop rows with critical missing values
df = df.dropna(subset=['Rating', 'Size', 'Category', 'Reviews', 'Installs', 'Last Updated'])

# Clean 'Size' column: convert 'M' to MB, 'k' to MB
def convert_size(size):
    try:
        size = size.strip()
        if 'M' in size:
            return float(size.replace('M', '').replace(',', ''))
        elif 'k' in size:
            return float(size.replace('k', '').replace(',', '')) / 1024
        else:
            return None
    except:
        return None

df['Size_MB'] = df['Size'].apply(convert_size)

# Remove rows with non-numeric 'Installs' values (e.g., 'Free')
df = df[df['Installs'].str.contains(r'^\d+[+,]*$', regex=True, na=False)]

# Clean and convert 'Installs' to integer
df['Installs'] = df['Installs'].str.replace('[+,]', '', regex=True).astype(int)

# Convert 'Reviews' to integer (handle possible non-numeric)
df['Reviews'] = pd.to_numeric(df['Reviews'], errors='coerce')
df = df.dropna(subset=['Reviews'])
df['Reviews'] = df['Reviews'].astype(int)

# Convert 'Last Updated' to datetime
df['Last Updated'] = pd.to_datetime(df['Last Updated'], errors='coerce')
df = df.dropna(subset=['Last Updated'])

# Filter data based on conditions
filtered_df = df[
    (df['Rating'] >= 4.0) &
    (df['Size_MB'] >= 10.0) &
    (df['Last Updated'].dt.month == 1)
]

# Group by category and compute stats
category_stats = filtered_df.groupby('Category').agg({
    'Rating': 'mean',
    'Reviews': 'sum',
    'Installs': 'sum'
}).sort_values(by='Installs', ascending=False).head(10).reset_index()

# Time-based control (3 PM to 5 PM IST)
india_time = datetime.now(pytz.timezone('Asia/Kolkata'))

if 15 <= india_time.hour < 17:
    # Create grouped bar chart
    fig = go.Figure(data=[
        go.Bar(name='Average Rating', x=category_stats['Category'], y=category_stats['Rating']),
        go.Bar(name='Total Reviews', x=category_stats['Category'], y=category_stats['Reviews'])
    ])
    fig.update_layout(
        barmode='group',
        title='Top 10 App Categories by Installs (Filtered)',
        xaxis_title='Category',
        yaxis_title='Values',
        height=500
    )
    fig.show()
else:
    print("⏰ This chart is only available from 3 PM to 5 PM IST.")
