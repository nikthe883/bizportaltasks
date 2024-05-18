import requests
from bs4 import BeautifulSoup
import pandas as pd

class QuoteScraper:
    def __init__(self, base_url='http://quotes.toscrape.com/'):
        self.base_url = base_url
        self.quotes = []

    def get_quotes_from_page(self, url):
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        quotes = []
        
        for quote in soup.find_all('div', class_='quote'):
            text = quote.find('span', class_='text').get_text()
            author = quote.find('small', class_='author').get_text()
            tags = [tag.get_text() for tag in quote.find_all('a', class_='tag')]
            tags_str = ';'.join(tags)
            quote_url = url
            
            quotes.append({
                'text': text,
                'author': author,
                'tags': tags_str,
                'url': quote_url
            })
        
        return quotes

    def get_all_quotes(self):
        page = 1
        while True:
            print(f'Scraping page {page}...')
            url = f'{self.base_url}page/{page}/'
            page_quotes = self.get_quotes_from_page(url)
            
            if not page_quotes:  
                break
            
            self.quotes.extend(page_quotes)
            page += 1

    def save_to_csv(self, filename='quotes.csv'):
        df = pd.DataFrame(self.quotes)
        df.to_csv(filename, index=False)
        print(f'Data saved to {filename}')

    def save_to_json(self, filename='quotes.json'):
        df = pd.DataFrame(self.quotes)
        df.to_json(filename, orient='records')
        print(f'Data saved to {filename}')

# Create an instance of the QuoteScraper class.
scraper = QuoteScraper()

# Scrape all quotes.
scraper.get_all_quotes()

# Save the quotes to a CSV file.
scraper.save_to_csv()

# Save the quotes to a JSON file.
scraper.save_to_json()

