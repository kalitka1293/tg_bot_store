from fastapi import APIRouter, Query
from meilisearch_python_sdk import AsyncClient

from dto.product import Meilisearch

router_product_search = APIRouter()

async def perform_search(query):
    client = AsyncClient('http://127.0.0.1:7700', 'masterKey')
    index = client.index('product')
    result = await index.search(query, limit=5)
    return result

@router_product_search.get('/search/', tags=['search'])
async def search(query: str = Query(..., min_length=1)):
    print(query)
    result = await perform_search(query)
    return result
