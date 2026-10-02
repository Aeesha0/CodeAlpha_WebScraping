# CodeAlpha Task 1: Web Scraping (Jumia Skincare Products)

## What this project does
I scraped product data from Jumia Nigeria's Health & Beauty category and filtered it down to a clean skincare dataset. I'll use this dataset for my EDA and visualization tasks.

## Data source
Scraped from jumia.com.ng (Health & Beauty, pages 1 to 25) on 24 September 2026.
Jumia is a live site, so prices, ratings and sponsored products change between runs. This is a snapshot from that date.

## Tools used
- Python
- cloudscraper (to get past Jumia's bot check)
- BeautifulSoup (to read the product cards in the page HTML)
- pandas (to build and clean the dataset)

## How it works
1. `scrape_pages.py` loads 25 category pages, reads every product card, and saves 1,048 unique products to `jumia_health_beauty.csv`.
2. `filter_skincare.py` keeps the skincare products and saves them to `jumia_skincare.csv`.

## Columns
id, name, brand, price, old_price, discount, category3, category4, category5, review_count, rating, link, page, scraped_on

## Problems I ran into and how I fixed them
- **Bot check:** my first request got a 403 "Just a moment..." page. I fixed it with a Chrome browser profile and retries with pauses.
- **Blank ratings and names after page 1:** my code was reading the wishlist heart button instead of the real product link. Switching to the correct tag (`a.core`) took rated products from 113 to 964.
- **Duplicates:** sponsored slots repeat products, so I removed duplicates using the product ID.
- **Missing prices:** 16 products (bundles and variants) had no single price, so I left them blank. None of them are skincare.
- **Messy categories:** Jumia's labels are not always right, and some face serums were filed under "Hair Care". I kept "Skin Care" and "Baby Skin Care", left out "Skin Care Tools" (they're devices, not products), and rescued 7 misfiled skincare products by name.

## Results
- 1,048 unique products scraped
- 159 skincare products after filtering
- 150 of them have ratings

## Files
- `scrape_pages.py`: the scraper
- `filter_skincare.py`: the skincare filter
- `jumia_health_beauty.csv`: all products scraped
- `jumia_skincare.csv`: the skincare dataset used for the next tasks
