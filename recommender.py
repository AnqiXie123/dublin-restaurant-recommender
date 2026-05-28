import pandas as pd
from sklearn.preprocessing import MinMaxScaler

df = pd.read_csv("restaurants.csv")

# Clean price level
df["price_level"] = df["price_level"].replace({
    "PRICE_LEVEL_INEXPENSIVE": 1,
    "PRICE_LEVEL_MODERATE": 2,
    "PRICE_LEVEL_EXPENSIVE": 3,
}).fillna(2)

# Normalize rating and review count
scaler = MinMaxScaler()
df["rating_score"] = scaler.fit_transform(df[["rating"]])
df["popularity_score"] = scaler.fit_transform(df[["review_count"]])

# Composite score
df["score"] = df["rating_score"] * 0.6 + df["popularity_score"] * 0.4

def recommend(cuisine=None, max_price=None, top_n=5):
    results = df.copy()

    if cuisine:
        results = results[results["cuisine"].str.lower() == cuisine.lower()]

    if max_price:
        results = results[results["price_level"] <= max_price]

    results = results.sort_values("score", ascending=False).head(top_n)

    print(f"\n=== Top {top_n} Recommendations ===")
    if cuisine:
        print(f"Cuisine: {cuisine}")
    if max_price:
        price_map = {1: "€", 2: "€€", 3: "€€€"}
        print(f"Max price: {price_map.get(max_price)}")
    print()

    for i, row in results.iterrows():
        price_map = {1: "€", 2: "€€", 3: "€€€", 2.0: "€€"}
        price = price_map.get(row["price_level"], "Unknown")
        print(f"{row['name']}")
        print(f"  Cuisine: {row['cuisine']} | Rating: {row['rating']} | Price: {price}")
        print(f"  Address: {row['address']}")
        if row["website"]:
            print(f"  Website: {row['website']}")
        print()

if __name__ == "__main__":
    # Test 1: best Japanese restaurants
    recommend(cuisine="Japanese", top_n=5)

    # Test 2: best budget options (€ or €€)
    recommend(max_price=2, top_n=5)

    # Test 3: best overall
    recommend(top_n=5)