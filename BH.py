from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager 
from bs4 import BeautifulSoup
import csv
import time
import re

def get_channel(url):
    return "bhstore"

category_name = input("Enter category in English: ").strip()  
url = "https://bhstore.com.sa/sa-en/browse?search=washing%20machine" 

def bhstore_scraper(link):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--start-maximized") 
    chrome_options.add_argument("--disable-notifications")
    chrome_options.add_argument("--disable-infobars")
    chrome_options.add_argument("--disable-extensions")

    service = Service(ChromeDriverManager().install())
    browser = webdriver.Chrome(service=service, options=chrome_options)
    wait = WebDriverWait(browser, 10)

    browser.get(link)
    time.sleep(5) 

    results = []
    channel = get_channel(link)
    page = 1

    while True:
        html = browser.page_source
        soup = BeautifulSoup(html, 'html.parser')

        print(f"Scraping page {page} ...")

        product_list = soup.select("a.box-info")

        for product in product_list:
            try:
                product_name = product.select_one("h4.title").get_text(strip=True)
            except:
                product_name = "no product name"

            try:
                brand = product_name.split()[0]
            except:
                brand = "no brand"

            try:
                promo_price_tag = product.select_one("div.price-amount div span")
                promo_price = promo_price_tag.get_text(strip=True) if promo_price_tag else "no promo price"
                promo_price = re.sub(r"[^\d.]", "", promo_price) if promo_price != "no promo price" else promo_price
            except:
                promo_price = "no promo price"

            try:
                regular_price_tag = product.select_one("div.old-price")
                regular_price = regular_price_tag.get_text(strip=True) if regular_price_tag else "no regular price"
                regular_price = re.sub(r"[^\d.]", "", regular_price) if regular_price != "no regular price" else regular_price
            except:
                regular_price = "no regular price"

            try:
                discount_tag = product.select_one("span.badge.bg-danger span")
                discount = discount_tag.get_text(strip=True) if discount_tag else "no discount"
            except:
                discount = "no discount"

            try:
                capacity = "no capacity"
                match = re.search(r"(\d+(?:\.\d+)?)\s*(Kg|kg|KG|L|l|liter|liters|LITERS|feet|Feet|ft|FT|قدم|Ft|Btu|Ft|fT)", product_name)
                if match:
                    capacity = match.group(1) + " " + match.group(2)
            except:
                capacity = "no capacity"

            try:
                relative_url = product.get("href")
                product_url = "https://www.bhstore.com.sa" + relative_url if relative_url else "no url"
            except:
                product_url = "no url"

            in_stock = True if product_name != "no product name" else False
            invoice_price = promo_price

            item = [channel, brand, category_name, product_name, regular_price, promo_price, invoice_price, discount, capacity, product_url, in_stock]
            if item not in results:
                results.append(item)

        
        try:
            next_btn = browser.find_element(By.CSS_SELECTOR, "li.page-item a.page-link[rel='next']")
            parent_li = next_btn.find_element(By.XPATH, "./..")
            if "disabled" in parent_li.get_attribute("class") or parent_li.get_attribute("aria-disabled") == "true":
                print("Reached last page.")
                break
            else:
                browser.execute_script("arguments[0].click();", next_btn)
                page += 1
                WebDriverWait(browser, 17).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "a.box-info"))
                )
                time.sleep(5)
        except NoSuchElementException:
            print("No Next button found, stopping.")
            break

    browser.quit()

   
    out_path = "/Users/ahmedelhadad/Desktop/extra_products.csv" 
    with open(out_path, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f)
        writer.writerow(["channel","brand","category","product_name","regular_price","promo_price","invoice_price","discount","capacity","url","in_stock"])
        writer.writerows(results)

    print(f"Saved {len(results)} products to: {out_path}")

bhstore_scraper(url)
