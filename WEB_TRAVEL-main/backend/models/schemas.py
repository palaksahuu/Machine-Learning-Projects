from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional
from datetime import date
from enum import Enum

class Budget(str, Enum):
    budget = "budget"
    moderate = "moderate"
    luxury = "luxury"

class TravelStyle(str, Enum):
    adventure = "adventure"
    relaxation = "relaxation"
    cultural = "cultural"
    foodie = "foodie"

class TravelRequest(BaseModel):
    destination: str
    starting_location: str
    trip_duration: int
    budget: Budget
    start_date: date 
    end_date: date 
    travel_style: List[TravelStyle]
    preferences: Optional[str] = None

    model_config = ConfigDict(arbitrary_types_allowed=True)
