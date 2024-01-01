import httpx
import logging
from fastapi import FastAPI, HTTPException
from typing import List

from models.country_model import CountryModel
import country_data

app = FastAPI()
logging.basicConfig(level=logging.INFO)

@app.get("/")
def index():
    return {"message": "welcome home!"}

@app.get("/api/countries", response_model=List[CountryModel])
async def get_all_countries():
    try:
        countries = await country_data.get_all_countries()
        return countries
    except httpx.HTTPError as e:
        logging.error(f"HTTP error occurred: {e}")
        raise HTTPException(status_code=503, detail="Service temporarily unavailable, try again later.")
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/api/country/{name}", response_model=CountryModel)
async def get_country(name: str):
    country = await country_data.get_country(name)
    if not country:
        raise HTTPException(status_code=404, detail="Country not found")
    return country
   