from typing import List
from pydantic import BaseModel, Field, RootModel


class GetResponseResourceModel(BaseModel):
    user_id: int = Field(alias='userId')
    id: int
    title: str
    body: str


class GetResponseResourceListModel(BaseModel):
    RootModel: List[GetResponseResourceModel]
