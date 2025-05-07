import pandas as pd
import plotly.express as px
from datetime import datetime
from pytz import timezone
from IPython.display import display, HTML
import json

# Load the dataset
try:
    df = pd.read_csv('googleplaystore.csv')
except FileNotFoundError:
    display(HTML("<p style='color:red;'>Error: The file 'googleplaystore.csv' was not found. Please make sure the file is in the same directory as your Jupyter Notebook or provide the correct path.</p>"))
    exit()

# Data Cleaning and Preparation
# Convert 'Installs' to numeric
def clean_installs(installs):
    if isinstance(installs, str):
        cleaned_str = ''.join(filter(str.isdigit, installs))
        if cleaned_str:
            return int(cleaned_str)
        else:
            return 0  # Or another appropriate default value
    return installs

df['Installs'] = df['Installs'].apply(clean_installs)

# Filter out rows where 'Installs' is NaN after cleaning (if any)
df = df.dropna(subset=['Installs'])

# Filter out categories starting with 'A', 'C', 'G', or 'S'
filtered_df = df[~df['Category'].str.startswith(('A', 'C', 'G', 'S'), na=False)].copy()

# Calculate total installs per category in the filtered data
category_installs = filtered_df.groupby('Category')['Installs'].sum()

# Get the top 5 categories that are also present in the inner dictionaries of country_data
country_data = {
    'USA': {'PRODUCTIVITY': 1500000, 'TOOLS': 1200000, 'FAMILY': 2000000, 'PHOTOGRAPHY': 1100000, 'NEWS_AND_MAGAZINES': 900000, 'Education': 600000, 'Entertainment': 1500000, 'Health & Fitness': 1100000, 'Finance': 700000},
    'Canada': {'PRODUCTIVITY': 400000, 'TOOLS': 350000, 'FAMILY': 500000, 'PHOTOGRAPHY': 400000, 'NEWS_AND_MAGAZINES': 300000, 'Education': 200000, 'Entertainment': 400000, 'Health & Fitness': 250000, 'Finance': 150000},
    'India': {'PRODUCTIVITY': 2500000, 'TOOLS': 3000000, 'FAMILY': 4000000, 'PHOTOGRAPHY': 2200000, 'NEWS_AND_MAGAZINES': 1800000, 'Education': 1200000, 'Entertainment': 2500000, 'Health & Fitness': 2000000, 'Finance': 1500000},
    'UK': {'PRODUCTIVITY': 500000, 'TOOLS': 450000, 'FAMILY': 650000, 'PHOTOGRAPHY': 500000, 'NEWS_AND_MAGAZINES': 400000, 'Education': 300000, 'Entertainment': 600000, 'Health & Fitness': 400000, 'Finance': 300000},
    'Brazil': {'PRODUCTIVITY': 800000, 'TOOLS': 700000, 'FAMILY': 1200000, 'PHOTOGRAPHY': 900000, 'NEWS_AND_MAGAZINES': 600000, 'Education': 500000, 'Entertainment': 1000000, 'Health & Fitness': 800000, 'Finance': 600000},
    'Japan': {'PRODUCTIVITY': 300000, 'TOOLS': 280000, 'FAMILY': 400000, 'PHOTOGRAPHY': 350000, 'NEWS_AND_MAGAZINES': 250000, 'Education': 150000, 'Entertainment': 350000, 'Health & Fitness': 200000, 'Finance': 180000},
    'Germany': {'PRODUCTIVITY': 600000, 'TOOLS': 550000, 'FAMILY': 750000, 'PHOTOGRAPHY': 600000, 'NEWS_AND_MAGAZINES': 500000, 'Education': 250000, 'Entertainment': 550000, 'Health & Fitness': 350000, 'Finance': 280000},
    'Australia': {'PRODUCTIVITY': 450000, 'TOOLS': 400000, 'FAMILY': 550000, 'PHOTOGRAPHY': 450000, 'NEWS_AND_MAGAZINES': 350000, 'Education': 180000, 'Entertainment': 420000, 'Health & Fitness': 220000, 'Finance': 190000},
    'Nigeria': {'PRODUCTIVITY': 700000, 'TOOLS': 850000, 'FAMILY': 1000000, 'PHOTOGRAPHY': 750000, 'NEWS_AND_MAGAZINES': 650000, 'Education': 400000, 'Entertainment': 800000, 'Health & Fitness': 600000, 'Finance': 450000},
    'Egypt': {'PRODUCTIVITY': 650000, 'TOOLS': 600000, 'FAMILY': 800000, 'PHOTOGRAPHY': 700000, 'NEWS_AND_MAGAZINES': 550000, 'Education': 350000, 'Entertainment': 700000, 'Health & Fitness': 550000, 'Finance': 400000}
}

available_categories = list(list(country_data.values())[0].keys())  # Get categories from country_data
top_5_available_categories = category_installs[category_installs.index.isin(available_categories)].nlargest(5).index.tolist()

print("Top 5 Available Categories:", top_5_available_categories)

# Create a simplified DataFrame for the Choropleth map
choropleth_data = []
for country, categories in country_data.items():
    for category, installs in categories.items():
        if category in top_5_available_categories:
            choropleth_data.append({'Country': country, 'Category': category, 'Installs': installs})

choropleth_df = pd.DataFrame(choropleth_data)

print("Columns of choropleth_df:", choropleth_df.columns)
print("\nFirst few rows of choropleth_df:")
print(choropleth_df.head())

# Create the Choropleth map
fig = px.choropleth(choropleth_df,
                    locations='Country',
                    locationmode='country names',
                    color='Installs',
                    hover_name='Country',
                    color_continuous_scale=px.colors.sequential.Plasma,
                    facet_col='Category',
                    facet_col_wrap=3,
                    title=f'Global Installs by Top {len(top_5_available_categories)} App Categories (Excluding A, C, G, S)',
                    labels={'Installs': 'Number of Installs'})

# Highlight countries where installs exceed 1 million for each category
for i, category in enumerate(top_5_available_categories):
    category_df = choropleth_df[choropleth_df['Category'] == category]
    highlighted_countries = category_df[category_df['Installs'] > 1000000]['Country'].tolist()
    if highlighted_countries:
        # Determine the correct row and column for the subplot
        row = (i // 3) + 1
        col = (i % 3) + 1
        for country in highlighted_countries:
            country_data_point = choropleth_df[(choropleth_df['Category'] == category) & (choropleth_df['Country'] == country)].iloc[0]
            fig.add_scattergeo(
                locations=[country],
                locationmode='country names',
                mode='markers',
                marker=dict(size=10, color='yellow', opacity=0.8),
                name=f'{category} > 1M Installs',
                showlegend=False,
                row=row,
                col=col
            )

fig.update_geos(fitbounds="locations", visible=False)

# Time-based display logic for Jupyter Notebook
now_ist = datetime.now(timezone('Asia/Kolkata'))
current_hour = now_ist.hour

if 12 <= current_hour < 20:
    fig.show()
else:
    display(HTML("<p>This visualization is available between 6 PM and 8 PM IST.</p>"))
