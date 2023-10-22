from typing import Optional, List
from pydantic import BaseModel, RootModel


class GetResponseBreweryModel(BaseModel):
    id: str
    name: str
    brewery_type: str
    address_1: Optional[str]
    address_2: Optional[str]
    address_3: Optional[str]
    city: str
    state_province: str
    postal_code: str
    country: str
    longitude: Optional[str]
    latitude: Optional[str]
    phone: Optional[str]
    website_url: Optional[str]
    state: Optional[str]
    street: Optional[str]


class GetResponseListBreweryModel(BaseModel):
    RootModel: List[GetResponseBreweryModel]


class GetResponseAutocompleteModel(BaseModel):
    id: str
    name: str


class GetResponseListAutocompleteModel(BaseModel):
    RootModel: List[GetResponseAutocompleteModel]
