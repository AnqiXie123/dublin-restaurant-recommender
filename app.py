import streamlit as st
import pandas as pd
from sklearn.preprocessing import MinMaxScaler

st.set_page_config(page_title="Dublin Restaurant Recommender", page_icon="🍽️", layout="wide")

@st.cache_data
def load_data():
    df = pd.read_csv("restaurants.csv")
    df["price_level"] = df["price_level"].replace({
        "PRICE_LEVEL_INEXPENSIVE": 1,
        "PRICE_LEVEL_MODERATE": 2,
        "PRICE_LEVEL_EXPENSIVE": 3,
    }).fillna(2)
    scaler = MinMaxScaler()
    df["rating_score"] = scaler.fit_transform(df[["rating"]])
    df["popularity_score"] = scaler.fit_transform(df[["review_count"]])
    df["score"] = df["rating_score"] * 0.6 + df["popularity_score"] * 0.4
    return df

df = load_data()

st.title("🍽️ Dublin Restaurant Recommender")
st.markdown("Find the best restaurants in Dublin based on your preferences.")

col1, col2, col3 = st.columns(3)

with col1:
    cuisine_options = ["All"] + sorted(df["cuisine"].unique().tolist())
    cuisine = st.selectbox("Cuisine", cuisine_options)

with col2:
    price = st.selectbox("Max Price", ["Any", "€ (Budget)", "€€ (Moderate)", "€€€ (Expensive)"])

with col3:
    top_n = st.slider("Number of results", 3, 20, 5)

results = df.copy()
if cuisine != "All":
    results = results[results["cuisine"] == cuisine]
if price == "€ (Budget)":
    results = results[results["price_level"] <= 1]
elif price == "€€ (Moderate)":
    results = results[results["price_level"] <= 2]
elif price == "€€€ (Expensive)":
    results = results[results["price_level"] <= 3]

results = results.sort_values("score", ascending=False).head(top_n)

st.markdown(f"### Top {len(results)} Restaurants")

for _, row in results.iterrows():
    price_map = {1: "€", 2: "€€", 3: "€€€"}
    price_str = price_map.get(row["price_level"], "Unknown")
    with st.expander(f"⭐ {row['rating']} — {row['name']} ({row['cuisine']}) {price_str}"):
        st.write(f"📍 {row['address']}")
        st.write(f"👥 {int(row['review_count'])} reviews")
        if pd.notna(row["website"]) and row["website"] != "nan":
            st.markdown(f"[🔗 Visit Website]({row['website']})")