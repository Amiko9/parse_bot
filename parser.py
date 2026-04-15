import requests
from bs4 import BeautifulSoup
from datetime import date

def parser(soup):
    title = soup.find(class_="section-title").get_text().strip()
    raw_price = soup.find(class_="value").get_text().strip()
    price = float(raw_price.replace(" ", ""))
    return date.today(), title, price

def load_product_info(url, parser):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36"}
    page = requests.get(url, headers=headers)
    soup1 = BeautifulSoup(page.content, "html.parser")
    soup = BeautifulSoup(soup1.prettify(), "html.parser")
    return parser(soup)


def run_price_bot(url, parser):
    try:
        product_info = load_product_info(url, parser)

        with open("price.csv", "a", encoding="utf-8", newline="") as f:
            f.write(f'{product_info[0]},"{product_info[1]}",{product_info[2]}\n')
    except Exception as e:
        print(e)
    return


run_price_bot(
    "https://neocomputer.md/memorie-64gb-kit-of-2x32gb-ddr4-3200-kingston-fury-beast-rgb", parser)
run_price_bot(
    "https://neocomputer.md/placa-video-gigabyte-geforce-rtx-5070-ti-eagle-oc-sff-16g-206741", parser)



