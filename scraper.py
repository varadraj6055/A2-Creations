import logging
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util import Retry  # type: ignore
from bs4 import BeautifulSoup
import pandas as pd
import time

logging.basicConfig(level=logging.INFO)
logging.info('Starting the scraper...')

url = 'https://www.noon.com/egypt-en/sports-and-outdoors/exercise-and-fitness/yoga-16328/'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}

session = requests.Session()
retries = Retry(total=5, backoff_factor=0.5)
session.mount('http://', HTTPAdapter(max_retries=retries))
session.mount('https://', HTTPAdapter(max_retries=retries))

try:
    logging.info(f'Sending GET request to {url}')
    start_time = time.time()
    response = session.get(url, headers=headers, timeout=30)
    end_time = time.time()
    logging.info(f'Request completed in {end_time - start_time:.2f} seconds.')

    if response.status_code == 200:
        logging.info('Request was successful. Parsing HTML content...')
        soup = BeautifulSoup(response.content, 'html.parser')
        titles = []
        prices = []
        brands = []
        sellers = []
        products = soup.find_all('div', class_='product')

        logging.info(f'Found {len(products)} products.')

        for product in products:
            title = product.find('h2', class_='product-title').text.strip()
            titles.append(title)
            price = product.find('span', class_='product-price').text.strip()
            prices.append(price)
            brand = product.find('span', class_='product-brand').text.strip()
            brands.append(brand)
            seller = product.find('span', class_='product-seller').text.strip()
            sellers.append(seller)

        df = pd.DataFrame({
            'title': titles,
            'price': prices,
            'brand': brands,
            'seller': sellers
        })

        df.to_csv('products.csv', index=False)
        logging.info('Data scraped and saved to products.csv successfully!')
    
    else:
        logging.error(f'Failed to retrieve the webpage. Status code: {response.status_code}')
except Exception as e:
    logging.error(f'An error occurred: {e}')
