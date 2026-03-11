import pandas as pd
import sqlite3

# Load dataset
df = pd.read_csv("data/Sample - Superstore.csv", encoding="latin1")

# Clean column names
df.columns = df.columns.str.lower().str.replace(" ", "_")

# Convert date columns
df['order_date'] = pd.to_datetime(df['order_date'])
df['ship_date'] = pd.to_datetime(df['ship_date'])

# Connect to database
conn = sqlite3.connect("sales.db")

# Store table
df.to_sql("sales", conn, if_exists="replace", index=False)

print("Data pipeline completed. sales.db created.")