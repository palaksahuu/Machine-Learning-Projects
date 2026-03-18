# AI-Powered Travel Planner

## Project Overview

This project is an AI-powered travel itinerary generator that creates personalized travel plans based on user preferences. It uses a FastAPI backend integrated with Google's Gemini API to generate intelligent travel itineraries, and a Streamlit frontend for user interaction.

Users can input details such as destination, budget, travel duration, and travel style, and the system generates a customized itinerary accordingly.

---

## Objectives

The main objectives of this project are:

- Generate personalized travel itineraries using AI
- Provide a user-friendly interface for travel planning
- Integrate large language models for real-time itinerary generation
- Build a scalable backend API for travel recommendations

---

## Technologies Used

The project is built using the following technologies:

- Python
- FastAPI
- Streamlit
- Google Generative AI (Gemini API)
- HTTPX (for API communication)
- Asyncio
- dotenv

---

## System Architecture

The project consists of two main components:

### 1. Backend (FastAPI)

- Handles API requests
- Processes user input
- Generates itinerary using Gemini API
- Returns response in JSON format

### 2. Frontend (Streamlit)

- Collects user input
- Sends request to backend API
- Displays generated itinerary
- Provides validation and user interaction

---

## Backend Implementation

### API Endpoints

#### Home Endpoint

```
GET /
```

Returns a welcome message.

---

#### Sample Itinerary Endpoint

```
GET /generate-itinerary/
```

Returns a sample itinerary for testing purposes.

---

#### Generate Itinerary Endpoint

```
POST /generate-itinerary/
```

### Request Body

```
{
    "destination": "Paris",
    "budget": "moderate",
    "travel_style": "cultural"
}
```

### Workflow

1. Validate input fields
2. Create a prompt based on user input
3. Send prompt to Gemini API
4. Generate itinerary using AI model
5. Return itinerary as response

---

## Frontend Implementation

The frontend is built using Streamlit and provides an interactive interface.

### User Inputs

- Destination
- Budget (Budget, Moderate, Luxury)
- Trip Duration
- Starting Location
- Purpose of Travel (Adventure, Relaxation, Cultural, Foodie)
- Preferences (optional)

---

### Input Validation

The app validates:

- Destination is not empty
- Duration is greater than zero
- Budget and purpose are valid selections

---

### API Communication

The frontend sends a POST request to the backend:

```
POST /generate-itinerary/
```

Using HTTPX async client for efficient communication.

---


## Environment Setup

Create a `.env` file and add your Gemini API key:

```
GEMINI_API_KEY=your_api_key_here
```

---

## Installation

Install dependencies using pip:

```
pip install requirements.txt
```

---
## Applications

This system can be used for:

- Travel planning platforms
- AI-based recommendation systems
- Personalized trip planners
- Tourism applications

---

## Future Improvements

Possible improvements include:

- Adding hotel and flight recommendations
- Multi-destination itinerary planning
- Integration with maps and booking APIs
- Saving and sharing itineraries
- User authentication and history tracking

---

## Author

Palak Sahu

Bachelor of Technology in Computer Science (AI and ML)

Interested in Machine Learning, Artificial Intelligence, Data Analytics, and Web Development.
