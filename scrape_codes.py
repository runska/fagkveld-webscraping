import requests
from fake_useragent import UserAgent
import json
import math
from tqdm import tqdm
import pandas as pd

TOTAL_PRODUCTS = 29677
PAGE_SIZE = 100
search_pages = range(math.ceil(TOTAL_PRODUCTS / PAGE_SIZE))

session = requests.session()
session.headers.update({"User-Agent": UserAgent().chrome})


def scrape_all_codes():
    all_codes = []
    for page in tqdm(search_pages):
        url = f"https://www.vinmonopolet.no/api/search?" \
              f"q=:relevance:visibleInSearch:true" \
              f"&searchType=product" \
              f"&fields=FULL" \
              f"&pageSize={PAGE_SIZE}" \
              f"&currentPage={page}"

        page_content = session.get(url).content
        json_content = json.loads(page_content)
        products = json_content["productSearchResult"]["products"]
        codes_on_page = [product["code"] for product in products]
        all_codes.extend(codes_on_page)

    return all_codes


product_codes = scrape_all_codes()

codes_df = pd.DataFrame(product_codes, columns=["code"])
codes_df.to_csv("data/codes.csv")
print(codes_df.describe())
