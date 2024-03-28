import pandas as pd
import matplotlib.pyplot as plt
from sqlalchemy import create_engine


engine = create_engine('sqlite:///vivino.db')

query = """
SELECT
    c.name AS country_name,
    AVG(w.ratings_average) AS avg_rating
FROM countries c
JOIN regions r ON c.code = r.country_code
JOIN wines w ON r.id = w.region_id
GROUP BY c.name
ORDER BY avg_rating DESC;

"""
query2 = """SELECT
    c.name AS country_name,
    AVG(v.ratings_average) AS avg_rating
FROM countries c
JOIN regions r ON c.code = r.country_code
JOIN wines w ON r.id = w.region_id
JOIN vintages v ON w.id = v.wine_id
GROUP BY c.name
ORDER BY avg_rating DESC;

"""

df = pd.read_sql_query(query, engine)
df2 = pd.read_sql_query(query2, engine)

# Step 3: Plot the results using Matplotlib
plt.figure(figsize=(10, 6))
plt.bar(df2['country_name'], df['avg_rating'], color='skyblue')
plt.xlabel('Country Name')
plt.ylabel('Average Vintage Wine Rating')
plt.title('Average Vintage Wine Rating by Country')
plt.xticks(rotation=45, ha='right')  # Rotate country names for better readability
plt.tight_layout()  # Adjust layout to fit country names
plt.show()
plt.figure(figsize=(10, 6))
plt.bar(df['country_name'], df['avg_rating'], color='skyblue')
plt.xlabel('Country Name')
plt.ylabel('Average Wine Rating')
plt.title('Average Wine Rating by Country')
plt.xticks(rotation=45, ha='right')  # Rotate country names for better readability
plt.tight_layout()  # Adjust layout to fit country names
plt.show()
