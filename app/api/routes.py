from api import store
from fastapi import APIRouter, Depends
from api.models import *
from api.utils import *
from fastapi import status, HTTPException
from api.rarity import get_rank_and_score, get_collections_list
import asyncio

router = APIRouter(tags=["Info"])


@router.get("/info", summary="Get the score and rank of an asset from https://rarity.tools", response_model=ResponseModel)
async def add_new_ride(collection_slug: str, asset_name: str):
    while True:
        try:
            driver = store.DRIVERS.pop()
            break
        except IndexError:
            await asyncio.sleep(1)
    rank, score = get_rank_and_score(
        driver, collection_slug, asset_name)
    store.DRIVERS.append(driver)
    if not rank:
        return await add_new_ride(collection_slug, asset_name)
    return ResponseModel(status=status.HTTP_200_OK, collection_slug=collection_slug,
                         asset_name=asset_name, rarity_score=score, rarity_rank=rank)


# @router.get("/collections", summary="Get All Collections", response_model=AllCollections)
# async def get_all_collections():
#     while True:
#         try:
#             driver = store.DRIVERS.pop()
#             break
#         except IndexError:
#             await asyncio.sleep(1)
#     collections = get_collections_list(driver)
#     store.DRIVERS.append(driver)
#     return AllCollections(status=status.HTTP_200_OK, collections=collections)
