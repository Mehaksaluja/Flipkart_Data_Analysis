import pandas as pd
import requests
from bs4 import BeautifulSoup

# Base URL for smartphone search
url = "https://www.flipkart.com/search?q=Smartphones&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off&page=1"

# Define lists to store details for all products
product_names = []
product_ratings = []
product_prices = []
no_of_ratings_reviews = []
discount = []
price_before_discount = []
is_flipkart_assured = []
product_urls = []
product_details_list = []

# Function to get product details from the individual product page
def get_product_details(product_url):
    r = requests.get(product_url)
    soup = BeautifulSoup(r.text, "html.parser")

    product_details = {}

    specifications_tables = soup.find_all('table', {'class': '_0ZhAN9'})
    if specifications_tables:
        for table in specifications_tables:
            rows = table.find_all('tr')
            for row in rows:
                cols = row.find_all('td')
                if len(cols) == 2:  # Ensure there are two columns (key and value)
                    spec_name = cols[0].get_text(strip=True)
                    spec_value = cols[1].get_text(strip=True)
                    product_details[spec_name] = spec_value

    return product_details

# Iterate over the pages to scrape product details
for page in range(1,100):  # Adjust page range as needed
    url = f"https://www.flipkart.com/search?q=Smartphones&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off&page={page}"

    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")

    products = soup.find_all('div', {'class': 'cPHDOP col-12-12'})

    for product in products:
        name_tag = product.find('div', {'class': 'KzDlHZ'})
        if name_tag:
            product_names.append(name_tag.get_text())
        else:
            product_names.append("Not Available")

        rating_tag = product.find('div', {'class': 'XQDdHH'})
        if rating_tag:
            product_ratings.append(rating_tag.get_text())
        else:
            product_ratings.append("No Rating")

        price_tag = product.find('div', {'class': 'Nx9bqj _4b5DiR'})
        if price_tag:
            product_prices.append(price_tag.get_text())
        else:
            product_prices.append("Price Not Available")

        rating_reviews_tag = product.find('span', {'class': 'Wphh3N'})
        if rating_reviews_tag:
            no_of_ratings_reviews.append(rating_reviews_tag.get_text())
        else:
            no_of_ratings_reviews.append("Not Available")

        link_tag = product.find('a', {'class': 'CGtC98'})
        if link_tag:
            product_url = "https://www.flipkart.com" + link_tag['href']
            product_urls.append(product_url)

            product_details = get_product_details(product_url)
            product_details_list.append(product_details)
        else:
            product_urls.append("Not Available")
            product_details_list.append({})

        discount_tag = product.find('div', {'class': 'UkUFwK'})
        if discount_tag:
            discount.append(discount_tag.get_text())
        else:
            discount.append("Not Available")

        price_before_discount_tag = product.find('div', {'class': 'yRaY8j ZYYwLA'})
        if price_before_discount_tag:
            price_before_discount.append(price_before_discount_tag.get_text())
        else:
            price_before_discount.append("Not Available")

        flipkart_assured_tag = product.find('div', {'class': '_0CSTHy'})
        if flipkart_assured_tag:
            is_flipkart_assured.append("Yes")
        else:
            is_flipkart_assured.append("No")

# Create the final data list
final_data = []
for i in range(len(product_names)):
    product_data = {
        'Product Name': product_names[i],
        'Rating': product_ratings[i],
        'Price': product_prices[i],
        'Number of Ratings and Reviews': no_of_ratings_reviews[i],
        'Discount': discount[i],
        'Price Before Discount': price_before_discount[i],
        'Is Flipkart Assured': is_flipkart_assured[i],
        'Product URL': product_urls[i],
    }

    if i < len(product_details_list):
        product_data.update(product_details_list[i])

    final_data.append(product_data)

# Create a DataFrame and save to a CSV file
df = pd.DataFrame(final_data)
df.to_csv('flipkart_smartphones_data.csv', index=False)

print("Data saved to flipkart_smartphones_data.csv")