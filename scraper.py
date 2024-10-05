import logging
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util import Retry # type: ignore
from bs4 import BeautifulSoup
import pandas as pd
import time

# Set up logging
logging.basicConfig(level=logging.INFO)
logging.info('Starting the scraper...')

# URL of the website you want to scrape
url = 'https://www.noon.com/egypt-en/sports-and-outdoors/exercise-and-fitness/yoga-16328/'  # Change to the actual URL

# Set headers to mimic a browser request
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}

# Create a session with retry logic
session = requests.Session()
retries = Retry(total=5, backoff_factor=0.5)
session.mount('http://', HTTPAdapter(max_retries=retries))
session.mount('https://', HTTPAdapter(max_retries=retries))

# Send a GET request to the website with a timeout
try:
    logging.info(f'Sending GET request to {url}')
    start_time = time.time()  # Start timing the request
    response = session.get(url, headers=headers, timeout=30)  # 30 seconds timeout
    end_time = time.time()  # End timing the request

    # Log the time taken for the request
    logging.info(f'Request completed in {end_time - start_time:.2f} seconds.')

    # Check if the request was successful
    if response.status_code == 200:
        logging.info('Request was successful. Parsing HTML content...')
        
        # Parse the HTML content
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Lists to store scraped data
        titles = []
        prices = []
        brands = []
        sellers = []
        
        # Find product elements (adjust selectors based on the website structure)
        products = soup.find_all('div', class_='product')  # Change to the correct class or tag

        logging.info(f'Found {len(products)} products.')

        for product in products:
            # Extract title
            title = product.find('h2', class_='product-title').text.strip()  # Adjust selector
            titles.append(title)
            
            # Extract price
            price = product.find('span', class_='product-price').text.strip()  # Adjust selector
            prices.append(price)
            
            # Extract brand (if available)
            brand = product.find('span', class_='product-brand').text.strip()  # Adjust selector
            brands.append(brand)
            
            # Extract seller (if available)
            seller = product.find('span', class_='product-seller').text.strip()  # Adjust selector
            sellers.append(seller)

        # Create a DataFrame from the lists
        df = pd.DataFrame({
            'title': titles,
            'price': prices,
            'brand': brands,
            'seller': sellers
        })

        # Save the DataFrame to a CSV file
        df.to_csv('products.csv', index=False)
        logging.info('Data scraped and saved to products.csv successfully!')
    
    else:
        logging.error(f'Failed to retrieve the webpage. Status code: {response.status_code}')
except Exception as e:
    logging.error(f'An error occurred: {e}')
