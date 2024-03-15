from flask import Flask, render_template, jsonify
import requests
from operator import itemgetter
import pandas as pd

app = Flask(__name__)

@app.route("/")
def index():
    location = "San Francisco, CA"
    merchants = get_merchants_with_reviews(location)
    return render_template("Search.html", merchants=merchants)

def get_merchants(location):
    url = f"https://api.yelp.com/v3/businesses/search?location={location}"
    headers = {"Authorization": "Bearer YOUR_API_KEY"}
    response = requests.get(url, headers=headers)
    data = response.json()
    return data["businesses"]

def get_reviews(merchant_id):
    url = f"https://api.yelp.com/v3/businesses/{merchant_id}/reviews"
    headers = {"Authorization": "Bearer YOUR_API_KEY"}
    response = requests.get(url, headers=headers)
    data = response.json()
    return data["reviews"]

def get_merchants_with_reviews(location):
    merchants = get_merchants(location)
    merchants_with_reviews = []
    for merchant in merchants:
        reviews = get_reviews(merchant["id"])
        merchant["reviews"] = reviews
        merchants_with_reviews.append(merchant)
    return merchants_with_reviews

if __name__ == "__main__":
    app.run(debug=True)