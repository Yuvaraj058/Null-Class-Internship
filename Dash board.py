import os
import webbrowser
import pandas as pd
import plotly.express as px
import plotly.io as pio
from datetime import datetime
import pytz
import numpy as np

# Load datasets (update paths if needed)
apps_df = pd.read_csv("googleplaystore.csv")
reviews_df = pd.read_csv("googleplaystore_user_reviews.csv")
file_path = "googleplaystore.csv"  # Update with the correct path

# Convert Last Updated column to datetime
apps_df["Last Updated"] = pd.to_datetime(apps_df["Last Updated"], errors='coerce')

# Remove non-numeric values and convert "Installs" column to float
apps_df["Installs"] = pd.to_numeric(apps_df["Installs"].str.replace(r'[,\+]', '', regex=True), errors='coerce')

# Convert "Reviews" column to numeric
apps_df["Reviews"] = pd.to_numeric(apps_df["Reviews"], errors='coerce')

# Merge datasets on 'App' column
merged_df = pd.merge(apps_df, reviews_df, on='App')

# Filter apps with more than 1,000 reviews
filtered_df = merged_df.groupby('App').filter(lambda x: len(x) > 1000)

# Identify top 5 categories by total reviews
top_categories = filtered_df.groupby('Category').size().nlargest(5).index

# Filter for top 5 categories
filtered_df = filtered_df[filtered_df['Category'].isin(top_categories)]

# Define rating groups
def rating_group(rating):
    if rating <= 2:
        return '1-2 Stars'
    elif rating <= 4:
        return '3-4 Stars'
    else:
        return '4-5 Stars'

filtered_df['Rating_Group'] = filtered_df['Rating'].apply(rating_group)

# Count sentiments within each group
sentiment_counts = filtered_df.groupby(['Category', 'Rating_Group', 'Sentiment']).size().reset_index(name='Count')

# Create stacked bar chart for Task 1
fig1 = px.bar(
    sentiment_counts,
    x='Rating_Group',
    y='Count',
    color='Sentiment',
    facet_col='Category',
    title='Sentiment Distribution by Rating Group for Top 5 App Categories',
    barmode='stack'
)
fig1.write_html("app_rating_distribution.html")

# Time-based access control function
ist = pytz.timezone('Asia/Kolkata')
current_time = datetime.now(ist).time()

def is_time_allowed(start, end):
    return start <= current_time <= end

# Delete previous files if they exist
for filename in ["top_categories.html", "global_installs.html", "filtered_apps.html", "app_size_vs_rating.html", "rating_category_counts.html", "app_reviews_distribution.html", "installs_vs_reviews.html", "app_category_trend.html", "app_sentiment_distribution.html"]:
    if os.path.exists(filename):
        os.remove(filename)

# Task 2: Available 3 PM – 5 PM IST
if is_time_allowed(datetime.strptime("15:00", "%H:%M").time(), datetime.strptime("17:00", "%H:%M").time()):
    category_counts = apps_df['Category'].value_counts().nlargest(10)
    fig2 = px.bar(category_counts, x=category_counts.index, y=category_counts.values, title='Top 10 Categories by Number of Apps', labels={'x': 'Category', 'y': 'Number of Apps'})
    fig2.write_html("top_categories.html")

# Task 3: Available 6 PM – 8 PM IST
# Task 3: Available 6 PM – 8 PM IST (without 'Country')
if is_time_allowed(datetime.strptime("18:00", "%H:%M").time(), datetime.strptime("20:00", "%H:%M").time()):
    df = pd.read_csv(file_path)
    df = df[['Category', 'Installs']].dropna()
    df['Installs'] = df['Installs'].astype(str).str.replace(r'[^\d]', '', regex=True)
    df['Installs'] = pd.to_numeric(df['Installs'], errors='coerce').fillna(0).astype(int)
    top_categories = df.groupby('Category')['Installs'].sum().nlargest(5).index
    df = df[df['Category'].isin(top_categories)]
    category_installs = df.groupby('Category')['Installs'].sum().reset_index()
    fig3 = px.bar(
        category_installs,
        x='Category',
        y='Installs',
        color='Category',
        title="Top Categories by Global Installs (Filtered)",
        labels={'Installs': 'Total Installs'}
    )
    fig3.write_html("global_installs.html")

# Task 4: Available 4 PM – 6 PM IST
if is_time_allowed(datetime.strptime("16:00", "%H:%M").time(), datetime.strptime("18:00", "%H:%M").time()):
    filtered_df = apps_df[(apps_df['Rating'] < 4.0) & (apps_df['Reviews'] >= 10)]
    category_counts = filtered_df['Category'].value_counts()
    valid_categories = category_counts[category_counts > 50].index
    filtered_df = filtered_df[filtered_df['Category'].isin(valid_categories)]
    fig4 = px.violin(filtered_df, x='Category', y='Rating', box=True, points='all', title='Distribution of Ratings for Each App Category', color='Category')
    fig4.write_html("filtered_apps.html")

# Task 5: Available 5 PM – 7 PM IST
if is_time_allowed(datetime.strptime("17:00", "%H:%M").time(), datetime.strptime("19:00", "%H:%M").time()):
    fig5 = px.scatter(filtered_df, x="Installs", y="Rating", size="Installs", color="Category", hover_name="App", title="App Installs vs. Average Rating")
    fig5.write_html("app_size_vs_rating.html")

