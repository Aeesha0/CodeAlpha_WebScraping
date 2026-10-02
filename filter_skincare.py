import pandas as pd

df = pd.read_csv("jumia_health_beauty.csv")
print("All products:", len(df))

# 1. products Jumia labelled as skincare
# (add "Skin Care Tools" to this list if you want the gadgets included)
labelled = df["category4"].isin(["Skin Care", "Baby Skin Care"])

# 2. skincare that Jumia filed under the wrong category, found by name
keywords = "face serum|facial toner|body cream|face day care"
by_name = (
    df["name"].str.contains(keywords, case=False, na=False)
    & ~df["name"].str.contains("hair", case=False, na=False)
)

skincare = df[labelled | by_name].drop_duplicates(subset="id")

print("Labelled skincare:", labelled.sum())
print("Rescued by name:", (by_name & ~labelled).sum())
print("Final skincare products:", len(skincare))
print("With a rating:", skincare["rating"].notna().sum())
print("Missing price:", skincare["price"].isna().sum())

skincare.to_csv("jumia_skincare.csv", index=False, encoding="utf-8-sig")
print("Saved jumia_skincare.csv")
