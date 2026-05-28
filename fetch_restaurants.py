import requests
import pandas as pd

from dotenv import load_dotenv
import os
load_dotenv()
API_KEY = os.getenv("GOOGLE_API_KEY")


CUISINES = [
    "Italian", "Chinese", "Indian", "Japanese", "Mexican",
    "Thai", "French", "Irish", "Mediterranean", "Vietnamese"
]

def fetch_by_query(query, api_key):
    url = "https://places.googleapis.com/v1/places:searchText"
    headers = {
        "Content-Type": "application/json",
        "X-Goog-Api-Key": api_key,
        "X-Goog-FieldMask": "places.displayName,places.formattedAddress,places.rating,places.userRatingCount,places.priceLevel,places.websiteUri,places.primaryTypeDisplayName,places.location"
    }
    body = {
        "textQuery": query,
        "maxResultCount": 20,
        "locationBias": {
            "circle": {
                "center": {"latitude": 53.3498, "longitude": -6.2603},
                "radius": 5000.0
            }
        }
    }
    response = requests.post(url, headers=headers, json=body)
    data = response.json()
    results = []
    if "places" in data:
        for place in data["places"]:
            results.append({
                "name": place.get("displayName", {}).get("text", ""),
                "address": place.get("formattedAddress", ""),
                "cuisine": query.split(" restaurants")[0],
                "rating": place.get("rating", None),
                "review_count": place.get("userRatingCount", 0),
                "price_level": place.get("priceLevel", ""),
                "website": place.get("websiteUri", ""),
                "lat": place.get("location", {}).get("latitude", None),
                "lng": place.get("location", {}).get("longitude", None),
            })
    return results

def fetch_all_restaurants():
    all_results = []
    for cuisine in CUISINES:
        query = f"{cuisine} restaurants in Dublin Ireland"
        print(f"Fetching {cuisine}...")
        results = fetch_by_query(query, API_KEY)
        all_results.extend(results)
        print(f"  Got {len(results)} results")

    df = pd.DataFrame(all_results)
    df = df.drop_duplicates(subset=["name", "address"])
    df = df[df["rating"].notna()]
    df = df.reset_index(drop=True)
    df.to_csv("restaurants.csv", index=False)
    print(f"\nTotal unique restaurants: {len(df)}")
    print(df.head(10))
    return df

if __name__ == "__main__":
    fetch_all_restaurants()