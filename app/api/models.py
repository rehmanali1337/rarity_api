from pydantic import BaseModel


class Request(BaseModel):
    collection_slug: str
    asset_name: str


class ResponseModel(BaseModel):
    status: int
    collection_slug: str
    asset_name: str
    rarity_score: str
    rarity_rank: str
