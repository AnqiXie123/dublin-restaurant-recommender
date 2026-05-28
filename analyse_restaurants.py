import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("restaurants.csv")

# Clean price level
df["price_level"] = df["price_level"].replace({
    "PRICE_LEVEL_INEXPENSIVE": "€",
    "PRICE_LEVEL_MODERATE": "€€",
    "PRICE_LEVEL_EXPENSIVE": "€€€",
    "": "Unknown"
}).fillna("Unknown")

# Basic stats
print("=== Dataset Overview ===")
print(f"Total restaurants: {len(df)}")
print(f"Average rating: {df['rating'].mean():.2f}")
print(f"Cuisines: {df['cuisine'].nunique()}")

print("\n=== Top 10 Highest Rated (min 500 reviews) ===")
top = df[df["review_count"] >= 500].sort_values("rating", ascending=False).head(10)
print(top[["name", "cuisine", "rating", "review_count", "price_level"]].to_string())

print("\n=== Average Rating by Cuisine ===")
cuisine_stats = df.groupby("cuisine").agg(
    avg_rating=("rating", "mean"),
    count=("name", "count")
).sort_values("avg_rating", ascending=False)
print(cuisine_stats.round(2))

# Plot
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# Chart 1: avg rating by cuisine
cuisine_stats["avg_rating"].plot(kind="bar", ax=axes[0], color="steelblue")
axes[0].set_title("Average Rating by Cuisine")
axes[0].set_ylabel("Rating")
axes[0].set_ylim(3.5, 5.0)
axes[0].tick_params(axis="x", rotation=45)

# Chart 2: rating distribution
df["rating"].hist(bins=15, ax=axes[1], color="coral", edgecolor="white")
axes[1].set_title("Rating Distribution")
axes[1].set_xlabel("Rating")
axes[1].set_ylabel("Count")

plt.tight_layout()
plt.savefig("analysis.png", dpi=150)
plt.show()
print("\nChart saved to analysis.png")