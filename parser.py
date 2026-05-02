import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

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
        # elif magazine == "Enter":
        #     title_tag = soup.find(class_="fw-semibold fs-22 lh-base text-gray-900")
        #     price_tag = soup.find(class_="fs-20")

        else:
            return None

        title = title_tag.get_text().strip()
        raw_price = price_tag.get_text().strip()
        price = raw_price.replace(" ", ".")
        if magazine == "Darwin":
            price = price.split("\n")[0]

        return {
            "url": url,
            "title": title,
            "price": price,
            "magazine": magazine
        }
    except Exception as e:
        print(f"Error for {url}: {e}")

def load_category_info(url):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                          "AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/120.0 Safari/537.36"
        }

        page = requests.get(url, headers=headers, timeout=10)
        page.raise_for_status()

        soup = BeautifulSoup(page.content, "html.parser")
        magazine = get_magazine_name(url)

        products = []

        if magazine == "Darwin":
            product_cards = soup.find_all(class_="product-card")

            for card in product_cards:
                title_tag = card.find(class_="title-product")
                price_tag = card.find(class_="price-new")
                link_tag = card.find("a", class_="product-link")


                if not title_tag or not price_tag or not link_tag:
                    continue

                title = title_tag.get_text().strip()
                price = price_tag.get_text().strip().replace(" ", ".").replace(".lei", "")

                product_url = urljoin(url, link_tag.get("href"))

                products.append({
                    "url": product_url,
                    "title": title,
                    "price": price,
                    "magazine": magazine
                })
        elif magazine == "Neocomputer":
                product_cards = soup.select(".products-list .col-lg-4.col-6")

                for card in product_cards:
                    title_tag = card.find(class_="title")
                    price_tag = card.find(class_="price-current")
                    link_tag = card.find("a", href=True)

                    if not title_tag or not price_tag:
                        continue

                    title = title_tag.get_text().strip()
                    price = price_tag.get_text().strip().replace(" ", ".").replace(".lei", "")

                    product_url = urljoin(url, link_tag["href"])

                    products.append({
                        "url": product_url,
                        "title": title,
                        "price": price,
                        "magazine": magazine
                    })

        else:
            return []

        return products

    except Exception as e:
        print(f"Error for category {url}: {e}")
        return []