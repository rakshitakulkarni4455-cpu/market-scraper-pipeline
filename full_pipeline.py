import requests
from bs4 import BeautifulSoup
import pandas as pd
import sqlite3
import re
import time

# Mapping textual ratings to numeric integers
RATING_MAP = {
    "One": 1,
    "Two": 2,
    "Three": 3,
    "Four": 4,
    "Five": 5
}

base_url = "https://books.toscrape.com/catalogue/page-{}.html"
headers = {"User-Agent": "Mozilla/5.0"}
scraped_data = []

print("Starting market scraping pipeline across pages 1 to 50...")

for page in range(1, 51):
    target_url = base_url.format(page)
    response = requests.get(target_url, headers=headers)
    
    if response.status_code != 200:
        print(f"Stopping at page {page} (Status: {response.status_code})")
        break
        
    soup = BeautifulSoup(response.text, "html.parser")
    products = soup.find_all("article", class_="product_pod")
    
    for product in products:
        # 1. Product Title
        title = product.h3.a["title"]
        
        # 2. Raw Price string
        raw_price = product.find("p", class_="price_color").text
        
        # 3. Star Rating (found in class attribute e.g. ['star-rating', 'Three'])
        rating_classes = product.find("p", class_="star-rating")["class"]
        rating_word = [cls for cls in rating_classes if cls != "star-rating"][0]
        numeric_rating = RATING_MAP.get(rating_word, 0)
        
        # 4. Stock Availability
        stock_status = product.find("p", class_="instock availability").text.strip()
        
        scraped_data.append({
            "title": title,
            "raw_price": raw_price,
            "star_rating": numeric_rating,
            "availability": stock_status
        })
    
    print(f"Processed Page {page}/50 | Total collected so far: {len(scraped_data)}")
    time.sleep(0.1)  # Polite crawling delay

# Convert into a Pandas DataFrame
df = pd.DataFrame(scraped_data)

# Data Cleaning with Regex and Pandas
# Extract only the digits and period from raw_price, drop the currency symbols
df["price_gbp"] = df["raw_price"].apply(lambda x: float(re.findall(r"[\d.]+", x)[0]))
df["in_stock"] = df["availability"].apply(lambda x: 1 if "In stock" in x else 0)

# Drop raw working columns
clean_df = df[["title", "price_gbp", "star_rating", "in_stock"]]

print("\nCleaning Complete! First 5 records:")
print(clean_df.head())

# Save to CSV
csv_filename = "books_scraped.csv"
clean_df.to_csv(csv_filename, index=False)
print(f"\nSaved clean CSV to: {csv_filename}")

# Save to SQLite Database
db_filename = "market_intelligence.db"
conn = sqlite3.connect(db_filename)
clean_df.to_sql("market_products", conn, if_exists="replace", index=False)
conn.close()
print(f"Stored records inside SQLite table 'market_products' in: {db_filename}")