from pydantic import BaseModel
import typing


class Request(BaseModel):
    collection_slug: str
    asset_name: str


class ResponseModel(BaseModel):
    status: int
    collection_slug: str
    asset_name: str
    rarity_score: str
    rarity_rank: str


class Collection(BaseModel):
    collection_name: str
    collection_url: str
    collection_slug: str


class AllCollections(BaseModel):
    status: int
    collections: typing.List[Collection]
