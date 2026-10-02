from datetime import date
import time
import cloudscraper
import pandas as pd
from bs4 import BeautifulSoup

scraper = cloudscraper.create_scraper(
    browser={"browser": "chrome", "platform": "windows", "desktop": True}
)

def get_text(tag):
    return tag.get_text(strip=True) if tag else None

def clean_price(text):
    if text is None:
        return None
    try:
        return float(text.replace("₦", "").replace(",", "").strip())
    except ValueError:
        return None

def scrape_page(page_number):
    url = f"https://www.jumia.com.ng/health-beauty/?page={page_number}"

    for attempt in range(3):
        response = scraper.get(url)
        if response.status_code == 200:
            break
        print(f"Page {page_number}, attempt {attempt + 1} -> {response.status_code}")
        time.sleep(5)
    else:
        print(f"Gave up on page {page_number}")
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    rows = []

    for card in soup.select("article.prd"):
        # the real product link, not the wishlist button
        a = card.select_one("a.core") or card.find("a")
        if a is None:
            continue
        price_tag = card.select_one("div.prc")

        rows.append({
            "id": a.get("data-ga4-item_id"),
            "name": a.get("data-ga4-item_name") or get_text(card.select_one(".name")),
            "brand": a.get("data-ga4-item_brand"),
            "price": clean_price(get_text(price_tag)),
            "old_price": clean_price(price_tag.get("data-oprc") if price_tag else None),
            "discount": get_text(card.select_one("div.bdg")),
            "category3": a.get("data-ga4-item_category3"),
            "category4": a.get("data-ga4-item_category4"),
            "category5": a.get("data-ga4-item_category5"),
            "review_count": a.get("data-gtm-dimension26"),
            "rating": a.get("data-gtm-dimension27"),
            "link": a.get("href"),
            "page": page_number,
        })
    return rows

# scrape pages 1 to 25
all_rows = []
for page in range(1, 26):
    rows = scrape_page(page)
    print("Page", page, "->", len(rows), "cards")
    all_rows.extend(rows)
    time.sleep(4)  # be polite to the site

# build the table and clean it
df = pd.DataFrame(all_rows).drop_duplicates(subset="id")
df["rating"] = pd.to_numeric(df["rating"], errors="coerce")
df["review_count"] = pd.to_numeric(df["review_count"], errors="coerce")
df["scraped_on"] = date.today().isoformat()

# save to a NEW file so the old one is not overwritten
df.to_csv("jumia_health_beauty.csv", index=False, encoding="utf-8-sig")
print("Saved", len(df), "rows")

# checks
print("Shape:", df.shape)
print("Missing names:", df["name"].isna().sum())
print("Missing prices:", df["price"].isna().sum())
print("Products with a rating:", df["rating"].notna().sum())

skin = df[df["category4"] == "Skin Care"]
print("Skin Care products:", len(skin))
print("Skin Care with a rating:", skin["rating"].notna().sum())

print(df[["rating", "review_count"]].describe())