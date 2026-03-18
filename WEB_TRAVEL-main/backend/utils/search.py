
import requests

class GoogleSearchAPI:
    def __init__(self, api_key):
        self.api_key = api_key

    def search(self, query):
        url = f"https://www.googleapis.com/customsearch/v1"
        params = {
            "q": query,
            "key": self.api_key,
            "cx": "YOUR_CX_ID"
        }
        response = requests.get(url, params=params)
        return response.json()


class TripAdvisorAPI:
    def __init__(self, api_key):
        self.api_key = api_key
    
    def search_hotels(self, location):
        url = "https://tripadvisor16.p.rapidapi.com/api/v1/hotels/searchLocation"
        headers = {
            "X-RapidAPI-Key": self.api_key,
            "X-RapidAPI-Host": "tripadvisor16.p.rapidapi.com"
        }
        params = {"query": location}
        response = requests.get(url, headers=headers, params=params)
        return response.json()
