from fastapi import FastAPI, Query, HTTPException
from typing import Optional
import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = FastAPI(
    title="AviationStack API Proxy",
    version="1.0.0",
    description="Interactive Swagger UI for testing AviationStack API endpoints using your configured access key"
)

BASE_URL = "https://api.aviationstack.com/v1"

# Get API key from environment variable
AVIATIONSTACK_API_KEY = os.getenv("AVIATIONSTACK_API_KEY")

if not AVIATIONSTACK_API_KEY:
    raise ValueError("AVIATIONSTACK_API_KEY not found in environment variables. Please set it in your .env file.")


@app.get("/flights", summary="Get real-time or historical flight data")
async def get_flights(
    flight_iata: Optional[str] = Query(None, description="IATA flight code"),
    flight_icao: Optional[str] = Query(None, description="ICAO flight code"),
    dep_iata: Optional[str] = Query(None, description="Departure airport IATA code"),
    arr_iata: Optional[str] = Query(None, description="Arrival airport IATA code"),
    flight_date: Optional[str] = Query(None, description="Date (YYYY-MM-DD) for historical flights")
):
    """Retrieve flight status and details from AviationStack API"""
    params = {
        "access_key": AVIATIONSTACK_API_KEY,
        "flight_iata": flight_iata,
        "flight_icao": flight_icao,
        "dep_iata": dep_iata,
        "arr_iata": arr_iata,
        "flight_date": flight_date
    }
    # Remove None values
    params = {k: v for k, v in params.items() if v is not None}
    
    response = requests.get(f"{BASE_URL}/flights", params=params)
    return response.json()


@app.get("/routes", summary="Get airline route data")
async def get_routes(
    airline_iata: Optional[str] = Query(None, description="Airline IATA code"),
    dep_iata: Optional[str] = Query(None, description="Departure airport IATA code"),
    arr_iata: Optional[str] = Query(None, description="Arrival airport IATA code")
):
    """Retrieve available routes by airline or airport"""
    params = {
        "access_key": AVIATIONSTACK_API_KEY,
        "airline_iata": airline_iata,
        "dep_iata": dep_iata,
        "arr_iata": arr_iata
    }
    params = {k: v for k, v in params.items() if v is not None}
    
    response = requests.get(f"{BASE_URL}/routes", params=params)
    return response.json()


@app.get("/airports", summary="Get airport information")
async def get_airports(
    search: Optional[str] = Query(None, description="Search term (city or airport name)")
):
    """Retrieve data on airports including location, IATA, ICAO codes"""
    params = {
        "access_key": AVIATIONSTACK_API_KEY,
        "search": search
    }
    params = {k: v for k, v in params.items() if v is not None}
    
    response = requests.get(f"{BASE_URL}/airports", params=params)
    return response.json()


@app.get("/airlines", summary="Get airline information")
async def get_airlines(
    search: Optional[str] = Query(None, description="Airline name or code")
):
    """Retrieve data about airlines worldwide"""
    params = {
        "access_key": AVIATIONSTACK_API_KEY,
        "search": search
    }
    params = {k: v for k, v in params.items() if v is not None}
    
    response = requests.get(f"{BASE_URL}/airlines", params=params)
    return response.json()


@app.get("/airplanes", summary="Get airplane details")
async def get_airplanes(
    registration_number: Optional[str] = Query(None, description="Tail number or registration code")
):
    """Retrieve details of specific aircraft (tail number, type, etc.)"""
    params = {
        "access_key": AVIATIONSTACK_API_KEY,
        "registration_number": registration_number
    }
    params = {k: v for k, v in params.items() if v is not None}
    
    response = requests.get(f"{BASE_URL}/airplanes", params=params)
    return response.json()


@app.get("/aircraft_types", summary="Get aircraft type information")
async def get_aircraft_types():
    """Retrieve a list of aircraft types (model names and IATA codes)"""
    params = {"access_key": AVIATIONSTACK_API_KEY}
    
    response = requests.get(f"{BASE_URL}/aircraft_types", params=params)
    return response.json()


@app.get("/taxes", summary="Get aviation tax data")
async def get_taxes():
    """Retrieve a list of aviation taxes and associated codes"""
    params = {"access_key": AVIATIONSTACK_API_KEY}
    
    response = requests.get(f"{BASE_URL}/taxes", params=params)
    return response.json()


@app.get("/cities", summary="Get city data")
async def get_cities(
    search: Optional[str] = Query(None, description="City name or keyword")
):
    """Retrieve information about cities including IATA city codes"""
    params = {
        "access_key": AVIATIONSTACK_API_KEY,
        "search": search
    }
    params = {k: v for k, v in params.items() if v is not None}
    
    response = requests.get(f"{BASE_URL}/cities", params=params)
    return response.json()


@app.get("/countries", summary="Get country data")
async def get_countries(
    search: Optional[str] = Query(None, description="Country name or code")
):
    """Retrieve countries by name or ISO code"""
    params = {
        "access_key": AVIATIONSTACK_API_KEY,
        "search": search
    }
    params = {k: v for k, v in params.items() if v is not None}
    
    response = requests.get(f"{BASE_URL}/countries", params=params)
    return response.json()


@app.get("/timetable", summary="Get flight timetable")
async def get_timetable(
    iataCode: str = Query(..., description="Airport IATA code"),
    type: str = Query(..., description="Type of schedule (arrival or departure)")
):
    """Retrieve daily flight schedules (arrivals/departures) for an airport"""
    params = {
        "access_key": AVIATIONSTACK_API_KEY,
        "iataCode": iataCode,
        "type": type
    }
    
    response = requests.get(f"{BASE_URL}/timetable", params=params)
    return response.json()


@app.get("/flightsfuture", summary="Get future flight schedules")
async def get_flights_future(
    iataCode: str = Query(..., description="Airport IATA code"),
    type: str = Query(..., description="Type (arrival or departure)"),
    date: str = Query(..., description="Future date (YYYY-MM-DD)")
):
    """Retrieve upcoming flights for a given airport and date"""
    params = {
        "access_key": AVIATIONSTACK_API_KEY,
        "iataCode": iataCode,
        "type": type,
        "date": date
    }
    
    response = requests.get(f"{BASE_URL}/flightsfuture", params=params)
    return response.json()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
