from flask import Flask, jsonify, request
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)  # allows your GitHub Pages site to call this backend from the browser

# You said you already enabled this — keep it here, never in the frontend HTML.
NEWS_API_KEY = "pub_37e638a7c3134ec8b53398d9e929f1a8"

NEWSDATA_URL = "https://newsdata.io/api/1/news"


@app.route("/api/news")
def get_news():
    category = request.args.get("category")   # top, business, sports, technology, environment, politics, world
    state = request.args.get("state")          # e.g. "Tamil Nadu" — NewsData free tier has no state param,
                                                 # so we fold it into the search query instead.
    language = request.args.get("language", "en")

    params = {
        "apikey": NEWS_API_KEY,
        "country": "in",
        "language": language,
    }
    if category and category != "top":
        params["category"] = category
    if state:
        params["q"] = state

    try:
        r = requests.get(NEWSDATA_URL, params=params, timeout=10)
        r.raise_for_status()
        data = r.json()
        return jsonify(data.get("results", []))
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 502


if __name__ == "__main__":
    app.run(debug=True, port=5000)
