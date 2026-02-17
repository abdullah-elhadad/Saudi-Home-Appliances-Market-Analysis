from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager 
from bs4 import BeautifulSoup
import csv
import time


def get_channel(url):
    return "almanea"


category_name = input("ادخل اسم القسم بالانجليزي: ") 
url = f"https://www.almanea.sa/en/search?q={category_name}"

def get_regular_price(product):
    try:
        el = product.select_one('p[class*="line-through"] span.font-semibold')
        if el:
            return el.get_text(strip=True)
        for span in product.select('span.font-semibold'):
            parent_p = span.find_parent('p')
            if parent_p and 'line-through' in (parent_p.get('class') or []):
                return span.get_text(strip=True)
    except:
        pass
    return "no regular_price"

def get_prom_price(product):
    try:
        el = product.select_one('p[class*="text-red"] span.font-semibold')
        if el:
            return el.get_text(strip=True)
        for span in product.select('span.font-semibold'):
            parent_p = span.find_parent('p')
            classes = parent_p.get('class', []) if parent_p else []
            if not any('line-through' in c for c in classes):
                return span.get_text(strip=True)
        spans = product.select('span.font-semibold')
        if spans:
            return spans[-1].get_text(strip=True)
    except:
        pass
    return "no prom_price"

def almanea(link):
    service = Service(ChromeDriverManager().install())
    browser = webdriver.Chrome(service=service)
    wait = WebDriverWait(browser, 10)

    browser.get(link)
    time.sleep(3)

    results = []
    channel = get_channel(link)

    while True:
        html = browser.page_source
        soup = BeautifulSoup(html, 'html.parser')
        product_list = soup.find_all('div', class_='rounded-xl')

        for product in product_list:
            try:
                product_brand = product.select_one('p.text-sm.text-zinc-500').get_text(strip=True)
            except:
                product_brand = 'no brand found'

            try:
                name_el = product.select_one('span.mx-2')
                product_name = name_el.get_text(strip=True) if name_el else 'no product name found'
            except:
                product_name = 'no product name found'

            regular_price = get_regular_price(product)
            prom_price = get_prom_price(product)
            invoice_price = prom_price

         
            link_el = product.select_one('a.cursor-pointer')
            product_url = "https://www.almanea.sa" + link_el['href'] if link_el else "no link found"

            # in_stock
            in_stock = True if product else False

       
            try:
                discount_box = product.find('div', class_="h-4")
                product_discount = discount_box.get_text(strip=True) if discount_box else "no discount found"
            except:
                product_discount = 'no discount found'

    
            item = [channel, product_brand, category_name, product_name, regular_price, prom_price, invoice_price, product_discount, product_url, in_stock]
            if item not in results:
                results.append(item)

      
        try:
            next_btn = wait.until(EC.element_to_be_clickable((By.XPATH, '//button[@aria-label="Next page" and not(@disabled)]')))
            browser.execute_script("arguments[0].click();", next_btn)
            time.sleep(3)
        except:
            break

    browser.quit()

  
    out_path = r"C:\Users\abdul\Downloads\Washing_Machines.csv"
    with open(out_path, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f)
        writer.writerow(["channel","brand","category","product_name","regular_price","promo_price","invoice_price","discount","url","in_stock"])
        writer.writerows(results)

    print(f"تم حفظ {len(results)} منتج في: {out_path}")

almanea(url)
