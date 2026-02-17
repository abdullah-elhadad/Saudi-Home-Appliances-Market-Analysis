from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager 
from bs4 import BeautifulSoup
import csv
import time
import re

def get_channel(url):
    return "alkhunaizan"

category_name = input("Enter category in English: ") 
url = f"https://www.alkhunaizan.sa/en/search?q={category_name}"

def alkhunaizan_scraper(link):
    service = Service(ChromeDriverManager().install())
    browser = webdriver.Chrome(service=service)

    browser.get(link)
    time.sleep(3)

    results = []
    channel = get_channel(link)


    last_height = browser.execute_script("return document.body.scrollHeight")
    scroll_count = 0
    while True:
        browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(5)
        new_height = browser.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height
        scroll_count += 1
        if scroll_count > 25:  # safety limit
            break

  
    html = browser.page_source
    soup = BeautifulSoup(html, 'html.parser')

    product_list = soup.select('a.line-clamp-3[href^="/en/product/"]')

    for product in product_list:
        # product name
        try:
            product_name = product.get_text(strip=True)
        except:
            product_name = "no product name"

     
        try:
            words = product_name.split()
            brand = words[1] if len(words) > 1 else "no brand"
        except:
            brand = "no brand"

        # capacity 
        try:

            capacity = "no capacity"
            match = re.search(r"(\d+)\s*(Kg|kg|L|l|feet|Feet|قدم)", product_name)
            if match:
                capacity = match.group(1)  # الرقم بس
            
            
        except:
            capacity = "no capacity"

        # product url
        try:
            relative_url = product.get("href")
            product_url = "https://www.alkhunaizan.sa" + relative_url if relative_url else "no url"
        except:
            product_url = "no url"

        # promo price
        try:
            promo_price_tag = product.find_next("span", class_="font-bold")
            promo_price = promo_price_tag.get_text(strip=True) if promo_price_tag else "no promo price"
        except:
            promo_price = "no promo price"

        # regular price
        try:
            regular_price_tag = product.find_next("span", class_=re.compile("line-through"))
            if regular_price_tag:
                regular_price = regular_price_tag.get_text(strip=True)
           
                regular_price = re.sub(r"[^\d.]", "", regular_price) 
            else:
                regular_price = "no regular price"
        except:
            regular_price = "no regular price"

        # discount
        try:
            discount_tag = product.find_next("div", string=re.compile("% Off"))
            discount = discount_tag.get_text(strip=True) if discount_tag else "no discount"
        except:
            discount = "no discount"

        in_stock = True if product else False
        invoice_price = promo_price

        item = [channel, brand, category_name, product_name, regular_price, promo_price, invoice_price, discount, capacity, product_url, in_stock]
        if item not in results:
            results.append(item)

    browser.quit()

  
    out_path = r"C:\Users\abdul\Downloads\alkhunaizan_products_full233.csv"
    with open(out_path, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f)
        writer.writerow(["channel","brand","category","product_name","regular_price","promo_price","invoice_price","discount","capacity","url","in_stock"])
        writer.writerows(results)

    print(f"Saved {len(results)} products to: {out_path}")

alkhunaizan_scraper(url)
