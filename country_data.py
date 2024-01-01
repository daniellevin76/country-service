import httpx
from typing import List, Optional
from models.country_model import CountryModel
import logging

# Initialize logging
logging.basicConfig(level=logging.INFO)

async def get_country(name: str) -> Optional[CountryModel]:
    url = f"https://restcountries.com/v3.1/name/{name}"
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            if response.status_code == 404:
                return None 
            response.raise_for_status()
            data = response.json()

        return CountryModel(**data[0])

    except httpx.HTTPStatusError as e:
        logging.warning(f"HTTP error occurred while fetching country: {e}")
        return None
    except (IndexError, ValueError) as e:
        logging.error(f"Error parsing country data: {e}")
        return None


async def get_all_countries() -> List[CountryModel]:
    url = "https://restcountries.com/v3.1/all"
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            response.raise_for_status()
            countries_data = response.json()

        countries = [CountryModel(**country_data) for country_data in countries_data]
        return countries

    except httpx.HTTPStatusError as e:
        logging.warning(f"HTTP error occurred while fetching all countries: {e}")
        return []
    except ValueError as e:
        logging.error(f"Error parsing countries data: {e}")
        return []
