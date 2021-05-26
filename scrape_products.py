import requests
from fake_useragent import UserAgent
import json
from tqdm import tqdm
import pandas as pd
from concurrent.futures import ThreadPoolExecutor, as_completed

session = requests.session()
session.headers.update({"User-Agent": UserAgent().chrome})

codes = pd.read_csv("codes.csv")


def scrape_single_product(code):
    url = f"https://www.vinmonopolet.no/api/products/{code}?fields=FULL"
    product_page_content = session.get(url).content
    return json.loads(product_page_content)


def scrape_products():
    product_data = []
    for code in tqdm(codes["code"]):
        product_data.append(scrape_single_product(code))
    return product_data


def scrape_products_mulithreaded():
    product_data = []
    with tqdm(total=len(codes)) as progressbar:
        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = [executor.submit(scrape_single_product, code) for code in
                       codes["code"]]
            for future in as_completed(futures):
                product_data.append(future.result())
                progressbar.update(1)
    return product_data


scraped_product_data = scrape_products_mulithreaded()

products_df = pd.DataFrame(data=scraped_product_data)
products_df.to_csv("data.csv")
print(products_df.describe())
