from pydantic import BaseModel
from typing import List

class NameModel(BaseModel):
    common: str
    official: str

class CountryModel(BaseModel):
    name: NameModel
    tld: List[str] = []
    capital: List[str] = []
    population: int
