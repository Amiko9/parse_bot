import requests
from bs4 import BeautifulSoup

def load_product_info(url):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36"
        }
        page = requests.get(url, headers=headers, timeout=10)
        page.raise_for_status()
        soup = BeautifulSoup(page.content, "html.parser")
        title_tag = soup.find(class_="section-title")
        price_tag = soup.find(class_="value")

        title = title_tag.get_text().strip()
        raw_price = price_tag.get_text().strip()
        price = raw_price.replace(" ", ".")

        return {
            "url": url,
            "title": title,
            "price": price
        }
    except Exception as e:
        print(f"Error for {url}: {e}")
        return None