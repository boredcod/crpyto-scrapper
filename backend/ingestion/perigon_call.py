import requests
from dotenv import load_dotenv
import os

load_dotenv()

headers = {
  "Content-Type": "application/json"
}

PERIGON_API_KEY = os.getenv('PERIGON_API_KEY')
URL=f"https://api.perigon.io/v1/articles/all?q=Crypto%20Currency%20OR%20Bitcoin&from=2026-01-24T00%3A00%3A00&&apiKey={PERIGON_API_KEY}"
def getPerigonCall():
    try:
        response = requests.get(URL, headers=headers)
        response.raise_for_status()  # Raise an HTTPError for bad responses (4xx and 5xx)
        # print(response.json())
        return response.json()
    except Exception as e:
        print(f"An error occurred: {e}")

