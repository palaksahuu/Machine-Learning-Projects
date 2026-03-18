from langchain.prompts import ChatPromptTemplate
import google.generativeai as genai
import os

# Configure Gemini API
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

itinerary_prompt = ChatPromptTemplate.from_messages([
    ("system", """Create detailed itinerary for {destination} from {start_date} to {end_date}.
Budget: {budget}. Style: {travel_style}. Preferences: {preferences}.
Include:
1. Time-specific activities with durations
2. Logical geographic grouping
3. Transportation options
4. Cost estimates"""),
])

def generate_itinerary(request, activities):
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(itinerary_prompt.format(
        destination=request.destination,
        start_date=request.start_date,
        end_date=request.end_date,
        budget=request.budget,
        travel_style=request.travel_style,
        preferences=request.preferences
    ))

    return response.text if response else "Failed to generate itinerary"
