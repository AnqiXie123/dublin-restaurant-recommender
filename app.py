import streamlit as st
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from math import radians, sin, cos, sqrt, atan2

st.set_page_config(page_title="Dublin Restaurant Recommender", page_icon="🍽️", layout="wide")

@st.cache_data
def load_data():
    df = pd.read_csv("restaurants.csv")
    df["price_level"] = df["price_level"].replace({
        "PRICE_LEVEL_INEXPENSIVE": 1,
        "PRICE_LEVEL_MODERATE": 2,
        "PRICE_LEVEL_EXPENSIVE": 3,
    }).fillna(2)
    df["price_level"] = pd.to_numeric(df["price_level"], errors="coerce").fillna(2).astype(int)
    scaler = MinMaxScaler()
    df["rating_score"] = scaler.fit_transform(df[["rating"]])
    df["popularity_score"] = scaler.fit_transform(df[["review_count"]])
    df["score"] = df["rating_score"] * 0.6 + df["popularity_score"] * 0.4
    return df

df = load_data()

st.title("🍽️ Dublin Restaurant Recommender")
st.markdown("Find the best restaurants in Dublin based on your preferences.")

col1, col2, col3, col4 = st.columns(4)

with col1:
    cuisine_options = ["All"] + sorted(df["cuisine"].unique().tolist())
    cuisine = st.selectbox("Cuisine", cuisine_options)

with col2:
    price = st.selectbox("Max Price", ["Any", "€ (Budget)", "€€ (Moderate)", "€€€ (Expensive)"])

with col3:
    top_n = st.slider("Number of results", 3, 20, 5)

with col4:
    area_coords = {
        "City Centre": (53.3498, -6.2603),
        "Temple Bar": (53.3454, -6.2672),
        "Rathmines": (53.3239, -6.2650),
        "Ranelagh": (53.3195, -6.2511),
        "Drumcondra": (53.3633, -6.2583),
        "Ballsbridge": (53.3289, -6.2302),
        "Belfield/UCD": (53.3066, -6.2236),
        "Stoneybatter": (53.3506, -6.2822),
        "Phibsborough": (53.3622, -6.2724),
        "Clontarf": (53.3593, -6.1958),
        "Dún Laoghaire": (53.2950, -6.1356),
        "Sandyford": (53.2793, -6.2193),
        "Glasnevin": (53.3660, -6.2719),
        "Portobello": (53.3334, -6.2657),
        "Smithfield": (53.3486, -6.2783),
        "IFSC/Docklands": (53.3497, -6.2434),
        "Tallaght": (53.2882, -6.3744),
        "Lucan": (53.3589, -6.4497),
        "Swords": (53.4597, -6.2181),
        "Malahide": (53.4509, -6.1543),
        "Home": (53.303571798189324, -6.237714073737056)
    }
    area = st.selectbox("Your area", list(area_coords.keys()))
    max_distance = st.slider("Max distance (km)", 1, 10, 3)

results = df.copy()

def haversine(lat1, lng1, lat2, lng2):
    R = 6371
    lat1, lng1, lat2, lng2 = map(radians, [lat1, lng1, lat2, lng2])
    dlat = lat2 - lat1
    dlng = lng2 - lng1
    a = sin(dlat/2)**2 + cos(lat1)*cos(lat2)*sin(dlng/2)**2
    return R * 2 * atan2(sqrt(a), sqrt(1-a))

user_lat, user_lng = area_coords[area]
results["distance_km"] = results.apply(
    lambda r: haversine(user_lat, user_lng, r["lat"], r["lng"]), axis=1
)
results = results[results["distance_km"] <= max_distance]

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


# Map
st.markdown("### 📍 Map")

import streamlit.components.v1 as components

map_data = results[["lat", "lng", "name", "rating", "cuisine"]].dropna()

markers_js = ""
for _, row in map_data.iterrows():
    markers_js += f"""
    L.circleMarker([{row['lat']}, {row['lng']}], {{
        color: '#ff4b4b', fillColor: '#ff4b4b', fillOpacity: 0.8, radius: 8
    }}).addTo(map).bindPopup("<b>{row['name']}</b><br>{row['cuisine']} | ⭐ {row['rating']}");
    """

map_html = f"""
<!DOCTYPE html>
<html>
<head>
    <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css"/>
    <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
    <style>body{{margin:0}} #map{{height:450px;width:100%}}</style>
</head>
<body>
<div id="map"></div>
<script>
    var map = L.map('map').setView([53.3498, -6.2603], 13);
    L.tileLayer('https://{{s}}.tile.openstreetmap.org/{{z}}/{{x}}/{{y}}.png', {{
        attribution: '© OpenStreetMap contributors'
    }}).addTo(map);
    
    var userMarker = L.circleMarker([53.3498, -6.2603], {{
        color: '#0078ff', fillColor: '#0078ff', fillOpacity: 1, radius: 10
    }}).addTo(map).bindPopup("You are here");
    
    if (navigator.geolocation) {{
        navigator.geolocation.getCurrentPosition(function(pos) {{
            var lat = pos.coords.latitude;
            var lng = pos.coords.longitude;
            userMarker.setLatLng([lat, lng]).bindPopup("You are here").openPopup();
            map.setView([lat, lng], 14);
        }});
    }}
    
    {markers_js}
</script>
</body>
</html>
"""

components.html(map_html, height=450)
st.caption("🔴 Restaurants   🔵streamlit run app.py Your location")