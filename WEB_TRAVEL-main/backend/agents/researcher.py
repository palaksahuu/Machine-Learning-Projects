import sys
import os
import httpx
import asyncio

from backend.models.schemas import TravelRequest

# Add 
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))



from backend.utils.search import GoogleSearchAPI, TripAdvisorAPI

class GoogleSearchAPI:
    def __init__(self, client: httpx.AsyncClient, api_key: str):
        self.client = client
        self.api_key = api_key

    async def fetch(self, request: TravelRequest):
        query = f"{request.destination} {request.preferences or ''} activities"
        url = "https://www.googleapis.com/customsearch/v1"
        params = {
            "q": query,
            "key": self.api_key,
            "cx": "YOUR_CX_ID" 
        }
        response = await self.client.get(url, params=params)
        response.raise_for_status()  
        return response.json()


async def research_activities(request: TravelRequest):
    async with httpx.AsyncClient() as client:
        google_api = GoogleSearchAPI(client, api_key="YOUR_GOOGLE_API_KEY")
        tripadvisor_api = TripAdvisorAPI(client)

        google_results = google_api.fetch(request)
        tripadvisor_results = tripadvisor_api.fetch(request)

        results = await asyncio.gather(google_results, tripadvisor_results)
    
    return merge_results(*results)


def merge_results(*api_results):
    merged_results = []
    for result in api_results:
        if "items" in result:
            merged_results.extend(result["items"])
    return merged_results
