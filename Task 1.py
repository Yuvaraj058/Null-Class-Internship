import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Load your dataset
df = pd.read_csv('googleplaystore_user_reviews.csv')

# Clean column names
df.columns = df.columns.str.strip()

# Filter rows with valid sentiment
df = df.dropna(subset=['Sentiment'])

# Simulate sentiment labels if needed (e.g., for some analysis)
# If sentiment is already in 'Sentiment' column, you can skip this part

# For example, if you want to group by 'Positive', 'Neutral', 'Negative':
# df['Sentiment'] = np.random.choice(['Positive', 'Neutral', 'Negative'], size=len(df))

# For example, if you're working with 'Sentiment_Polarity' to classify reviews:
# You can classify based on polarity
df['Sentiment'] = df['Sentiment_Polarity'].apply(lambda x: 'Positive' if x > 0 else ('Negative' if x < 0 else 'Neutral'))

# Filter out rows with missing sentiment labels
df = df.dropna(subset=['Sentiment'])

# Top 5 app categories (If available in the dataset, assuming 'App' column represents app names)
# You can adjust based on the actual categories in your dataset
top_categories = df['App'].value_counts().nlargest(5).index

# Group by the app and sentiment
sentiment_counts = df[df['App'].isin(top_categories)].groupby(['App', 'Sentiment']).size().unstack().fillna(0)

# Plot stacked bar chart for sentiment distribution by app
ax = sentiment_counts.plot(kind='bar', stacked=True, colormap='Set3')

# Add title and labels
plt.title('Sentiment Distribution by App')
plt.xlabel('App')
plt.ylabel('Number of Reviews')
plt.legend(title='Sentiment')

# Annotate bars with values
for p in ax.patches:
    ax.annotate(f'{int(p.get_height())}', (p.get_x() + p.get_width() / 2., p.get_height()), 
                ha='center', va='center', fontsize=10, color='black', xytext=(0, 5), textcoords='offset points')

plt.tight_layout()
plt.show()
