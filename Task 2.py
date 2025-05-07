import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load your dataset
df = pd.read_csv('googleplaystore.csv')

# Clean column names
df.columns = df.columns.str.strip()

# Filter only paid apps with valid numeric data
df_paid = df[
    (df['Type'] == 'Paid') & 
    (df['Installs'].notnull()) & 
    (df['Category'].notnull()) & 
    (df['Price'].notnull())
]

# Clean 'Installs' column by removing commas and '+' and converting to numeric
df_paid['Installs'] = df_paid['Installs'].str.replace(',', '').str.replace('+', '').astype(float)

# Clean 'Price' column by removing the '$' sign and converting to numeric
df_paid['Price'] = df_paid['Price'].str.replace('$', '').astype(float)

# Calculate 'Revenue' as Price * Installs
df_paid['Revenue'] = df_paid['Price'] * df_paid['Installs']

# Drop rows where 'Revenue' or 'Installs' are NaN after conversion
df_paid = df_paid.dropna(subset=['Revenue', 'Installs'])

# Plot
plt.figure(figsize=(12, 6))
sns.scatterplot(
    data=df_paid,
    x='Installs',
    y='Revenue',
    hue='Category',  # Use 'Category' to color the points
    palette='tab10',  # You can change the palette to any color palette you like
    alpha=0.7
)

# Add trendline using seaborn’s regplot (no hue support, so do it separately)
sns.regplot(
    data=df_paid,
    x='Installs',
    y='Revenue',
    scatter=False,
    color='black',
    line_kws={'linewidth': 2, 'label': 'Trendline'}
)

plt.title('Revenue vs Installs for Paid Apps')
plt.xlabel('Number of Installs')
plt.ylabel('Revenue ($)')
plt.legend(loc='upper left', bbox_to_anchor=(1, 1))
plt.tight_layout()
plt.show()