# Task 6: Available 9 AM – 11 AM IST
if is_time_allowed(datetime.strptime("09:00", "%H:%M").time(), datetime.strptime("11:00", "%H:%M").time()):
    rating_category_counts = apps_df.groupby(['Category', 'Rating']).size().reset_index(name='Count')
    fig6 = px.bar(rating_category_counts, x='Rating', y='Count', color='Category', title='App Ratings Distribution by Category')
    fig6.write_html("rating_category_counts.html")

# Task 7: Available 10 AM – 12 PM IST
if is_time_allowed(datetime.strptime("10:00", "%H:%M").time(), datetime.strptime("12:00", "%H:%M").time()):
    app_reviews_distribution = apps_df[['App', 'Reviews']].dropna()
    fig7 = px.histogram(app_reviews_distribution, x='Reviews', title='Distribution of Reviews for Apps')
    fig7.write_html("app_reviews_distribution.html")

# Task 8: Available 11 AM – 1 PM IST
if is_time_allowed(datetime.strptime("11:00", "%H:%M").time(), datetime.strptime("13:00", "%H:%M").time()):
    installs_vs_reviews = apps_df[['Installs', 'Reviews']].dropna()
    fig8 = px.scatter(installs_vs_reviews, x='Installs', y='Reviews', title='Installs vs Reviews for Apps')
    fig8.write_html("installs_vs_reviews.html")

# Task 9: Available 12 PM – 2 PM IST
if is_time_allowed(datetime.strptime("12:00", "%H:%M").time(), datetime.strptime("14:00", "%H:%M").time()):
    app_category_trend = apps_df.groupby(['Last Updated', 'Category']).size().reset_index(name='App Count')
    fig9 = px.line(app_category_trend, x='Last Updated', y='App Count', color='Category', title='App Category Trend Over Time')
    fig9.write_html("app_category_trend.html")

# Generate dashboard with buttons
html_content = """
<!DOCTYPE html>
<html>
<head>
    <title>Google Play Store Data Analytics</title>
    <style>
         body {
            background: url('https://img-s-msn-com.akamaized.net/tenant/amp/entityid/AA1mjW7J.img?w=728&h=385&m=4&q=98') no-repeat center center fixed;
            background-size: cover;
            color: white;
            text-align: center;
            font-family: Arial, sans-serif;
        button {
            margin: 10px;
            padding: 12px 24px;
            font-size: 16px;
            color: white;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            transition: background-color 0.3s ease;
        }
        button:hover {
            background-color: #0c56d0;
        }
        .sentiment-btn {
            background-color: red;
        }
        .categories-btn {
            background-color: yellow;
            color: black;
        }
        .installs-btn {
            background-color: white;
            color: black;
        }
        .filtered-btn {
            background-color: green;
            color: black;
        }
        .size-rating-btn {
            background-color: blue;
        }
        .rating-category-btn {
            background-color: orange;
        }
        .reviews-btn {
            background-color: purple;
        }
        .trend-btn {
            background-color: brown;
        }
        .installs-reviews-btn {
            background-color: teal;
        }
    </style>
    <script>
        function openPlot(filename, startHour, endHour) {
            const now = new Date();
            const hours = now.getHours();

            if (hours >= startHour && hours < endHour) {
                window.open(filename, '_blank');
            } else {
                alert("This feature is only available between " + startHour + ":00 and " + endHour + ":00.");
            }
        }
    </script>
</head>
<body style='background-color: black; color: white; text-align: center;'>
    <h1><img src='https://tse4.mm.bing.net/th?id=OIP.aK0pFHbj6X0jqS0ZGmqGmAHaEK&pid=Api&P=0&h=180' alt='Google Play Store Logo' width='50' style='vertical-align: middle;'> Google Play Store Data Analytics</h1>
    
    <!-- Each button has its own time window and color -->
    <button class="sentiment-btn" onclick="openPlot('app_rating_distribution.html', 00, 24)">Sentiment Distribution </button>
    <button class="categories-btn" onclick="openPlot('top_categories.html', 15, 17)">Top Categories </button>
    <button class="installs-btn" onclick="openPlot('global_installs.html', 18, 20)">Global Installs </button>
    <button class="filtered-btn" onclick="openPlot('filtered_apps.html', 16, 18)">Filtered Apps </button>
    <button class="size-rating-btn" onclick="openPlot('app_size_vs_rating.html', 17, 19)">App Size vs Rating </button>
    <button class="rating-category-btn" onclick="openPlot('rating_category_counts.html', 09, 11)">Rating by Category</button>
    <button class="reviews-btn" onclick="openPlot('app_reviews_distribution.html', 10, 12)">App Reviews Distribution</button>
    <button class="installs-reviews-btn" onclick="openPlot('installs_vs_reviews.html', 11, 13)">Installs vs Reviews</button>
    <button class="trend-btn" onclick="openPlot('app_category_trend.html', 12, 14)">App Category Trend</button>
</body>
</html>
"""
with open("dashboard.html", "w", encoding="utf-8") as f:
    f.write(html_content)

webbrowser.open('file://' + os.path.realpath("dashboard.html"))
