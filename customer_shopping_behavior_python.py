import pandas as pd
from sqlalchemy import create_engine

# Read CSV
df = pd.read_csv('customer_shopping_behavior.csv')

# Fill missing Review Rating with category median
df['Review Rating'] = (
    df.groupby('Category')['Review Rating']
    .transform(lambda x: x.fillna(x.median()))
)

# Convert column names
df.columns = df.columns.str.lower()
df.columns = df.columns.str.replace(' ', '_')

# Rename column
df = df.rename(columns={
    'purchase_amount_(usd)': 'purchase_amount'
})

# Create age_group column
labels = ['Young Adult', 'Adult', 'Middle-aged', 'Senior']
df['age_group'] = pd.qcut(df['age'], q=4, labels=labels)

# Purchase frequency mapping
frequency_mapping = {
    'Fortnightly': 14,
    'Weekly': 7,
    'Monthly': 30,
    'Quarterly': 90,
    'Bi-Weekly': 14,
    'Annually': 365,
    'Every 3 Months': 90
}

df['purchase_frequency_days'] = (
    df['frequency_of_purchases'].map(frequency_mapping)
)

# Drop unnecessary column
df = df.drop('promo_code_used', axis=1)

# -------------------------------
# PostgreSQL Connection
# -------------------------------

engine = create_engine(
    "postgresql+psycopg2://postgres:12345@localhost:5432/customer_behavior"
)

# Upload DataFrame to PostgreSQL
df.to_sql(
    "customer_behavior",
    engine,
    if_exists="replace",   # replace existing table
    index=False
)

print("Data uploaded successfully!")
