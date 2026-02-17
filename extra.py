from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager 
from bs4 import BeautifulSoup
import csv
import time
import re

def get_channel(url):
    return "extra"

category_name = input("Enter category in English: ") 
url = f"https://www.extra.com/en-sa/search/?text={category_name}"

def extra_scraper(link):
    service = Service(ChromeDriverManager().install())
    browser = webdriver.Chrome(service=service)
    wait = WebDriverWait(browser, 10)

    browser.get(link)
    time.sleep(3)

    results = []
    channel = get_channel(link)

    page = 1
    while True:
        html = browser.page_source
        soup = BeautifulSoup(html, 'html.parser')

    
        pagination = soup.select('ul.nav li.nav-item a.nav-link')
        last_page = int(pagination[-1].get_text(strip=True)) if pagination else 1

        print(f"Scraping page {page} of {last_page} ...")

        product_list = soup.find_all('div', class_='product-tile-container')

        for product in product_list:
            # brand
            try:
                brand = product.select_one('span.brand-name').get_text(strip=True)
            except:
                brand = "no brand"

            # product name
            try:
                product_name = product.select_one('span.product-name-data').get_text(strip=True)
            except:
                product_name = "no product name"

            # promo price
            try:
                promo_price = product.select_one('section.price span.price strong').get_text(strip=True)
            except:
                promo_price = "no promo price"

            # regular price
            try:
                regular_price = product.select_one('span.striked-off').get_text(strip=True)
            except:
                regular_price = "no regular price"

            # discount
            try:
                discount = product.select_one('section.save-percent-tag').get_text(strip=True)
            except:
                discount = "no discount"

            # capacity
            try:
                capacity = "no capacity"
                ul_stats = product.find("ul", class_="product-stats svelte-7u9gj8")
                if ul_stats:
                    for li in ul_stats.find_all("li"):
                        li_text = li.get_text(strip=True)
                        if "Capacity" in li_text:
                            match = re.search(r"([\d\.]+)\s*(Kg|Cu\.ft|L)?", li_text)
                            if match:
                                capacity = match.group(0)
                                break
            except:
                capacity = "no capacity"

            # product url
            try:
                parent_a = product.find_parent("a", href=True)
                product_url = "https://www.extra.com" + parent_a['href'] if parent_a else "no url"
            except:
                product_url = "no url"

            in_stock = True if product else False
            invoice_price = promo_price

            item = [channel, brand, category_name, product_name, regular_price, promo_price, invoice_price, discount, capacity, product_url, in_stock]
            if item not in results:
                results.append(item)

      
        if page < last_page:
            try:
                next_btn = browser.find_element(By.CSS_SELECTOR, "li.next div.icon-inline")
                browser.execute_script("arguments[0].click();", next_btn)
                time.sleep(4)
                page += 1
            except:
                print("Cannot go to next page.")
                break
        else:
            break

    browser.quit()

   
    out_path = r"C:\Users\abdul\Downloads\extra_products_full.csv"
    with open(out_path, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f)
        writer.writerow(["channel","brand","category","product_name","regular_price","promo_price","invoice_price","discount","capacity","url","in_stock"])
        writer.writerows(results)

    print(f"Saved {len(results)} products to: {out_path}")

extra_scraper(url)
