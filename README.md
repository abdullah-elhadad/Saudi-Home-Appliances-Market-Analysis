# 🇸🇦 Saudi Home Appliances Market Analysis (End-to-End Project)

## 📌 Project Overview
This project focuses on analyzing the home appliances market in Saudi Arabia by scraping data from the top 4 retailers: Almanea, Extra, Alkhunaizan, and BHStore. The project covers the entire data pipeline: from automated web scraping to deep data cleaning in Excel, and finally, building a professional interactive dashboard in Power BI.

The analysis aims to answer key business questions such as:

- Which retailer offers the most competitive prices and highest discounts?
- Which brands dominate the Saudi market in the Washing Machines and Refrigerators categories?
- What is the price gap for the same brand across different platforms?

---

## 📂 Dataset Description
The dataset was built from scratch and processed through multiple stages:

- **Raw Data (Scraped):** 4 CSV files (one for each site) containing product names, prices (regular & promo), brands, and categories.
- **Processed Files:** Individual Excel workbooks for each retailer where data was standardized and cleaned.
- **Master Dataset:** A consolidated dataset (Appended) created during the project to facilitate cross-market comparison.

---

## ⚙️ Methodology
The project followed these main steps:

1. **Web Scraping (Python & Selenium):** Developed 4 custom scripts to handle dynamic content, scrolling, and pagination across different site architectures.

2. **Data Cleaning & Transformation (Excel Power Query):**
   - Removing duplicates and handling missing values.
   - Standardizing inconsistent category names (e.g., fixing "Refrigerators" vs "Refrigerator").
   - Merging categories (Washing Machines & Refrigerators) for each site.

3. **Data Integration:** Using Append queries to combine all retailers into one "Master Table".

4. **Final Dashboard (Power BI):** Building an interactive dashboard with DAX measures, KPIs, and advanced visuals.

---

## 🔍 Exploratory Analysis (Excel & Power Query)
During the cleaning phase in Excel, specific questions were addressed:

- How to handle the "Inconsistency" in brand naming across sites?
- How to extract the "Capacity" (Kg/Liters) from product titles using Regex and Power Query?
- Standardizing the "Discount Percentage" to be a unified numerical field.

---

## 📊 Final Dashboard
The interactive Power BI dashboard provides a 360-degree view of the market:

### Key Performance Indicators (KPIs)
- Total Market Inventory (1.68K+ products)
- Average Market Savings (40.38%)
- Brand Variety (72 Brands)
- Number of Monitored Websites (4)

### Market Insights
- **Price Share by Retailer:** Comparing average prices across stores.
- **Discount Leaderboard:** Identifying which site is the "King of Offers".
- **Brand Pricing Index:** Ranking brands from "Premium" to "Budget-friendly".
- **Availability Matrix:** A detailed grid showing which brands are exclusive to certain retailers.

### Interactivity
- Slicers for Category (Refrigerator/Washing machines), Channel, and Brand.

---

## 🖼️ Visuals & Preview
The dashboard layout is designed for clarity and professional storytelling.

**Main Market Dashboard (KPIs, Charts, and Filters)**  
(Insert your Dashboard Screenshot Here)

**Data Transformation Process (Power Query & Excel)**  
(Insert a screenshot of your Excel Sheets or Power Query steps)

---

## 💡 Key Insights
- **Discount Trends:** The market shows a high average discount rate (~40%), with specific retailers like Alkhunaizan leading in aggressive pricing.
- **Brand Dominance:** A few global brands (Samsung, LG) have a massive presence, but local or budget-friendly brands are catching up in specific stores.
- **Pricing Strategy:** There is a noticeable price variance for the same product category between retailers, suggesting high competition.

---

## 🛠️ Tools Used
- Python (Selenium & BeautifulSoup): Automated Data Extraction.
- Excel Power Query: Data cleaning, standardization, and merging.
- Power BI: Data modeling (DAX) and interactive visualizations.

---

## 📁 Project Files
- `Scrapers/`: Python scripts for the 4 websites.
- `Cleaned_Data/`: Final Excel workbooks after Power Query processing.
- `Market_Analysis.pbix`: The full Power BI project file.
