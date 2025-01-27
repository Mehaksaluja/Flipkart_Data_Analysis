import pandas as pd
import requests
from bs4 import BeautifulSoup

url = "https://www.flipkart.com/search?q=Laptops&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off&page=1"

r = requests.get(url)

soup = BeautifulSoup(r.text, "html.parser")

# Define lists to store the details for all products
product_names = []
product_ratings = []
product_prices = []
no_of_ratings_reviews = []
processor = []
RAM = []
windows = []
storage = []
laptop_size = []
warranty = []
discount = []
price_before_discount = []
is_flipkart_assured = []
product_urls = []  # List to store product URLs
product_details_list = []

# Function to get product details from the individual product page
def get_product_details(product_url):
    # Send a GET request to the individual product page
    r = requests.get(product_url)
    soup = BeautifulSoup(r.text, "html.parser")

    # Dictionary to store product specifications
    product_details = {}

    # Extracting specifications from all tables with the same class
    specifications_tables = soup.find_all('table', {'class': '_0ZhAN9'})  # Find all tables with this class
    if specifications_tables:
        # Extract the first table as the main specifications
        main_specifications_table = specifications_tables[0]
        rows = main_specifications_table.find_all('tr')
        for row in rows:
            cols = row.find_all('td')
            if len(cols) == 2:  # Ensure there are two columns (key and value)
                spec_name = cols[0].get_text(strip=True)
                spec_value = cols[1].get_text(strip=True)
                product_details[spec_name] = spec_value

        # Extract the second table as the processor and memory features
        if len(specifications_tables) > 1:
            processor_memory_table = specifications_tables[1]
            rows = processor_memory_table.find_all('tr')
            for row in rows:
                cols = row.find_all('td')
                if len(cols) == 2:  # Ensure there are two columns (key and value)
                    spec_name = cols[0].get_text(strip=True)
                    spec_value = cols[1].get_text(strip=True)
                    product_details[spec_name] = spec_value

    return product_details


# Iterate over the pages to scrape product details
for page in range(1, 86):  # Adjust page range as needed
    # Construct the URL for the current page
    url = f"https://www.flipkart.com/search?q=Laptops&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off&page={page}"

    # Send a GET request to the URL
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")

    # Find all product containers on the current page
    products = soup.find_all('div', {'class': '_75nlfW'})

    # Extract details for each product on this page
    for product in products:
        # Extract product name
        name_tag = product.find('div', {'class': 'KzDlHZ'})
        if name_tag:
            product_names.append(name_tag.get_text())
        else:
            product_names.append("Not Available")

        # Extract product rating
        rating_tag = product.find('div', {'class': 'XQDdHH'})
        if rating_tag:
            product_ratings.append(rating_tag.get_text())
        else:
            product_ratings.append("No Rating")

        # Extract product price
        price_tag = product.find('div', {'class': 'Nx9bqj _4b5DiR'})
        if price_tag:
            product_prices.append(price_tag.get_text())
        else:
            product_prices.append("Price Not Available")

        # Extract the number of ratings and reviews
        # Extract the number of ratings and reviews for each product
        rating_reviews_tag = product.find('span', class_='Wphh3N')

        if rating_reviews_tag:
            spans = rating_reviews_tag.find_all('span')
            if len(spans) >= 3:
                # Extract and append ratings
                ratings = spans[0].text.strip()
                no_of_ratings_reviews.append(ratings)
            else:
                # Append "Not Available" when spans are insufficient
                no_of_ratings_reviews.append("Not Available")
        else:
            # Append "Not Available" when the tag is missing
            no_of_ratings_reviews.append("Not Available")

        # Extract product URL (anchor tag with href)
        link_tag = product.find('a', {'class': 'CGtC98'})
        if link_tag:
            product_url = "https://www.flipkart.com" + link_tag['href']
            product_urls.append(product_url)

            # Get detailed info from the individual product page
            product_details = get_product_details(product_url)
            product_details_list.append(product_details)
        else:
            product_urls.append("Not Available")
            product_details_list.append({})

        # Extract discount information
        discount_tag = product.find('div', {'class': 'UkUFwK'})
        if discount_tag:
            discount.append(discount_tag.get_text())
        else:
            discount.append("Not Available")

        # Extract price before discount
        price_before_discount_tag = product.find('div', {'class': 'yRaY8j ZYYwLA'})
        if price_before_discount_tag:
            price_before_discount.append(price_before_discount_tag.get_text())
        else:
            price_before_discount.append("Not Available")

        # Check if the product is Flipkart Assured
        flipkart_assured_tag = product.find('div', {'class': '_0CSTHy'})
        if flipkart_assured_tag:
            is_flipkart_assured.append("Yes")
        else:
            is_flipkart_assured.append("No")

# Create the final data list to include all the details
final_data = []

# Loop through product details and store them in the final_data list
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

    # Add specifications from the individual product page
    if i < len(product_details_list):
        product_data.update(product_details_list[i])

    final_data.append(product_data)

# Create a DataFrame from the extracted data
df = pd.DataFrame(final_data)

# Convert dataframe to csv file
df.to_csv('flipkart_laptops_data.csv', index=False)

print("Data saved to flipkart_laptops_data.csv")
