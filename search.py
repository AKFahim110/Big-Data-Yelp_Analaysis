import requests
from operator import itemgetter
import pandas as pd

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

def sort_merchants(merchants, sort_by):
    if sort_by == "review recommendations":
        sorted_merchants = sorted(merchants, key=lambda x: len(x["reviews"]), reverse=True)
    elif sort_by == "distance":
        sorted_merchants = sorted(merchants, key=lambda x: x["distance"], reverse=True)
    elif sort_by == "ratings":
        sorted_merchants = sorted(merchants, key=lambda x: x["rating"], reverse=True)
    return sorted_merchants

def filter_merchants(merchants, filter_by):
    if filter_by == "distance":
        filtered_merchants = [merchant for merchant in merchants if