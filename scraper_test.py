import requests
from bs4 import BeautifulSoup

# The site we are scraping
url = "https://books.toscrape.com/"

# Send request to website
headers = {"User-Agent": "Mozilla/5.0"}
response = requests.get(url, headers=headers)

# Check connection
if response.status_code == 200:
    print("SUCCESS: Connected to the website!")
    soup = BeautifulSoup(response.text, "html.parser")
    
    # Grab the very first book on the page to test
    first_book = soup.find("article", class_="product_pod")
    title = first_book.h3.a["title"]
    price = first_book.find("p", class_="price_color").text
    
    print("---------------------------------")
    print(f"Sample Book Title: {title}")
    print(f"Sample Book Price: {price}")
    print("---------------------------------")
else:
    print(f"Failed to connect. Status Code: {response.status_code}")