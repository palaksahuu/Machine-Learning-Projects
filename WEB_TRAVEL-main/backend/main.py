from fastapi import FastAPI, HTTPException, Request
from dotenv import load_dotenv
import os
import google.generativeai as genai  # Import Gemini API SDK

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise RuntimeError("Missing GEMINI_API_KEY. Set it as an environment variable.")

# Configure Gemini API
genai.configure(api_key=GEMINI_API_KEY)

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Welcome to the AI Travel Assistant!"}

# ✅ Allow GET requests for testing (Returns a sample itinerary)
@app.get("/generate-itinerary/")
def get_sample_itinerary():
    return {"itinerary": "Sample itinerary: 3 days in Paris, exploring cafes, museums, and the Eiffel Tower."}

# ✅ Keep POST for actual itinerary generation
@app.post("/generate-itinerary/")
async def generate_itinerary(request_data: dict):
    try:
        destination = request_data.get("destination")
        budget = request_data.get("budget")
        travel_style = request_data.get("travel_style")

        if not destination or not budget or not travel_style:
            raise HTTPException(status_code=400, detail="Missing required fields!")

        prompt = f"Generate a detailed {budget} travel itinerary for {destination} focusing on {travel_style} experiences."

        # Call Gemini API for itinerary generation
        model = genai.GenerativeModel("gemini-1.5-pro-latest")  
        response = model.generate_content(prompt)

        if response and hasattr(response, "candidates"):
            return {"itinerary": response.candidates[0].text}
        else:
            raise HTTPException(status_code=500, detail="Failed to generate itinerary.")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
