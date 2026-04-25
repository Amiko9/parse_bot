import requests
from bs4 import BeautifulSoup

def get_magazine_name(url):
    if "darwin.md" in url:
        return "Darwin"
    elif "enter.md" in url:
        return "Enter"
    elif "neocomputer.md" in url:
        return "Neocomputer"
    else:
        return None

def load_product_info(url):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (HTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36"
        }
        page = requests.get(url, headers=headers, timeout=10)
        page.raise_for_status()
        soup = BeautifulSoup(page.content, "html.parser")
        magazine = get_magazine_name(url)
        if magazine == "Neocomputer":
            title_tag = soup.find(class_="section-title")
            price_tag = soup.find(class_="value")

        elif magazine == "Darwin":
            title_tag = soup.find(class_="fs-24 lh-25-fix")
            price_tag = soup.find(class_="block-price")

        elif magazine == "Enter":
            title_tag = soup.find(class_="fw-semibold fs-22 lh-base text-gray-900")
            price_tag = soup.find(class_="fs-20")

        else:
            return None

        title = title_tag.get_text().strip()
        raw_price = price_tag.get_text().strip()
        price = raw_price.replace(" ", ".")

        return {
            "url": url,
            "title": title,
            "price": price,
            "magazine": magazine
        }
    except Exception as e:
        print(f"Error for {url}: {e}")