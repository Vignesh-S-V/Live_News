from flask import Flask, jsonify, request
import requests

app = Flask(__name__)
NEWS_API_KEY = "pub_37e638a7c3134ec8b53398d9e929f1a8"

@app.route("/api/news")
def get_news():
    year = request.args.get("year")
    month = request.args.get("month")
    r = requests.get(f"https://newsdata.io/api/1/news?apikey={NEWS_API_KEY}&country=in")
    articles = r.json().get("results", [])
    if year:
        articles = [a for a in articles if a.get("pubDate","").startswith(year)]
    return jsonify(articles)

if __name__ == "__main__":
    app.run(debug=True, port=5000)
