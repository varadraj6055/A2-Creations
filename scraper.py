import logging
import requests
from bs4 import BeautifulSoup
import pandas as pd


logging.basicConfig(level=logging.INFO)
logging.info('Starting the scraper...')


url = 'https://www.noon.com/egypt-en/sports-and-outdoors/exercise-and-fitness/yoga-16328/'  # Change to the actual URL


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}


try:
    logging.info(f'Sending GET request to {url}')
    response = requests.get(url, headers=headers, timeout=10)  # 10 seconds timeout

   
    if response.status_code == 200:
        logging.info('Request was successful. Parsing HTML content...')
        
       
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Lists to store scraped data
        titles = []
        prices = []
        brands = []
        sellers = []
        
       
        products = soup.find_all('div', class_='product')  # Change to the correct class or tag

        logging.info(f'Found {len(products)} products.')

        for product in products:
            
            title = product.find('h2', class_='product-title').text.strip()  # Adjust selector
            titles.append(title)
            
           
            price = product.find('span', class_='product-price').text.strip()  # Adjust selector
            prices.append(price)
            
           
            brand = product.find('span', class_='product-brand').text.strip()  # Adjust selector
            brands.append(brand)
            
          
            seller = product.find('span', class_='product-seller').text.strip()  # Adjust selector
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
