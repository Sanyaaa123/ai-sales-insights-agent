import sqlite3
import pandas as pd

conn = sqlite3.connect("sales.db")

query = """
SELECT region, SUM(sales) as revenue
FROM sales
GROUP BY region
ORDER BY revenue DESC
"""

df = pd.read_sql(query, conn)

print("Revenue by Region")
print(df)