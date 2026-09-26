import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Connect to the SQLite database created by our scraper
conn = sqlite3.connect("market_intelligence.db")

# Query the clean product dataset
query = """
SELECT 
    title,
    price_gbp,
    star_rating,
    in_stock
FROM market_products
"""
df = pd.read_sql_query(query, conn)
conn.close()

# ----------------- STATISTICAL SUMMARY -----------------
print("================ MARKET SUMMARY STATISTICS ================")
print(df[["price_gbp", "star_rating"]].describe().round(2))

avg_price_by_rating = df.groupby("star_rating")["price_gbp"].agg(["count", "mean", "median"]).round(2)
print("\n=============== AVERAGE PRICE BY STAR RATING ===============")
print(avg_price_by_rating)

# ----------------- VISUALIZATIONS -----------------
sns.set_theme(style="whitegrid")
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# Chart 1: Price Distribution (Histogram + KDE curve)
sns.histplot(df["price_gbp"], kde=True, color="#2b5c8f", bins=20, ax=axes[0])
axes[0].set_title("Market Price Distribution (£)", fontsize=13, fontweight="bold")
axes[0].set_xlabel("Price (£)")
axes[0].set_ylabel("Product Count")

# Chart 2: Price Boxplot by Star Rating (Checking price vs rating variance)
sns.boxplot(x="star_rating", y="price_gbp", data=df, palette="Blues", ax=axes[1])
axes[1].set_title("Price Distribution Across Star Ratings", fontsize=13, fontweight="bold")
axes[1].set_xlabel("Star Rating (1 - 5)")
axes[1].set_ylabel("Price (£)")

plt.tight_layout()

# Save the visualization figure to file
chart_filename = "market_analysis_charts.png"
plt.savefig(chart_filename, dpi=300)
print(f"\nSaved analysis charts to: {chart_filename}")

# Display the charts on screen
plt.show()