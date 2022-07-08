#!/usr/bin/env python3
import json
import time
from datetime import datetime

from selenium import webdriver
from selenium.webdriver.common.by import By


def read_json(file_name: str):
    listings = {}
    try:
        with open(file_name, "r") as f:
            listings = json.load(f)
    except FileNotFoundError:
        pass
    return listings


def scrape_cex():
    file_name = "CEX_NVIDIA_GDDR6_6GB.json"
    listings = read_json(file_name)
    search_date_index = datetime.utcnow().strftime("%y%m%d")
    if listings.get(search_date_index, {}):
        # Don't bother servers if we have today's figures.
        return
    driver = webdriver.Firefox()
    driver.get("https://uk.webuy.com/boxsearch?stext=NVIDIA%20GDDR6%206GB")
    time.sleep(10)
    elems = driver.find_elements(By.CLASS_NAME, "searchRcrd")
    listings[search_date_index] = {}
    for elem in elems:
        # Could go the extra mile and check stock levels at:
        # https://uk.webuy.com/product-detail/?id=...
        prod_id = elem.get_attribute("data-insights-object-id")  # SGRANVI2060RTX6GBA
        title = elem.find_element(By.CLASS_NAME, "ais-highlight").text
        prices = [x.split("£")[-1] for x in elem.find_element(
            By.CLASS_NAME, "prodPrice").text.split("\n")]
        listings[search_date_index][title] = [prod_id] + prices
    driver.close()
    with open(file_name, "w+") as f:
        f.write(json.dumps(listings))


if __name__ == "__main__":
    scrape_cex()

