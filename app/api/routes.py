from api import store
from fastapi import APIRouter, Depends
from api.models import *
from api.utils import *
from fastapi import status, HTTPException
from api.rarity import get_rank_and_score

router = APIRouter(tags=["Info"])


@router.get("/info", summary="Get the score and rank of an asset from https://rarity.tools", response_model=ResponseModel)
async def add_new_ride(collection_slug: str, asset_name: str):
    driver = store.DRIVERS.pop()
    rank, score = get_rank_and_score(
        driver, collection_slug, asset_name)
    store.DRIVERS.append(driver)
    return ResponseModel(status=status.HTTP_200_OK, collection_slug=collection_slug,
                         asset_name=asset_name, rarity_score=score, rarity_rank=rank)
