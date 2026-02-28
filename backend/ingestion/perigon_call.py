import requests
from dotenv import load_dotenv
import os
from datetime import datetime, timedelta

load_dotenv()

headers = {
  "Content-Type": "application/json"
}

PERIGON_API_KEY = os.getenv('PERIGON_API_KEY')

def getPerigonCall(days):
    # Calculate the date range based on the number of days provided
    to_date = datetime.utcnow()
    from_date = to_date - timedelta(days=days)

    # Format the dates to always include T00:00:00 for the entire day
    to_date_str = to_date.strftime('%Y-%m-%dT00:00:00')
    from_date_str = from_date.strftime('%Y-%m-%dT00:00:00')

    URL = f"https://api.perigon.io/v1/articles/all?q=Crypto%20Currency%20OR%20Bitcoin&from={from_date_str}&to={to_date_str}&sortBy=relevance&showNumResults=false&page=0&size=100&showReprints=false&apiKey={PERIGON_API_KEY}"

    print(URL)
    try:
        response = requests.get(URL, headers=headers)
        response.raise_for_status()  # Raise an HTTPError for bad responses (4xx and 5xx)
        return response.json()
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

