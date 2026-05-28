# Dublin Restaurant Recommender 🍽️

A data-driven restaurant recommendation system for Dublin, built with Python.

## Features
- Fetches real-time restaurant data via Google Places API
- Filters by cuisine, price range, and number of results
- Recommends restaurants using a scoring algorithm (rating + popularity)
- Interactive web app built with Streamlit

## Tech Stack
- Python 3.13
- Google Places API
- pandas, scikit-learn
- Streamlit

## How to Run
1. Clone the repo
2. Install dependencies: `pip install -r requirements.txt`
3. Add your Google API key to `.env`: `GOOGLE_API_KEY=your_key_here`
4. Fetch data: `python fetch_restaurants.py`
5. Run the app: `streamlit run app.py`

## Project Structure
- `fetch_restaurants.py` — fetches restaurant data from Google Places API
- `analyse_restaurants.py` — exploratory data analysis and visualisation
- `recommender.py` — recommendation algorithm
- `app.py` — Streamlit web application
