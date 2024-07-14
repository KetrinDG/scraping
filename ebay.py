import json
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
from bs4 import BeautifulSoup


class EbayScraper:
    def __init__(self, url):
        self.url = url
        self.data = {}
        self.driver = None

    def setup_driver(self):
        options = Options()
        options.headless = True
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    def fetch_page(self):
        self.driver.get(self.url)
        time.sleep(5)
        return self.driver.page_source

    def parse_page(self, html):
        soup = BeautifulSoup(html, 'html.parser')

        title_element = soup.find('h1', {'class': 'x-item-title__mainTitle'})
        self.data['title'] = title_element.get_text(strip=True) if title_element else 'N/A'

        image_elements = soup.select('.image > img')
        self.data['image_urls'] = [img['src'] for img in image_elements if img.get('src')] or 'N/A'

        self.data['product_url'] = self.url

        price_element = soup.find('div', {'class': 'x-price-primary'}).find('span', {'class': 'ux-textspans'})
        self.data['price'] = price_element.get_text(strip=True) if price_element else 'N/A'

        seller_section = soup.find('div', {'class': 'vim x-sellercard-atf_main mar-t-12'})
        if seller_section:
            seller_name_element = seller_section.find('span', {'class': 'ux-textspans ux-textspans--BOLD'})
            self.data['seller'] = seller_name_element.get_text(strip=True) if seller_name_element else 'N/A'
        else:
            self.data['seller'] = 'N/A'

        shipping_section = soup.find('div', {'class': 'ux-labels-values col-12 ux-labels-values--shipping'})
        if shipping_section:
            shipping_info = shipping_section.find('span', {'class': 'ux-textspans ux-textspans--BOLD'})
            self.data['shipping_price'] = shipping_info.get_text(strip=True) if shipping_info else 'N/A'
        else:
            self.data['shipping_price'] = 'N/A'

        # Additional data (optional)
        item_condition = soup.find('div', {'class': 'ux-icon-text'})
        self.data['item_condition'] = item_condition.get_text(strip=True) if item_condition else 'N/A'

        item_location_elem = soup.find('div', {'class': 'ux-labels-values__values-content'})
        if item_location_elem:
            item_location_text = item_location_elem.find('span', {'class': 'ux-textspans ux-textspans--SECONDARY'}).get_text(strip=True)
            item_location_text = item_location_text.replace('Located in: ', '')
            self.data['item_location'] = item_location_text if item_location_text else 'N/A'
        else:
            self.data['item_location'] = 'N/A'

    def to_json(self):
        return json.dumps(self.data, ensure_ascii=False, indent=4)

    def save_to_file(self, filename):
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, ensure_ascii=False, indent=4)

    def scrape(self):
        self.setup_driver()
        html = self.fetch_page()
        if html:
            self.parse_page(html)
            print(self.to_json())
        self.driver.quit()


# Usage example
url = 'https://www.ebay.com/itm/364986782252'
scraper = EbayScraper(url)
scraper.scrape()
