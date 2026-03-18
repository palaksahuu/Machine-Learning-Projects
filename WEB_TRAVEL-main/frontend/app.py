import streamlit as st
import httpx
import asyncio
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()


BACKEND_URL = "https://web-travel-29p1.onrender.com/" 

#  Correct Enum Mapping
budget_mapping = {
    "Budget": "budget",
    "Moderate": "moderate",
    "Luxury": "luxury"
}

travel_style_mapping = {
    "Adventure": "adventure",
    "Relaxation": "relaxation",
    "Cultural": "cultural",
    "Foodie": "foodie"
}

#  Validate User Inputs
def validate_inputs(destination, duration, budget, purpose, preferences):
    if not destination:
        st.error("Please enter a valid destination.")
        return False
    if duration <= 0:
        st.error("Trip duration must be at least 1 day.")
        return False
    if budget not in budget_mapping:
        st.error("Invalid budget selected.")
        return False
    if purpose not in travel_style_mapping:
        st.error("Invalid purpose. Choose from 'Adventure', 'Relaxation', 'Cultural', or 'Foodie'.")
        return False
    return True

async def fetch_itinerary(trip_data):
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                f"{BACKEND_URL}/generate-itinerary/", 
                json=trip_data,
                headers={"Content-Type": "application/json"},
            )
            response.raise_for_status()
            return response.json()
    except httpx.RequestError as e:
        st.error(f"Could not connect to backend: {str(e)}")
    except httpx.HTTPStatusError as e:
        st.error(f"Backend error: {e.response.text}")
    except Exception as e:
        st.error(f"Unexpected error: {str(e)}")
    return None

#  Main App Logic
def main():
    st.title("AI-Powered Travel Planner")

    #  Form Inputs
    destination = st.text_input("Destination:", "America")
    budget = st.selectbox("Select your budget:", ["Budget", "Moderate", "Luxury"], index=1)
    trip_duration = st.number_input("Trip Duration (in days):", min_value=1, max_value=30, value=15)
    start_location = st.text_input("Starting Location:", "Delhi")
    purpose = st.selectbox("Purpose of Travel:", ["Adventure", "Relaxation", "Cultural", "Foodie"], index=0)
    preferences = st.text_area("Preferences (e.g., activities, interests):", "")

    #  Button to Generate Itinerary
    if st.button("Generate Itinerary"):
        if not validate_inputs(destination, trip_duration, budget, purpose, preferences):
            return

        #  Date Calculation
        start_date = datetime.now().date()
        end_date = start_date + timedelta(days=trip_duration)

        #  Prepare Correct Payload for API
        trip_data = {
            "destination": destination,
            "trip_duration": trip_duration,
            "starting_location": start_location,
            "budget": budget_mapping[budget],
            "start_date": start_date.isoformat(),
            "end_date": end_date.isoformat(),
            "travel_style": [travel_style_mapping[purpose]],
            "preferences": preferences,
        }

        #  Show Loading Indicator
        with st.spinner("Creating your perfect itinerary..."):
            result = asyncio.run(fetch_itinerary(trip_data))

            if result and "itinerary" in result:
                st.success("Itinerary generated successfully! 🎉")

                #  Display Itinerary
                st.subheader("Your Personalized Itinerary")
                st.write(result["itinerary"])
            else:
                st.error("Failed to generate itinerary. Please check your inputs and try again.")


if __name__ == "__main__":
    main()
